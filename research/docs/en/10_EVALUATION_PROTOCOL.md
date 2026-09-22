# 10. Executed evaluation protocol

[한국어](../ko/10_EVALUATION_PROTOCOL.md) · [Implementation](09_IMPLEMENTATION.md) · [Original evaluation plan](../../../docs/en/03_EVALUATION.md)

## Study status

Version 1.1.0 is a **developmental synthetic pilot**, not independent preregistration, external biological validation, or a confirmatory study. Configuration and execution matrix are hashed before this recorded run, but scenarios and gates were inspected during development. Results must not be described as established general improvement. This chapter records the implemented evaluation, not completion of the original plan.

## Matrix and budget

| Scenario | Deliberate condition | Policies |
|---|---|---:|
| smooth | Smooth target broadly compatible with the GP prior | 4 |
| narrow_peak | A peak much narrower than the fixed kernel scale | 4 |
| confounded | Sum observations identify only a coefficient sum | 5 |
| biased_sensor | True selective-readout gain 0.55, assumed gain 1 | 5 |
| missing_term | Nonlinear term absent from the linear model | 5 |
| fidelity_helpful | LF shares useful HF structure | 4 |
| fidelity_deceptive | Input-dependent adverse LF/HF relationship | 4 |
| mechanism_pair | Identical sum observations for A/B mechanisms | 5 |
| mechanism_outside | Truth belongs to neither candidate | 5 |

There are 41 scenario-policy cells plus one identity-operator confounded cell: **42 × seeds 0–11 = 504 runs**. Every cell is reported. These are Monte Carlo executions, not 504 cells, patients, or animals. Truth families and coefficients do not vary across seeds.

Each run has training budget 24. Declared synthetic costs are 1 for sum/HF, 1.8 for selective readout, 2.2 for attenuation, and 0.25 for LF. These are experimental design weights, not measured real laboratory prices or simulation runtime.

## Partitions and reuse

GP, linear, and committee runs start with four sum observations. MF starts with three paired HF/LF locations. HF-only starts with only three HF observations. Policies then select from a finite query grid. A second measurement is an explicit replicate, eligible only after its first measurement.

Validation uses nine locations and final test sixty-one. Linear/committee targets include three readout/intervention variants at each location, producing 27 validation and 183 test observations. Diagnostic plus test overhead is therefore 70 synthetic cost units for GP/MF and 350 for linear/committee. Total measurement cost adds actual training cost. All comparison policies acquire the same diagnostic partition, even when they do not use it for model selection.

Validation is reused for kernel selection, fidelity fallback, and stopping. It is not independent final validation. Each run reveals its final test once, after model freeze and completion of adaptive choices. No code retunes thresholds from that final result. A researcher who modifies subsequent code after reviewing this pilot must create a new version and evaluation set.

## Metrics and success definitions

The latent response means the noise-free observed response function, not recovery of every hidden state. Saved prediction metrics include observation RMSE, MAE, predictive NLL, observation-interval coverage and width, and evaluator-only latent RMSE, coverage, and width. Linear runs record likelihood-design rank without the prior. Finite-candidate runs separately record maximum posterior, resolution at 0.95, candidate correctness, and diagnostic status.

The final dashboard target requires latent RMSE ≤ 0.12 AND observation coverage ≥ 0.80 AND mean interval width ≤ 0.80. **80% coverage of nominal 95% intervals is not claimed to be calibrated 95% coverage.** These are loose developmental acceptance thresholds. Inspect the raw metrics. An unresolved candidate is not counted as identified, and high confidence cannot recover an out-of-library mechanism.

First-passage cost to target is not estimated because the locked final test is not repeatedly inspected. `cost_to_target=null` is intentional. Early stopping and successful cost-to-target are different outcomes. A separate sequential evaluation design would be needed.

## Comparators and confounds

Uniform random samples all eligible actions. Information gain is cost-normalized; observation variance is maximized directly. Fixed readout restricts the action space. Guarded policies combine model selection, exploration, diagnostics, and stopping. Differences cannot therefore be attributed to one isolated causal mechanism of the implementation.

For H2, the separate identity cell uses a misspecified operator during both acquisition and fitting. Additionally, each linear run fits aware and identity models on **the same acquired queries** to isolate fitting effects. Constant, ridge, and known-operator weighted least-squares baselines use identical training records.

GP length scale, noise standard deviation, MF discrepancy, and linear prior are declared constants. Hyperparameter uncertainty, estimated observation noise, actual sensor drift, biological hierarchies, and causal validity of real interventions are not evaluated. A two-candidate library is not symbolic equation discovery.

## Statistical interpretation

Every cell reports mean, seed SD, min, max, target passes, assumption stops, and fidelity fallbacks. Guarded-minus-reference RMSE contrasts pair common seeds and use 2,000 bootstrap resamples. These are descriptive intervals for **seed variation around fixed synthetic functions**, not donor-population confidence intervals, multiplicity-adjusted tests, or general model rankings. Runtime is recorded but not treated as a controlled computational benchmark.

Noise is indexed by scenario, seed, partition, and query ID. Two policies making the same measurement receive the same noise draw. Distinct measurements are not paired merely because they occur at the same iteration. Partition noise streams are separate, and groups cannot cross partitions. These synthetic grouping keys do not represent participants.

## Artifacts and checking

Inspect the [configuration](../../configs/pilot.json), [pre-execution matrix](../../results/pilot/protocol.lock.json), and [full summary](../../results/pilot/summary.json) together. All 504 detailed records are in runs/. The 42 seed-zero records are JSON; remaining records are JSON.gz with complete measurements, events, budgets, and scalar snapshots. Only plotting arrays are omitted from nonrepresentative runs.

```bash
python -m unittest discover -s research/tests -v
python -m unittest discover -s tests -v
python research/validate_research.py
```

Checks cover provenance, budgets, hash links, test-access ordering, schemas, baseline preservation, and UI execution paths. Passing tests does not establish scientific validity or comprehensive security. Actual checks are recorded in [QA](../../quality/QA.md).

## Next evaluation boundary

Any later method designed after viewing these results should treat the current pilot as development data. A new synthetic test bank should vary unseen function families, effect sizes, noise laws, sensor gains, and mismatch strengths before policy evaluation. Report false alarms, missed detection, stop delay, total cost, and final prediction loss jointly. This is a proposed next study, not an experiment already present in the 504 runs.
