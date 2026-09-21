# Executed synthetic demonstration

Twenty seeds with shared initialization, noise and budgets. The table reports means at **30 queries**. Zero biological observations; not a biological benchmark.

| Scenario | Policy | RMSE mean | RMSE SD | Latent 95% coverage | Mean width |
|---|---|---:|---:|---:|---:|
| smooth | random | 0.03719 | 0.01360 | 94.31% | 0.13674 |
| smooth | max_variance | 0.02838 | 0.00795 | 97.14% | 0.12669 |
| narrow_peak | random | 0.18809 | 0.01929 | 66.34% | 0.13674 |
| narrow_peak | max_variance | 0.17636 | 0.01465 | 70.11% | 0.12669 |

## Interpretation

Max-variance acquisition had lower mean RMSE in both fixed functions. In the narrow-peak case, both policies nevertheless had empirical coverage far below the nominal 95%. More data can shrink intervals while model bias remains. This observation applies to a fixed-kernel example, not a universal ranking of AL or GPs. Task-specific kernel/hyperparameter selection could change the outcome.

Coverage is a diagnostic over a fixed-function test grid and noise seeds, not a population-coverage proof or an interval for a new noisy measurement. No statistical significance test was performed.

![Smooth RMSE](results/smooth_rmse.png)

![Narrow-peak coverage](results/narrow_peak_coverage.png)

[All runs](results/runs.json) · [Aggregates](results/summary.json) · [Environment](results/environment.json) · [Identifiability counterexample](results/identifiability.json)
