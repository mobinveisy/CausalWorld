"""Fast in-process development validation. Not a paper experiment."""
import json
from pathlib import Path
import numpy as np, torch
from torch.utils.data import DataLoader
from causalworld.config import PhysicsConfig, SplitConfig, ModelConfig
from causalworld.dataset import DatasetSpec, CollisionDataset
from causalworld.model import CausalWorld, NoContextDynamics, OracleMassDynamics
from causalworld.engine import train, evaluate_neural, evaluate_nonlearning
from causalworld.utils import seed_all, get_device

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'verified_dev'
OUT.mkdir(exist_ok=True)
physics=PhysicsConfig(); split=SplitConfig(); mc=ModelConfig(); dev=get_device()

def dl(masses, cf, samples, seed, context=3, shuffle=False):
    return DataLoader(CollisionDataset(DatasetSpec(tuple(masses),tuple(cf),samples,context,seed)),batch_size=64,shuffle=shuffle,num_workers=0)

rows=[]
for seed in [11,22]:
    for name,w_effect in [('causal_full',1.0),('ablate_no_effect',0.0)]:
        seed_all(seed)
        tr=dl(split.train_masses,split.train_masses,128,seed,3,True)
        va=dl(split.train_masses,split.train_masses,64,seed+100)
        model=CausalWorld(mc.latent_dim,mc.encoder_hidden,mc.decoder_hidden).to(dev)
        opt=torch.optim.AdamW(model.parameters(),lr=2e-3)
        model=train('causal',model,tr,va,opt,dev,1,OUT/f'{name}_{seed}',{'w_cf':1.0,'w_effect':w_effect,'w_cons':0.1,'w_var':0.03})
        for sp,masses in [('iid',split.iid_masses),('interpolation',split.interpolation_masses),('extrapolation',split.extrapolation_masses)]:
            metrics=evaluate_neural('causal',model,dl(masses,split.train_masses,64,seed+200+len(rows)),dev)
            rows.append({'experiment':name,'seed':seed,'split':sp,**metrics})
# Nonlearning baselines need no training.
for name in ['constant_velocity','analytic_oracle']:
    for sp,masses in [('iid',split.iid_masses),('interpolation',split.interpolation_masses),('extrapolation',split.extrapolation_masses)]:
        metrics=evaluate_nonlearning(name,dl(masses,split.train_masses,64,999),physics)
        rows.append({'experiment':name,'seed':0,'split':sp,**metrics})
(OUT/'results.json').write_text(json.dumps(rows,indent=2,allow_nan=True))
# tiny markdown summary
from collections import defaultdict
acc=defaultdict(list)
for r in rows:
    if r['experiment'] in ('causal_full','ablate_no_effect'):
        acc[(r['experiment'],r['split'])].append(r['cee'])
lines=['# Verified development run','','This is a fast pipeline validation, **not a paper result**.','','| Experiment | Split | CEE mean |','|---|---|---:|']
for k,v in sorted(acc.items()): lines.append(f'| {k[0]} | {k[1]} | {np.mean(v):.4f} |')
(OUT/'REPORT.md').write_text('\n'.join(lines))
print('\n'.join(lines))
