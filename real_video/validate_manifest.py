import argparse
from pathlib import Path
import pandas as pd

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--manifest',required=True); a=ap.parse_args()
    p=Path(a.manifest); df=pd.read_csv(p)
    req={'trial_id','state_path','mass_b','split','pair_id','query_ok'}
    missing=req-set(df.columns)
    if missing: raise SystemExit(f'Missing columns: {sorted(missing)}')
    if df.trial_id.duplicated().any(): raise SystemExit('Duplicate trial_id values found.')
    bad=[]
    for _,r in df.iterrows():
        fp=Path(r.state_path); fp=fp if fp.is_absolute() else p.parent/fp
        if not fp.exists(): bad.append(str(fp))
    if bad: raise SystemExit('Missing state files:\n'+'\n'.join(bad[:20]))
    print('Rows:',len(df)); print('\nBy split/mass:\n',df.groupby(['split','mass_b']).size().to_string())
    paired=df.groupby(['split','pair_id']).mass_b.nunique(); print('\nMatched counterfactual pair groups:',int((paired>=2).sum()))
    for split in df['split'].unique():
        q=df[(df['split']==split)&(df.query_ok.astype(bool))]
        print(split,'query_ok=',len(q))
    print('\nMANIFEST VALIDATION PASSED')
if __name__=='__main__':main()
