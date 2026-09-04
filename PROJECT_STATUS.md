# CausalWorld release-candidate status

## Repository engineering complete
- Core CausalWorld model
- Causal latent replacement objective
- Controlled synthetic benchmark
- IID / interpolation / extrapolation evaluation
- Baselines and ablations
- Multi-seed runner
- Automatic tables and figures
- Physion++ downloader and copy0/copy1 index builder
- GAUGE rigid-body subset downloader
- Optional Morpheus downloader
- GitHub Actions
- Package metadata
- Colab demo / reproduction notebooks
- Citation, reproducibility, anonymization and release documentation

## Public-data evidence plan

**Physion++** is the primary controlled hidden-property benchmark. Its test release includes
matched copy0/copy1 trials in which initial conditions are matched but latent physical
properties/outcomes differ.

**GAUGE** is the independent real-world measurement source, providing controlled
motion-capture trajectories and calibrated physical metadata.

## Remaining before paper claims

The remaining work is experimental:
1. download and prepare the chosen public subsets;
2. execute full multi-seed experiments;
3. validate Physion++ extraction on the downloaded official release;
4. run GAUGE real-world validation;
5. analyze statistics and failure cases;
6. re-check novelty immediately before submission;
7. write the paper using measured results only.

Smoke/development results must not be reported as final paper evidence.
