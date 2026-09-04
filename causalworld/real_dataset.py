from pathlib import Path
import random,numpy as np,pandas as pd,torch
from torch.utils.data import Dataset

def resample(s,steps):
    if len(s)==steps:return s.astype(np.float32)
    old=np.linspace(0,1,len(s)); new=np.linspace(0,1,steps)
    return np.stack([np.interp(new,old,s[:,i]) for i in range(4)],-1).astype(np.float32)

class RealMatchedDataset(Dataset):
    # Manifest columns: trial_id,state_path,mass_b,split,pair_id,query_ok
    def __init__(self,manifest,split,context_size=3,steps=60,seed=42,samples=None):
        self.manifest=Path(manifest); self.root=self.manifest.parent; df=pd.read_csv(self.manifest)
        req={"trial_id","state_path","mass_b","split","pair_id","query_ok"}
        if req-set(df.columns): raise ValueError(f"Missing {req-set(df.columns)}")
        self.df=df[df.split==split].reset_index(drop=True); self.context_size=context_size; self.steps=steps; self.seed=seed
        if self.df.empty: raise ValueError(f"No rows for {split}")
        self.by_mass={float(m):g.index.tolist() for m,g in self.df.groupby("mass_b")}
        self.by_pair={str(p):g.index.tolist() for p,g in self.df.groupby("pair_id")}
        self.eligible=[]
        for i,r in self.df.iterrows():
            same=[j for j in self.by_mass[float(r.mass_b)] if j!=i]
            cf=[j for j in self.by_pair[str(r.pair_id)] if float(self.df.loc[j,"mass_b"])!=float(r.mass_b) and bool(self.df.loc[j,"query_ok"])]
            if bool(r.query_ok) and len(same)>=context_size and cf:self.eligible.append(i)
        if not self.eligible: raise ValueError("No eligible matched counterfactual queries.")
        self.samples=samples or len(self.eligible)
    def __len__(self): return self.samples
    def load(self,i):
        p=Path(self.df.loc[i,"state_path"]); p=p if p.is_absolute() else self.root/p
        return resample(np.load(p),self.steps)
    def __getitem__(self,k):
        rng=random.Random(self.seed*1000003+k); qi=rng.choice(self.eligible); q=self.df.loc[qi]; m=float(q.mass_b)
        cfi=rng.choice([j for j in self.by_pair[str(q.pair_id)] if float(self.df.loc[j,"mass_b"])!=m and bool(self.df.loc[j,"query_ok"])])
        cf=self.df.loc[cfi]; mcf=float(cf.mass_b)
        ctxi=rng.sample([j for j in self.by_mass[m] if j!=qi],self.context_size)
        cfctxi=rng.sample([j for j in self.by_mass[mcf] if j!=cfi],self.context_size)
        y=self.load(qi); ycf=self.load(cfi)
        return {"context":torch.tensor(np.stack([self.load(i) for i in ctxi])),
                "query_initial":torch.tensor(y[0]),"target":torch.tensor(y),"mass":torch.tensor(m),
                "cf_context":torch.tensor(np.stack([self.load(i) for i in cfctxi])),
                "cf_target":torch.tensor(ycf),"cf_mass":torch.tensor(mcf)}
