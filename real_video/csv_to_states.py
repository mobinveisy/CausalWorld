import argparse
from pathlib import Path
import numpy as np,pandas as pd
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--input",required=True); ap.add_argument("--output",required=True)
    ap.add_argument("--axis",choices=["x","y"],default="x"); ap.add_argument("--meters-per-pixel",type=float,required=True)
    ap.add_argument("--smooth",type=int,default=5); a=ap.parse_args()
    df=pd.read_csv(a.input); t=df.time_s.to_numpy(np.float32)
    A=df[f"a_{a.axis}_px"].interpolate(limit_direction="both").rolling(a.smooth,center=True,min_periods=1).mean().to_numpy()*a.meters_per_pixel
    B=df[f"b_{a.axis}_px"].interpolate(limit_direction="both").rolling(a.smooth,center=True,min_periods=1).mean().to_numpy()*a.meters_per_pixel
    VA=np.gradient(A,t); VB=np.gradient(B,t); states=np.stack([A,B,VA,VB],-1).astype(np.float32)
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); np.save(out,states); print(states.shape,out)
if __name__=="__main__": main()
