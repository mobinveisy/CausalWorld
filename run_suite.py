import argparse,csv,json,subprocess,sys
from pathlib import Path

def defs(mode):
    if mode=="smoke": epochs,samples,ev=1,96,48
    elif mode=="quick": epochs,samples,ev=5,700,220
    else: epochs,samples,ev=35,5000,1200
    return [
      ("causal_full",dict(model="causal",context=3,wcf=1,we=1,wc=.1,epochs=epochs,samples=samples,ev=ev)),
      ("ablate_no_effect",dict(model="causal",context=3,wcf=1,we=0,wc=.1,epochs=epochs,samples=samples,ev=ev)),
      ("ablate_no_cf",dict(model="causal",context=3,wcf=0,we=0,wc=.1,epochs=epochs,samples=samples,ev=ev)),
      ("ablate_no_consistency",dict(model="causal",context=3,wcf=1,we=1,wc=0,epochs=epochs,samples=samples,ev=ev)),
      ("ablate_single_context",dict(model="causal",context=1,wcf=1,we=1,wc=0,epochs=epochs,samples=samples,ev=ev)),
      ("baseline_no_context",dict(model="no_context",context=3,wcf=0,we=0,wc=0,epochs=epochs,samples=samples,ev=ev)),
      ("baseline_oracle_mass",dict(model="oracle_mass",context=3,wcf=0,we=0,wc=0,epochs=epochs,samples=samples,ev=ev)),
      ("baseline_constant_velocity",dict(model="constant_velocity",context=3,wcf=0,we=0,wc=0,epochs=0,samples=64,ev=ev)),
      ("upperbound_analytic_oracle",dict(model="analytic_oracle",context=3,wcf=0,we=0,wc=0,epochs=0,samples=64,ev=ev)),
    ]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--mode",choices=["smoke","quick","full"],default="quick")
    ap.add_argument("--seeds",nargs="+",type=int,default=[11,22,33]); ap.add_argument("--output",default="results_suite")
    args=ap.parse_args(); root=Path(__file__).resolve().parent; out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    rows=[]
    for seed in args.seeds:
      for name,c in defs(args.mode):
        eo=out/f"{name}_seed{seed}"
        cmd=[sys.executable,str(root/"run_experiment.py"),"--model",c["model"],"--epochs",str(c["epochs"]),
             "--samples",str(c["samples"]),"--eval-samples",str(c["ev"]),"--context",str(c["context"]),
             "--seed",str(seed),"--w-cf",str(c["wcf"]),"--w-effect",str(c["we"]),"--w-cons",str(c["wc"]),
             "--output",str(eo)]
        subprocess.check_call(cmd,cwd=root,stdout=subprocess.DEVNULL)
        obj=json.loads((eo/"eval.json").read_text())
        for sp,m in obj["splits"].items():
          row={"experiment":name,"model":obj["model"],"seed":seed,"split":sp}; row.update(m); rows.append(row)
    keys=sorted({k for r in rows for k in r})
    with (out/"results.csv").open("w",newline="",encoding="utf-8") as f:
      w=csv.DictWriter(f,fieldnames=keys); w.writeheader(); w.writerows(rows)
    (out/"results.json").write_text(json.dumps(rows,indent=2,allow_nan=True),encoding="utf-8")
    print(out/"results.csv")
if __name__=="__main__": main()
