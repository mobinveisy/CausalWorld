# CausalWorld

**Learning Causally Editable Latent Physics from Passive Observations**

[![Tests](https://github.com/YOUR_GITHUB_USER/CausalWorld/actions/workflows/tests.yml/badge.svg)](https://github.com/YOUR_GITHUB_USER/CausalWorld/actions/workflows/tests.yml)
[![Open Demo in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_GITHUB_USER/CausalWorld/blob/main/notebooks/01_CausalWorld_Quick_Demo.ipynb)

CausalWorld asks a stronger question than ordinary future prediction:

> If a model learns a hidden physical representation from passive observations, can replacing
> only that representation produce the **correct counterfactual dynamics**?

## Method

```text
Passive context
      ↓
Physics Encoder
      ↓
z_physics
      ↓
Dynamics Decoder
      ↓
Future trajectory
```

Counterfactual evaluation keeps the initial scene fixed and replaces only `z_physics`.

## Metrics

- ADE
- FDE
- PCVE
- **CEE — Counterfactual Effect Error**
- latent-property probes

## Public datasets

### Physion++
Primary controlled hidden-property benchmark. The public test set contains matched
`copy0` / `copy1` trials with matched initial conditions and changed latent physical
property/outcome.

### GAUGE
Independent real-world measurement source with controlled motion-capture trajectories
and calibrated physical metadata.

The repository does not redistribute these datasets.

## Quick start

```bash
git clone https://github.com/YOUR_GITHUB_USER/CausalWorld.git
cd CausalWorld
python -m venv .venv
source .venv/bin/activate
pip install -e .
python run_tests.py
```

## Full synthetic suite

```bash
python run_suite.py   --mode full   --seeds 11 22 33 44 55   --output results_full

python make_report.py   --csv results_full/results.csv   --output paper_assets_full
```

## Colab

- `notebooks/01_CausalWorld_Quick_Demo.ipynb`
- `notebooks/02_Reproduce_CausalWorld.ipynb`
- `notebooks/03_Public_Data_Setup.ipynb`

## Configure repository links

```bash
python scripts/configure_repo.py   --github-user YOUR_USERNAME   --repo CausalWorld
```

Then:

```bash
python scripts/verify_release.py
```

## Documentation

- `docs/REPRODUCIBILITY.md`
- `docs/ANONYMIZATION.md`
- `docs/RELEASE_CHECKLIST.md`
- `docs/PUBLICATION_FA.md`
- `docs/PUBLIC_DATA_PLAN_FA.md`

## Status

`v0.9.0-rc1` — release candidate before the paper experiment freeze.

Development/smoke numbers are not final scientific evidence.

## License

Code: MIT. Public datasets retain their own licenses and citation requirements.
