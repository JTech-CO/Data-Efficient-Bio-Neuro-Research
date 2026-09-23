# 22. Results: additional measurements add information, not assumption-free truth

**v1.3.0-research.1. Completed evaluation: D 3,600 + E 10,560 + F 2,160 = 16,320 runs/trajectories. Zero biological observations.** F refits each of its 2,160 collection runs with three estimators (6,480 fits), with 1,200 unique acquired datasets. Reused measurements, policy comparisons, and testing rules are not independent samples.

[한국어](../ko/22_TRIAD_RESULTS.md) · [Design](18_TRIAD_DESIGN.md) · [All numbers](../../triad/results/v130/summary.json) · [Paired comparisons](../../triad/results/v130/paired_comparisons.json)

All numbers are executions of the bundled code, not copied paper performance. The final bank is `evaluation-v130-c`, seeds starting at 41000. An earlier partial evaluation aborted on a floating-point coordinate lineage mismatch; after the implementation fix, every evaluation was rerun on the new bank. Chapter 18 and QA preserve this history. This is exploratory synthetic research with a developer-known generator, not independent preregistration or external blinding.

## 1. D: addition, blanks, and orthogonal references remove different ambiguities

For six expanded physical parameters, external calibration alone has rank 4, addition alone rank 5, and a valid blank or orthogonal reference raises rank to 6. More repeated measurements do not automatically eliminate these ambiguities. Addition separates gain but not sample offset from the latent intercept. This is consistent with the documented limitation of standard addition for translational matrix effects. [T01](../../triad/references/REFERENCES.md#t01)

When both sample gain and offset shift, the assumption-based external-calibration baseline has RMSE 0.5968. Addition + blank gives 0.0602, the orthogonal reference 0.0298, and triangulation 0.0624, each with acquisition cost 48. In normal worlds the simple external-transfer assumption is correct, so its baseline RMSE is 0.0399 while addition + blank reaches 0.0788. Added information is not a universal performance advantage once cost and noise are considered. The assumed-transfer baseline is never promoted to a uniquely identified physical estimate.

Triangulation can flag inconsistent anchors without repairing its point estimate. Under blank mismatch, addition + blank flags model contradiction in 2/80 runs, versus 63/80 for triangulation. However, the current triangulation estimate still uses the addition/blank branch, yielding RMSE 0.2277 versus 0.2264; the orthogonal-reference estimate reaches 0.0298. When that orthogonal reference drifts instead, its RMSE rises to 0.3804, versus 0.0780 for addition + blank and 0.0840 for triangulation. No single anchor is adopted as an unconditional authority.

In the shared-anchor-bias counterexample, triangulation flags contradiction in only 5/80 runs and has RMSE 0.5995. Chapter 19 shows observational equivalence, not merely a weak detector. `identifiable-under-assumptions` does not certify those assumptions. Every `causal_source_identified` flag remains false. Practical commutability depends on specified measurement procedures and tolerances; the toy equality-rejection test is not a replacement for that assessment. [T02](../../triad/references/REFERENCES.md#t02)

## 2. E: broad coverage encounters local faults more often, but controls and noise still matter

With audit budget 48 and control cost 1 (24 pairs), Bonferroni any-alarm rates for narrow faults are 6/64 (9.4%) for three fixed sites, 37/64 (57.8%) for uniform random, 46/64 (71.9%) for stratification, 48/64 (75.0%) for largest-gap coverage, and 46/64 (71.9%) for adaptive coverage. Corresponding normal-world alarms are 10/256 (3.9%), 17/256 (6.6%), 10/256 (3.9%), 13/256 (5.1%), and 11/256 (4.3%). These point estimates do not establish a universal empirical rate at or below 5%; Wilson intervals accompany every rate in JSON.

The most complex adaptive policy is not a universal winner. Simple largest-gap exploration is a strong comparator. For weak faults it still alarms in only 13/64 (20.3%). Encountering a fault region and obtaining sufficiently strong evidence are different events.

Raising control cost from 1 to 3 leaves only 12 rather than 24 pairs under the same budget 48. Largest-gap narrow-fault alarms fall from 48/64 to 31/64. This comparison also uses setting-specific location random streams; it is not a literal prefix truncation of one path. Budget 24/control cost 1 is reported separately. Costs are declared synthetic measurement units, not currency, travel, or setup costs.

The central new assumption is a **valid matched sample–control contrast**. This is not the previous fitted GP residual with a new p-value attached. If locations depend only on the past and fresh null observations have equal means, independent Gaussian noise, and known variances, the conditional p-values are super-uniform. The rule `alpha_t=0.05/[t(t+1)]` spends at most 0.05, controlling cumulative false alarms under those conditions. It is not a general residual, conformal, or e-process implementation. Cost-aware location design and the need for explicit sequential-inference assumptions motivate the comparison. [T03](../../triad/references/REFERENCES.md#t03) [T08](../../triad/references/REFERENCES.md#t08)

With zero mean contrast but t3 or heteroscedastic noise, the Gaussian rule is misspecified. Largest-gap/48-budget Bonferroni alarms are 14/64 (21.9%) and 59/64 (92.2%), respectively. These worlds violate the full Gaussian null: they do not disprove its mathematical guarantee, but interpreting their alarms as mechanistic mean faults would be misleading. A common physical fault in both sample and control cancels in the contrast and remains invisible even with broad spatial coverage.

## 3. F: robustness, heteroscedasticity, and acquisition are not interchangeable gains

Three acquisition controllers, three policies, and three final estimators are fully crossed, with the same quadratic mean basis throughout. Random and space-filling acquisition produce the same measurements regardless of controller. The following same-dataset comparisons fix the homoscedastic controller and random policy over 40 worlds. Replication and input-dependent-noise literature motivates the design, but this small regression implementation is not a reproduction of a heteroscedastic GP paper. [T04](../../triad/references/REFERENCES.md#t04) [T05](../../triad/references/REFERENCES.md#t05)

| World | Final estimator | RMSE | NLL | CRPS | Observed coverage | Width |
|---|---|---:|---:|---:|---:|---:|
| Normal | Homoscedastic Gaussian | 0.0208 | -0.6626 | 0.0694 | 94.7% | 0.4925 |
| Normal | Student-t | 0.0245 | -0.6422 | 0.0698 | 96.8% | 0.5468 |
| Contamination | Homoscedastic Gaussian | 0.0499 | 0.1895 | 0.1158 | 94.9% | 0.9198 |
| Contamination | Student-t | 0.0263 | -0.3315 | 0.1052 | 94.0% | 0.6606 |
| Missing mean term | Homoscedastic Gaussian | 0.1659 | 0.4621 | 0.1284 | 70.1% | 0.4661 |
| Missing mean term | Student-t | 0.1689 | -0.0744 | 0.1217 | 96.5% | 0.9030 |

Under contamination the Student-t minus Gaussian RMSE difference is -0.02357, with descriptive world-bootstrap interval [-0.03301, -0.01527]. Under normal noise it is +0.00362 [0.00143, 0.00623], and under missing mean structure +0.00294 [0.00142, 0.00474]. In the latter case predictive coverage and scores improve while the mean remains wrong and interval width nearly doubles. Better probabilistic prediction is not mechanistic repair. The Student-t calculation is a documented IRLS/forecast approximation, not a general GP posterior. [T06](../../triad/references/REFERENCES.md#t06) [T07](../../triad/references/REFERENCES.md#t07)

For loglinear noise, the same random observations give logvariance-model RMSE 0.0359 versus 0.0391 for the constant-variance model. Fixing both controller and final estimator to logvariance and switching to IVR lowers RMSE to 0.0251, yet NLL worsens from random -0.4757 to -0.4143. The descriptive NLL-difference interval [-0.08809, 0.22236] includes zero. Improvement in one metric does not establish a better predictive distribution.

For missing mean structure, the fixed Gaussian estimator has RMSE 0.2058 under IVR versus 0.1659 under random acquisition. Reducing variance within a wrong mean model can worsen prediction. A loglinear variance function is itself misspecified for nonmonotone noise; Student-t does not learn arbitrary spatial variance patterns either.

## 4. Reproducibility and scope

The package retains 16,320 raw records, 890,880 serialized observations, and 219 representative runs. Observation counts include policy reuse, calibration, and testing, not independent biological samples. Event hashes and indices are distributed in a **losslessly reconstructible format**, with full-record and chain-tip verification on restore. No observations, assumptions, costs, fitted models, or outcomes are dropped. Numerical sources and thresholds remain those of the final pre-evaluation lock.

Every cell follows below rather than a favorable subset. Continuous-density NLL, CRPS, coverage, and sharpness measure different properties. The finite sets of 40, 64, 80, or 256 synthetic worlds and local generative rules limit generalization. None of these results establishes biological efficacy or absolute truth for real samples.

## All D results

| Scenario | Protocol | n | Rank | Latent RMSE ± SD | Latent coverage | Width | Contradicted | Transfer-null rejected |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| blank_mismatch | addition_blank | 80 | 6/6 | 0.2264 ± 0.0473 | 7.9% | 0.2419 | 2/80 | 80/80 |
| blank_mismatch | addition_only | 80 | 5/6 | — ± — | — | — | 0/80 | 78/80 |
| blank_mismatch | external_only | 80 | 4/6 | — ± — | — | — | 0/80 | — |
| blank_mismatch | orthogonal_only | 80 | 6/6 | 0.0298 ± 0.0156 | 95.3% | 0.1352 | 2/80 | 80/80 |
| blank_mismatch | triangulated | 80 | 6/6 | 0.2277 ± 0.0524 | 11.0% | 0.2549 | 63/80 | 80/80 |
| both_shift | addition_blank | 80 | 6/6 | 0.0602 ± 0.0408 | 94.0% | 0.2656 | 2/80 | 79/80 |
| both_shift | addition_only | 80 | 5/6 | — ± — | — | — | 0/80 | 78/80 |
| both_shift | external_only | 80 | 4/6 | — ± — | — | — | 0/80 | — |
| both_shift | orthogonal_only | 80 | 6/6 | 0.0298 ± 0.0159 | 96.7% | 0.1352 | 2/80 | 80/80 |
| both_shift | triangulated | 80 | 6/6 | 0.0624 ± 0.0463 | 93.8% | 0.2821 | 4/80 | 79/80 |
| common_anchor_failure | addition_blank | 80 | 6/6 | 0.5940 ± 0.1549 | 0.6% | 0.4627 | 4/80 | 1/80 |
| common_anchor_failure | addition_only | 80 | 5/6 | — ± — | — | — | 0/80 | 5/80 |
| common_anchor_failure | external_only | 80 | 4/6 | — ± — | — | — | 0/80 | — |
| common_anchor_failure | orthogonal_only | 80 | 6/6 | 0.5965 ± 0.1127 | 0.2% | 0.1352 | 6/80 | 8/80 |
| common_anchor_failure | triangulated | 80 | 6/6 | 0.5995 ± 0.1675 | 0.9% | 0.4946 | 5/80 | 2/80 |
| gain_shift | addition_blank | 80 | 6/6 | 0.0587 ± 0.0398 | 94.2% | 0.2649 | 2/80 | 77/80 |
| gain_shift | addition_only | 80 | 5/6 | — ± — | — | — | 0/80 | 80/80 |
| gain_shift | external_only | 80 | 4/6 | — ± — | — | — | 0/80 | — |
| gain_shift | orthogonal_only | 80 | 6/6 | 0.0313 ± 0.0162 | 95.4% | 0.1352 | 2/80 | 79/80 |
| gain_shift | triangulated | 80 | 6/6 | 0.0643 ± 0.0420 | 93.8% | 0.2819 | 6/80 | 76/80 |
| nonlinear_sensor | addition_blank | 80 | 6/6 | 0.1500 ± 0.0709 | 38.1% | 0.2351 | 46/80 | 80/80 |
| nonlinear_sensor | addition_only | 80 | 5/6 | — ± — | — | — | 0/80 | 80/80 |
| nonlinear_sensor | external_only | 80 | 4/6 | — ± — | — | — | 0/80 | — |
| nonlinear_sensor | orthogonal_only | 80 | 6/6 | 0.0305 ± 0.0162 | 95.3% | 0.1352 | 27/80 | 78/80 |
| nonlinear_sensor | triangulated | 80 | 6/6 | 0.1433 ± 0.0694 | 45.3% | 0.2508 | 50/80 | 79/80 |
| normal | addition_blank | 80 | 6/6 | 0.0788 ± 0.0538 | 94.9% | 0.3644 | 2/80 | 6/80 |
| normal | addition_only | 80 | 5/6 | — ± — | — | — | 0/80 | 4/80 |
| normal | external_only | 80 | 4/6 | — ± — | — | — | 0/80 | — |
| normal | orthogonal_only | 80 | 6/6 | 0.0339 ± 0.0158 | 94.2% | 0.1352 | 2/80 | 5/80 |
| normal | triangulated | 80 | 6/6 | 0.0843 ± 0.0599 | 95.3% | 0.3877 | 8/80 | 5/80 |
| offset_shift | addition_blank | 80 | 6/6 | 0.0696 ± 0.0463 | 97.0% | 0.3541 | 0/80 | 78/80 |
| offset_shift | addition_only | 80 | 5/6 | — ± — | — | — | 0/80 | 4/80 |
| offset_shift | external_only | 80 | 4/6 | — ± — | — | — | 0/80 | — |
| offset_shift | orthogonal_only | 80 | 6/6 | 0.0281 ± 0.0144 | 98.2% | 0.1352 | 1/80 | 80/80 |
| offset_shift | triangulated | 80 | 6/6 | 0.0739 ± 0.0465 | 96.1% | 0.3765 | 2/80 | 78/80 |
| reference_drift | addition_blank | 80 | 6/6 | 0.0780 ± 0.0531 | 97.7% | 0.3577 | 3/80 | 1/80 |
| reference_drift | addition_only | 80 | 5/6 | — ± — | — | — | 0/80 | 4/80 |
| reference_drift | external_only | 80 | 4/6 | — ± — | — | — | 0/80 | — |
| reference_drift | orthogonal_only | 80 | 6/6 | 0.3804 ± 0.0391 | 0.1% | 0.1352 | 2/80 | 80/80 |
| reference_drift | triangulated | 80 | 6/6 | 0.0840 ± 0.0609 | 97.5% | 0.3790 | 60/80 | 3/80 |
| spike_recovery | addition_blank | 80 | 6/6 | 0.5742 ± 0.1638 | 16.0% | 0.5334 | 1/80 | 79/80 |
| spike_recovery | addition_only | 80 | 5/6 | — ± — | — | — | 0/80 | 40/80 |
| spike_recovery | external_only | 80 | 4/6 | — ± — | — | — | 0/80 | — |
| spike_recovery | orthogonal_only | 80 | 6/6 | 0.0308 ± 0.0189 | 91.5% | 0.1352 | 1/80 | 80/80 |
| spike_recovery | triangulated | 80 | 6/6 | 0.5754 ± 0.1707 | 17.3% | 0.5670 | 76/80 | 78/80 |

External-only/addition-only do not uniquely identify the expanded physical system; their latent RMSE is not manufactured. Transfer-null rejection differs from model contradiction and tests gain only under addition-only. All full-rank errors are reported, including contradicted runs. Every cell costs 48 fitting + 33 testing = 81.

## All E results

| Scenario | Placement | Budget / control cost | n worlds / pairs | Naive alarm | Bonferroni alarm | Spending alarm | Region hit | Restricted cost (Bonferroni) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| boundary | adaptive_cover | 24/1 | 64/12 | 43/64 | 27/64 | 28/64 | 27/64 | 17.5938 |
| boundary | adaptive_cover | 48/1 | 64/24 | 59/64 | 41/64 | 40/64 | 41/64 | 28.5312 |
| boundary | adaptive_cover | 48/3 | 64/12 | 50/64 | 33/64 | 33/64 | 33/64 | 34.4375 |
| boundary | fixed_three | 24/1 | 64/12 | 45/64 | 25/64 | 22/64 | 10/64 | 17.9062 |
| boundary | fixed_three | 48/1 | 64/24 | 55/64 | 23/64 | 22/64 | 10/64 | 35.6562 |
| boundary | fixed_three | 48/3 | 64/12 | 45/64 | 25/64 | 22/64 | 10/64 | 35.8125 |
| boundary | max_gap | 24/1 | 64/12 | 47/64 | 24/64 | 23/64 | 21/64 | 19.8750 |
| boundary | max_gap | 48/1 | 64/24 | 61/64 | 45/64 | 39/64 | 45/64 | 32.3125 |
| boundary | max_gap | 48/3 | 64/12 | 45/64 | 22/64 | 21/64 | 18/64 | 39.6875 |
| boundary | stratified | 24/1 | 64/12 | 51/64 | 29/64 | 27/64 | 28/64 | 18.6875 |
| boundary | stratified | 48/1 | 64/24 | 61/64 | 46/64 | 37/64 | 52/64 | 28.7500 |
| boundary | stratified | 48/3 | 64/12 | 49/64 | 35/64 | 31/64 | 31/64 | 33.4375 |
| boundary | uniform | 24/1 | 64/12 | 52/64 | 32/64 | 26/64 | 26/64 | 18.0625 |
| boundary | uniform | 48/1 | 64/24 | 58/64 | 39/64 | 36/64 | 43/64 | 29.9375 |
| boundary | uniform | 48/3 | 64/12 | 50/64 | 27/64 | 28/64 | 26/64 | 38.0000 |
| broad | adaptive_cover | 24/1 | 64/12 | 63/64 | 56/64 | 56/64 | 54/64 | 11.3750 |
| broad | adaptive_cover | 48/1 | 64/24 | 64/64 | 61/64 | 62/64 | 64/64 | 13.8750 |
| broad | adaptive_cover | 48/3 | 64/12 | 63/64 | 58/64 | 58/64 | 57/64 | 23.0625 |
| broad | fixed_three | 24/1 | 64/12 | 42/64 | 23/64 | 20/64 | 13/64 | 18.4375 |
| broad | fixed_three | 48/1 | 64/24 | 55/64 | 25/64 | 22/64 | 13/64 | 33.4688 |
| broad | fixed_three | 48/3 | 64/12 | 42/64 | 23/64 | 20/64 | 13/64 | 36.8750 |
| broad | max_gap | 24/1 | 64/12 | 64/64 | 61/64 | 59/64 | 64/64 | 10.8438 |
| broad | max_gap | 48/1 | 64/24 | 64/64 | 63/64 | 61/64 | 64/64 | 12.4688 |
| broad | max_gap | 48/3 | 64/12 | 64/64 | 60/64 | 60/64 | 64/64 | 21.6250 |
| broad | stratified | 24/1 | 64/12 | 64/64 | 61/64 | 58/64 | 64/64 | 10.8125 |
| broad | stratified | 48/1 | 64/24 | 64/64 | 64/64 | 63/64 | 64/64 | 12.0312 |
| broad | stratified | 48/3 | 64/12 | 64/64 | 63/64 | 61/64 | 64/64 | 19.3125 |
| broad | uniform | 24/1 | 64/12 | 58/64 | 54/64 | 52/64 | 53/64 | 11.4062 |
| broad | uniform | 48/1 | 64/24 | 64/64 | 60/64 | 60/64 | 61/64 | 16.9688 |
| broad | uniform | 48/3 | 64/12 | 61/64 | 52/64 | 50/64 | 59/64 | 24.5625 |
| common_mode | adaptive_cover | 24/1 | 64/12 | 30/64 | 3/64 | 3/64 | — | 23.3438 |
| common_mode | adaptive_cover | 48/1 | 64/24 | 48/64 | 5/64 | 3/64 | — | 46.2188 |
| common_mode | adaptive_cover | 48/3 | 64/12 | 34/64 | 4/64 | 3/64 | — | 46.5000 |
| common_mode | fixed_three | 24/1 | 64/12 | 37/64 | 2/64 | 1/64 | — | 23.5312 |
| common_mode | fixed_three | 48/1 | 64/24 | 55/64 | 4/64 | 1/64 | — | 47.1562 |
| common_mode | fixed_three | 48/3 | 64/12 | 37/64 | 2/64 | 1/64 | — | 47.0625 |
| common_mode | max_gap | 24/1 | 64/12 | 34/64 | 3/64 | 3/64 | — | 23.3125 |
| common_mode | max_gap | 48/1 | 64/24 | 45/64 | 2/64 | 3/64 | — | 46.6875 |
| common_mode | max_gap | 48/3 | 64/12 | 30/64 | 3/64 | 3/64 | — | 46.7500 |
| common_mode | stratified | 24/1 | 64/12 | 21/64 | 1/64 | 2/64 | — | 23.9688 |
| common_mode | stratified | 48/1 | 64/24 | 45/64 | 4/64 | 2/64 | — | 46.8438 |
| common_mode | stratified | 48/3 | 64/12 | 29/64 | 4/64 | 3/64 | — | 46.3125 |
| common_mode | uniform | 24/1 | 64/12 | 37/64 | 3/64 | 2/64 | — | 23.3750 |
| common_mode | uniform | 48/1 | 64/24 | 50/64 | 4/64 | 2/64 | — | 46.4375 |
| common_mode | uniform | 48/3 | 64/12 | 31/64 | 0/64 | 2/64 | — | 48.0000 |
| hetero_null | adaptive_cover | 24/1 | 64/12 | 63/64 | 49/64 | 48/64 | — | 13.3750 |
| hetero_null | adaptive_cover | 48/1 | 64/24 | 64/64 | 60/64 | 56/64 | — | 17.0938 |
| hetero_null | adaptive_cover | 48/3 | 64/12 | 62/64 | 50/64 | 50/64 | — | 26.2500 |
| hetero_null | fixed_three | 24/1 | 64/12 | 59/64 | 49/64 | 41/64 | — | 15.2812 |
| hetero_null | fixed_three | 48/1 | 64/24 | 63/64 | 58/64 | 52/64 | — | 21.3750 |
| hetero_null | fixed_three | 48/3 | 64/12 | 59/64 | 49/64 | 41/64 | — | 30.5625 |
| hetero_null | max_gap | 24/1 | 64/12 | 61/64 | 49/64 | 46/64 | — | 13.3438 |
| hetero_null | max_gap | 48/1 | 64/24 | 64/64 | 59/64 | 56/64 | — | 18.0938 |
| hetero_null | max_gap | 48/3 | 64/12 | 62/64 | 50/64 | 46/64 | — | 26.6875 |
| hetero_null | stratified | 24/1 | 64/12 | 63/64 | 50/64 | 46/64 | — | 12.5312 |
| hetero_null | stratified | 48/1 | 64/24 | 64/64 | 60/64 | 50/64 | — | 20.3125 |
| hetero_null | stratified | 48/3 | 64/12 | 62/64 | 50/64 | 44/64 | — | 25.8750 |
| hetero_null | uniform | 24/1 | 64/12 | 64/64 | 52/64 | 42/64 | — | 13.0000 |
| hetero_null | uniform | 48/1 | 64/24 | 64/64 | 58/64 | 52/64 | — | 19.8750 |
| hetero_null | uniform | 48/3 | 64/12 | 62/64 | 43/64 | 41/64 | — | 30.1250 |
| narrow | adaptive_cover | 24/1 | 64/12 | 47/64 | 25/64 | 25/64 | 27/64 | 19.2500 |
| narrow | adaptive_cover | 48/1 | 64/24 | 61/64 | 46/64 | 45/64 | 46/64 | 28.5000 |
| narrow | adaptive_cover | 48/3 | 64/12 | 50/64 | 27/64 | 26/64 | 30/64 | 38.7500 |
| narrow | fixed_three | 24/1 | 64/12 | 40/64 | 5/64 | 8/64 | 3/64 | 22.8125 |
| narrow | fixed_three | 48/1 | 64/24 | 51/64 | 6/64 | 8/64 | 3/64 | 45.2812 |
| narrow | fixed_three | 48/3 | 64/12 | 40/64 | 5/64 | 8/64 | 3/64 | 45.6250 |
| narrow | max_gap | 24/1 | 64/12 | 53/64 | 27/64 | 27/64 | 33/64 | 19.5000 |
| narrow | max_gap | 48/1 | 64/24 | 62/64 | 48/64 | 41/64 | 54/64 | 29.1250 |
| narrow | max_gap | 48/3 | 64/12 | 52/64 | 31/64 | 28/64 | 36/64 | 38.8750 |
| narrow | stratified | 24/1 | 64/12 | 50/64 | 34/64 | 26/64 | 30/64 | 17.5000 |
| narrow | stratified | 48/1 | 64/24 | 59/64 | 46/64 | 39/64 | 51/64 | 28.9062 |
| narrow | stratified | 48/3 | 64/12 | 49/64 | 35/64 | 27/64 | 35/64 | 35.6250 |
| narrow | uniform | 24/1 | 64/12 | 44/64 | 25/64 | 23/64 | 23/64 | 19.2188 |
| narrow | uniform | 48/1 | 64/24 | 60/64 | 37/64 | 37/64 | 46/64 | 32.4375 |
| narrow | uniform | 48/3 | 64/12 | 46/64 | 22/64 | 22/64 | 24/64 | 38.8750 |
| normal | adaptive_cover | 24/1 | 256/12 | 110/256 | 10/256 | 10/256 | — | 23.6172 |
| normal | adaptive_cover | 48/1 | 256/24 | 183/256 | 11/256 | 9/256 | — | 46.7109 |
| normal | adaptive_cover | 48/3 | 256/12 | 109/256 | 12/256 | 11/256 | — | 47.2344 |
| normal | fixed_three | 24/1 | 256/12 | 117/256 | 8/256 | 6/256 | — | 23.6016 |
| normal | fixed_three | 48/1 | 256/24 | 171/256 | 10/256 | 8/256 | — | 46.9922 |
| normal | fixed_three | 48/3 | 256/12 | 117/256 | 8/256 | 6/256 | — | 47.2031 |
| normal | max_gap | 24/1 | 256/12 | 116/256 | 14/256 | 10/256 | — | 23.4375 |
| normal | max_gap | 48/1 | 256/24 | 174/256 | 13/256 | 10/256 | — | 46.4219 |
| normal | max_gap | 48/3 | 256/12 | 109/256 | 13/256 | 11/256 | — | 46.9375 |
| normal | stratified | 24/1 | 256/12 | 120/256 | 9/256 | 14/256 | — | 23.3594 |
| normal | stratified | 48/1 | 256/24 | 179/256 | 10/256 | 10/256 | — | 47.1719 |
| normal | stratified | 48/3 | 256/12 | 120/256 | 14/256 | 16/256 | — | 46.5312 |
| normal | uniform | 24/1 | 256/12 | 130/256 | 13/256 | 16/256 | — | 23.4922 |
| normal | uniform | 48/1 | 256/24 | 184/256 | 17/256 | 14/256 | — | 46.7812 |
| normal | uniform | 48/3 | 256/12 | 125/256 | 14/256 | 12/256 | — | 47.0156 |
| t3_null | adaptive_cover | 24/1 | 64/12 | 25/64 | 6/64 | 7/64 | — | 22.8750 |
| t3_null | adaptive_cover | 48/1 | 64/24 | 37/64 | 9/64 | 9/64 | — | 43.8438 |
| t3_null | adaptive_cover | 48/3 | 64/12 | 26/64 | 8/64 | 8/64 | — | 45.4375 |
| t3_null | fixed_three | 24/1 | 64/12 | 33/64 | 12/64 | 9/64 | — | 22.5312 |
| t3_null | fixed_three | 48/1 | 64/24 | 48/64 | 17/64 | 13/64 | — | 41.7188 |
| t3_null | fixed_three | 48/3 | 64/12 | 33/64 | 12/64 | 9/64 | — | 45.0625 |
| t3_null | max_gap | 24/1 | 64/12 | 25/64 | 8/64 | 10/64 | — | 22.8438 |
| t3_null | max_gap | 48/1 | 64/24 | 42/64 | 14/64 | 13/64 | — | 42.8750 |
| t3_null | max_gap | 48/3 | 64/12 | 23/64 | 8/64 | 10/64 | — | 45.4375 |
| t3_null | stratified | 24/1 | 64/12 | 31/64 | 10/64 | 6/64 | — | 22.6875 |
| t3_null | stratified | 48/1 | 64/24 | 45/64 | 13/64 | 8/64 | — | 43.5625 |
| t3_null | stratified | 48/3 | 64/12 | 18/64 | 8/64 | 5/64 | — | 45.6875 |
| t3_null | uniform | 24/1 | 64/12 | 32/64 | 10/64 | 9/64 | — | 22.3750 |
| t3_null | uniform | 48/1 | 64/24 | 43/64 | 20/64 | 15/64 | — | 39.0625 |
| t3_null | uniform | 48/3 | 64/12 | 28/64 | 9/64 | 11/64 | — | 44.1875 |
| weak | adaptive_cover | 24/1 | 64/12 | 40/64 | 12/64 | 7/64 | 34/64 | 22.1250 |
| weak | adaptive_cover | 48/1 | 64/24 | 53/64 | 13/64 | 8/64 | 50/64 | 43.3438 |
| weak | adaptive_cover | 48/3 | 64/12 | 41/64 | 13/64 | 6/64 | 37/64 | 44.8750 |
| weak | fixed_three | 24/1 | 64/12 | 29/64 | 3/64 | 5/64 | 5/64 | 23.4062 |
| weak | fixed_three | 48/1 | 64/24 | 52/64 | 6/64 | 6/64 | 5/64 | 45.9375 |
| weak | fixed_three | 48/3 | 64/12 | 29/64 | 3/64 | 5/64 | 5/64 | 46.8125 |
| weak | max_gap | 24/1 | 64/12 | 40/64 | 10/64 | 5/64 | 39/64 | 22.1562 |
| weak | max_gap | 48/1 | 64/24 | 53/64 | 13/64 | 9/64 | 61/64 | 43.2812 |
| weak | max_gap | 48/3 | 64/12 | 43/64 | 13/64 | 9/64 | 44/64 | 44.1875 |
| weak | stratified | 24/1 | 64/12 | 42/64 | 5/64 | 4/64 | 38/64 | 23.0312 |
| weak | stratified | 48/1 | 64/24 | 52/64 | 9/64 | 9/64 | 57/64 | 45.3125 |
| weak | stratified | 48/3 | 64/12 | 37/64 | 9/64 | 7/64 | 43/64 | 45.9375 |
| weak | uniform | 24/1 | 64/12 | 29/64 | 10/64 | 6/64 | 30/64 | 21.4375 |
| weak | uniform | 48/1 | 64/24 | 51/64 | 9/64 | 6/64 | 49/64 | 44.0938 |
| weak | uniform | 48/3 | 64/12 | 38/64 | 8/64 | 8/64 | 31/64 | 45.0000 |

Any-alarm does not establish a correct location or cause. Region hit means at least one sample within one fault width of the center; it is not applicable in no-contrast/common-mode worlds. Restricted detection cost counts a miss at the exhausted budget rather than dropping missed runs. Coverage of every possible fault is not guaranteed.

## All F crossed results

| Scenario | Controller | Acquisition | Final estimator | n | Latent RMSE ± SD | NLL | CRPS | Observed coverage | Width | Converged |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| contamination | hom_gaussian | ivr | hom_gaussian | 40 | 0.0412 ± 0.0183 | 0.2205 | 0.1134 | 94.6% | 0.8687 | 100.0% |
| contamination | hom_gaussian | ivr | logvar_gaussian | 40 | 0.0410 ± 0.0184 | 0.7997 | 0.1092 | 91.1% | 0.6124 | 100.0% |
| contamination | hom_gaussian | ivr | student_t | 40 | 0.0247 ± 0.0116 | -0.3252 | 0.1056 | 93.3% | 0.6219 | 100.0% |
| contamination | hom_gaussian | random | hom_gaussian | 40 | 0.0499 ± 0.0318 | 0.1895 | 0.1158 | 94.9% | 0.9198 | 100.0% |
| contamination | hom_gaussian | random | logvar_gaussian | 40 | 0.0498 ± 0.0350 | 1.3791 | 0.1125 | 90.9% | 0.6587 | 100.0% |
| contamination | hom_gaussian | random | student_t | 40 | 0.0263 ± 0.0109 | -0.3315 | 0.1052 | 94.0% | 0.6606 | 100.0% |
| contamination | hom_gaussian | spacefill | hom_gaussian | 40 | 0.0521 ± 0.0324 | 0.0949 | 0.1185 | 95.9% | 0.9997 | 100.0% |
| contamination | hom_gaussian | spacefill | logvar_gaussian | 40 | 0.0515 ± 0.0312 | 0.4294 | 0.1121 | 92.1% | 0.6777 | 100.0% |
| contamination | hom_gaussian | spacefill | student_t | 40 | 0.0257 ± 0.0104 | -0.3314 | 0.1054 | 93.7% | 0.6642 | 100.0% |
| contamination | logvar_gaussian | ivr | hom_gaussian | 40 | 0.0388 ± 0.0197 | 0.1099 | 0.1143 | 95.7% | 0.9206 | 100.0% |
| contamination | logvar_gaussian | ivr | logvar_gaussian | 40 | 0.0391 ± 0.0197 | 1.8612 | 0.1099 | 89.1% | 0.5889 | 100.0% |
| contamination | logvar_gaussian | ivr | student_t | 40 | 0.0208 ± 0.0089 | -0.3301 | 0.1052 | 93.5% | 0.6265 | 100.0% |
| contamination | logvar_gaussian | random | hom_gaussian | 40 | 0.0499 ± 0.0318 | 0.1895 | 0.1158 | 94.9% | 0.9198 | 100.0% |
| contamination | logvar_gaussian | random | logvar_gaussian | 40 | 0.0498 ± 0.0350 | 1.3791 | 0.1125 | 90.9% | 0.6587 | 100.0% |
| contamination | logvar_gaussian | random | student_t | 40 | 0.0263 ± 0.0109 | -0.3315 | 0.1052 | 94.0% | 0.6606 | 100.0% |
| contamination | logvar_gaussian | spacefill | hom_gaussian | 40 | 0.0521 ± 0.0324 | 0.0949 | 0.1185 | 95.9% | 0.9997 | 100.0% |
| contamination | logvar_gaussian | spacefill | logvar_gaussian | 40 | 0.0515 ± 0.0312 | 0.4294 | 0.1121 | 92.1% | 0.6777 | 100.0% |
| contamination | logvar_gaussian | spacefill | student_t | 40 | 0.0257 ± 0.0104 | -0.3314 | 0.1054 | 93.7% | 0.6642 | 100.0% |
| contamination | student_t | ivr | hom_gaussian | 40 | 0.0447 ± 0.0250 | 0.2002 | 0.1146 | 94.8% | 0.8974 | 100.0% |
| contamination | student_t | ivr | logvar_gaussian | 40 | 0.0444 ± 0.0248 | 0.8500 | 0.1104 | 90.5% | 0.6139 | 100.0% |
| contamination | student_t | ivr | student_t | 40 | 0.0233 ± 0.0098 | -0.3325 | 0.1052 | 93.5% | 0.6310 | 100.0% |
| contamination | student_t | random | hom_gaussian | 40 | 0.0499 ± 0.0318 | 0.1895 | 0.1158 | 94.9% | 0.9198 | 100.0% |
| contamination | student_t | random | logvar_gaussian | 40 | 0.0498 ± 0.0350 | 1.3791 | 0.1125 | 90.9% | 0.6587 | 100.0% |
| contamination | student_t | random | student_t | 40 | 0.0263 ± 0.0109 | -0.3315 | 0.1052 | 94.0% | 0.6606 | 100.0% |
| contamination | student_t | spacefill | hom_gaussian | 40 | 0.0521 ± 0.0324 | 0.0949 | 0.1185 | 95.9% | 0.9997 | 100.0% |
| contamination | student_t | spacefill | logvar_gaussian | 40 | 0.0515 ± 0.0312 | 0.4294 | 0.1121 | 92.1% | 0.6777 | 100.0% |
| contamination | student_t | spacefill | student_t | 40 | 0.0257 ± 0.0104 | -0.3314 | 0.1054 | 93.7% | 0.6642 | 100.0% |
| gaussian | hom_gaussian | ivr | hom_gaussian | 40 | 0.0195 ± 0.0077 | -0.6517 | 0.0692 | 93.8% | 0.4697 | 100.0% |
| gaussian | hom_gaussian | ivr | logvar_gaussian | 40 | 0.0198 ± 0.0075 | -0.5855 | 0.0700 | 92.5% | 0.4887 | 100.0% |
| gaussian | hom_gaussian | ivr | student_t | 40 | 0.0218 ± 0.0078 | -0.6452 | 0.0693 | 96.6% | 0.5431 | 100.0% |
| gaussian | hom_gaussian | random | hom_gaussian | 40 | 0.0208 ± 0.0102 | -0.6626 | 0.0694 | 94.7% | 0.4925 | 100.0% |
| gaussian | hom_gaussian | random | logvar_gaussian | 40 | 0.0221 ± 0.0118 | -0.6128 | 0.0706 | 94.1% | 0.5179 | 100.0% |
| gaussian | hom_gaussian | random | student_t | 40 | 0.0245 ± 0.0121 | -0.6422 | 0.0698 | 96.8% | 0.5468 | 100.0% |
| gaussian | hom_gaussian | spacefill | hom_gaussian | 40 | 0.0252 ± 0.0099 | -0.6468 | 0.0699 | 93.9% | 0.4899 | 100.0% |
| gaussian | hom_gaussian | spacefill | logvar_gaussian | 40 | 0.0263 ± 0.0098 | -0.5606 | 0.0711 | 93.2% | 0.5211 | 100.0% |
| gaussian | hom_gaussian | spacefill | student_t | 40 | 0.0275 ± 0.0102 | -0.6362 | 0.0701 | 96.5% | 0.5495 | 100.0% |
| gaussian | logvar_gaussian | ivr | hom_gaussian | 40 | 0.0219 ± 0.0099 | -0.6582 | 0.0694 | 93.9% | 0.4727 | 100.0% |
| gaussian | logvar_gaussian | ivr | logvar_gaussian | 40 | 0.0222 ± 0.0098 | -0.5936 | 0.0702 | 92.4% | 0.4758 | 100.0% |
| gaussian | logvar_gaussian | ivr | student_t | 40 | 0.0243 ± 0.0118 | -0.6390 | 0.0697 | 96.4% | 0.5420 | 100.0% |
| gaussian | logvar_gaussian | random | hom_gaussian | 40 | 0.0208 ± 0.0102 | -0.6626 | 0.0694 | 94.7% | 0.4925 | 100.0% |
| gaussian | logvar_gaussian | random | logvar_gaussian | 40 | 0.0221 ± 0.0118 | -0.6128 | 0.0706 | 94.1% | 0.5179 | 100.0% |
| gaussian | logvar_gaussian | random | student_t | 40 | 0.0245 ± 0.0121 | -0.6422 | 0.0698 | 96.8% | 0.5468 | 100.0% |
| gaussian | logvar_gaussian | spacefill | hom_gaussian | 40 | 0.0252 ± 0.0099 | -0.6468 | 0.0699 | 93.9% | 0.4899 | 100.0% |
| gaussian | logvar_gaussian | spacefill | logvar_gaussian | 40 | 0.0263 ± 0.0098 | -0.5606 | 0.0711 | 93.2% | 0.5211 | 100.0% |
| gaussian | logvar_gaussian | spacefill | student_t | 40 | 0.0275 ± 0.0102 | -0.6362 | 0.0701 | 96.5% | 0.5495 | 100.0% |
| gaussian | student_t | ivr | hom_gaussian | 40 | 0.0192 ± 0.0076 | -0.6531 | 0.0691 | 93.5% | 0.4661 | 100.0% |
| gaussian | student_t | ivr | logvar_gaussian | 40 | 0.0195 ± 0.0073 | -0.5819 | 0.0700 | 92.5% | 0.4821 | 100.0% |
| gaussian | student_t | ivr | student_t | 40 | 0.0206 ± 0.0085 | -0.6482 | 0.0691 | 96.6% | 0.5437 | 100.0% |
| gaussian | student_t | random | hom_gaussian | 40 | 0.0208 ± 0.0102 | -0.6626 | 0.0694 | 94.7% | 0.4925 | 100.0% |
| gaussian | student_t | random | logvar_gaussian | 40 | 0.0221 ± 0.0118 | -0.6128 | 0.0706 | 94.1% | 0.5179 | 100.0% |
| gaussian | student_t | random | student_t | 40 | 0.0245 ± 0.0121 | -0.6422 | 0.0698 | 96.8% | 0.5468 | 100.0% |
| gaussian | student_t | spacefill | hom_gaussian | 40 | 0.0252 ± 0.0099 | -0.6468 | 0.0699 | 93.9% | 0.4899 | 100.0% |
| gaussian | student_t | spacefill | logvar_gaussian | 40 | 0.0263 ± 0.0098 | -0.5606 | 0.0711 | 93.2% | 0.5211 | 100.0% |
| gaussian | student_t | spacefill | student_t | 40 | 0.0275 ± 0.0102 | -0.6362 | 0.0701 | 96.5% | 0.5495 | 100.0% |
| loglinear_noise | hom_gaussian | ivr | hom_gaussian | 40 | 0.0334 ± 0.0177 | -0.3413 | 0.0888 | 93.3% | 0.6803 | 100.0% |
| loglinear_noise | hom_gaussian | ivr | logvar_gaussian | 40 | 0.0329 ± 0.0162 | -0.5338 | 0.0828 | 92.4% | 0.5689 | 100.0% |
| loglinear_noise | hom_gaussian | ivr | student_t | 40 | 0.0430 ± 0.0252 | -0.4375 | 0.0876 | 92.3% | 0.6243 | 92.5% |
| loglinear_noise | hom_gaussian | random | hom_gaussian | 40 | 0.0391 ± 0.0244 | -0.3457 | 0.0882 | 92.0% | 0.6163 | 100.0% |
| loglinear_noise | hom_gaussian | random | logvar_gaussian | 40 | 0.0359 ± 0.0205 | -0.4757 | 0.0832 | 90.3% | 0.5440 | 100.0% |
| loglinear_noise | hom_gaussian | random | student_t | 40 | 0.0384 ± 0.0223 | -0.4534 | 0.0867 | 91.7% | 0.5873 | 97.5% |
| loglinear_noise | hom_gaussian | spacefill | hom_gaussian | 40 | 0.0408 ± 0.0261 | -0.3219 | 0.0880 | 91.6% | 0.5892 | 100.0% |
| loglinear_noise | hom_gaussian | spacefill | logvar_gaussian | 40 | 0.0400 ± 0.0256 | -0.4608 | 0.0837 | 89.8% | 0.5412 | 100.0% |
| loglinear_noise | hom_gaussian | spacefill | student_t | 40 | 0.0434 ± 0.0266 | -0.4494 | 0.0869 | 91.4% | 0.5770 | 100.0% |
| loglinear_noise | logvar_gaussian | ivr | hom_gaussian | 40 | 0.0308 ± 0.0176 | -0.2854 | 0.0926 | 95.3% | 0.8441 | 100.0% |
| loglinear_noise | logvar_gaussian | ivr | logvar_gaussian | 40 | 0.0251 ± 0.0106 | -0.4143 | 0.0826 | 89.9% | 0.5608 | 100.0% |
| loglinear_noise | logvar_gaussian | ivr | student_t | 40 | 0.0309 ± 0.0152 | -0.3975 | 0.0886 | 96.6% | 0.8647 | 100.0% |
| loglinear_noise | logvar_gaussian | random | hom_gaussian | 40 | 0.0391 ± 0.0244 | -0.3457 | 0.0882 | 92.0% | 0.6163 | 100.0% |
| loglinear_noise | logvar_gaussian | random | logvar_gaussian | 40 | 0.0359 ± 0.0205 | -0.4757 | 0.0832 | 90.3% | 0.5440 | 100.0% |
| loglinear_noise | logvar_gaussian | random | student_t | 40 | 0.0384 ± 0.0223 | -0.4534 | 0.0867 | 91.7% | 0.5873 | 97.5% |
| loglinear_noise | logvar_gaussian | spacefill | hom_gaussian | 40 | 0.0408 ± 0.0261 | -0.3219 | 0.0880 | 91.6% | 0.5892 | 100.0% |
| loglinear_noise | logvar_gaussian | spacefill | logvar_gaussian | 40 | 0.0400 ± 0.0256 | -0.4608 | 0.0837 | 89.8% | 0.5412 | 100.0% |
| loglinear_noise | logvar_gaussian | spacefill | student_t | 40 | 0.0434 ± 0.0266 | -0.4494 | 0.0869 | 91.4% | 0.5770 | 100.0% |
| loglinear_noise | student_t | ivr | hom_gaussian | 40 | 0.0302 ± 0.0171 | -0.3420 | 0.0895 | 94.6% | 0.7393 | 100.0% |
| loglinear_noise | student_t | ivr | logvar_gaussian | 40 | 0.0298 ± 0.0162 | -0.4749 | 0.0829 | 90.0% | 0.5533 | 100.0% |
| loglinear_noise | student_t | ivr | student_t | 40 | 0.0364 ± 0.0177 | -0.4384 | 0.0869 | 94.0% | 0.7015 | 100.0% |
| loglinear_noise | student_t | random | hom_gaussian | 40 | 0.0391 ± 0.0244 | -0.3457 | 0.0882 | 92.0% | 0.6163 | 100.0% |
| loglinear_noise | student_t | random | logvar_gaussian | 40 | 0.0359 ± 0.0205 | -0.4757 | 0.0832 | 90.3% | 0.5440 | 100.0% |
| loglinear_noise | student_t | random | student_t | 40 | 0.0384 ± 0.0223 | -0.4534 | 0.0867 | 91.7% | 0.5873 | 97.5% |
| loglinear_noise | student_t | spacefill | hom_gaussian | 40 | 0.0408 ± 0.0261 | -0.3219 | 0.0880 | 91.6% | 0.5892 | 100.0% |
| loglinear_noise | student_t | spacefill | logvar_gaussian | 40 | 0.0400 ± 0.0256 | -0.4608 | 0.0837 | 89.8% | 0.5412 | 100.0% |
| loglinear_noise | student_t | spacefill | student_t | 40 | 0.0434 ± 0.0266 | -0.4494 | 0.0869 | 91.4% | 0.5770 | 100.0% |
| missing_mean | hom_gaussian | ivr | hom_gaussian | 40 | 0.2058 ± 0.0115 | 1.0484 | 0.1535 | 62.9% | 0.4717 | 100.0% |
| missing_mean | hom_gaussian | ivr | logvar_gaussian | 40 | 0.2056 ± 0.0115 | 1.2968 | 0.1541 | 61.7% | 0.4653 | 100.0% |
| missing_mean | hom_gaussian | ivr | student_t | 40 | 0.2108 ± 0.0127 | 0.3728 | 0.1526 | 76.8% | 0.6257 | 100.0% |
| missing_mean | hom_gaussian | random | hom_gaussian | 40 | 0.1659 ± 0.0063 | 0.4621 | 0.1284 | 70.1% | 0.4661 | 100.0% |
| missing_mean | hom_gaussian | random | logvar_gaussian | 40 | 0.1660 ± 0.0074 | 0.5242 | 0.1283 | 70.6% | 0.4915 | 100.0% |
| missing_mean | hom_gaussian | random | student_t | 40 | 0.1689 ± 0.0103 | -0.0744 | 0.1217 | 96.5% | 0.9030 | 100.0% |
| missing_mean | hom_gaussian | spacefill | hom_gaussian | 40 | 0.1631 ± 0.0031 | 0.4097 | 0.1267 | 71.0% | 0.4640 | 100.0% |
| missing_mean | hom_gaussian | spacefill | logvar_gaussian | 40 | 0.1630 ± 0.0033 | 0.6696 | 0.1276 | 69.5% | 0.4658 | 100.0% |
| missing_mean | hom_gaussian | spacefill | student_t | 40 | 0.1647 ± 0.0043 | -0.0961 | 0.1195 | 97.9% | 0.9371 | 100.0% |
| missing_mean | logvar_gaussian | ivr | hom_gaussian | 40 | 0.2007 ± 0.0217 | 0.8569 | 0.1493 | 64.9% | 0.4791 | 100.0% |
| missing_mean | logvar_gaussian | ivr | logvar_gaussian | 40 | 0.2006 ± 0.0218 | 1.1853 | 0.1502 | 63.7% | 0.4721 | 100.0% |
| missing_mean | logvar_gaussian | ivr | student_t | 40 | 0.2072 ± 0.0250 | 0.2964 | 0.1486 | 80.3% | 0.6592 | 100.0% |
| missing_mean | logvar_gaussian | random | hom_gaussian | 40 | 0.1659 ± 0.0063 | 0.4621 | 0.1284 | 70.1% | 0.4661 | 100.0% |
| missing_mean | logvar_gaussian | random | logvar_gaussian | 40 | 0.1660 ± 0.0074 | 0.5242 | 0.1283 | 70.6% | 0.4915 | 100.0% |
| missing_mean | logvar_gaussian | random | student_t | 40 | 0.1689 ± 0.0103 | -0.0744 | 0.1217 | 96.5% | 0.9030 | 100.0% |
| missing_mean | logvar_gaussian | spacefill | hom_gaussian | 40 | 0.1631 ± 0.0031 | 0.4097 | 0.1267 | 71.0% | 0.4640 | 100.0% |
| missing_mean | logvar_gaussian | spacefill | logvar_gaussian | 40 | 0.1630 ± 0.0033 | 0.6696 | 0.1276 | 69.5% | 0.4658 | 100.0% |
| missing_mean | logvar_gaussian | spacefill | student_t | 40 | 0.1647 ± 0.0043 | -0.0961 | 0.1195 | 97.9% | 0.9371 | 100.0% |
| missing_mean | student_t | ivr | hom_gaussian | 40 | 0.2073 ± 0.0126 | 1.0215 | 0.1542 | 63.5% | 0.4764 | 100.0% |
| missing_mean | student_t | ivr | logvar_gaussian | 40 | 0.2072 ± 0.0126 | 1.2634 | 0.1547 | 62.5% | 0.4741 | 100.0% |
| missing_mean | student_t | ivr | student_t | 40 | 0.2119 ± 0.0138 | 0.3704 | 0.1531 | 77.0% | 0.6322 | 100.0% |
| missing_mean | student_t | random | hom_gaussian | 40 | 0.1659 ± 0.0063 | 0.4621 | 0.1284 | 70.1% | 0.4661 | 100.0% |
| missing_mean | student_t | random | logvar_gaussian | 40 | 0.1660 ± 0.0074 | 0.5242 | 0.1283 | 70.6% | 0.4915 | 100.0% |
| missing_mean | student_t | random | student_t | 40 | 0.1689 ± 0.0103 | -0.0744 | 0.1217 | 96.5% | 0.9030 | 100.0% |
| missing_mean | student_t | spacefill | hom_gaussian | 40 | 0.1631 ± 0.0031 | 0.4097 | 0.1267 | 71.0% | 0.4640 | 100.0% |
| missing_mean | student_t | spacefill | logvar_gaussian | 40 | 0.1630 ± 0.0033 | 0.6696 | 0.1276 | 69.5% | 0.4658 | 100.0% |
| missing_mean | student_t | spacefill | student_t | 40 | 0.1647 ± 0.0043 | -0.0961 | 0.1195 | 97.9% | 0.9371 | 100.0% |
| nonmonotone_noise | hom_gaussian | ivr | hom_gaussian | 40 | 0.0231 ± 0.0195 | -0.3478 | 0.0782 | 90.3% | 0.5027 | 100.0% |
| nonmonotone_noise | hom_gaussian | ivr | logvar_gaussian | 40 | 0.0231 ± 0.0191 | -0.1359 | 0.0781 | 85.5% | 0.4036 | 100.0% |
| nonmonotone_noise | hom_gaussian | ivr | student_t | 40 | 0.0280 ± 0.0213 | -0.5637 | 0.0783 | 90.2% | 0.4946 | 100.0% |
| nonmonotone_noise | hom_gaussian | random | hom_gaussian | 40 | 0.0274 ± 0.0157 | -0.3825 | 0.0789 | 91.2% | 0.5438 | 100.0% |
| nonmonotone_noise | hom_gaussian | random | logvar_gaussian | 40 | 0.0272 ± 0.0153 | -0.1792 | 0.0781 | 86.0% | 0.4104 | 100.0% |
| nonmonotone_noise | hom_gaussian | random | student_t | 40 | 0.0205 ± 0.0129 | -0.5797 | 0.0766 | 90.2% | 0.4924 | 100.0% |
| nonmonotone_noise | hom_gaussian | spacefill | hom_gaussian | 40 | 0.0245 ± 0.0116 | -0.3920 | 0.0786 | 91.5% | 0.5561 | 100.0% |
| nonmonotone_noise | hom_gaussian | spacefill | logvar_gaussian | 40 | 0.0240 ± 0.0110 | -0.0548 | 0.0777 | 84.9% | 0.3908 | 100.0% |
| nonmonotone_noise | hom_gaussian | spacefill | student_t | 40 | 0.0174 ± 0.0091 | -0.5842 | 0.0762 | 89.9% | 0.4849 | 100.0% |
| nonmonotone_noise | logvar_gaussian | ivr | hom_gaussian | 40 | 0.0233 ± 0.0153 | -0.2107 | 0.0781 | 87.7% | 0.4457 | 100.0% |
| nonmonotone_noise | logvar_gaussian | ivr | logvar_gaussian | 40 | 0.0232 ± 0.0151 | 0.3503 | 0.0787 | 81.1% | 0.3467 | 100.0% |
| nonmonotone_noise | logvar_gaussian | ivr | student_t | 40 | 0.0217 ± 0.0136 | -0.5485 | 0.0776 | 88.5% | 0.4533 | 100.0% |
| nonmonotone_noise | logvar_gaussian | random | hom_gaussian | 40 | 0.0274 ± 0.0157 | -0.3825 | 0.0789 | 91.2% | 0.5438 | 100.0% |
| nonmonotone_noise | logvar_gaussian | random | logvar_gaussian | 40 | 0.0272 ± 0.0153 | -0.1792 | 0.0781 | 86.0% | 0.4104 | 100.0% |
| nonmonotone_noise | logvar_gaussian | random | student_t | 40 | 0.0205 ± 0.0129 | -0.5797 | 0.0766 | 90.2% | 0.4924 | 100.0% |
| nonmonotone_noise | logvar_gaussian | spacefill | hom_gaussian | 40 | 0.0245 ± 0.0116 | -0.3920 | 0.0786 | 91.5% | 0.5561 | 100.0% |
| nonmonotone_noise | logvar_gaussian | spacefill | logvar_gaussian | 40 | 0.0240 ± 0.0110 | -0.0548 | 0.0777 | 84.9% | 0.3908 | 100.0% |
| nonmonotone_noise | logvar_gaussian | spacefill | student_t | 40 | 0.0174 ± 0.0091 | -0.5842 | 0.0762 | 89.9% | 0.4849 | 100.0% |
| nonmonotone_noise | student_t | ivr | hom_gaussian | 40 | 0.0225 ± 0.0163 | -0.3767 | 0.0786 | 91.6% | 0.5503 | 100.0% |
| nonmonotone_noise | student_t | ivr | logvar_gaussian | 40 | 0.0227 ± 0.0161 | -0.2561 | 0.0780 | 88.0% | 0.4476 | 100.0% |
| nonmonotone_noise | student_t | ivr | student_t | 40 | 0.0258 ± 0.0190 | -0.5720 | 0.0780 | 92.1% | 0.5565 | 100.0% |
| nonmonotone_noise | student_t | random | hom_gaussian | 40 | 0.0274 ± 0.0157 | -0.3825 | 0.0789 | 91.2% | 0.5438 | 100.0% |
| nonmonotone_noise | student_t | random | logvar_gaussian | 40 | 0.0272 ± 0.0153 | -0.1792 | 0.0781 | 86.0% | 0.4104 | 100.0% |
| nonmonotone_noise | student_t | random | student_t | 40 | 0.0205 ± 0.0129 | -0.5797 | 0.0766 | 90.2% | 0.4924 | 100.0% |
| nonmonotone_noise | student_t | spacefill | hom_gaussian | 40 | 0.0245 ± 0.0116 | -0.3920 | 0.0786 | 91.5% | 0.5561 | 100.0% |
| nonmonotone_noise | student_t | spacefill | logvar_gaussian | 40 | 0.0240 ± 0.0110 | -0.0548 | 0.0777 | 84.9% | 0.3908 | 100.0% |
| nonmonotone_noise | student_t | spacefill | student_t | 40 | 0.0174 ± 0.0091 | -0.5842 | 0.0762 | 89.9% | 0.4849 | 100.0% |
| student3 | hom_gaussian | ivr | hom_gaussian | 40 | 0.0238 ± 0.0115 | -0.4929 | 0.0635 | 93.3% | 0.4554 | 100.0% |
| student3 | hom_gaussian | ivr | logvar_gaussian | 40 | 0.0238 ± 0.0116 | -0.4378 | 0.0631 | 90.6% | 0.3959 | 100.0% |
| student3 | hom_gaussian | ivr | student_t | 40 | 0.0174 ± 0.0083 | -0.8118 | 0.0613 | 92.5% | 0.4089 | 100.0% |
| student3 | hom_gaussian | random | hom_gaussian | 40 | 0.0256 ± 0.0143 | -0.5820 | 0.0633 | 92.7% | 0.4332 | 100.0% |
| student3 | hom_gaussian | random | logvar_gaussian | 40 | 0.0248 ± 0.0124 | -0.4311 | 0.0630 | 90.2% | 0.3811 | 100.0% |
| student3 | hom_gaussian | random | student_t | 40 | 0.0182 ± 0.0077 | -0.8132 | 0.0613 | 92.3% | 0.3973 | 100.0% |
| student3 | hom_gaussian | spacefill | hom_gaussian | 40 | 0.0281 ± 0.0201 | -0.5559 | 0.0654 | 94.7% | 0.5069 | 100.0% |
| student3 | hom_gaussian | spacefill | logvar_gaussian | 40 | 0.0274 ± 0.0169 | -0.3882 | 0.0637 | 90.5% | 0.3985 | 100.0% |
| student3 | hom_gaussian | spacefill | student_t | 40 | 0.0179 ± 0.0075 | -0.8172 | 0.0611 | 92.6% | 0.4093 | 100.0% |
| student3 | logvar_gaussian | ivr | hom_gaussian | 40 | 0.0221 ± 0.0118 | -0.5629 | 0.0631 | 93.1% | 0.4423 | 100.0% |
| student3 | logvar_gaussian | ivr | logvar_gaussian | 40 | 0.0220 ± 0.0119 | -0.3714 | 0.0630 | 90.3% | 0.3825 | 100.0% |
| student3 | logvar_gaussian | ivr | student_t | 40 | 0.0171 ± 0.0079 | -0.8157 | 0.0612 | 92.9% | 0.4223 | 100.0% |
| student3 | logvar_gaussian | random | hom_gaussian | 40 | 0.0256 ± 0.0143 | -0.5820 | 0.0633 | 92.7% | 0.4332 | 100.0% |
| student3 | logvar_gaussian | random | logvar_gaussian | 40 | 0.0248 ± 0.0124 | -0.4311 | 0.0630 | 90.2% | 0.3811 | 100.0% |
| student3 | logvar_gaussian | random | student_t | 40 | 0.0182 ± 0.0077 | -0.8132 | 0.0613 | 92.3% | 0.3973 | 100.0% |
| student3 | logvar_gaussian | spacefill | hom_gaussian | 40 | 0.0281 ± 0.0201 | -0.5559 | 0.0654 | 94.7% | 0.5069 | 100.0% |
| student3 | logvar_gaussian | spacefill | logvar_gaussian | 40 | 0.0274 ± 0.0169 | -0.3882 | 0.0637 | 90.5% | 0.3985 | 100.0% |
| student3 | logvar_gaussian | spacefill | student_t | 40 | 0.0179 ± 0.0075 | -0.8172 | 0.0611 | 92.6% | 0.4093 | 100.0% |
| student3 | student_t | ivr | hom_gaussian | 40 | 0.0229 ± 0.0109 | -0.5353 | 0.0630 | 93.0% | 0.4437 | 100.0% |
| student3 | student_t | ivr | logvar_gaussian | 40 | 0.0229 ± 0.0111 | -0.4307 | 0.0627 | 90.8% | 0.3870 | 100.0% |
| student3 | student_t | ivr | student_t | 40 | 0.0170 ± 0.0072 | -0.8167 | 0.0611 | 92.3% | 0.4072 | 100.0% |
| student3 | student_t | random | hom_gaussian | 40 | 0.0256 ± 0.0143 | -0.5820 | 0.0633 | 92.7% | 0.4332 | 100.0% |
| student3 | student_t | random | logvar_gaussian | 40 | 0.0248 ± 0.0124 | -0.4311 | 0.0630 | 90.2% | 0.3811 | 100.0% |
| student3 | student_t | random | student_t | 40 | 0.0182 ± 0.0077 | -0.8132 | 0.0613 | 92.3% | 0.3973 | 100.0% |
| student3 | student_t | spacefill | hom_gaussian | 40 | 0.0281 ± 0.0201 | -0.5559 | 0.0654 | 94.7% | 0.5069 | 100.0% |
| student3 | student_t | spacefill | logvar_gaussian | 40 | 0.0274 ± 0.0169 | -0.3882 | 0.0637 | 90.5% | 0.3985 | 100.0% |
| student3 | student_t | spacefill | student_t | 40 | 0.0179 ± 0.0075 | -0.8172 | 0.0611 | 92.6% | 0.4093 | 100.0% |

Lower NLL and CRPS are better; continuous-density NLL may be negative. Predictive intervals for new observations differ from intervals for latent means. Estimated noise-parameter uncertainty is not integrated; Student-t covariance and convolution forecasts are approximate. Each cell costs 48 fitting + 81 testing = 129. Six of 6,480 final fits failed the configured convergence tolerance and remain in every summary. Duplicate passive datasets are not independent evidence.

