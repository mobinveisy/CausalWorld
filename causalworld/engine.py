from pathlib import Path
import json, numpy as np, torch
import torch.nn.functional as F
from .losses import causal_loss
from .metrics import trajectory_metrics, cee, latent_probe
from .baselines import constant_velocity, analytic_oracle

def _dev(batch,dev):
    return {k:(v.to(dev) if torch.is_tensor(v) else v) for k,v in batch.items()}

def train(model_name,model,loader,val_loader,opt,dev,epochs,outdir,weights):
    outdir=Path(outdir); outdir.mkdir(parents=True,exist_ok=True)
    best=1e30; hist=[]
    for ep in range(1,epochs+1):
        model.train(); total=0.; n=0
        for b in loader:
            b=_dev(b,dev); steps=b["target"].shape[1]; opt.zero_grad()
            if model_name=="causal":
                pred,z,ze=model(b["context"],b["query_initial"],steps)
                zcf,zecf=model.encode(b["cf_context"])
                cfp=model.predict(b["query_initial"],zcf,steps)
                loss,parts=causal_loss(pred,b["target"],cfp,b["cf_target"],z,ze,zcf,zecf,**weights)
            elif model_name=="no_context":
                pred=model(b["query_initial"],steps); loss=F.mse_loss(pred,b["target"]); parts={"loss":float(loss.detach())}
            elif model_name=="oracle_mass":
                pred=model(b["query_initial"],b["mass"],steps); loss=F.mse_loss(pred,b["target"]); parts={"loss":float(loss.detach())}
            loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),2.0); opt.step()
            total+=parts["loss"]; n+=1
        val=evaluate_neural(model_name,model,val_loader,dev)
        row={"epoch":ep,"train_loss":total/max(n,1),**{f"val_{k}":v for k,v in val.items()}}
        hist.append(row)
        if val["mse"]<best:
            best=val["mse"]; torch.save({"state_dict":model.state_dict(),"epoch":ep},outdir/"best.pt")
    (outdir/"history.json").write_text(json.dumps(hist,indent=2),encoding="utf-8")
    ckpt=torch.load(outdir/"best.pt",map_location=dev); model.load_state_dict(ckpt["state_dict"])
    return model

@torch.no_grad()
def evaluate_neural(model_name,model,loader,dev):
    model.eval(); P=[];Y=[];CP=[];CY=[];Z=[];M=[]
    for b in loader:
        b=_dev(b,dev); steps=b["target"].shape[1]
        if model_name=="causal":
            p,z,_=model(b["context"],b["query_initial"],steps)
            zcf,_=model.encode(b["cf_context"]); cp=model.predict(b["query_initial"],zcf,steps); Z.append(z.cpu().numpy())
        elif model_name=="no_context":
            p=model(b["query_initial"],steps); cp=p
        else:
            p=model(b["query_initial"],b["mass"],steps); cp=model(b["query_initial"],b["cf_mass"],steps)
        P.append(p.cpu().numpy());Y.append(b["target"].cpu().numpy());CP.append(cp.cpu().numpy());CY.append(b["cf_target"].cpu().numpy());M.append(b["mass"].cpu().numpy())
    p=np.concatenate(P);y=np.concatenate(Y);cp=np.concatenate(CP);cy=np.concatenate(CY);m=np.concatenate(M)
    out=trajectory_metrics(p,y); out["cee"]=cee(p,y,cp,cy)
    if Z: out.update(latent_probe(np.concatenate(Z),m))
    return out

def evaluate_nonlearning(name,loader,physics):
    P=[];Y=[];CP=[];CY=[]
    for b in loader:
        init=b["query_initial"].numpy(); y=b["target"].numpy(); cy=b["cf_target"].numpy(); steps=y.shape[1]
        if name=="constant_velocity":
            p=constant_velocity(init,steps,physics.dt); cp=p.copy()
        else:
            p=analytic_oracle(init,b["mass"].numpy(),steps,physics)
            cp=analytic_oracle(init,b["cf_mass"].numpy(),steps,physics)
        P.append(p);Y.append(y);CP.append(cp);CY.append(cy)
    p=np.concatenate(P);y=np.concatenate(Y);cp=np.concatenate(CP);cy=np.concatenate(CY)
    out=trajectory_metrics(p,y); out["cee"]=cee(p,y,cp,cy); return out
