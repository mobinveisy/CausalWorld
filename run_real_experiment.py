import argparse,json
from pathlib import Path
import torch
from torch.utils.data import DataLoader
from causalworld.real_dataset import RealMatchedDataset
from causalworld.model import CausalWorld,NoContextDynamics,OracleMassDynamics
from causalworld.engine import train,evaluate_neural
from causalworld.config import ModelConfig
from causalworld.utils import seed_all,get_device

def make(manifest,split,context,steps,seed,batch,samples=None,shuffle=False):
    ds=RealMatchedDataset(manifest,split,context,steps,seed,samples)
    return DataLoader(ds,batch_size=batch,shuffle=shuffle,num_workers=0)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--manifest',required=True)
    ap.add_argument('--model',choices=['causal','no_context','oracle_mass'],default='causal')
    ap.add_argument('--epochs',type=int,default=60); ap.add_argument('--batch',type=int,default=32)
    ap.add_argument('--context',type=int,default=3); ap.add_argument('--steps',type=int,default=60)
    ap.add_argument('--seed',type=int,default=42); ap.add_argument('--output',default='results_real/causal')
    ap.add_argument('--train-samples',type=int,default=None); ap.add_argument('--eval-samples',type=int,default=None)
    a=ap.parse_args(); seed_all(a.seed); dev=get_device(); mc=ModelConfig(); out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
    tr=make(a.manifest,'train',a.context,a.steps,a.seed,a.batch,a.train_samples,True)
    va=make(a.manifest,'val',a.context,a.steps,a.seed+100,a.batch,a.eval_samples)
    if a.model=='causal': model=CausalWorld(mc.latent_dim,mc.encoder_hidden,mc.decoder_hidden).to(dev)
    elif a.model=='no_context': model=NoContextDynamics(mc.decoder_hidden).to(dev)
    else: model=OracleMassDynamics(mc.decoder_hidden).to(dev)
    opt=torch.optim.AdamW(model.parameters(),lr=1e-3,weight_decay=1e-4)
    model=train(a.model,model,tr,va,opt,dev,a.epochs,out,{'w_cf':1.0,'w_effect':1.0,'w_cons':0.1,'w_var':0.03})
    result={'model':a.model,'seed':a.seed,'splits':{}}
    for sp in ['test_iid','test_interpolation','test_extrapolation']:
        try: dl=make(a.manifest,sp,a.context,a.steps,a.seed+200,a.batch,a.eval_samples)
        except ValueError as e: result['splits'][sp]={'skipped':str(e)}; continue
        result['splits'][sp]=evaluate_neural(a.model,model,dl,dev)
    (out/'eval_real.json').write_text(json.dumps(result,indent=2,allow_nan=True)); print(json.dumps(result,indent=2,allow_nan=True))
if __name__=='__main__':main()
