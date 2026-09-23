# 29. Results: set honesty, false alarms and predictive accuracy are different objectives

[한국어](../ko/29_BOUNDED_RESULTS.md) · [All 363 cells](../../bounded/results/v140/ALL_RESULTS.md) · [Machine-readable summary](../../bounded/results/v140/summary.json) · [Paired descriptive contrasts](../../bounded/results/v140/paired.json)


**v1.4.0-research.1; zero biological observations.** After 60 development runs, source/configuration were locally frozen. We executed 720 G runs, 6,720 H trajectories and 768 I datasets: **8,208 runs**, with 3,840 final I estimators and 49,152 internal parametric-bootstrap fits. Refits are not new evidence. All cells and raw observations are retained. Numerical code was not changed after final evaluation. A local hash freeze is not independent preregistration; developers knew the generators and supplied model bases.

## 1. G: partial identification exposes assumptions but cannot certify them

The following uses `triangulated`, cost 72, 40 worlds per cell. Full-q inclusion and coordinate-projection inclusion differ. Empty sets count as inclusion failures; widths exclude them and show the available denominator.

| World | Bias profile | θ0 included | Joint q included | Empty | θ0 width (n) |
|---|---|---|---|---|---|
| bounded_bias | assume_unbiased | 11/40 (27.5%) | 0/40 (0.0%) | 0/40 (0.0%) | 0.0680 (n=40) |
| bounded_bias | bounded | 40/40 (100.0%) | 39/40 (97.5%) | 0/40 (0.0%) | 0.3054 (n=40) |
| common_in_bounds | bounded | 40/40 (100.0%) | 37/40 (92.5%) | 0/40 (0.0%) | 0.3071 (n=40) |
| common_out_of_bounds | bounded | 0/40 (0.0%) | 0/40 (0.0%) | 0/40 (0.0%) | 0.3116 (n=40) |
| correlated_repeats | bounded | 34/40 (85.0%) | 1/40 (2.5%) | 4/40 (10.0%) | 0.2521 (n=36) |
| nonlinear_sensor | bounded | 14/40 (35.0%) | 0/40 (0.0%) | 25/40 (62.5%) | 0.2095 (n=15) |

In bounded-bias worlds, assuming zero bias gives θ0 inclusion in 11/40 worlds; bounded bias gives 40/40. This is a statement about allowed ranges, not improved posterior confidence or point-estimation RMSE. With common bias inside the limits, coordinate inclusion is 40/40 but full-q inclusion is **37/40=92.5%**, Wilson 95% interval **80.1–97.4%**. Do not turn this finite Monte Carlo result into an empirical 95% guarantee.

When common bias exceeds the limits, coordinate inclusion is 0/40 while all 40 sets remain nonempty. **Feasibility does not certify the external bias limits.** Correlated technical repeats reduce full-q inclusion to 1/40 because the within-group mean intervals omit shared error. Adding nuisance-bias bounds does not repair that sampling assumption.

Evaluator-only noiseless θ0 widths under the default bounded profile are 0.1926 for `bounded_bias` and 0.2154 for `common_in_bounds`. They illustrate remaining identification uncertainty rather than extra observations. The raw `structural_theta0_width` field repeats this **default bounded reference** across profiles; it is not recomputed for each profile. Spending the same budget on more reference repeats can be better for a particular coordinate than combining all channels; no design is declared universally optimal.

## 2. H: replacing known variance adds conditions and a power trade-off

Results below use maximum-gap locations and 50% audit allocation. The three monitors receive identical observations and **are not OR-combined**. Each of the first three valid-null families has 192 worlds, the other families 64.

| World | n | Nominal z | Local t | Conditional-sign e |
|---|---:|---|---|---|
| gaussian_null | 192 | 11/192 (5.7%) | 8/192 (4.2%) | 3/192 (1.6%) |
| hetero_null | 192 | 57/192 (29.7%) | 6/192 (3.1%) | 2/192 (1.0%) |
| symmetric_t3_null | 192 | 6/192 (3.1%) | 4/192 (2.1%) | 4/192 (2.1%) |
| broad_mean | 64 | 64/64 (100.0%) | 63/64 (98.4%) | 64/64 (100.0%) |
| narrow_mean | 64 | 39/64 (60.9%) | 30/64 (46.9%) | 1/64 (1.6%) |
| weak_narrow | 64 | 7/64 (10.9%) | 4/64 (6.2%) | 0/64 (0.0%) |
| common_mode | 64 | 1/64 (1.6%) | 3/64 (4.7%) | 0/64 (0.0%) |
| correlated_repeats | 64 | 51/64 (79.7%) | 43/64 (67.2%) | 18/64 (28.1%) |
| skew_mean_null | 64 | 27/64 (42.2%) | 8/64 (12.5%) | 2/64 (3.1%) |

Under heteroscedastic Gaussian nulls, nominal z alarms in 57/192 worlds, local t in 6/192 and conditional-sign e in 2/192. Local t can tolerate changing variance across locations if the six new differences within each location are iid Gaussian. The sign e-process replaces numerical scale information with **conditional sign balance given history and the selected location**. Symmetric t3 errors satisfy that premise; zero mean alone, skewness or shared within-batch error do not. Stress results under failed premises are not valid-null error rates.

For narrow alternatives, the sign process alarms in **1/64** worlds versus **30/64** for local t. Broad changes are much easier. Common-mode changes cancel in the paired contrast, so prediction error and a false contrast null are distinct. A broad constant effect may already be represented by the predictive intercept; an audit alarm need not imply a misspecified fitted predictor.

### Audit allocation and cost

