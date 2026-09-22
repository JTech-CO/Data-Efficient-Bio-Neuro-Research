# 15. Follow-up results: fewer warnings do not identify the cause

[한국어](../ko/15_FOLLOWUP_RESULTS.md) · [Design](13_FOLLOWUP_DESIGN.md) · [Protocol](14_DIAGNOSTIC_PROTOCOL.md) · [Decisions](16_RESEARCH_DECISIONS.md) · [Raw summary](../../followup/results/v120/summary.json)

**v1.2.0-research.1; zero biological observations.** These are executions of the bundled code, not numbers from cited papers. Forty development runs and 2,000 all-null calibration trajectories preceded the locked evaluation: 1,900 diagnostic trajectories in study A and 1,920 acquisition runs in study B. Study A applies three detectors to the same observations. Study B applies six policies to 320 distinct synthetic worlds, not 1,920 independent worlds or patients.

The code, configuration and thresholds were locally hashed before evaluation and not modified after outcomes were seen. This is not independent preregistration or external blinding. The generator rules are known to the developer. Evaluation uses new public feature families, but those features are supplied to inference; this is not unknown-function discovery or biological domain generalization.

## 1. Findings that change the next research decision

### Repeated testing requires an explicit error budget

Among 1,000 normal evaluation worlds, naive p<0.05 at each look/channel warned in **385 (38.5%)**, finite-look Bonferroni in **55 (5.5%)**, and calibrated maximum-score monitoring in **61 (6.1%)**. Wilson 95% intervals for the latter two are 4.25–7.09% and 4.78–7.76%. Both point estimates exceed 5%; the experiment does not empirically establish a rate below 5%. Both intervals contain 5%. The calibrated rule has a marginal exchangeability statement over the calibration trajectories plus a new null trajectory, not a conditional guarantee for this one fixed calibration bank.

This supports F1 within the declared finite-look setting, not unrestricted anytime validity under arbitrary adaptive audits, heteroscedasticity or heavy tails. No e-process or confidence sequence is implemented.

### A diagnostic flag is not a causal source certificate

Calibrated monitoring warned in 100/100 gain/offset worlds and 99/100 known-intervention-effect worlds. Yet exact tag-set agreement was only 66% for combined faults. All nonlinear-sensor worlds warned, but **88/100 also triggered the mechanism lack-of-fit channel**; exact agreement with the generator's source tags was only 10%.

