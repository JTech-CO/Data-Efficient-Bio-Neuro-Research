# 25. Bounded evidence: design of studies G/H/I

[한국어](../ko/25_BOUNDED_DESIGN.md) · [Sources](../../bounded/references/REFERENCES.md) · [Research entry](../../../BOUNDED.md)


## Purpose and preservation

This extension implements the three next questions from the prior research decisions. G relaxes perfect-reference assumptions; H compares control diagnostics without known noise variance; I separates information in technical-replicate differences from information in replicate means. The new numerical package is `research/bounded_loop/`. Chapters 01–24 and old code, results and viewers are unchanged. Accumulated README release introductions move to `VERSIONS.en.md`.

There are zero biological observations. Latent responses, sensors and additions are dimensionless synthetic variables, not concentration claims, dose recommendations or laboratory procedures. The modules share evidence roles and logging conventions, not an end-to-end autonomous biological investigator.

## Frozen evaluation scope

| Study | Families | Fixed factors | Runs |
|---|---|---|---:|
| G | Normal, bounded bias, common bias inside/outside bounds, nonlinear sensor, correlated repeats | Three designs, acquisition cost 72, 40 worlds per family | 720 |
| H | Gaussian, heteroscedastic, symmetric t3, skew mean-zero, correlated repeats, broad/narrow/weak shifts, common mode | No-audit comparator plus two policies × three audit fractions; cap 144 | 6,720 |
| I | Normal, heteroscedastic, omitted mean, combined, local omission, contamination, shared batch, within-batch drift | 2/4/6 repeats under 48 observations; 32 worlds per family | 768 |

G computes zero/default/doubled bias envelopes on each dataset. H runs three separate monitors on the same observations. I applies five final analyses to each dataset, including 64 conditional parametric bootstrap fits. These computations are not new independent observations.

After 60 development runs and unit tests, source, configuration and the plan were locally hashed before evaluation. Evaluation IDs and random streams differ from development; generating families remain known to the developer. This is not independent preregistration or external blinding. Chapter 30 is post-result interpretation. Numerical source and thresholds were not retuned after final results.

## Questions and falsification

G asks whether an uncertainty envelope contains the true parameter under its declared bias and sampling assumptions. Hiding the non-vanishing noiseless width, or presenting nonemptiness under excessive common bias as proof of truth, is a failure.

H asks how local variance estimation and sign information trade false alarms, power and acquisition cost. Mean-zero and sign-balance nulls differ. Correlated repeats, skew mean-zero differences and common-mode cancellation remain explicit counterexamples.

I asks whether differences identify technical noise while a fixed extra mean basis addresses structured lack of fit. Shared batch effects and ordered replicate drift are not independent technical noise. Predictive interval widening is not recovery of a mechanism.

## Evidence and cost boundaries

Records preserve `fit / audit / final`, `source=simulated`, and technical-replicate identity. H audits never enter the predictor. All I fits and bootstrap fits complete before final labels are generated. G truth and noiseless projections are evaluator-only and never constrain the noisy-data solver.

G uses analytic evaluator truth, with no additional final assay. H/I use 81 fresh final measurements and separately charge them. H setup and movement costs have their own ledger, not fake observation records. Unspent allocation is visible; equal caps do not imply equal actual spending.

## What is implemented

G is a fixed affine inverse-calibration polytope with a linear response. H combines a few spatial policies and conditional monitors with a quadratic predictor. I uses a quadratic response, one prespecified `sin(pi*x)` residual basis and a two-coefficient logvariance function. No ODE, SINDy, PINN, foundation training or real-data uploader was added.
