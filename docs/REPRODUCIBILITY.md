# Reproducibility

## Environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Sanity check

```bash
python run_tests.py
python run_suite.py --mode smoke --seeds 11 --output results_smoke
```

## Synthetic paper-grade suite

```bash
python run_suite.py   --mode full   --seeds 11 22 33 44 55   --output results_full
```

## Tables and figures

```bash
python make_report.py   --csv results_full/results.csv   --output paper_assets_full
```

## Physion++

```bash
python public_data/download_public_data.py physion-train
python public_data/download_public_data.py physion-readout
python public_data/download_public_data.py physion-test
```

After extraction:

```bash
python public_data/build_physionpp_index.py   --root data_public/physionpp/extracted   --output data_public/physionpp/index.csv
```

## GAUGE

```bash
python public_data/download_public_data.py gauge-rigid-json
```

Final paper tables must use multiple independent seeds. Development smoke numbers are not final evidence.