The mechanism test targets the restricted no-intervention [1,phi] null. The acquisition regression already includes the intervention coefficient. Thus a flag does not necessarily mean that the expanded fitted regression is wrong. The `causal_source_identified` field remains false in every record. Negative-control literature motivates caution about assumptions but does not make sensor calibration standards identical to causal negative controls. [D06](../../followup/references/REFERENCES.md#d06)

### Calibration transport is an unresolved identifiability boundary

When reference standards have an identity sensor but specimens have changed gain/offset, calibrated monitoring warns only **4/100** times. Nonspecific chance flags are not evidence that the causal fault was correctly detected. Specimen response g(theta0+theta1 phi)+b is exactly equivalent to an identity sensor with theta0'=g theta0+b and theta1'=g theta1, while references remain identical. Repeating the same measurements or increasing model size cannot distinguish these worlds. A new observation with independently justified transport or an additional measurement operator is required; specimen-matched standards or standard addition are future synthetic design options, not implemented biological procedures.

### Fixed audit locations have blind spots

The narrow `local_bump` lies between x=-1,0,1 audit locations. There were 6/100 nonspecific warnings and **zero mechanism-channel hits**. Passing a sparse panel cannot certify the whole domain. Equal-variance t3 errors produced only 19% warnings: an overdispersion test is not an omnibus test for heavy-tail misspecification.

### Targeted acquisition helps in some settings, but no new universal winner emerges

For gain/offset, latent RMSE was 0.1392 for random, 0.0822 for reference-first, 0.0642 for joint-information and 0.0731 for block-targeted. Block targeting did not outperform joint-information there. For combined faults the latter three were 0.1658, 0.1204 and 0.1063. Descriptive paired bootstrap intervals do not constitute multiplicity-adjusted superiority tests.

The no-reference ablation achieved normal-world RMSE 0.0357 but had rank 3 and mean interval width 2.2107. Its prior mean happens to match the normal sensor; that is not data-based identification. Gain/offset RMSE deteriorated to 0.2999.

### Same-data uncertainty ablations matter

On block-targeted normal worlds, removing calibration uncertainty while keeping the same prediction mean reduced inclusion from **94.6% to 86.4%** and width from **0.2421 to 0.1730**. On combined worlds, estimated noise plus calibration propagation yielded 94.3% inclusion versus 73.8% with nominal noise, but width increased from 0.2635 to 0.4684. Wider intervals and better point prediction are different effects.

Block-targeted inclusion remained only 58.1% for nonlinear sensors and 27.6% for reference/specimen mismatch. The plug-in global variance and Gaussian delta approximation do not solve arbitrary misspecification. The calibration literature supports modeling the measurement process, not generalizing these toy outcomes to the biological experiments in that literature. [D01](../../followup/references/REFERENCES.md#d01)

### Diagnostic measurement cost dominates this small design

Three panels cost 77.4 units against a fit budget of 36: **2.15 times** the training cost and about **68.3%** of the 113.4 acquisition cap. Final test measurements cost another 114.8. The no-audit reference-first baseline spends the same acquisition cap on fitting. It still uses only two initial endpoint calibration batches, so it is not an optimally budget-allocated representative of every non-monitoring approach.

For block-targeted combined faults, a model frozen at the first alarm had RMSE 0.1896 versus 0.1063 after continued acquisition. The earlier acquisition cost of 51.03 is not successful data-efficiency improvement. This is an **offline counterfactual using prefixes frozen before final testing**, not a separately executed online stopping policy.

## 2. Full study A results

Any alarm includes irrelevant channels. For faulty worlds, the miss rate is one minus this frequency, but a nonspecific warning is not correct source attribution. Exact tag-set agreement is a descriptive comparison to synthetic generator labels. Channel columns contain counts. *Mean first look conditions on detection; the JSON also reports a restricted mean assigning undetected trajectories look 4.

### `naive`

| Scenario | N | Any alarm | Wilson 95% | Sensor affine / nonlinear | Mechanism | Noise | Exact tag set | First look* |
|---|---:|---:|---|---:|---:|---:|---:|---:|
| normal | 1000 | 385/1000 | 0.355–0.416 | 119 / 100 | 109 | 107 | 61.5% | 1.77 |
| gain_offset | 100 | 100/100 | 0.963–1.000 | 100 / 9 | 14 | 11 | 75.0% | 1.07 |
| mechanism | 100 | 100/100 | 0.963–1.000 | 8 / 11 | 100 | 9 | 76.0% | 1.06 |
| noise_scale | 100 | 100/100 | 0.963–1.000 | 12 / 9 | 10 | 100 | 74.0% | 1.11 |
| combined | 100 | 100/100 | 0.963–1.000 | 99 / 14 | 91 | 100 | 91.0% | 1.00 |
| nonlinear_sensor | 100 | 100/100 | 0.963–1.000 | 98 / 99 | 97 | 9 | 3.0% | 1.12 |
| heteroscedastic | 100 | 100/100 | 0.963–1.000 | 18 / 4 | 13 | 100 | 67.0% | 1.16 |
| heavy_tail | 100 | 41/100 | 0.319–0.508 | 10 / 10 | 10 | 16 | 14.0% | 1.56 |
| local_bump | 100 | 40/100 | 0.309–0.498 | 10 / 16 | 12 | 11 | 7.0% | 1.80 |
| reference_mismatch | 100 | 37/100 | 0.282–0.468 | 14 / 5 | 7 | 15 | 16.0% | 1.70 |

### `bonferroni`

| Scenario | N | Any alarm | Wilson 95% | Sensor affine / nonlinear | Mechanism | Noise | Exact tag set | First look* |
|---|---:|---:|---|---:|---:|---:|---:|---:|
| normal | 1000 | 55/1000 | 0.042–0.071 | 11 / 14 | 15 | 15 | 94.5% | 1.78 |
| gain_offset | 100 | 100/100 | 0.963–1.000 | 100 / 0 | 0 | 1 | 99.0% | 1.46 |
| mechanism | 100 | 99/100 | 0.946–0.998 | 0 / 0 | 99 | 1 | 98.0% | 1.61 |
| noise_scale | 100 | 100/100 | 0.963–1.000 | 3 / 2 | 2 | 98 | 93.0% | 1.33 |
| combined | 100 | 100/100 | 0.963–1.000 | 95 / 2 | 69 | 100 | 66.0% | 1.20 |
| nonlinear_sensor | 100 | 100/100 | 0.963–1.000 | 78 / 81 | 86 | 1 | 13.0% | 1.77 |
| heteroscedastic | 100 | 99/100 | 0.946–0.998 | 2 / 0 | 1 | 99 | 96.0% | 1.48 |
| heavy_tail | 100 | 19/100 | 0.125–0.278 | 1 / 4 | 2 | 13 | 13.0% | 1.89 |
| local_bump | 100 | 6/100 | 0.028–0.125 | 1 / 4 | 0 | 1 | 0.0% | 1.17 |
| reference_mismatch | 100 | 4/100 | 0.016–0.098 | 2 / 1 | 0 | 1 | 3.0% | 1.75 |

### `calibrated_max`

| Scenario | N | Any alarm | Wilson 95% | Sensor affine / nonlinear | Mechanism | Noise | Exact tag set | First look* |
|---|---:|---:|---|---:|---:|---:|---:|---:|
| normal | 1000 | 61/1000 | 0.048–0.078 | 12 / 15 | 17 | 17 | 93.9% | 1.77 |
| gain_offset | 100 | 100/100 | 0.963–1.000 | 100 / 0 | 0 | 1 | 99.0% | 1.44 |
| mechanism | 100 | 99/100 | 0.946–0.998 | 0 / 0 | 99 | 1 | 98.0% | 1.57 |
| noise_scale | 100 | 100/100 | 0.963–1.000 | 3 / 2 | 2 | 98 | 93.0% | 1.33 |
| combined | 100 | 100/100 | 0.963–1.000 | 95 / 2 | 69 | 100 | 66.0% | 1.19 |
| nonlinear_sensor | 100 | 100/100 | 0.963–1.000 | 81 / 84 | 88 | 2 | 10.0% | 1.74 |
| heteroscedastic | 100 | 99/100 | 0.946–0.998 | 2 / 0 | 1 | 99 | 96.0% | 1.46 |
| heavy_tail | 100 | 19/100 | 0.125–0.278 | 1 / 4 | 2 | 13 | 13.0% | 1.89 |
| local_bump | 100 | 6/100 | 0.028–0.125 | 1 / 4 | 0 | 1 | 0.0% | 1.17 |
| reference_mismatch | 100 | 4/100 | 0.016–0.098 | 2 / 1 | 0 | 1 | 3.0% | 1.75 |

## 3. Full study B results

Every cell contains 32 worlds paired across policies. Inclusion concerns the latent z, not future noisy sensor observations; the latter remain in raw `evaluation.estimators.*.observed`. *Total includes the 114.8 final-test measurement cost. Rank is conditional on the assumed linear design, not proof that the observation law is true. No-audit warning frequency is missing/not monitored, not zero.

### `normal`

| Policy | RMSE mean ± SD | Latent 95% inclusion | Mean width | Rank 5 | Alarm | Fit / audit / total* |
|---|---:|---:|---:|---:|---:|---:|
| `random` | 0.0649 ± 0.0356 | 98.1% | 0.7003 | 68.8% | 3.1% | 35.33 / 77.40 / 227.53 |
| `reference_first` | 0.0682 ± 0.0341 | 96.2% | 0.3123 | 100.0% | 3.1% | 36.00 / 77.40 / 228.20 |
| `joint_information` | 0.0554 ± 0.0295 | 95.0% | 0.2522 | 100.0% | 3.1% | 34.80 / 77.40 / 227.00 |
| `block_targeted` | 0.0546 ± 0.0276 | 94.6% | 0.2421 | 100.0% | 3.1% | 35.59 / 77.40 / 227.79 |
| `no_reference` | 0.0357 ± 0.0185 | 100.0% | 2.2107 | 0.0% | 3.1% | 35.86 / 77.40 / 228.06 |
| `reference_first_no_audit` | 0.0657 ± 0.0326 | 96.0% | 0.2887 | 100.0% | not monitored | 112.40 / 0.00 / 227.20 |

### `gain_offset`

| Policy | RMSE mean ± SD | Latent 95% inclusion | Mean width | Rank 5 | Alarm | Fit / audit / total* |
|---|---:|---:|---:|---:|---:|---:|
| `random` | 0.1392 ± 0.1023 | 98.6% | 0.8030 | 59.4% | 100.0% | 35.20 / 77.40 / 227.40 |
| `reference_first` | 0.0822 ± 0.0513 | 91.9% | 0.3373 | 100.0% | 100.0% | 36.00 / 77.40 / 228.20 |
| `joint_information` | 0.0642 ± 0.0434 | 95.7% | 0.2714 | 100.0% | 100.0% | 34.80 / 77.40 / 227.00 |
| `block_targeted` | 0.0731 ± 0.0418 | 90.8% | 0.2596 | 100.0% | 100.0% | 35.22 / 77.40 / 227.42 |
| `no_reference` | 0.2999 ± 0.0850 | 100.0% | 2.2465 | 0.0% | 100.0% | 35.80 / 77.40 / 228.00 |
| `reference_first_no_audit` | 0.0715 ± 0.0412 | 97.1% | 0.3311 | 100.0% | not monitored | 112.40 / 0.00 / 227.20 |

### `mechanism`

| Policy | RMSE mean ± SD | Latent 95% inclusion | Mean width | Rank 5 | Alarm | Fit / audit / total* |
|---|---:|---:|---:|---:|---:|---:|
| `random` | 0.0617 ± 0.0448 | 97.3% | 0.8662 | 56.2% | 100.0% | 35.30 / 77.40 / 227.50 |
| `reference_first` | 0.0727 ± 0.0381 | 94.0% | 0.3214 | 100.0% | 100.0% | 36.00 / 77.40 / 228.20 |
| `joint_information` | 0.0640 ± 0.0322 | 90.2% | 0.2461 | 100.0% | 100.0% | 34.80 / 77.40 / 227.00 |
| `block_targeted` | 0.0599 ± 0.0283 | 93.8% | 0.2398 | 100.0% | 100.0% | 35.78 / 77.40 / 227.98 |
| `no_reference` | 0.0364 ± 0.0190 | 100.0% | 2.2289 | 0.0% | 100.0% | 35.69 / 77.40 / 227.89 |
| `reference_first_no_audit` | 0.0625 ± 0.0372 | 96.5% | 0.2907 | 100.0% | not monitored | 112.40 / 0.00 / 227.20 |

### `noise_scale`

| Policy | RMSE mean ± SD | Latent 95% inclusion | Mean width | Rank 5 | Alarm | Fit / audit / total* |
|---|---:|---:|---:|---:|---:|---:|
| `random` | 0.1280 ± 0.0836 | 93.6% | 1.0294 | 53.1% | 100.0% | 35.27 / 77.40 / 227.47 |
| `reference_first` | 0.1495 ± 0.0584 | 86.1% | 0.5387 | 100.0% | 100.0% | 36.00 / 77.40 / 228.20 |
| `joint_information` | 0.0994 ± 0.0419 | 94.9% | 0.4459 | 100.0% | 100.0% | 34.80 / 77.40 / 227.00 |
| `block_targeted` | 0.0922 ± 0.0432 | 95.6% | 0.4296 | 100.0% | 100.0% | 35.72 / 77.40 / 227.93 |
| `no_reference` | 0.0590 ± 0.0253 | 100.0% | 2.2122 | 0.0% | 100.0% | 35.71 / 77.40 / 227.91 |
| `reference_first_no_audit` | 0.1251 ± 0.0521 | 91.7% | 0.5149 | 100.0% | not monitored | 112.40 / 0.00 / 227.20 |

### `combined`

| Policy | RMSE mean ± SD | Latent 95% inclusion | Mean width | Rank 5 | Alarm | Fit / audit / total* |
|---|---:|---:|---:|---:|---:|---:|
| `random` | 0.2253 ± 0.1240 | 93.2% | 1.0179 | 43.8% | 100.0% | 35.42 / 77.40 / 227.62 |
| `reference_first` | 0.1658 ± 0.1210 | 90.5% | 0.6435 | 100.0% | 100.0% | 36.00 / 77.40 / 228.20 |
| `joint_information` | 0.1204 ± 0.1026 | 95.9% | 0.5058 | 100.0% | 100.0% | 34.80 / 77.40 / 227.00 |
| `block_targeted` | 0.1063 ± 0.0610 | 94.3% | 0.4684 | 100.0% | 100.0% | 35.28 / 77.40 / 227.47 |
| `no_reference` | 0.2962 ± 0.0815 | 100.0% | 2.2943 | 0.0% | 100.0% | 35.71 / 77.40 / 227.91 |
| `reference_first_no_audit` | 0.1449 ± 0.1189 | 91.5% | 0.5688 | 100.0% | not monitored | 112.40 / 0.00 / 227.20 |

### `nonlinear_sensor`

| Policy | RMSE mean ± SD | Latent 95% inclusion | Mean width | Rank 5 | Alarm | Fit / audit / total* |
|---|---:|---:|---:|---:|---:|---:|
| `random` | 0.2388 ± 0.2307 | 74.9% | 0.7098 | 78.1% | 100.0% | 35.12 / 77.40 / 227.32 |
| `reference_first` | 0.1402 ± 0.0577 | 63.1% | 0.3243 | 100.0% | 100.0% | 36.00 / 77.40 / 228.20 |
| `joint_information` | 0.1194 ± 0.0809 | 62.6% | 0.2559 | 100.0% | 100.0% | 34.80 / 77.40 / 227.00 |
| `block_targeted` | 0.1252 ± 0.0733 | 58.1% | 0.2479 | 100.0% | 100.0% | 35.33 / 77.40 / 227.53 |
| `no_reference` | 0.2772 ± 0.1149 | 100.0% | 2.2399 | 0.0% | 100.0% | 35.77 / 77.40 / 227.98 |
| `reference_first_no_audit` | 0.1492 ± 0.0581 | 49.6% | 0.2954 | 100.0% | not monitored | 112.40 / 0.00 / 227.20 |

### `heteroscedastic`

| Policy | RMSE mean ± SD | Latent 95% inclusion | Mean width | Rank 5 | Alarm | Fit / audit / total* |
|---|---:|---:|---:|---:|---:|---:|
| `random` | 0.1229 ± 0.0628 | 94.1% | 0.8619 | 65.6% | 100.0% | 35.30 / 77.40 / 227.50 |
| `reference_first` | 0.1504 ± 0.0853 | 91.2% | 0.5845 | 100.0% | 100.0% | 36.00 / 77.40 / 228.20 |
| `joint_information` | 0.1270 ± 0.0578 | 95.0% | 0.5303 | 100.0% | 100.0% | 34.80 / 77.40 / 227.00 |
| `block_targeted` | 0.1250 ± 0.0521 | 93.3% | 0.5145 | 100.0% | 100.0% | 35.66 / 77.40 / 227.86 |
| `no_reference` | 0.0721 ± 0.0371 | 100.0% | 2.2183 | 0.0% | 100.0% | 35.70 / 77.40 / 227.90 |
| `reference_first_no_audit` | 0.1322 ± 0.0875 | 91.0% | 0.5016 | 100.0% | not monitored | 112.40 / 0.00 / 227.20 |

### `heavy_tail`

| Policy | RMSE mean ± SD | Latent 95% inclusion | Mean width | Rank 5 | Alarm | Fit / audit / total* |
|---|---:|---:|---:|---:|---:|---:|
| `random` | 0.0652 ± 0.0385 | 98.8% | 0.6819 | 62.5% | 12.5% | 35.21 / 77.40 / 227.41 |
| `reference_first` | 0.0564 ± 0.0277 | 98.1% | 0.2909 | 100.0% | 12.5% | 36.00 / 77.40 / 228.20 |
| `joint_information` | 0.0455 ± 0.0258 | 96.8% | 0.2255 | 100.0% | 12.5% | 34.76 / 77.40 / 226.96 |
| `block_targeted` | 0.0458 ± 0.0268 | 96.4% | 0.2181 | 100.0% | 12.5% | 35.58 / 77.40 / 227.77 |
| `no_reference` | 0.0374 ± 0.0286 | 100.0% | 2.2115 | 0.0% | 12.5% | 35.86 / 77.40 / 228.06 |
| `reference_first_no_audit` | 0.0484 ± 0.0253 | 98.8% | 0.2805 | 100.0% | not monitored | 112.40 / 0.00 / 227.20 |

### `local_bump`

| Policy | RMSE mean ± SD | Latent 95% inclusion | Mean width | Rank 5 | Alarm | Fit / audit / total* |
|---|---:|---:|---:|---:|---:|---:|
| `random` | 0.1462 ± 0.0366 | 90.8% | 0.5508 | 75.0% | 0.0% | 35.27 / 77.40 / 227.47 |
| `reference_first` | 0.1356 ± 0.0249 | 92.9% | 0.3275 | 100.0% | 0.0% | 36.00 / 77.40 / 228.20 |
| `joint_information` | 0.1320 ± 0.0220 | 89.5% | 0.2570 | 100.0% | 0.0% | 34.80 / 77.40 / 227.00 |
| `block_targeted` | 0.1343 ± 0.0267 | 87.5% | 0.2479 | 100.0% | 0.0% | 35.71 / 77.40 / 227.91 |
| `no_reference` | 0.1234 ± 0.0241 | 100.0% | 2.1968 | 0.0% | 0.0% | 35.79 / 77.40 / 227.99 |
| `reference_first_no_audit` | 0.1325 ± 0.0263 | 93.8% | 0.2948 | 100.0% | not monitored | 112.40 / 0.00 / 227.20 |

### `reference_mismatch`

| Policy | RMSE mean ± SD | Latent 95% inclusion | Mean width | Rank 5 | Alarm | Fit / audit / total* |
|---|---:|---:|---:|---:|---:|---:|
| `random` | 0.3051 ± 0.1142 | 55.1% | 0.6817 | 65.6% | 3.1% | 35.24 / 77.40 / 227.44 |
| `reference_first` | 0.2902 ± 0.0926 | 35.4% | 0.3230 | 100.0% | 3.1% | 36.00 / 77.40 / 228.20 |
| `joint_information` | 0.2937 ± 0.0745 | 27.1% | 0.2638 | 100.0% | 3.1% | 34.80 / 77.40 / 227.00 |
| `block_targeted` | 0.2943 ± 0.0732 | 27.6% | 0.2529 | 100.0% | 3.1% | 35.52 / 77.40 / 227.72 |
| `no_reference` | 0.2920 ± 0.0708 | 100.0% | 2.2879 | 0.0% | 3.1% | 35.81 / 77.40 / 228.01 |
| `reference_first_no_audit` | 0.2868 ± 0.0825 | 33.7% | 0.3102 | 100.0% | not monitored | 112.40 / 0.00 / 227.20 |

## 4. Same-acquired-data estimator ablations

All estimators use the same fit observations within each policy run. The table shows all ten world types for block-targeted acquisition. `plugin_calibration` keeps the mean but omits sensor uncertainty. `oracle_affine_calibration` uses evaluator-only true affine gain/offset, not full knowledge of a nonlinear sensor. It is not a deployable policy. Results for five estimators on all 1,920 runs remain in the raw and compact records.

| Scenario | Estimator on identical block-targeted data | RMSE | Inclusion | Width |
|---|---|---:|---:|---:|
| `normal` | `propagated` | 0.0546 | 94.6% | 0.2421 |
| `normal` | `plugin_calibration` | 0.0546 | 86.4% | 0.1730 |
| `normal` | `nominal_noise` | 0.0546 | 95.9% | 0.2472 |
| `normal` | `identity_baseline` | 0.0396 | 93.8% | 0.1733 |
| `normal` | `oracle_affine_calibration` | 0.0396 | 93.8% | 0.1731 |
| `gain_offset` | `propagated` | 0.0731 | 90.8% | 0.2596 |
| `gain_offset` | `plugin_calibration` | 0.0731 | 82.3% | 0.1952 |
| `gain_offset` | `nominal_noise` | 0.0731 | 93.6% | 0.2783 |
| `gain_offset` | `identity_baseline` | 0.3000 | 20.7% | 0.1754 |
| `gain_offset` | `oracle_affine_calibration` | 0.0538 | 93.5% | 0.1921 |
| `mechanism` | `propagated` | 0.0599 | 93.8% | 0.2398 |
| `mechanism` | `plugin_calibration` | 0.0599 | 77.5% | 0.1668 |
| `mechanism` | `nominal_noise` | 0.0598 | 94.8% | 0.2488 |
| `mechanism` | `identity_baseline` | 0.0398 | 91.7% | 0.1655 |
| `mechanism` | `oracle_affine_calibration` | 0.0399 | 91.7% | 0.1654 |
| `noise_scale` | `propagated` | 0.0922 | 95.6% | 0.4296 |
| `noise_scale` | `plugin_calibration` | 0.0922 | 83.7% | 0.3040 |
| `noise_scale` | `nominal_noise` | 0.0931 | 74.9% | 0.2410 |
| `noise_scale` | `identity_baseline` | 0.0691 | 94.0% | 0.3114 |
| `noise_scale` | `oracle_affine_calibration` | 0.0687 | 94.1% | 0.3106 |
| `combined` | `propagated` | 0.1063 | 94.3% | 0.4684 |
| `combined` | `plugin_calibration` | 0.1063 | 86.0% | 0.3483 |
| `combined` | `nominal_noise` | 0.1069 | 73.8% | 0.2635 |
| `combined` | `identity_baseline` | 0.2858 | 40.7% | 0.3335 |
| `combined` | `oracle_affine_calibration` | 0.0799 | 95.8% | 0.3546 |
| `nonlinear_sensor` | `propagated` | 0.1252 | 58.1% | 0.2479 |
| `nonlinear_sensor` | `plugin_calibration` | 0.1252 | 49.2% | 0.1834 |
| `nonlinear_sensor` | `nominal_noise` | 0.1252 | 57.9% | 0.2497 |
| `nonlinear_sensor` | `identity_baseline` | 0.3429 | 3.6% | 0.1822 |
| `nonlinear_sensor` | `oracle_affine_calibration` | 0.3427 | 3.5% | 0.1821 |
| `heteroscedastic` | `propagated` | 0.1250 | 93.3% | 0.5145 |
| `heteroscedastic` | `plugin_calibration` | 0.1250 | 79.5% | 0.3658 |
| `heteroscedastic` | `nominal_noise` | 0.1267 | 59.0% | 0.2444 |
| `heteroscedastic` | `identity_baseline` | 0.0893 | 93.8% | 0.3688 |
| `heteroscedastic` | `oracle_affine_calibration` | 0.0888 | 94.0% | 0.3675 |
| `heavy_tail` | `propagated` | 0.0458 | 96.4% | 0.2181 |
| `heavy_tail` | `plugin_calibration` | 0.0458 | 86.9% | 0.1565 |
| `heavy_tail` | `nominal_noise` | 0.0458 | 97.1% | 0.2463 |
| `heavy_tail` | `identity_baseline` | 0.0350 | 98.0% | 0.1573 |
| `heavy_tail` | `oracle_affine_calibration` | 0.0349 | 98.0% | 0.1571 |
| `local_bump` | `propagated` | 0.1343 | 87.5% | 0.2479 |
| `local_bump` | `plugin_calibration` | 0.1343 | 77.1% | 0.1753 |
| `local_bump` | `nominal_noise` | 0.1343 | 89.3% | 0.2455 |
| `local_bump` | `identity_baseline` | 0.1287 | 84.2% | 0.1756 |
| `local_bump` | `oracle_affine_calibration` | 0.1287 | 84.2% | 0.1755 |
| `reference_mismatch` | `propagated` | 0.2943 | 27.6% | 0.2529 |
| `reference_mismatch` | `plugin_calibration` | 0.2943 | 21.0% | 0.1801 |
| `reference_mismatch` | `nominal_noise` | 0.2943 | 27.8% | 0.2530 |
| `reference_mismatch` | `identity_baseline` | 0.2949 | 20.7% | 0.1791 |
| `reference_mismatch` | `oracle_affine_calibration` | 0.0387 | 95.4% | 0.1789 |
## 5. Paired RMSE differences

Policy minus reference_first; negative is smaller RMSE in this sample. Intervals are descriptive 95% bootstrap intervals from 2,000 resamples of 32 paired worlds, not multiplicity-adjusted tests or biological-population intervals. Do not interpret no-reference RMSE separately from rank and interval width.

| Scenario | Policy minus reference_first | Δ RMSE | Descriptive paired 95% |
|---|---|---:|---|
| `normal` | `block_targeted` | -0.01361 | [-0.02258, -0.00463] |
| `normal` | `joint_information` | -0.01274 | [-0.02193, -0.00362] |
| `normal` | `no_reference` | -0.03252 | [-0.04764, -0.01688] |
| `normal` | `reference_first_no_audit` | -0.00244 | [-0.00752, 0.00249] |
| `gain_offset` | `block_targeted` | -0.00910 | [-0.02600, 0.00771] |
| `gain_offset` | `joint_information` | -0.01806 | [-0.03586, -0.00247] |
| `gain_offset` | `no_reference` | 0.21773 | [0.18460, 0.24964] |
| `gain_offset` | `reference_first_no_audit` | -0.01071 | [-0.01981, -0.00162] |
| `mechanism` | `block_targeted` | -0.01288 | [-0.02498, -0.00043] |
| `mechanism` | `joint_information` | -0.00869 | [-0.02088, 0.00251] |
| `mechanism` | `no_reference` | -0.03633 | [-0.04821, -0.02395] |
| `mechanism` | `reference_first_no_audit` | -0.01022 | [-0.01614, -0.00438] |
| `noise_scale` | `block_targeted` | -0.05732 | [-0.08168, -0.03445] |
| `noise_scale` | `joint_information` | -0.05005 | [-0.07058, -0.03059] |
| `noise_scale` | `no_reference` | -0.09045 | [-0.11065, -0.06924] |
| `noise_scale` | `reference_first_no_audit` | -0.02433 | [-0.03459, -0.01380] |
| `combined` | `block_targeted` | -0.05949 | [-0.09250, -0.02950] |
| `combined` | `joint_information` | -0.04535 | [-0.07246, -0.02025] |
| `combined` | `no_reference` | 0.13044 | [0.08223, 0.17885] |
| `combined` | `reference_first_no_audit` | -0.02091 | [-0.03880, -0.00498] |
| `nonlinear_sensor` | `block_targeted` | -0.01500 | [-0.04730, 0.01826] |
| `nonlinear_sensor` | `joint_information` | -0.02079 | [-0.05360, 0.01447] |
| `nonlinear_sensor` | `no_reference` | 0.13704 | [0.09019, 0.18578] |
| `nonlinear_sensor` | `reference_first_no_audit` | 0.00901 | [0.00385, 0.01414] |
| `heteroscedastic` | `block_targeted` | -0.02536 | [-0.05861, 0.00429] |
| `heteroscedastic` | `joint_information` | -0.02340 | [-0.05614, 0.00679] |
| `heteroscedastic` | `no_reference` | -0.07832 | [-0.11255, -0.04709] |
| `heteroscedastic` | `reference_first_no_audit` | -0.01821 | [-0.02957, -0.00460] |
| `heavy_tail` | `block_targeted` | -0.01058 | [-0.01921, -0.00163] |
| `heavy_tail` | `joint_information` | -0.01092 | [-0.01915, -0.00237] |
| `heavy_tail` | `no_reference` | -0.01902 | [-0.03163, -0.00628] |
| `heavy_tail` | `reference_first_no_audit` | -0.00804 | [-0.01497, -0.00152] |
| `local_bump` | `block_targeted` | -0.00138 | [-0.00890, 0.00700] |
| `local_bump` | `joint_information` | -0.00368 | [-0.00933, 0.00323] |
| `local_bump` | `no_reference` | -0.01228 | [-0.01944, -0.00582] |
| `local_bump` | `reference_first_no_audit` | -0.00310 | [-0.00606, 0.00016] |
| `reference_mismatch` | `block_targeted` | 0.00411 | [-0.01494, 0.02374] |
| `reference_mismatch` | `joint_information` | 0.00354 | [-0.01416, 0.02179] |
| `reference_mismatch` | `no_reference` | 0.00181 | [-0.01603, 0.02011] |
| `reference_mismatch` | `reference_first_no_audit` | -0.00336 | [-0.01074, 0.00420] |
## 6. Stop-at-first-alarm counterfactual: block-targeted

Prefixes were frozen during collection and scored only after final testing was opened. No policy received these metrics before acquisition ended. Summary JSON includes all five monitored policies. Acquisition cost excludes final test measurement overhead.

| Scenario | Would stop / 32 | Frozen-prefix RMSE | Full-budget RMSE | Prefix acquisition cost |
|---|---:|---:|---:|---:|
| `normal` | 1/32 | 0.0555 | 0.0546 | 110.69 |
| `gain_offset` | 32/32 | 0.0871 | 0.0731 | 63.91 |
| `mechanism` | 32/32 | 0.0809 | 0.0599 | 67.34 |
| `noise_scale` | 32/32 | 0.1609 | 0.0922 | 54.50 |
| `combined` | 32/32 | 0.1896 | 0.1063 | 51.02 |
| `nonlinear_sensor` | 32/32 | 0.1282 | 0.1252 | 73.07 |
| `heteroscedastic` | 32/32 | 0.1854 | 0.1250 | 51.02 |
| `heavy_tail` | 4/32 | 0.0464 | 0.0458 | 108.39 |
| `local_bump` | 0/32 | 0.1343 | 0.1343 | 113.11 |
| `reference_mismatch` | 1/32 | 0.2954 | 0.2943 | 111.80 |
## 7. Execution interruption and completeness

A per-call execution limit terminated the initial driver partway through an acquisition cell. Completed cells were retained; the incomplete gzip was archived under `execution_interruptions/`. An orchestration helper resumed missing cells using the **same locked source, thresholds and world IDs**, without outcome-driven cell selection or retuning. Start, resume and completion metadata and the incomplete file are retained. All 30 detector-summary cells and 60 acquisition cells are reported.

Any subsequent development informed by these outcomes turns this bank into development material for that later version. It cannot be retuned and reported as the same independent evaluation.
