import argparse
import numpy as np, matplotlib.pyplot as plt
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--states",required=True); ap.add_argument("--output",required=True); a=ap.parse_args()
    s=np.load(a.states); t=np.arange(len(s))
    plt.figure(figsize=(9,4)); plt.plot(t,s[:,0],label="A position"); plt.plot(t,s[:,1],label="B position")
    plt.xlabel("frame"); plt.ylabel("position"); plt.legend(); plt.tight_layout(); plt.savefig(a.output,dpi=180)
if __name__=="__main__": main()
