# 16. Research decisions: establish distinguishability before repairing a model

[한국어](../ko/16_RESEARCH_DECISIONS.md) · [Results](15_FOLLOWUP_RESULTS.md) · [Previous agenda](12_RESEARCH_DIRECTION.md)

## Decisions from this version

This is a bounded execution of prior tasks A (detector evaluation) and B (measurement-type choice), not completed causal fault isolation. Earlier documents 01–12 remain unchanged.

| Question | Decision | Evidence and boundary |
|---|---|---|
| Use naive repeated p<0.05 as default? | No | 38.5% all-null warnings; retain explicit finite error budgets |
| Declare empirical calibration better than Bonferroni? | No | Normal evaluation rates 6.1% versus 5.5% |
| Stop automatically at every first alarm? | Not the default | A detected effect may already be modeled; stopping can remove useful learning |
| Retain only block-targeted acquisition? | No | Joint-information has lower gain/offset RMSE; cost-matched no-audit remains relevant |
| Will more identical measurements isolate the cause? | Explicitly no | Reference/specimen mismatch admits an observationally equivalent reparameterization |
| Expand directly to ODE/PINN/foundation models? | Defer | Calibration transport and spatial audit blind spots are unresolved |

## Task D: observations that test calibration transport

Can the equality of the reference and specimen measurement laws be tested using information beyond model residuals? Introduce a second measurement operator or a known within-specimen change in a new synthetic study. Distinguish a measurement that merely assumes shared calibration from one that independently tests it. A known increment can identify gain while leaving offset confounded with the latent intercept; compute the full information rank and equivalence classes.

**Falsification:** if the added action lies in the previous observation row space, or shares the same untested fault, do not claim source identification. Model-generated reference values must never count as fresh calibration evidence.

Evaluate observational equivalence, true parameter recovery, missed violations and cost. A future interface might distinguish unresolved, identifiable-under-assumptions and contradicted; these are proposed states, not implemented API claims.

## Task E: diagnostics that cover the domain without dominating cost

Compare the current three-location panel with a prespecified randomized broad-domain audit and a budgeted progressive coverage design. Keep acquisition and diagnostic data permissions separate. Choosing checks solely from a misspecified model's own uncertainty may perpetuate overconfidence.

**Falsification:** reject additional complexity if normal false warnings or cost increase without lower local-fault misses and predictive loss compared with uniform diagnostics at the same total cost. Once locations or look counts become data-adaptive, do not reuse v1.2's fixed-panel validity statement unchanged. Only then introduce an appropriate sequential test or separately calibrated trajectory bank. [D04](../../followup/references/REFERENCES.md#d04) [D05](../../followup/references/REFERENCES.md#d05)

## Task F: separate noise-model effects from acquisition effects

Technical replicates currently estimate one noise variance and pass it to the likelihood, acquisition and prediction; no heteroscedastic variance function or tail model is learned. Next, fit homoscedastic Gaussian, a small variance-function model and a robust likelihood on identical observations, then hold the estimator fixed while varying the acquisition policy. Cross the dataset, estimator and policy factors rather than attributing a combined pipeline improvement to one component.

**Falsification:** do not promote robustification when it only widens intervals without better proper scores, error or cost, or when normal/small-effect sensitivity deteriorates materially. A flexible residual term that absorbs both noise and discrepancy creates another identifiability problem. [D02](../../followup/references/REFERENCES.md#d02)

## Next-bank governance

The v1.2 generator and outcomes are now development information. A v1.3 bank needs new world IDs plus new observation-law failures, relationships between audit and fault locations, cost ratios and weaker effects. External evaluator ownership would strengthen independence; when unavailable, state the limits of a local lock. Post-result follow-up hypotheses are not retrospective preregistration.

Original H1/H2 received bounded additional tests. H3 covers provenance barriers only; H4 hierarchical biological effects remains unimplemented. H5 multi-fidelity behavior is preserved from v1.1 but not extended here. H6 now includes finite diagnostic testing, not distribution-free coverage for adaptively acquired predictions. Real biological data, ODE/SINDy/PINN and foundation-model training remain out of scope.
