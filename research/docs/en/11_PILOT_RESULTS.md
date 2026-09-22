# 11. Synthetic pilot results and interpretation

[한국어](../ko/11_PILOT_RESULTS.md) · [Executed protocol](10_EVALUATION_PROTOCOL.md) · [Raw summary](../../results/pilot/summary.json)

**504 runs, 42 design cells, twelve seeds per cell; zero biological observations.** Values below were computed by the included code, not borrowed from earlier papers. Every cell is reported. Seeds vary measurement noise and acquisition around the same fixed functions.

## Findings that constrain the research direction

### Correct observation semantics can make simple regression sufficient

In confounded, observation-aware information_gain achieved mean latent RMSE **0.0226**, versus **0.3402** for the separate identity-operator cell. That contrast includes different acquired queries.

Refitting the identical information_gain observations gives aware **0.0226** versus identity **0.2516**. Weighted least squares with the known operator on the same observations also achieved **0.0226**, essentially matching Bayesian regression. The defensible interpretation is that **correct measurement semantics matter**, not that complex AI defeats a simple appropriate model. Bayesian inference and performance superiority are separate claims.

### Passing a prediction target is not identifying a mechanism

For mechanism_pair, fixed_readout passed the predictive composite target in **12/12** runs while leaving A/B at 0.5/0.5: **0/12** resolved at probability 0.95. Information_gain selected A in **12/12**; random also resolved **11/12**. This small two-candidate example therefore does not establish a uniquely capable new acquisition method.

The implementation records prediction acceptance and candidate identification separately. An unresolved candidate is `null`, not an arbitrary tie-break counted as correct.

### A wrong candidate library can produce confident mistakes

In mechanism_outside, information_gain resolved a candidate above 0.95 in **12/12** runs but was correct in **0/12**. Mean maximum probability was numerically 1.0 because the true function was outside both candidates. Guarded stopped in **12/12**, with mean training cost **11.2**, but RMSE **0.6124** and poor coverage did not recover. This is an example of acknowledging assumption failure, not successful mechanism discovery or demonstrated sample efficiency.

### The diagnostic gate can miss errors

For biased_sensor, guarded stopped for assumption failure in only **3/12** runs. The other **9/12** did not meet this stopping rule despite the declared mismatch. Mean RMSE was **0.1452** for information_gain and slightly worse, **0.1464**, for guarded. Mean coverage was about **75.4%**. A modest residual does not certify the observation operator. This motivates studying missed detection and false alarms next.

For missing_term, guarded stopped **12/12** runs at mean training cost **9.6**, below the cap of 24, but RMSE **0.5153** and coverage **19.3%** failed the final target throughout. Stopping does not itself supply a corrected mechanism or a useful new measurement.

### Separate fidelities, but retain a strong HF-only baseline

For fidelity_deceptive, naive pooling achieved mean RMSE **0.8162**, joint GP **0.0472**, and guarded **0.0458**. However, **HF-only was lower at 0.0439**. Guarded switched in 12/12 runs; this does not establish universal superiority over MF.

For fidelity_helpful, HF-only achieved **0.0334**, MF **0.0452**, and guarded **0.0442**. A useful LF relationship does not guarantee that the chosen MF model wins at equal cost. Fixed hyperparameters, cost ratios, and acquisition rules matter. Guarded switched in 2/12 runs.

### Better fit need not reach the target

For narrow_peak, guarded reduced RMSE from max_variance **0.1882** to **0.1417**, with coverage increasing **74.9% → 88.3%**. Nonetheless, the final target passed in **0/12** runs. In smooth, RMSE was nearly equal at **0.0435 / 0.0434**, and the descriptive bootstrap does not establish a clear improvement. Guarded is not declared a general winner.

## All design cells

“Latent RMSE” here evaluates the **noise-free observed response function**, not reconstruction of every hidden biological state. Coverage refers to final observation predictive intervals. Costs are synthetic units; total cost includes diagnostics and test. SD describes seed variation.

### `smooth`

| Policy / operator | RMSE mean ± SD | Obs. coverage | Train / total cost | Target passes | Stops | Fallback |
|---|---:|---:|---:|---:|---:|---:|
| `guarded` / aware | 0.0434 ± 0.0127 | 95.6% | 24.00 / 94.00 | 12/12 | 0/12 | 0/12 |
| `max_variance` / aware | 0.0435 ± 0.0096 | 94.3% | 24.00 / 94.00 | 12/12 | 0/12 | 0/12 |
| `random` / aware | 0.0488 ± 0.0104 | 95.4% | 24.00 / 94.00 | 12/12 | 0/12 | 0/12 |
| `space_filling` / aware | 0.0446 ± 0.0069 | 94.0% | 24.00 / 94.00 | 12/12 | 0/12 | 0/12 |

