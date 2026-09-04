"""Inspect official Physion++ metadata without assuming one internal pickle schema."""
import argparse, pickle
from pathlib import Path
import numpy as np

def walk(x,path='root',depth=0,max_depth=5):
    if depth>max_depth: return
    if isinstance(x,dict):
        for k,v in list(x.items())[:100]: walk(v,f'{path}.{k}',depth+1,max_depth)
    elif isinstance(x,(list,tuple)):
        if x and all(isinstance(v,(int,float,np.number)) for v in x[:min(10,len(x))]):
            print(path,'numeric-list',len(x))
        else:
            for i,v in enumerate(x[:20]): walk(v,f'{path}[{i}]',depth+1,max_depth)
    elif isinstance(x,np.ndarray): print(path,'ndarray',x.shape,x.dtype)
    elif isinstance(x,(int,float,str,bool,type(None))):
        if any(key in path.lower() for key in ['mass','friction','elastic','position','velocity','start_frame']): print(path,'=',x)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('pkl'); a=ap.parse_args()
    with open(Path(a.pkl),'rb') as f: obj=pickle.load(f)
    walk(obj)
if __name__=='__main__': main()
