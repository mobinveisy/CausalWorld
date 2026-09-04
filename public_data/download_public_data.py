import argparse
from pathlib import Path

PHYSION_URLS = {
    'train': 'https://physion-v2.s3.amazonaws.com/train_data.zip',
    'readout': 'https://physion-v2.s3.amazonaws.com/readout_data.zip',
    'test': 'https://physion-v2.s3.amazonaws.com/test_data.zip',
}

def download_physion(split: str, out: Path):
    import requests
    url = PHYSION_URLS[split]
    out.mkdir(parents=True, exist_ok=True)
    dest = out / f'{split}_data.zip'
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        total = int(r.headers.get('content-length', 0))
        got = 0
        with open(dest, 'wb') as f:
            for chunk in r.iter_content(8 * 1024 * 1024):
                if not chunk:
                    continue
                f.write(chunk); got += len(chunk)
                if total:
                    print(f'\r{got/total:.1%}', end='', flush=True)
    print('\nSaved', dest)


def download_hf(repo_id: str, out: Path, allow_patterns=None):
    from huggingface_hub import snapshot_download
    out.mkdir(parents=True, exist_ok=True)
    snapshot_download(repo_id=repo_id, repo_type='dataset', local_dir=str(out), allow_patterns=allow_patterns)
    print('Saved under', out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dataset', choices=['physion-test','physion-train','physion-readout','gauge-rigid-json','morpheus-collisions'])
    ap.add_argument('--output', default='data_public')
    a = ap.parse_args(); root = Path(a.output)
    if a.dataset.startswith('physion-'):
        download_physion(a.dataset.split('-')[1], root/'physionpp')
    elif a.dataset == 'gauge-rigid-json':
        patterns = [
            'metadata/rigid/*.json',
            "data/rigid/newton's cradle/json/*.json",
            'data/rigid/bouncing ball/json/*.json',
            'data/rigid/slope slider/json/*.json',
            'data/rigid/pendulum/json/*.json',
            'data/rigid/turntable/json/*.json',
        ]
        download_hf('InternRobotics/GAUGE-Dataset', root/'gauge', patterns)
    else:
        patterns = [
            'real-world-cropped/collision_equal/**',
            'real-world-cropped/collision_big_hits_small/**',
            'real-world-cropped/collision_small_hits_big/**',
        ]
        download_hf('physics-from-video/morpheus-real-world', root/'morpheus', patterns)

if __name__ == '__main__':
    main()
