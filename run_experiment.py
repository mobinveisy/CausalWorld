import argparse,json
from pathlib import Path
import torch
from torch.utils.data import DataLoader
from causalworld.config import PhysicsConfig,SplitConfig,ModelConfig
from causalworld.dataset import DatasetSpec,CollisionDataset
from causalworld.model import CausalWorld,NoContextDynamics,OracleMassDynamics
from causalworld.engine import train,evaluate_neural,evaluate_nonlearning
from causalworld.utils import seed_all,get_device

def loader(masses,cf,samples,context,seed,batch,shuffle=False):
    return DataLoader(CollisionDataset(DatasetSpec(tuple(masses),tuple(cf),samples,context,seed)),
                      batch_size=batch,shuffle=shuffle,num_workers=0)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--model",choices=["causal","no_context","oracle_mass","constant_velocity","analytic_oracle"],default="causal")
    ap.add_argument("--epochs",type=int,default=20); ap.add_argument("--samples",type=int,default=1200)
    ap.add_argument("--eval-samples",type=int,default=400); ap.add_argument("--batch",type=int,default=128)
    ap.add_argument("--context",type=int,default=3); ap.add_argument("--seed",type=int,default=42)
    ap.add_argument("--w-cf",type=float,default=1.0); ap.add_argument("--w-effect",type=float,default=1.0)
    ap.add_argument("--w-cons",type=float,default=0.1); ap.add_argument("--w-var",type=float,default=0.03)
    ap.add_argument("--output",default="outputs/exp"); args=ap.parse_args()
    seed_all(args.seed); dev=get_device(); physics=PhysicsConfig(); split=SplitConfig(); mc=ModelConfig()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    tr=loader(split.train_masses,split.train_masses,args.samples,args.context,args.seed,args.batch,True)
    va=loader(split.train_masses,split.train_masses,max(128,args.eval_samples//2),args.context,args.seed+101,args.batch)
    tests={
      "iid":loader(split.iid_masses,split.train_masses,args.eval_samples,args.context,args.seed+201,args.batch),
      "interpolation":loader(split.interpolation_masses,split.train_masses,args.eval_samples,args.context,args.seed+301,args.batch),
      "extrapolation":loader(split.extrapolation_masses,split.train_masses,args.eval_samples,args.context,args.seed+401,args.batch),
    }
    model=None
    if args.model=="causal": model=CausalWorld(mc.latent_dim,mc.encoder_hidden,mc.decoder_hidden).to(dev)
    elif args.model=="no_context": model=NoContextDynamics(mc.decoder_hidden).to(dev)
    elif args.model=="oracle_mass": model=OracleMassDynamics(mc.decoder_hidden).to(dev)
    if model is not None:
        opt=torch.optim.AdamW(model.parameters(),lr=2e-3,weight_decay=1e-4)
        model=train(args.model,model,tr,va,opt,dev,args.epochs,out,
                    {"w_cf":args.w_cf,"w_effect":args.w_effect,"w_cons":args.w_cons,"w_var":args.w_var})
    res={"model":args.model,"seed":args.seed,"context":args.context,"splits":{}}
    for name,dl in tests.items():
        res["splits"][name]=evaluate_neural(args.model,model,dl,dev) if model is not None else evaluate_nonlearning(args.model,dl,physics)
    (out/"eval.json").write_text(json.dumps(res,indent=2,allow_nan=True),encoding="utf-8")
    print(json.dumps(res,indent=2,allow_nan=True))
if __name__=="__main__": main()