### `narrow_peak`

| Policy / operator | RMSE mean ± SD | Obs. coverage | Train / total cost | Target passes | Stops | Fallback |
|---|---:|---:|---:|---:|---:|---:|
| `guarded` / aware | 0.1417 ± 0.0236 | 88.3% | 24.00 / 94.00 | 0/12 | 0/12 | 0/12 |
| `max_variance` / aware | 0.1882 ± 0.0051 | 74.9% | 24.00 / 94.00 | 0/12 | 0/12 | 0/12 |
| `random` / aware | 0.2156 ± 0.0212 | 78.0% | 24.00 / 94.00 | 0/12 | 0/12 | 0/12 |
| `space_filling` / aware | 0.1896 ± 0.0049 | 79.9% | 24.00 / 94.00 | 0/12 | 0/12 | 0/12 |

### `confounded`

| Policy / operator | RMSE mean ± SD | Obs. coverage | Train / total cost | Target passes | Stops | Fallback |
|---|---:|---:|---:|---:|---:|---:|
| `fixed_readout` / aware | 0.0864 ± 0.0073 | 98.2% | 24.00 / 374.00 | 0/12 | 0/12 | 0/12 |
| `guarded` / aware | 0.0226 ± 0.0131 | 96.0% | 23.80 / 373.80 | 12/12 | 0/12 | 0/12 |
| `information_gain` / aware | 0.0226 ± 0.0131 | 96.0% | 23.80 / 373.80 | 12/12 | 0/12 | 0/12 |
| `information_gain` / identity | 0.3402 ± 0.0138 | 49.1% | 24.00 / 374.00 | 0/12 | 0/12 | 0/12 |
| `observation_variance` / aware | 0.0219 ± 0.0110 | 96.1% | 23.40 / 373.40 | 12/12 | 0/12 | 0/12 |
| `random` / aware | 0.0298 ± 0.0221 | 95.7% | 23.68 / 373.68 | 12/12 | 0/12 | 0/12 |

### `biased_sensor`

| Policy / operator | RMSE mean ± SD | Obs. coverage | Train / total cost | Target passes | Stops | Fallback |
|---|---:|---:|---:|---:|---:|---:|
| `fixed_readout` / aware | 0.1254 ± 0.0015 | 98.4% | 24.00 / 374.00 | 0/12 | 0/12 | 0/12 |
| `guarded` / aware | 0.1464 ± 0.0118 | 75.4% | 20.57 / 370.57 | 0/12 | 3/12 | 0/12 |
| `information_gain` / aware | 0.1452 ± 0.0108 | 75.4% | 23.80 / 373.80 | 0/12 | 0/12 | 0/12 |
| `observation_variance` / aware | 0.1452 ± 0.0114 | 75.2% | 23.40 / 373.40 | 0/12 | 0/12 | 0/12 |
| `random` / aware | 0.1397 ± 0.0256 | 78.7% | 23.68 / 373.68 | 3/12 | 0/12 | 0/12 |

### `missing_term`

| Policy / operator | RMSE mean ± SD | Obs. coverage | Train / total cost | Target passes | Stops | Fallback |
|---|---:|---:|---:|---:|---:|---:|
| `fixed_readout` / aware | 0.5287 ± 0.0010 | 59.9% | 24.00 / 374.00 | 0/12 | 0/12 | 0/12 |
| `guarded` / aware | 0.5153 ± 0.0027 | 19.3% | 9.60 / 359.60 | 0/12 | 12/12 | 0/12 |
| `information_gain` / aware | 0.5242 ± 0.0037 | 19.2% | 23.80 / 373.80 | 0/12 | 0/12 | 0/12 |
| `observation_variance` / aware | 0.5247 ± 0.0051 | 19.8% | 23.40 / 373.40 | 0/12 | 0/12 | 0/12 |
| `random` / aware | 0.5553 ± 0.0534 | 18.3% | 23.68 / 373.68 | 0/12 | 0/12 | 0/12 |

### `fidelity_helpful`

| Policy / operator | RMSE mean ± SD | Obs. coverage | Train / total cost | Target passes | Stops | Fallback |
|---|---:|---:|---:|---:|---:|---:|
| `guarded` / aware | 0.0442 ± 0.0115 | 94.7% | 23.73 / 93.73 | 12/12 | 0/12 | 2/12 |
| `hf_only` / aware | 0.0334 ± 0.0096 | 95.6% | 24.00 / 94.00 | 12/12 | 0/12 | 0/12 |
| `multifidelity` / aware | 0.0452 ± 0.0118 | 94.8% | 23.75 / 93.75 | 12/12 | 0/12 | 0/12 |
| `naive_pool` / aware | 0.1836 ± 0.0110 | 61.5% | 24.00 / 94.00 | 0/12 | 0/12 | 0/12 |

