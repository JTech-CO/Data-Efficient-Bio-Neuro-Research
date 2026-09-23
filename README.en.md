# Data-Efficient Bio & Neuro Research

[한국어](README.md) · **Current version: v1.4.0-research.1** · [Release history](VERSIONS.en.md)

A research repository separating observations, model assumptions and the next measurement/intervention in a closed loop. Literature reviews and executable small synthetic experiments examine data efficiency alongside the limits of detecting calibration, noise and model errors.

**Synthetic research only. No real biological training data, clinical model or laboratory-device controller.**

## Current research

| Topic | Documentation |
|---|---|
| Partial identification with biased references | [Sets, assumptions and identification](research/docs/en/26_PARTIAL_IDENTIFICATION.md) |
| Control diagnostics with unknown noise variance | [Test conditions, locations and budgets](research/docs/en/27_UNKNOWN_SCALE_AUDIT.md) |
| Technical replication for noise/mean decomposition | [Same-data comparisons and counterexamples](research/docs/en/28_REPLICATE_DECOMPOSITION.md) |

[Start and run](BOUNDED.en.md) · [Results](research/docs/en/29_BOUNDED_RESULTS.md) · [Results viewer](research/bounded/web/index.html) · [Next decisions](research/docs/en/30_RESEARCH_DECISIONS.md)

## Run

Run from the repository root. Python is required; API keys, GPUs and model weights are not.

```bash
python -m pip install -r research/requirements.txt
python -m research.bounded_loop demo --study G --scenario common_in_bounds --design triangulated --out research/bounded/results/demo-G.json
```

The static viewer reads saved records rather than executing models. New calculations and full reproduction are described in the [guide](BOUNDED.en.md).

## Foundations and reproducibility

[Research review](docs/en/01_RESEARCH_REPORT.md) · [Original architecture](docs/en/02_ARCHITECTURE.md) · [Original evaluation plan](docs/en/03_EVALUATION.md) · [Current QA scope](research/bounded/quality/QA.md) · [License notes](LICENSE.md)

Previous designs, code and raw results are preserved. See [VERSIONS.en.md](VERSIONS.en.md) for release-specific changes and entry points. Synthetic results are not biological performance estimates or unconditional statistical guarantees.
