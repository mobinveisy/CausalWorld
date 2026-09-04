import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--csv",required=True); ap.add_argument("--output",default="paper_assets")
    a=ap.parse_args(); out=Path(a.output); out.mkdir(parents=True,exist_ok=True); df=pd.read_csv(a.csv)
    metrics=["mse","ade","fde","pcve","cee","mass_probe_r2","pc1_mass_spearman"]
    agg=df.groupby(["experiment","split"])[[m for m in metrics if m in df]].agg(["mean","std"])
    agg.to_csv(out/"summary.csv")
    # Primary paper table
    primary=df[df["split"].isin(["iid","interpolation","extrapolation"])]
    table=primary.groupby(["experiment","split"])[["ade","pcve","cee"]].agg(["mean","std"])
    (out/"paper_table.md").write_text(table.to_markdown(),encoding="utf-8")
    # One figure per metric (no subplots)
    for metric in ["cee","ade","pcve"]:
        piv=primary.groupby(["experiment","split"])[metric].mean().unstack("split")
        ax=piv.plot(kind="bar",figsize=(10,5))
        ax.set_ylabel(metric.upper()); ax.set_title(f"{metric.upper()} across evaluation splits")
        plt.tight_layout(); plt.savefig(out/f"{metric}.png",dpi=180); plt.close()
    best=primary[primary["experiment"]=="causal_full"].groupby("split")[["ade","pcve","cee"]].agg(["mean","std"])
    text = "# CausalWorld automatic experiment report\n\n"
    text += "## Full model\n\n" + best.to_markdown() + "\n\n"
    text += "## Interpretation guardrail\n\nSynthetic results validate the pipeline only. Real-world matched counterfactual trials are required before claiming causally editable physics from real videos.\n"
    (out/"REPORT.md").write_text(text,encoding="utf-8")
    print(out)
if __name__=="__main__": main()
