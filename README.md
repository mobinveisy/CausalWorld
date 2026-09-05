# CausalWorld

**Learning causally editable latent physics from passive observations.**

[![Research code tests](https://github.com/mobinveisy/CausalWorld/actions/workflows/tests.yml/badge.svg)](https://github.com/mobinveisy/CausalWorld/actions/workflows/tests.yml)
[![Three.js Pages](https://github.com/mobinveisy/CausalWorld/actions/workflows/pages.yml/badge.svg)](https://github.com/mobinveisy/CausalWorld/actions/workflows/pages.yml)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mobinveisy/CausalWorld/blob/main/notebooks/01_CausalWorld_Quick_Demo.ipynb)

CausalWorld asks whether a predictive model has learned something stronger than a correlation:

> If the model infers a hidden physical representation from passive observations, can replacing only that latent state produce the correct counterfactual dynamics?

## Research idea

```text
Passive observations
        ↓
  Physics Encoder
        ↓
    z_physics
        ↓
 Dynamics Decoder
        ↓
future trajectory
```

For the causal intervention test, the initial scene is held fixed while only `z_physics` is replaced.

## Main objective

The model combines factual prediction, counterfactual prediction, consistency and causal-effect matching. The intervention objective is:

```text
L_effect = || (tau_hat_cf - tau_hat) - (tau_cf - tau) ||^2
```

## Metrics

- **ADE** — Average Displacement Error
- **FDE** — Final Displacement Error
- **PCVE** — Post-Collision Velocity Error
- **CEE** — Counterfactual Effect Error (primary intervention metric)
- latent-property linear-probe diagnostics

## Public-data plan

- **Physion++** — controlled hidden physical properties and matched counterfactual conditions.
- **GAUGE** — independent real-world motion-capture validation with calibrated physical metadata.

The repository does not redistribute third-party datasets.

## Quick research setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python run_tests.py
```

Smoke suite:

```bash
python run_suite.py --mode smoke --seeds 11 --output results_smoke
```

Full synthetic suite:

```bash
python run_suite.py \
  --mode full \
  --seeds 11 22 33 44 55 \
  --output results_full

python make_report.py \
  --csv results_full/results.csv \
  --output paper_assets_full
```

## Colab

- [Quick Demo](https://colab.research.google.com/github/mobinveisy/CausalWorld/blob/main/notebooks/01_CausalWorld_Quick_Demo.ipynb)
- [Reproduce Experiments](https://colab.research.google.com/github/mobinveisy/CausalWorld/blob/main/notebooks/02_Reproduce_CausalWorld.ipynb)
- [Public Data Setup](https://colab.research.google.com/github/mobinveisy/CausalWorld/blob/main/notebooks/03_Public_Data_Setup.ipynb)

## Three.js research landing

The project website is a real WebGL experience built with **Three.js 0.185.1** and **Vite 8.2.2**.

Local development:

```bash
cd web
npm install
npm run dev
```

Production build:

```bash
npm run build
```

GitHub Pages deploys automatically through `.github/workflows/pages.yml`.

Live URL after enabling Pages with **GitHub Actions**:

**https://mobinveisy.github.io/CausalWorld/**

## Repository structure

```text
CausalWorld/
├── causalworld/              # research package
├── public_data/              # dataset download/index utilities
├── notebooks/                # Colab notebooks
├── real_video/               # optional real-video tools
├── web/                      # Three.js + Vite landing
├── docs/                     # reproducibility / publication docs
├── .github/workflows/        # Python tests + Pages deploy
├── run_experiment.py
├── run_suite.py
├── make_report.py
├── pyproject.toml
├── CITATION.cff
└── LICENSE
```

## Scientific status

The repository engineering and reproducibility pipeline are ready. Final paper claims must be based on the completed public-dataset runs and multi-seed statistics — not smoke/development numbers.

## Author

**Mobin Veisy**

© 2026 Mobin Veisy. All rights reserved for the project website and authored project materials. Research code is distributed under the repository license.
