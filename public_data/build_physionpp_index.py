import argparse, csv, re
from pathlib import Path

COPY_RE = re.compile(r'(.+?)-copy([01])$')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True, help='Extracted Physion++ root')
    ap.add_argument('--output', default='physionpp_index.csv')
    a=ap.parse_args(); root=Path(a.root)
    rows=[]
    for video in root.rglob('*_image.mp4'):
        rel=video.relative_to(root)
        parts=list(rel.parts)
        copy_idx=None; copy_no=None; family=None
        for i,p in enumerate(parts):
            m=COPY_RE.match(p)
            if m:
                copy_idx=i; family=m.group(1); copy_no=int(m.group(2)); break
        if copy_idx is None: continue
        base=video.name[:-len('_image.mp4')]
        pkl=video.with_name(base+'.pkl'); js=video.with_name(base+'.json')
        seg=video.with_name(base+'_seg.mp4'); mp=video.with_name(base+'_map.png')
        canonical=parts.copy(); canonical[copy_idx]=family
        canonical[-1]=base
        pair_id='/'.join(canonical)
        rows.append({
            'pair_id':pair_id,'copy':copy_no,'family':family,
            'scenario':parts[copy_idx+1] if len(parts)>copy_idx+1 else '',
            'instance_id':base,'video':str(video),'pkl':str(pkl) if pkl.exists() else '',
            'json':str(js) if js.exists() else '', 'seg_video':str(seg) if seg.exists() else '',
            'map_png':str(mp) if mp.exists() else ''
        })
    rows.sort(key=lambda x:(x['pair_id'],x['copy']))
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys() if rows else ['pair_id']); w.writeheader(); w.writerows(rows)
    pairs={}
    for r in rows: pairs.setdefault(r['pair_id'],set()).add(r['copy'])
    complete=sum(v=={0,1} for v in pairs.values())
    print(f'Indexed {len(rows)} trials, {complete} complete copy0/copy1 pairs -> {out}')
if __name__=='__main__': main()
