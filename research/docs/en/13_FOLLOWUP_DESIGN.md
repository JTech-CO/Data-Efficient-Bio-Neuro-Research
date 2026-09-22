# 13. Follow-up A and B: detection is not source identification

[한국어](../ko/13_FOLLOWUP_DESIGN.md) · [Previous agenda](12_RESEARCH_DIRECTION.md) · [Protocol](14_DIAGNOSTIC_PROTOCOL.md) · [Results](15_FOLLOWUP_RESULTS.md)

## Research question

v1.2.0-research.1 adds executable studies A and B without rewriting chapters 01-12. It asks whether assumptions are violated, which measurement channels carry evidence of a violation, and which next measurement reduces the relevant uncertainty. It does not create a biological foundation model, discover neural dynamics, make clinical diagnoses, or authorize real experiments.

Measurement calibration with a noise likelihood already has biotechnology implementations, including calibr8 and murefi. Calibration parameters and unexplained model discrepancy can be confounded. These established problems motivate this implementation; combining the components is not presented as a new regression theory. [D01](../../followup/references/REFERENCES.md#d01) [D02](../../followup/references/REFERENCES.md#d02)

## Two distinct studies

**Study A tests the detector.** Measurement locations and looks are fixed. Naive, finite-look Bonferroni and calibration-bank maximum-score rules use exactly the same observations. This separates error-rate behavior from adaptive acquisition.

**Study B tests acquisition and inference.** Sensor gain/offset and latent-response coefficients are unknown. Reference measurements, ordinary measurements and declared synthetic interventions have different costs. Multiple estimators are evaluated on the same acquired records to separate acquisition effects from inference effects. A simple calibration-then-regression strategy is a serious comparator, not a deliberately weak baseline.

Identifiability-directed acquisition already exists, for example E-ALPIPE; our local information surrogate is not its implementation. Active learning has also been applied to synaptic recordings, but neither those recordings nor ESB-BAL are reproduced here. [D03](../../followup/references/REFERENCES.md#d03) [D07](../../followup/references/REFERENCES.md#d07)

## Synthetic bank and available information

Development and null-calibration banks use phi(x)=x. Evaluation alternates normalized tanh and a monotone cubic feature, with new nuisance coefficients, fault magnitudes/signs and observation noise per world. The public feature is supplied to the model. This is not discovery of an unknown function family or demonstrated biological-domain transfer. A separate local-bump scenario explicitly violates the fitted feature dictionary.

| Scenario | Violated assumption | Diagnostic purpose |
|---|---|---|
| normal | none | all-null sequential false warning |
| gain_offset | sensor gain/offset | separable calibration error |
| mechanism | no intervention-associated departure | mechanism-like signal versus calibration |
| noise_scale | nominal noise magnitude | repeated-measurement variance |
| combined | sensor, mechanism and noise | avoid forced single-cause labels |
| nonlinear_sensor | affine sensor | ambiguity between sensor and mechanism residuals |
| heteroscedastic | constant variance | limits of homoscedastic tests and intervals |
| heavy_tail | Gaussianity, but not variance | distribution mismatch |
| local_bump | no unmodelled local departure | blind spots between fixed probes |
| reference_mismatch | shared sensor law for reference and specimen | calibration transport failure |

Not rejecting a diagnostic null is not certification. The final two scenarios are deliberate counterexamples to the belief that more measurements under the same assumptions necessarily resolve the problem. Causal negative controls and metrology standards are different techniques; D06 is cited only for the methodological caution about assumptions linking controls to the primary process. [D06](../../followup/references/REFERENCES.md#d06)

## Implementation boundary

The new module `research/diagnostic_loop/` uses new contracts and leaves v1.1 time/replicate restrictions untouched. It reuses only the earlier serialization/hash-log utility. Observations must be simulated, never count as new biological units, and never carry real-world authorization.

The runner owns synthetic truth. Policies and inference receive PublicDesign, observed records and current fits, not World objects, fault labels or final outcomes. Truth is attached to output for evaluator-side scoring. Python module boundaries are reproducibility checks, not a security sandbox against malicious code.

## Hypotheses and falsification

F1 compares error control of three warning rules. F2 compares reference-enabled inference with a no-reference ablation and retains rank deficiency instead of hiding it with priors. F3 compares fixed calibration, joint and block information policies, including an equal-total-cost no-audit baseline; complexity is not promoted without benefit. F4 compares calibration/noise uncertainty treatment on identical data. F5 checks diagnostic-channel agreement and missed faults without equating a warning with causal attribution.

Chapter 15 reports all results. Time-dependent dynamics, PINN/BINN/SINDy, donor hierarchies and real-data ingestion remain outside this release.