### `fidelity_deceptive`

| Policy / operator | RMSE mean ± SD | Obs. coverage | Train / total cost | Target passes | Stops | Fallback |
|---|---:|---:|---:|---:|---:|---:|
| `guarded` / aware | 0.0458 ± 0.0099 | 93.9% | 23.52 / 93.52 | 12/12 | 0/12 | 12/12 |
| `hf_only` / aware | 0.0439 ± 0.0098 | 94.0% | 24.00 / 94.00 | 12/12 | 0/12 | 0/12 |
| `multifidelity` / aware | 0.0472 ± 0.0093 | 94.0% | 23.75 / 93.75 | 12/12 | 0/12 | 0/12 |
| `naive_pool` / aware | 0.8162 ± 0.0070 | 31.7% | 24.00 / 94.00 | 0/12 | 0/12 | 0/12 |

### `mechanism_pair`

| Policy / operator | RMSE mean ± SD | Obs. coverage | Train / total cost | Target passes | Stops | Fallback |
|---|---:|---:|---:|---:|---:|---:|
| `fixed_readout` / aware | 0.0676 ± 0.0000 | 95.2% | 24.00 / 374.00 | 12/12 | 0/12 | 0/12 |
| `guarded` / aware | 0.0000 ± 0.0000 | 95.1% | 23.80 / 373.80 | 12/12 | 0/12 | 0/12 |
| `information_gain` / aware | 0.0000 ± 0.0000 | 95.1% | 23.80 / 373.80 | 12/12 | 0/12 | 0/12 |
| `observation_variance` / aware | 0.0000 ± 0.0000 | 95.1% | 23.63 / 373.63 | 12/12 | 0/12 | 0/12 |
| `random` / aware | 0.0037 ± 0.0129 | 95.2% | 23.68 / 373.68 | 12/12 | 0/12 | 0/12 |

### `mechanism_outside`

| Policy / operator | RMSE mean ± SD | Obs. coverage | Train / total cost | Target passes | Stops | Fallback |
|---|---:|---:|---:|---:|---:|---:|
| `fixed_readout` / aware | 0.5980 ± 0.0000 | 14.9% | 24.00 / 374.00 | 0/12 | 0/12 | 0/12 |
| `guarded` / aware | 0.6124 ± 0.0000 | 12.3% | 11.20 / 361.20 | 0/12 | 12/12 | 0/12 |
| `information_gain` / aware | 0.6124 ± 0.0000 | 12.3% | 23.80 / 373.80 | 0/12 | 0/12 | 0/12 |
| `observation_variance` / aware | 0.6124 ± 0.0000 | 12.3% | 23.60 / 373.60 | 0/12 | 0/12 | 0/12 |
| `random` / aware | 0.5965 ± 0.0096 | 11.7% | 23.68 / 373.68 | 0/12 | 0/12 | 0/12 |

## Paired seed variation

Differences are guarded minus the reference RMSE; negative means lower guarded error for this metric. Intervals use 2,000 seed-bootstrap resamples. They are descriptive, not biological-population intervals or multiplicity-adjusted inference.

| Scenario | Reference | Mean difference | Descriptive 95% interval |
|---|---|---:|---:|
| `smooth` | max_variance | -0.00011 | [-0.00721, 0.00810] |
| `narrow_peak` | max_variance | -0.04648 | [-0.05687, -0.03297] |
| `confounded` | information_gain | 0.00000 | [0.00000, 0.00000] |
| `biased_sensor` | information_gain | 0.00115 | [-0.00010, 0.00294] |
| `missing_term` | information_gain | -0.00890 | [-0.01167, -0.00551] |
| `fidelity_helpful` | multifidelity | -0.00099 | [-0.00233, 0.00000] |
| `fidelity_deceptive` | multifidelity | -0.00140 | [-0.00903, 0.00609] |
| `mechanism_pair` | information_gain | 0.00000 | [0.00000, 0.00000] |
| `mechanism_outside` | information_gain | 0.00000 | [0.00000, 0.00000] |

## Decision supported by these results

Study missed assumption failure, false alarms, and choice of additional measurement type before integrating more model families. The [next research direction](12_RESEARCH_DIRECTION.md) states falsification criteria. These results do not establish real biological data efficiency, laboratory safety, unknown mechanism discovery, or nominal coverage guarantees.