| Audit allocation | Alarm (local t) | Acquisition cost | Predictive RMSE |
|---:|---|---:|---:|
| 0% | not monitored | 144.00 | 0.1297 |
| 25% | 13/64 (20.3%) | 133.50 | 0.1302 |
| 50% | 30/64 (46.9%) | 138.75 | 0.1310 |
| 75% | 42/64 (65.6%) | 142.88 | 0.1361 |

The acquisition cap is 144, with 81 final held-out measurements charged separately. Setup costs 1 and movement costs 0.5 per distance unit. Leftover audit budget is not reallocated to training. More auditing detects more narrow effects but leaves fewer training observations and slightly increases RMSE. Training datasets are identical across audit policies at fixed allocation; audits never refit the predictor. Shadow first-alarm costs are not an executed optimal stopping/allocation policy.

## 3. I: replicate contrasts do not repair a missing mean term

At cost 48 and four repeats, there are 12 unique input locations. Each cell contains 32 worlds; every dataset is refitted by five estimators. Four appear below; `residual_logvar_base` and all 120 I cells are in the complete table/JSON. Latent and observation inclusion are distinct quantities.

| World | Estimator | Latent RMSE | NLL | Latent inclusion | Observation inclusion | Observation width |
|---|---|---:|---:|---:|---:|---:|
| normal | pooled_base | 0.0251 | -0.7077 | 0.9603 | 0.9468 | 0.4741 |
| normal | difference_logvar_base | 0.0264 | -0.6606 | 0.9456 | 0.9344 | 0.4905 |
| normal | difference_logvar_plus | 0.0312 | -0.6457 | 0.9329 | 0.9356 | 0.4951 |
| normal | plus_bootstrap | 0.0313 | -0.6598 | 0.9255 | 0.9514 | 0.5322 |
| mean_missing | pooled_base | 0.1293 | -0.3452 | 0.3256 | 0.9688 | 0.7070 |
| mean_missing | difference_logvar_base | 0.1361 | -0.1173 | 0.2234 | 0.8198 | 0.4921 |
| mean_missing | difference_logvar_plus | 0.0270 | -0.6458 | 0.9572 | 0.9394 | 0.4968 |
| mean_missing | plus_bootstrap | 0.0277 | -0.6640 | 0.9417 | 0.9572 | 0.5396 |
| combined | pooled_base | 0.1343 | -0.1952 | 0.3920 | 0.9583 | 0.8499 |
| combined | difference_logvar_base | 0.1792 | -0.1830 | 0.2650 | 0.8657 | 0.6243 |
| combined | difference_logvar_plus | 0.0413 | -0.6240 | 0.9676 | 0.9583 | 0.6311 |
| combined | plus_bootstrap | 0.0412 | -0.6296 | 0.9279 | 0.9660 | 0.6722 |
| local_missing | pooled_base | 0.1084 | -0.3798 | 0.6354 | 0.9352 | 0.6305 |
| local_missing | difference_logvar_base | 0.1089 | -0.0607 | 0.4919 | 0.8291 | 0.4594 |
| local_missing | difference_logvar_plus | 0.1052 | -0.0986 | 0.5540 | 0.8310 | 0.4638 |
| local_missing | plus_bootstrap | 0.1053 | -0.2267 | 0.5463 | 0.8542 | 0.4976 |
| shared_batch | pooled_base | 0.0863 | 0.0899 | 0.6416 | 0.8654 | 0.7175 |
| shared_batch | difference_logvar_base | 0.0870 | 1.2162 | 0.4664 | 0.6667 | 0.4573 |
| shared_batch | difference_logvar_plus | 0.1017 | 1.3229 | 0.4579 | 0.6497 | 0.4617 |
| shared_batch | plus_bootstrap | 0.1016 | 0.7444 | 0.4309 | 0.6802 | 0.4939 |

For `mean_missing`, learning noise from differences while retaining the base mean gives RMSE 0.1361 and latent inclusion 22.3%. Adding the predeclared sin(πx) term gives RMSE 0.0270 and latent inclusion 95.7%. A flexible noise model does not fix the mean; this is not automatic mechanism discovery. The same added term has limited value for the unrepresented local bump.

On normal worlds the pooled base mean has RMSE 0.0251 versus 0.0312 with the additional term, retaining the cost of complexity. Shared group errors vanish in technical differences. For `shared_batch`, observation inclusion is only 65.0% for difference-plus and 68.0% after parametric bootstrap. Bootstrap samples from the assumed independent Gaussian model and cannot reconstruct an omitted batch component.

The classical lack-of-fit F alarm is 2/32 for normal r=4 and 32/32 for shared batches. The latter violates independence and is not evidence of 32 newly discovered mechanisms. The pure-error/LOF decomposition holds to 1.78e-15 numerically, but algebra does not certify the F distribution. `within_batch_drift` additionally contains a final measurement-phase shift, as documented in chapter 28.

## 4. Statistical and execution scope

All 363 cells are public. Boolean metrics have whole-world denominators and Wilson intervals; G widths show available nonempty n. H/I summaries retain mean, SD and ranges. Prespecified same-world contrasts use 2,000 descriptive bootstrap resamples, without multiplicity-adjusted superiority claims or generalization to a biological population. Continuous-density NLL can be negative; lower is better. Wider intervals or absorbing mean error into noise can improve observation inclusion without recovering the mean.

All 8,208 records, 1,575,072 serialized observations, costs, role boundaries, freeze ordering, summaries and paired contrasts were revalidated. All 105 representative runs were recomputed exactly. This is not external biological validation or a reproduction of cited papers. See [QA](../../bounded/quality/QA.md) and [next decisions](30_RESEARCH_DECISIONS.md).
