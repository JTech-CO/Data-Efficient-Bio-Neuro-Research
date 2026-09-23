# All evaluated cells / 전체 평가 셀

Synthetic only. Means, available denominators and all policies are retained. `summary.json` also contains SD, min/max and Wilson intervals. Width means exclude empty sets; their available n is shown. No multiplicity-adjusted superiority claims.

## G
| Scenario | Design | Assumptions | Runs | Empty | Joint q included | θ0 included | θ0 width (available n) | Cost |
|---|---|---|---:|---|---|---|---|---:|
| bounded_bias | addition_blank | assume_unbiased | 40 | 0/40 (0.0%) | 0/40 (0.0%) | 38/40 (95.0%) | 0.3071 (n=40) | 72.00 |
| bounded_bias | addition_blank | bounded | 40 | 0/40 (0.0%) | 38/40 (95.0%) | 40/40 (100.0%) | 0.6771 (n=40) | 72.00 |
| bounded_bias | addition_blank | wide | 40 | 0/40 (0.0%) | 38/40 (95.0%) | 40/40 (100.0%) | 1.0372 (n=40) | 72.00 |
| bounded_bias | reference_only | assume_unbiased | 40 | 0/40 (0.0%) | 0/40 (0.0%) | 6/40 (15.0%) | 0.0439 (n=40) | 72.00 |
| bounded_bias | reference_only | bounded | 40 | 0/40 (0.0%) | 38/40 (95.0%) | 40/40 (100.0%) | 0.2839 (n=40) | 72.00 |
| bounded_bias | reference_only | wide | 40 | 0/40 (0.0%) | 38/40 (95.0%) | 40/40 (100.0%) | 0.5239 (n=40) | 72.00 |
| bounded_bias | triangulated | assume_unbiased | 40 | 0/40 (0.0%) | 0/40 (0.0%) | 11/40 (27.5%) | 0.0680 (n=40) | 72.00 |
| bounded_bias | triangulated | bounded | 40 | 0/40 (0.0%) | 39/40 (97.5%) | 40/40 (100.0%) | 0.3054 (n=40) | 72.00 |
| bounded_bias | triangulated | wide | 40 | 0/40 (0.0%) | 39/40 (97.5%) | 40/40 (100.0%) | 0.5377 (n=40) | 72.00 |
| common_in_bounds | addition_blank | assume_unbiased | 40 | 0/40 (0.0%) | 1/40 (2.5%) | 40/40 (100.0%) | 0.2903 (n=40) | 72.00 |
| common_in_bounds | addition_blank | bounded | 40 | 0/40 (0.0%) | 39/40 (97.5%) | 40/40 (100.0%) | 0.6609 (n=40) | 72.00 |
| common_in_bounds | addition_blank | wide | 40 | 0/40 (0.0%) | 39/40 (97.5%) | 40/40 (100.0%) | 1.0215 (n=40) | 72.00 |
| common_in_bounds | reference_only | assume_unbiased | 40 | 0/40 (0.0%) | 0/40 (0.0%) | 0/40 (0.0%) | 0.0410 (n=40) | 72.00 |
| common_in_bounds | reference_only | bounded | 40 | 0/40 (0.0%) | 38/40 (95.0%) | 40/40 (100.0%) | 0.2810 (n=40) | 72.00 |
| common_in_bounds | reference_only | wide | 40 | 0/40 (0.0%) | 38/40 (95.0%) | 40/40 (100.0%) | 0.5210 (n=40) | 72.00 |
| common_in_bounds | triangulated | assume_unbiased | 40 | 0/40 (0.0%) | 0/40 (0.0%) | 0/40 (0.0%) | 0.0677 (n=40) | 72.00 |
| common_in_bounds | triangulated | bounded | 40 | 0/40 (0.0%) | 37/40 (92.5%) | 40/40 (100.0%) | 0.3071 (n=40) | 72.00 |
| common_in_bounds | triangulated | wide | 40 | 0/40 (0.0%) | 37/40 (92.5%) | 40/40 (100.0%) | 0.5432 (n=40) | 72.00 |
| common_out_of_bounds | addition_blank | assume_unbiased | 40 | 0/40 (0.0%) | 0/40 (0.0%) | 0/40 (0.0%) | 0.3351 (n=40) | 72.00 |
| common_out_of_bounds | addition_blank | bounded | 40 | 0/40 (0.0%) | 0/40 (0.0%) | 27/40 (67.5%) | 0.7672 (n=40) | 72.00 |
| common_out_of_bounds | addition_blank | wide | 40 | 0/40 (0.0%) | 0/40 (0.0%) | 40/40 (100.0%) | 1.1758 (n=40) | 72.00 |
| common_out_of_bounds | reference_only | assume_unbiased | 40 | 0/40 (0.0%) | 0/40 (0.0%) | 0/40 (0.0%) | 0.0422 (n=40) | 72.00 |
| common_out_of_bounds | reference_only | bounded | 40 | 0/40 (0.0%) | 0/40 (0.0%) | 0/40 (0.0%) | 0.2822 (n=40) | 72.00 |
| common_out_of_bounds | reference_only | wide | 40 | 0/40 (0.0%) | 0/40 (0.0%) | 0/40 (0.0%) | 0.5222 (n=40) | 72.00 |
| common_out_of_bounds | triangulated | assume_unbiased | 40 | 0/40 (0.0%) | 0/40 (0.0%) | 0/40 (0.0%) | 0.0721 (n=40) | 72.00 |
| common_out_of_bounds | triangulated | bounded | 40 | 0/40 (0.0%) | 0/40 (0.0%) | 0/40 (0.0%) | 0.3116 (n=40) | 72.00 |
| common_out_of_bounds | triangulated | wide | 40 | 0/40 (0.0%) | 0/40 (0.0%) | 0/40 (0.0%) | 0.5497 (n=40) | 72.00 |
| correlated_repeats | addition_blank | assume_unbiased | 40 | 9/40 (22.5%) | 0/40 (0.0%) | 17/40 (42.5%) | 0.2607 (n=31) | 72.00 |
| correlated_repeats | addition_blank | bounded | 40 | 9/40 (22.5%) | 0/40 (0.0%) | 27/40 (67.5%) | 0.6319 (n=31) | 72.00 |
| correlated_repeats | addition_blank | wide | 40 | 9/40 (22.5%) | 1/40 (2.5%) | 31/40 (77.5%) | 0.9848 (n=31) | 72.00 |
| correlated_repeats | reference_only | assume_unbiased | 40 | 0/40 (0.0%) | 0/40 (0.0%) | 7/40 (17.5%) | 0.0404 (n=40) | 72.00 |
| correlated_repeats | reference_only | bounded | 40 | 0/40 (0.0%) | 3/40 (7.5%) | 39/40 (97.5%) | 0.2804 (n=40) | 72.00 |
| correlated_repeats | reference_only | wide | 40 | 0/40 (0.0%) | 5/40 (12.5%) | 40/40 (100.0%) | 0.5204 (n=40) | 72.00 |
| correlated_repeats | triangulated | assume_unbiased | 40 | 20/40 (50.0%) | 0/40 (0.0%) | 6/40 (15.0%) | 0.0463 (n=20) | 72.00 |
| correlated_repeats | triangulated | bounded | 40 | 4/40 (10.0%) | 1/40 (2.5%) | 34/40 (85.0%) | 0.2521 (n=36) | 72.00 |
| correlated_repeats | triangulated | wide | 40 | 2/40 (5.0%) | 2/40 (5.0%) | 37/40 (92.5%) | 0.4844 (n=38) | 72.00 |
| nonlinear_sensor | addition_blank | assume_unbiased | 40 | 40/40 (100.0%) | 0/40 (0.0%) | 0/40 (0.0%) | NA (n=0) | 72.00 |
| nonlinear_sensor | addition_blank | bounded | 40 | 40/40 (100.0%) | 0/40 (0.0%) | 0/40 (0.0%) | NA (n=0) | 72.00 |
| nonlinear_sensor | addition_blank | wide | 40 | 40/40 (100.0%) | 0/40 (0.0%) | 0/40 (0.0%) | NA (n=0) | 72.00 |
| nonlinear_sensor | reference_only | assume_unbiased | 40 | 6/40 (15.0%) | 0/40 (0.0%) | 34/40 (85.0%) | 0.0417 (n=34) | 72.00 |
| nonlinear_sensor | reference_only | bounded | 40 | 0/40 (0.0%) | 0/40 (0.0%) | 40/40 (100.0%) | 0.2673 (n=40) | 72.00 |
| nonlinear_sensor | reference_only | wide | 40 | 0/40 (0.0%) | 0/40 (0.0%) | 40/40 (100.0%) | 0.5073 (n=40) | 72.00 |
| nonlinear_sensor | triangulated | assume_unbiased | 40 | 39/40 (97.5%) | 0/40 (0.0%) | 1/40 (2.5%) | 0.0246 (n=1) | 72.00 |
| nonlinear_sensor | triangulated | bounded | 40 | 25/40 (62.5%) | 0/40 (0.0%) | 14/40 (35.0%) | 0.2095 (n=15) | 72.00 |
| nonlinear_sensor | triangulated | wide | 40 | 23/40 (57.5%) | 0/40 (0.0%) | 17/40 (42.5%) | 0.4490 (n=17) | 72.00 |
| normal | addition_blank | assume_unbiased | 40 | 0/40 (0.0%) | 40/40 (100.0%) | 40/40 (100.0%) | 0.2906 (n=40) | 72.00 |
| normal | addition_blank | bounded | 40 | 0/40 (0.0%) | 40/40 (100.0%) | 40/40 (100.0%) | 0.6498 (n=40) | 72.00 |
| normal | addition_blank | wide | 40 | 0/40 (0.0%) | 40/40 (100.0%) | 40/40 (100.0%) | 0.9961 (n=40) | 72.00 |
| normal | reference_only | assume_unbiased | 40 | 0/40 (0.0%) | 39/40 (97.5%) | 40/40 (100.0%) | 0.0421 (n=40) | 72.00 |
| normal | reference_only | bounded | 40 | 0/40 (0.0%) | 39/40 (97.5%) | 40/40 (100.0%) | 0.2821 (n=40) | 72.00 |
| normal | reference_only | wide | 40 | 0/40 (0.0%) | 39/40 (97.5%) | 40/40 (100.0%) | 0.5221 (n=40) | 72.00 |
| normal | triangulated | assume_unbiased | 40 | 0/40 (0.0%) | 37/40 (92.5%) | 40/40 (100.0%) | 0.0669 (n=40) | 72.00 |
| normal | triangulated | bounded | 40 | 0/40 (0.0%) | 38/40 (95.0%) | 40/40 (100.0%) | 0.3065 (n=40) | 72.00 |
| normal | triangulated | wide | 40 | 0/40 (0.0%) | 38/40 (95.0%) | 40/40 (100.0%) | 0.5439 (n=40) | 72.00 |
## H
| Scenario | Policy | Audit share | Monitor | Runs | Alarm | Wilson 95% | Acquisition cost | RMSE | NLL |
|---|---|---:|---|---:|---|---|---:|---:|---:|
| broad_mean | adaptive_cover | 0.25 | conditional_sign_e | 64 | 41/64 (64.1%) | 51.8%–74.7% | 133.50 | 0.0162 | -0.7925 |
| broad_mean | adaptive_cover | 0.25 | local_t_bonferroni | 64 | 61/64 (95.3%) | 87.1%–98.4% | 133.50 | 0.0162 | -0.7925 |
| broad_mean | adaptive_cover | 0.25 | nominal_z | 64 | 64/64 (100.0%) | 94.3%–100.0% | 133.50 | 0.0162 | -0.7925 |
| broad_mean | adaptive_cover | 0.5 | conditional_sign_e | 64 | 64/64 (100.0%) | 94.3%–100.0% | 138.46 | 0.0188 | -0.7847 |
| broad_mean | adaptive_cover | 0.5 | local_t_bonferroni | 64 | 63/64 (98.4%) | 91.7%–99.7% | 138.46 | 0.0188 | -0.7847 |
| broad_mean | adaptive_cover | 0.5 | nominal_z | 64 | 64/64 (100.0%) | 94.3%–100.0% | 138.46 | 0.0188 | -0.7847 |
| broad_mean | adaptive_cover | 0.75 | conditional_sign_e | 64 | 64/64 (100.0%) | 94.3%–100.0% | 142.71 | 0.0257 | -0.7545 |
| broad_mean | adaptive_cover | 0.75 | local_t_bonferroni | 64 | 64/64 (100.0%) | 94.3%–100.0% | 142.71 | 0.0257 | -0.7545 |
| broad_mean | adaptive_cover | 0.75 | nominal_z | 64 | 64/64 (100.0%) | 94.3%–100.0% | 142.71 | 0.0257 | -0.7545 |
| broad_mean | max_gap | 0.0 | conditional_sign_e | 64 | not monitored | NA | 144.00 | 0.0144 | -0.7977 |
| broad_mean | max_gap | 0.0 | local_t_bonferroni | 64 | not monitored | NA | 144.00 | 0.0144 | -0.7977 |
| broad_mean | max_gap | 0.0 | nominal_z | 64 | not monitored | NA | 144.00 | 0.0144 | -0.7977 |
| broad_mean | max_gap | 0.25 | conditional_sign_e | 64 | 41/64 (64.1%) | 51.8%–74.7% | 133.50 | 0.0162 | -0.7925 |
| broad_mean | max_gap | 0.25 | local_t_bonferroni | 64 | 61/64 (95.3%) | 87.1%–98.4% | 133.50 | 0.0162 | -0.7925 |
| broad_mean | max_gap | 0.25 | nominal_z | 64 | 64/64 (100.0%) | 94.3%–100.0% | 133.50 | 0.0162 | -0.7925 |
| broad_mean | max_gap | 0.5 | conditional_sign_e | 64 | 64/64 (100.0%) | 94.3%–100.0% | 138.75 | 0.0188 | -0.7847 |
| broad_mean | max_gap | 0.5 | local_t_bonferroni | 64 | 63/64 (98.4%) | 91.7%–99.7% | 138.75 | 0.0188 | -0.7847 |
| broad_mean | max_gap | 0.5 | nominal_z | 64 | 64/64 (100.0%) | 94.3%–100.0% | 138.75 | 0.0188 | -0.7847 |
| broad_mean | max_gap | 0.75 | conditional_sign_e | 64 | 64/64 (100.0%) | 94.3%–100.0% | 142.88 | 0.0257 | -0.7545 |
| broad_mean | max_gap | 0.75 | local_t_bonferroni | 64 | 63/64 (98.4%) | 91.7%–99.7% | 142.88 | 0.0257 | -0.7545 |
| broad_mean | max_gap | 0.75 | nominal_z | 64 | 64/64 (100.0%) | 94.3%–100.0% | 142.88 | 0.0257 | -0.7545 |
| common_mode | adaptive_cover | 0.25 | conditional_sign_e | 64 | 0/64 (0.0%) | 0.0%–5.7% | 133.50 | 0.1307 | -0.3276 |
| common_mode | adaptive_cover | 0.25 | local_t_bonferroni | 64 | 2/64 (3.1%) | 0.9%–10.7% | 133.50 | 0.1307 | -0.3276 |
| common_mode | adaptive_cover | 0.25 | nominal_z | 64 | 0/64 (0.0%) | 0.0%–5.7% | 133.50 | 0.1307 | -0.3276 |
| common_mode | adaptive_cover | 0.5 | conditional_sign_e | 64 | 0/64 (0.0%) | 0.0%–5.7% | 138.45 | 0.1323 | -0.3115 |
| common_mode | adaptive_cover | 0.5 | local_t_bonferroni | 64 | 2/64 (3.1%) | 0.9%–10.7% | 138.45 | 0.1323 | -0.3115 |
| common_mode | adaptive_cover | 0.5 | nominal_z | 64 | 1/64 (1.6%) | 0.3%–8.3% | 138.45 | 0.1323 | -0.3115 |
| common_mode | adaptive_cover | 0.75 | conditional_sign_e | 64 | 0/64 (0.0%) | 0.0%–5.7% | 142.67 | 0.1375 | -0.2713 |
| common_mode | adaptive_cover | 0.75 | local_t_bonferroni | 64 | 1/64 (1.6%) | 0.3%–8.3% | 142.67 | 0.1375 | -0.2713 |
| common_mode | adaptive_cover | 0.75 | nominal_z | 64 | 1/64 (1.6%) | 0.3%–8.3% | 142.67 | 0.1375 | -0.2713 |
| common_mode | max_gap | 0.0 | conditional_sign_e | 64 | not monitored | NA | 144.00 | 0.1299 | -0.3357 |
| common_mode | max_gap | 0.0 | local_t_bonferroni | 64 | not monitored | NA | 144.00 | 0.1299 | -0.3357 |
| common_mode | max_gap | 0.0 | nominal_z | 64 | not monitored | NA | 144.00 | 0.1299 | -0.3357 |
| common_mode | max_gap | 0.25 | conditional_sign_e | 64 | 0/64 (0.0%) | 0.0%–5.7% | 133.50 | 0.1307 | -0.3276 |
| common_mode | max_gap | 0.25 | local_t_bonferroni | 64 | 2/64 (3.1%) | 0.9%–10.7% | 133.50 | 0.1307 | -0.3276 |
| common_mode | max_gap | 0.25 | nominal_z | 64 | 0/64 (0.0%) | 0.0%–5.7% | 133.50 | 0.1307 | -0.3276 |
| common_mode | max_gap | 0.5 | conditional_sign_e | 64 | 0/64 (0.0%) | 0.0%–5.7% | 138.75 | 0.1323 | -0.3115 |
| common_mode | max_gap | 0.5 | local_t_bonferroni | 64 | 3/64 (4.7%) | 1.6%–12.9% | 138.75 | 0.1323 | -0.3115 |
| common_mode | max_gap | 0.5 | nominal_z | 64 | 1/64 (1.6%) | 0.3%–8.3% | 138.75 | 0.1323 | -0.3115 |
| common_mode | max_gap | 0.75 | conditional_sign_e | 64 | 0/64 (0.0%) | 0.0%–5.7% | 142.88 | 0.1375 | -0.2713 |
| common_mode | max_gap | 0.75 | local_t_bonferroni | 64 | 5/64 (7.8%) | 3.4%–17.0% | 142.88 | 0.1375 | -0.2713 |
| common_mode | max_gap | 0.75 | nominal_z | 64 | 3/64 (4.7%) | 1.6%–12.9% | 142.88 | 0.1375 | -0.2713 |
| correlated_repeats | adaptive_cover | 0.25 | conditional_sign_e | 64 | 5/64 (7.8%) | 3.4%–17.0% | 133.50 | 0.0342 | -0.1302 |
| correlated_repeats | adaptive_cover | 0.25 | local_t_bonferroni | 64 | 25/64 (39.1%) | 28.1%–51.3% | 133.50 | 0.0342 | -0.1302 |
| correlated_repeats | adaptive_cover | 0.25 | nominal_z | 64 | 35/64 (54.7%) | 42.6%–66.3% | 133.50 | 0.0342 | -0.1302 |
| correlated_repeats | adaptive_cover | 0.5 | conditional_sign_e | 64 | 16/64 (25.0%) | 16.0%–36.8% | 138.42 | 0.0424 | -0.1222 |
| correlated_repeats | adaptive_cover | 0.5 | local_t_bonferroni | 64 | 47/64 (73.4%) | 61.5%–82.7% | 138.42 | 0.0424 | -0.1222 |
| correlated_repeats | adaptive_cover | 0.5 | nominal_z | 64 | 55/64 (85.9%) | 75.4%–92.4% | 138.42 | 0.0424 | -0.1222 |
| correlated_repeats | adaptive_cover | 0.75 | conditional_sign_e | 64 | 25/64 (39.1%) | 28.1%–51.3% | 142.60 | 0.0560 | -0.0983 |
| correlated_repeats | adaptive_cover | 0.75 | local_t_bonferroni | 64 | 53/64 (82.8%) | 71.8%–90.1% | 142.60 | 0.0560 | -0.0983 |
| correlated_repeats | adaptive_cover | 0.75 | nominal_z | 64 | 63/64 (98.4%) | 91.7%–99.7% | 142.60 | 0.0560 | -0.0983 |
| correlated_repeats | max_gap | 0.0 | conditional_sign_e | 64 | not monitored | NA | 144.00 | 0.0284 | -0.1356 |
| correlated_repeats | max_gap | 0.0 | local_t_bonferroni | 64 | not monitored | NA | 144.00 | 0.0284 | -0.1356 |
| correlated_repeats | max_gap | 0.0 | nominal_z | 64 | not monitored | NA | 144.00 | 0.0284 | -0.1356 |
| correlated_repeats | max_gap | 0.25 | conditional_sign_e | 64 | 5/64 (7.8%) | 3.4%–17.0% | 133.50 | 0.0342 | -0.1302 |
| correlated_repeats | max_gap | 0.25 | local_t_bonferroni | 64 | 25/64 (39.1%) | 28.1%–51.3% | 133.50 | 0.0342 | -0.1302 |
| correlated_repeats | max_gap | 0.25 | nominal_z | 64 | 35/64 (54.7%) | 42.6%–66.3% | 133.50 | 0.0342 | -0.1302 |
| correlated_repeats | max_gap | 0.5 | conditional_sign_e | 64 | 18/64 (28.1%) | 18.6%–40.1% | 138.75 | 0.0424 | -0.1222 |
| correlated_repeats | max_gap | 0.5 | local_t_bonferroni | 64 | 43/64 (67.2%) | 55.0%–77.4% | 138.75 | 0.0424 | -0.1222 |
| correlated_repeats | max_gap | 0.5 | nominal_z | 64 | 51/64 (79.7%) | 68.3%–87.7% | 138.75 | 0.0424 | -0.1222 |
| correlated_repeats | max_gap | 0.75 | conditional_sign_e | 64 | 31/64 (48.4%) | 36.6%–60.4% | 142.88 | 0.0560 | -0.0983 |
| correlated_repeats | max_gap | 0.75 | local_t_bonferroni | 64 | 47/64 (73.4%) | 61.5%–82.7% | 142.88 | 0.0560 | -0.0983 |
| correlated_repeats | max_gap | 0.75 | nominal_z | 64 | 62/64 (96.9%) | 89.3%–99.1% | 142.88 | 0.0560 | -0.0983 |
| gaussian_null | adaptive_cover | 0.25 | conditional_sign_e | 192 | 0/192 (0.0%) | 0.0%–2.0% | 133.50 | 0.0180 | -0.7575 |
| gaussian_null | adaptive_cover | 0.25 | local_t_bonferroni | 192 | 5/192 (2.6%) | 1.1%–6.0% | 133.50 | 0.0180 | -0.7575 |
| gaussian_null | adaptive_cover | 0.25 | nominal_z | 192 | 9/192 (4.7%) | 2.5%–8.7% | 133.50 | 0.0180 | -0.7575 |
| gaussian_null | adaptive_cover | 0.5 | conditional_sign_e | 192 | 3/192 (1.6%) | 0.5%–4.5% | 138.42 | 0.0218 | -0.7478 |
| gaussian_null | adaptive_cover | 0.5 | local_t_bonferroni | 192 | 5/192 (2.6%) | 1.1%–6.0% | 138.42 | 0.0218 | -0.7478 |
| gaussian_null | adaptive_cover | 0.5 | nominal_z | 192 | 11/192 (5.7%) | 3.2%–10.0% | 138.42 | 0.0218 | -0.7478 |
| gaussian_null | adaptive_cover | 0.75 | conditional_sign_e | 192 | 3/192 (1.6%) | 0.5%–4.5% | 142.56 | 0.0317 | -0.7152 |
| gaussian_null | adaptive_cover | 0.75 | local_t_bonferroni | 192 | 8/192 (4.2%) | 2.1%–8.0% | 142.56 | 0.0317 | -0.7152 |
| gaussian_null | adaptive_cover | 0.75 | nominal_z | 192 | 11/192 (5.7%) | 3.2%–10.0% | 142.56 | 0.0317 | -0.7152 |
| gaussian_null | max_gap | 0.0 | conditional_sign_e | 192 | not monitored | NA | 144.00 | 0.0159 | -0.7611 |
| gaussian_null | max_gap | 0.0 | local_t_bonferroni | 192 | not monitored | NA | 144.00 | 0.0159 | -0.7611 |
| gaussian_null | max_gap | 0.0 | nominal_z | 192 | not monitored | NA | 144.00 | 0.0159 | -0.7611 |
| gaussian_null | max_gap | 0.25 | conditional_sign_e | 192 | 0/192 (0.0%) | 0.0%–2.0% | 133.50 | 0.0180 | -0.7575 |
| gaussian_null | max_gap | 0.25 | local_t_bonferroni | 192 | 5/192 (2.6%) | 1.1%–6.0% | 133.50 | 0.0180 | -0.7575 |
| gaussian_null | max_gap | 0.25 | nominal_z | 192 | 9/192 (4.7%) | 2.5%–8.7% | 133.50 | 0.0180 | -0.7575 |
| gaussian_null | max_gap | 0.5 | conditional_sign_e | 192 | 3/192 (1.6%) | 0.5%–4.5% | 138.75 | 0.0218 | -0.7478 |
| gaussian_null | max_gap | 0.5 | local_t_bonferroni | 192 | 8/192 (4.2%) | 2.1%–8.0% | 138.75 | 0.0218 | -0.7478 |
| gaussian_null | max_gap | 0.5 | nominal_z | 192 | 11/192 (5.7%) | 3.2%–10.0% | 138.75 | 0.0218 | -0.7478 |
| gaussian_null | max_gap | 0.75 | conditional_sign_e | 192 | 3/192 (1.6%) | 0.5%–4.5% | 142.88 | 0.0317 | -0.7152 |
| gaussian_null | max_gap | 0.75 | local_t_bonferroni | 192 | 9/192 (4.7%) | 2.5%–8.7% | 142.88 | 0.0317 | -0.7152 |
| gaussian_null | max_gap | 0.75 | nominal_z | 192 | 12/192 (6.2%) | 3.6%–10.6% | 142.88 | 0.0317 | -0.7152 |
| hetero_null | adaptive_cover | 0.25 | conditional_sign_e | 192 | 0/192 (0.0%) | 0.0%–2.0% | 133.50 | 0.0229 | -0.5267 |
| hetero_null | adaptive_cover | 0.25 | local_t_bonferroni | 192 | 3/192 (1.6%) | 0.5%–4.5% | 133.50 | 0.0229 | -0.5267 |
| hetero_null | adaptive_cover | 0.25 | nominal_z | 192 | 5/192 (2.6%) | 1.1%–6.0% | 133.50 | 0.0229 | -0.5267 |
| hetero_null | adaptive_cover | 0.5 | conditional_sign_e | 192 | 1/192 (0.5%) | 0.1%–2.9% | 138.34 | 0.0289 | -0.5109 |
| hetero_null | adaptive_cover | 0.5 | local_t_bonferroni | 192 | 5/192 (2.6%) | 1.1%–6.0% | 138.34 | 0.0289 | -0.5109 |
| hetero_null | adaptive_cover | 0.5 | nominal_z | 192 | 57/192 (29.7%) | 23.7%–36.5% | 138.34 | 0.0289 | -0.5109 |
| hetero_null | adaptive_cover | 0.75 | conditional_sign_e | 192 | 2/192 (1.0%) | 0.3%–3.7% | 142.37 | 0.0407 | -0.4649 |
| hetero_null | adaptive_cover | 0.75 | local_t_bonferroni | 192 | 7/192 (3.6%) | 1.8%–7.3% | 142.37 | 0.0407 | -0.4649 |
| hetero_null | adaptive_cover | 0.75 | nominal_z | 192 | 67/192 (34.9%) | 28.5%–41.9% | 142.37 | 0.0407 | -0.4649 |
| hetero_null | max_gap | 0.0 | conditional_sign_e | 192 | not monitored | NA | 144.00 | 0.0195 | -0.5320 |
| hetero_null | max_gap | 0.0 | local_t_bonferroni | 192 | not monitored | NA | 144.00 | 0.0195 | -0.5320 |
| hetero_null | max_gap | 0.0 | nominal_z | 192 | not monitored | NA | 144.00 | 0.0195 | -0.5320 |
| hetero_null | max_gap | 0.25 | conditional_sign_e | 192 | 0/192 (0.0%) | 0.0%–2.0% | 133.50 | 0.0229 | -0.5267 |
| hetero_null | max_gap | 0.25 | local_t_bonferroni | 192 | 3/192 (1.6%) | 0.5%–4.5% | 133.50 | 0.0229 | -0.5267 |
| hetero_null | max_gap | 0.25 | nominal_z | 192 | 5/192 (2.6%) | 1.1%–6.0% | 133.50 | 0.0229 | -0.5267 |
| hetero_null | max_gap | 0.5 | conditional_sign_e | 192 | 2/192 (1.0%) | 0.3%–3.7% | 138.75 | 0.0289 | -0.5109 |
| hetero_null | max_gap | 0.5 | local_t_bonferroni | 192 | 6/192 (3.1%) | 1.4%–6.6% | 138.75 | 0.0289 | -0.5109 |
| hetero_null | max_gap | 0.5 | nominal_z | 192 | 57/192 (29.7%) | 23.7%–36.5% | 138.75 | 0.0289 | -0.5109 |
| hetero_null | max_gap | 0.75 | conditional_sign_e | 192 | 3/192 (1.6%) | 0.5%–4.5% | 142.88 | 0.0407 | -0.4649 |
| hetero_null | max_gap | 0.75 | local_t_bonferroni | 192 | 5/192 (2.6%) | 1.1%–6.0% | 142.88 | 0.0407 | -0.4649 |
| hetero_null | max_gap | 0.75 | nominal_z | 192 | 55/192 (28.6%) | 22.7%–35.4% | 142.88 | 0.0407 | -0.4649 |
| narrow_mean | adaptive_cover | 0.25 | conditional_sign_e | 64 | 0/64 (0.0%) | 0.0%–5.7% | 133.50 | 0.1302 | -0.3569 |
| narrow_mean | adaptive_cover | 0.25 | local_t_bonferroni | 64 | 13/64 (20.3%) | 12.3%–31.7% | 133.50 | 0.1302 | -0.3569 |
| narrow_mean | adaptive_cover | 0.25 | nominal_z | 64 | 13/64 (20.3%) | 12.3%–31.7% | 133.50 | 0.1302 | -0.3569 |
| narrow_mean | adaptive_cover | 0.5 | conditional_sign_e | 64 | 12/64 (18.8%) | 11.1%–30.0% | 138.41 | 0.1310 | -0.3485 |
| narrow_mean | adaptive_cover | 0.5 | local_t_bonferroni | 64 | 23/64 (35.9%) | 25.3%–48.2% | 138.41 | 0.1310 | -0.3485 |
| narrow_mean | adaptive_cover | 0.5 | nominal_z | 64 | 25/64 (39.1%) | 28.1%–51.3% | 138.41 | 0.1310 | -0.3485 |
| narrow_mean | adaptive_cover | 0.75 | conditional_sign_e | 64 | 22/64 (34.4%) | 23.9%–46.6% | 142.32 | 0.1361 | -0.3093 |
| narrow_mean | adaptive_cover | 0.75 | local_t_bonferroni | 64 | 35/64 (54.7%) | 42.6%–66.3% | 142.32 | 0.1361 | -0.3093 |
| narrow_mean | adaptive_cover | 0.75 | nominal_z | 64 | 41/64 (64.1%) | 51.8%–74.7% | 142.32 | 0.1361 | -0.3093 |
| narrow_mean | max_gap | 0.0 | conditional_sign_e | 64 | not monitored | NA | 144.00 | 0.1297 | -0.3622 |
| narrow_mean | max_gap | 0.0 | local_t_bonferroni | 64 | not monitored | NA | 144.00 | 0.1297 | -0.3622 |
| narrow_mean | max_gap | 0.0 | nominal_z | 64 | not monitored | NA | 144.00 | 0.1297 | -0.3622 |
| narrow_mean | max_gap | 0.25 | conditional_sign_e | 64 | 0/64 (0.0%) | 0.0%–5.7% | 133.50 | 0.1302 | -0.3569 |
| narrow_mean | max_gap | 0.25 | local_t_bonferroni | 64 | 13/64 (20.3%) | 12.3%–31.7% | 133.50 | 0.1302 | -0.3569 |
| narrow_mean | max_gap | 0.25 | nominal_z | 64 | 13/64 (20.3%) | 12.3%–31.7% | 133.50 | 0.1302 | -0.3569 |
| narrow_mean | max_gap | 0.5 | conditional_sign_e | 64 | 1/64 (1.6%) | 0.3%–8.3% | 138.75 | 0.1310 | -0.3485 |
| narrow_mean | max_gap | 0.5 | local_t_bonferroni | 64 | 30/64 (46.9%) | 35.2%–58.9% | 138.75 | 0.1310 | -0.3485 |
| narrow_mean | max_gap | 0.5 | nominal_z | 64 | 39/64 (60.9%) | 48.7%–71.9% | 138.75 | 0.1310 | -0.3485 |
| narrow_mean | max_gap | 0.75 | conditional_sign_e | 64 | 6/64 (9.4%) | 4.4%–19.0% | 142.88 | 0.1361 | -0.3093 |
| narrow_mean | max_gap | 0.75 | local_t_bonferroni | 64 | 42/64 (65.6%) | 53.4%–76.1% | 142.88 | 0.1361 | -0.3093 |
| narrow_mean | max_gap | 0.75 | nominal_z | 64 | 57/64 (89.1%) | 79.1%–94.6% | 142.88 | 0.1361 | -0.3093 |
| skew_mean_null | adaptive_cover | 0.25 | conditional_sign_e | 64 | 0/64 (0.0%) | 0.0%–5.7% | 133.50 | 0.0458 | 0.1744 |
| skew_mean_null | adaptive_cover | 0.25 | local_t_bonferroni | 64 | 4/64 (6.2%) | 2.5%–15.0% | 133.50 | 0.0458 | 0.1744 |
| skew_mean_null | adaptive_cover | 0.25 | nominal_z | 64 | 15/64 (23.4%) | 14.7%–35.1% | 133.50 | 0.0458 | 0.1744 |
| skew_mean_null | adaptive_cover | 0.5 | conditional_sign_e | 64 | 3/64 (4.7%) | 1.6%–12.9% | 138.41 | 0.0603 | 0.1983 |
| skew_mean_null | adaptive_cover | 0.5 | local_t_bonferroni | 64 | 6/64 (9.4%) | 4.4%–19.0% | 138.41 | 0.0603 | 0.1983 |
| skew_mean_null | adaptive_cover | 0.5 | nominal_z | 64 | 23/64 (35.9%) | 25.3%–48.2% | 138.41 | 0.0603 | 0.1983 |
| skew_mean_null | adaptive_cover | 0.75 | conditional_sign_e | 64 | 8/64 (12.5%) | 6.5%–22.8% | 142.55 | 0.0813 | 0.2251 |
| skew_mean_null | adaptive_cover | 0.75 | local_t_bonferroni | 64 | 11/64 (17.2%) | 9.9%–28.2% | 142.55 | 0.0813 | 0.2251 |
| skew_mean_null | adaptive_cover | 0.75 | nominal_z | 64 | 28/64 (43.8%) | 32.3%–55.9% | 142.55 | 0.0813 | 0.2251 |
| skew_mean_null | max_gap | 0.0 | conditional_sign_e | 64 | not monitored | NA | 144.00 | 0.0390 | 0.1657 |
| skew_mean_null | max_gap | 0.0 | local_t_bonferroni | 64 | not monitored | NA | 144.00 | 0.0390 | 0.1657 |
| skew_mean_null | max_gap | 0.0 | nominal_z | 64 | not monitored | NA | 144.00 | 0.0390 | 0.1657 |
| skew_mean_null | max_gap | 0.25 | conditional_sign_e | 64 | 0/64 (0.0%) | 0.0%–5.7% | 133.50 | 0.0458 | 0.1744 |
| skew_mean_null | max_gap | 0.25 | local_t_bonferroni | 64 | 4/64 (6.2%) | 2.5%–15.0% | 133.50 | 0.0458 | 0.1744 |
| skew_mean_null | max_gap | 0.25 | nominal_z | 64 | 15/64 (23.4%) | 14.7%–35.1% | 133.50 | 0.0458 | 0.1744 |
| skew_mean_null | max_gap | 0.5 | conditional_sign_e | 64 | 2/64 (3.1%) | 0.9%–10.7% | 138.75 | 0.0603 | 0.1983 |
| skew_mean_null | max_gap | 0.5 | local_t_bonferroni | 64 | 8/64 (12.5%) | 6.5%–22.8% | 138.75 | 0.0603 | 0.1983 |
| skew_mean_null | max_gap | 0.5 | nominal_z | 64 | 27/64 (42.2%) | 30.9%–54.4% | 138.75 | 0.0603 | 0.1983 |
| skew_mean_null | max_gap | 0.75 | conditional_sign_e | 64 | 6/64 (9.4%) | 4.4%–19.0% | 142.88 | 0.0813 | 0.2251 |
| skew_mean_null | max_gap | 0.75 | local_t_bonferroni | 64 | 12/64 (18.8%) | 11.1%–30.0% | 142.88 | 0.0813 | 0.2251 |
| skew_mean_null | max_gap | 0.75 | nominal_z | 64 | 29/64 (45.3%) | 33.7%–57.4% | 142.88 | 0.0813 | 0.2251 |
| symmetric_t3_null | adaptive_cover | 0.25 | conditional_sign_e | 192 | 2/192 (1.0%) | 0.3%–3.7% | 133.50 | 0.0164 | -0.7633 |
| symmetric_t3_null | adaptive_cover | 0.25 | local_t_bonferroni | 192 | 4/192 (2.1%) | 0.8%–5.2% | 133.50 | 0.0164 | -0.7633 |
| symmetric_t3_null | adaptive_cover | 0.25 | nominal_z | 192 | 5/192 (2.6%) | 1.1%–6.0% | 133.50 | 0.0164 | -0.7633 |
| symmetric_t3_null | adaptive_cover | 0.5 | conditional_sign_e | 192 | 3/192 (1.6%) | 0.5%–4.5% | 138.43 | 0.0212 | -0.7322 |
| symmetric_t3_null | adaptive_cover | 0.5 | local_t_bonferroni | 192 | 4/192 (2.1%) | 0.8%–5.2% | 138.43 | 0.0212 | -0.7322 |
| symmetric_t3_null | adaptive_cover | 0.5 | nominal_z | 192 | 10/192 (5.2%) | 2.9%–9.3% | 138.43 | 0.0212 | -0.7322 |
| symmetric_t3_null | adaptive_cover | 0.75 | conditional_sign_e | 192 | 5/192 (2.6%) | 1.1%–6.0% | 142.58 | 0.0291 | -0.6624 |
| symmetric_t3_null | adaptive_cover | 0.75 | local_t_bonferroni | 192 | 6/192 (3.1%) | 1.4%–6.6% | 142.58 | 0.0291 | -0.6624 |
| symmetric_t3_null | adaptive_cover | 0.75 | nominal_z | 192 | 19/192 (9.9%) | 6.4%–14.9% | 142.58 | 0.0291 | -0.6624 |
| symmetric_t3_null | max_gap | 0.0 | conditional_sign_e | 192 | not monitored | NA | 144.00 | 0.0142 | -0.7708 |
| symmetric_t3_null | max_gap | 0.0 | local_t_bonferroni | 192 | not monitored | NA | 144.00 | 0.0142 | -0.7708 |
| symmetric_t3_null | max_gap | 0.0 | nominal_z | 192 | not monitored | NA | 144.00 | 0.0142 | -0.7708 |
| symmetric_t3_null | max_gap | 0.25 | conditional_sign_e | 192 | 2/192 (1.0%) | 0.3%–3.7% | 133.50 | 0.0164 | -0.7633 |
| symmetric_t3_null | max_gap | 0.25 | local_t_bonferroni | 192 | 4/192 (2.1%) | 0.8%–5.2% | 133.50 | 0.0164 | -0.7633 |
| symmetric_t3_null | max_gap | 0.25 | nominal_z | 192 | 5/192 (2.6%) | 1.1%–6.0% | 133.50 | 0.0164 | -0.7633 |
| symmetric_t3_null | max_gap | 0.5 | conditional_sign_e | 192 | 4/192 (2.1%) | 0.8%–5.2% | 138.75 | 0.0212 | -0.7322 |
| symmetric_t3_null | max_gap | 0.5 | local_t_bonferroni | 192 | 4/192 (2.1%) | 0.8%–5.2% | 138.75 | 0.0212 | -0.7322 |
| symmetric_t3_null | max_gap | 0.5 | nominal_z | 192 | 6/192 (3.1%) | 1.4%–6.6% | 138.75 | 0.0212 | -0.7322 |
| symmetric_t3_null | max_gap | 0.75 | conditional_sign_e | 192 | 4/192 (2.1%) | 0.8%–5.2% | 142.88 | 0.0291 | -0.6624 |
| symmetric_t3_null | max_gap | 0.75 | local_t_bonferroni | 192 | 5/192 (2.6%) | 1.1%–6.0% | 142.88 | 0.0291 | -0.6624 |
| symmetric_t3_null | max_gap | 0.75 | nominal_z | 192 | 9/192 (4.7%) | 2.5%–8.7% | 142.88 | 0.0291 | -0.6624 |
| weak_narrow | adaptive_cover | 0.25 | conditional_sign_e | 64 | 0/64 (0.0%) | 0.0%–5.7% | 133.50 | 0.0464 | -0.7264 |
| weak_narrow | adaptive_cover | 0.25 | local_t_bonferroni | 64 | 3/64 (4.7%) | 1.6%–12.9% | 133.50 | 0.0464 | -0.7264 |
| weak_narrow | adaptive_cover | 0.25 | nominal_z | 64 | 6/64 (9.4%) | 4.4%–19.0% | 133.50 | 0.0464 | -0.7264 |
| weak_narrow | adaptive_cover | 0.5 | conditional_sign_e | 64 | 3/64 (4.7%) | 1.6%–12.9% | 138.41 | 0.0485 | -0.7188 |
| weak_narrow | adaptive_cover | 0.5 | local_t_bonferroni | 64 | 8/64 (12.5%) | 6.5%–22.8% | 138.41 | 0.0485 | -0.7188 |
| weak_narrow | adaptive_cover | 0.5 | nominal_z | 64 | 9/64 (14.1%) | 7.6%–24.6% | 138.41 | 0.0485 | -0.7188 |
| weak_narrow | adaptive_cover | 0.75 | conditional_sign_e | 64 | 12/64 (18.8%) | 11.1%–30.0% | 142.36 | 0.0541 | -0.6756 |
| weak_narrow | adaptive_cover | 0.75 | local_t_bonferroni | 64 | 14/64 (21.9%) | 13.5%–33.4% | 142.36 | 0.0541 | -0.6756 |
| weak_narrow | adaptive_cover | 0.75 | nominal_z | 64 | 17/64 (26.6%) | 17.3%–38.5% | 142.36 | 0.0541 | -0.6756 |
| weak_narrow | max_gap | 0.0 | conditional_sign_e | 64 | not monitored | NA | 144.00 | 0.0457 | -0.7300 |
| weak_narrow | max_gap | 0.0 | local_t_bonferroni | 64 | not monitored | NA | 144.00 | 0.0457 | -0.7300 |
| weak_narrow | max_gap | 0.0 | nominal_z | 64 | not monitored | NA | 144.00 | 0.0457 | -0.7300 |
| weak_narrow | max_gap | 0.25 | conditional_sign_e | 64 | 0/64 (0.0%) | 0.0%–5.7% | 133.50 | 0.0464 | -0.7264 |
| weak_narrow | max_gap | 0.25 | local_t_bonferroni | 64 | 3/64 (4.7%) | 1.6%–12.9% | 133.50 | 0.0464 | -0.7264 |
| weak_narrow | max_gap | 0.25 | nominal_z | 64 | 6/64 (9.4%) | 4.4%–19.0% | 133.50 | 0.0464 | -0.7264 |
| weak_narrow | max_gap | 0.5 | conditional_sign_e | 64 | 0/64 (0.0%) | 0.0%–5.7% | 138.75 | 0.0485 | -0.7188 |
| weak_narrow | max_gap | 0.5 | local_t_bonferroni | 64 | 4/64 (6.2%) | 2.5%–15.0% | 138.75 | 0.0485 | -0.7188 |
| weak_narrow | max_gap | 0.5 | nominal_z | 64 | 7/64 (10.9%) | 5.4%–20.9% | 138.75 | 0.0485 | -0.7188 |
| weak_narrow | max_gap | 0.75 | conditional_sign_e | 64 | 0/64 (0.0%) | 0.0%–5.7% | 142.88 | 0.0541 | -0.6756 |
| weak_narrow | max_gap | 0.75 | local_t_bonferroni | 64 | 8/64 (12.5%) | 6.5%–22.8% | 142.88 | 0.0541 | -0.6756 |
| weak_narrow | max_gap | 0.75 | nominal_z | 64 | 15/64 (23.4%) | 14.7%–35.1% | 142.88 | 0.0541 | -0.6756 |
## I
| Scenario | Repeats | Estimator | Runs | RMSE | NLL | Latent coverage | Observation coverage | Observation width |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| combined | 2 | difference_logvar_base | 32 | 0.1850 | -0.1020 | 0.2600 | 0.8414 | 0.5852 |
| combined | 2 | difference_logvar_plus | 32 | 0.0358 | -0.5877 | 0.9468 | 0.9344 | 0.5924 |
| combined | 2 | plus_bootstrap | 32 | 0.0370 | -0.6054 | 0.9201 | 0.9552 | 0.6688 |
| combined | 2 | pooled_base | 32 | 0.1321 | -0.2023 | 0.3908 | 0.9556 | 0.7959 |
| combined | 2 | residual_logvar_base | 32 | 0.1427 | -0.2821 | 0.3526 | 0.9518 | 0.7431 |
| combined | 4 | difference_logvar_base | 32 | 0.1792 | -0.1830 | 0.2650 | 0.8657 | 0.6243 |
| combined | 4 | difference_logvar_plus | 32 | 0.0413 | -0.6240 | 0.9676 | 0.9583 | 0.6311 |
| combined | 4 | plus_bootstrap | 32 | 0.0412 | -0.6296 | 0.9279 | 0.9660 | 0.6722 |
| combined | 4 | pooled_base | 32 | 0.1343 | -0.1952 | 0.3920 | 0.9583 | 0.8499 |
| combined | 4 | residual_logvar_base | 32 | 0.1459 | -0.2928 | 0.3654 | 0.9610 | 0.7907 |
| combined | 6 | difference_logvar_base | 32 | 0.1754 | -0.1206 | 0.2361 | 0.8156 | 0.5550 |
| combined | 6 | difference_logvar_plus | 32 | 0.0444 | -0.6549 | 0.9136 | 0.9448 | 0.5605 |
| combined | 6 | plus_bootstrap | 32 | 0.0444 | -0.6571 | 0.8873 | 0.9552 | 0.5885 |
| combined | 6 | pooled_base | 32 | 0.1370 | -0.1923 | 0.3719 | 0.9545 | 0.8296 |
| combined | 6 | residual_logvar_base | 32 | 0.1439 | -0.2696 | 0.3515 | 0.9618 | 0.7825 |
| contamination | 2 | difference_logvar_base | 32 | 0.0608 | 0.6478 | 0.7843 | 0.8935 | 0.6597 |
| contamination | 2 | difference_logvar_plus | 32 | 0.0670 | 0.6404 | 0.8025 | 0.8943 | 0.6669 |
| contamination | 2 | plus_bootstrap | 32 | 0.0689 | 0.0380 | 0.7724 | 0.9124 | 0.7400 |
| contamination | 2 | pooled_base | 32 | 0.0634 | 0.1919 | 0.9387 | 0.9402 | 0.9604 |
| contamination | 2 | residual_logvar_base | 32 | 0.0619 | 0.5478 | 0.8156 | 0.9016 | 0.6470 |
| contamination | 4 | difference_logvar_base | 32 | 0.0573 | 0.8834 | 0.8862 | 0.9043 | 0.7360 |
| contamination | 4 | difference_logvar_plus | 32 | 0.0669 | 0.8630 | 0.8515 | 0.9020 | 0.7432 |
| contamination | 4 | plus_bootstrap | 32 | 0.0677 | 0.2040 | 0.8264 | 0.9117 | 0.7992 |
| contamination | 4 | pooled_base | 32 | 0.0602 | 0.2911 | 0.9622 | 0.9313 | 0.9928 |
| contamination | 4 | residual_logvar_base | 32 | 0.0577 | 0.6324 | 0.8908 | 0.9059 | 0.7198 |
| contamination | 6 | difference_logvar_base | 32 | 0.0476 | 0.7169 | 0.8916 | 0.9086 | 0.6879 |
| contamination | 6 | difference_logvar_plus | 32 | 0.0566 | 0.7127 | 0.8669 | 0.9082 | 0.6941 |
| contamination | 6 | plus_bootstrap | 32 | 0.0569 | 0.1575 | 0.8484 | 0.9159 | 0.7356 |
| contamination | 6 | pooled_base | 32 | 0.0490 | 0.1451 | 0.9425 | 0.9371 | 0.8603 |
| contamination | 6 | residual_logvar_base | 32 | 0.0475 | 0.4689 | 0.8904 | 0.9128 | 0.6883 |
| heteroscedastic | 2 | difference_logvar_base | 32 | 0.0298 | -0.6507 | 0.9525 | 0.9290 | 0.5404 |
| heteroscedastic | 2 | difference_logvar_plus | 32 | 0.0375 | -0.6444 | 0.9390 | 0.9294 | 0.5470 |
| heteroscedastic | 2 | plus_bootstrap | 32 | 0.0392 | -0.6652 | 0.9167 | 0.9483 | 0.6131 |
| heteroscedastic | 2 | pooled_base | 32 | 0.0336 | -0.5065 | 0.9248 | 0.9306 | 0.5716 |
| heteroscedastic | 2 | residual_logvar_base | 32 | 0.0292 | -0.7191 | 0.9552 | 0.9417 | 0.5272 |
| heteroscedastic | 4 | difference_logvar_base | 32 | 0.0300 | -0.7202 | 0.9765 | 0.9514 | 0.5528 |
| heteroscedastic | 4 | difference_logvar_plus | 32 | 0.0382 | -0.7115 | 0.9668 | 0.9506 | 0.5588 |
| heteroscedastic | 4 | plus_bootstrap | 32 | 0.0387 | -0.7123 | 0.9487 | 0.9595 | 0.5969 |
| heteroscedastic | 4 | pooled_base | 32 | 0.0357 | -0.4904 | 0.9529 | 0.9425 | 0.6103 |
| heteroscedastic | 4 | residual_logvar_base | 32 | 0.0295 | -0.7309 | 0.9664 | 0.9452 | 0.5306 |
| heteroscedastic | 6 | difference_logvar_base | 32 | 0.0321 | -0.6932 | 0.9479 | 0.9344 | 0.5188 |
| heteroscedastic | 6 | difference_logvar_plus | 32 | 0.0333 | -0.6861 | 0.9390 | 0.9348 | 0.5240 |
| heteroscedastic | 6 | plus_bootstrap | 32 | 0.0339 | -0.7039 | 0.9209 | 0.9464 | 0.5475 |
| heteroscedastic | 6 | pooled_base | 32 | 0.0307 | -0.4879 | 0.9541 | 0.9352 | 0.5748 |
| heteroscedastic | 6 | residual_logvar_base | 32 | 0.0302 | -0.7180 | 0.9502 | 0.9340 | 0.4834 |
| local_missing | 2 | difference_logvar_base | 32 | 0.1106 | 0.0172 | 0.4622 | 0.8283 | 0.4620 |
| local_missing | 2 | difference_logvar_plus | 32 | 0.1067 | -0.0138 | 0.5370 | 0.8283 | 0.4670 |
| local_missing | 2 | plus_bootstrap | 32 | 0.1068 | -0.2143 | 0.5278 | 0.8611 | 0.5273 |
| local_missing | 2 | pooled_base | 32 | 0.1097 | -0.3922 | 0.6200 | 0.9387 | 0.6151 |
| local_missing | 2 | residual_logvar_base | 32 | 0.1103 | -0.3517 | 0.5374 | 0.8997 | 0.5346 |
| local_missing | 4 | difference_logvar_base | 32 | 0.1089 | -0.0607 | 0.4919 | 0.8291 | 0.4594 |
| local_missing | 4 | difference_logvar_plus | 32 | 0.1052 | -0.0986 | 0.5540 | 0.8310 | 0.4638 |
| local_missing | 4 | plus_bootstrap | 32 | 0.1053 | -0.2267 | 0.5463 | 0.8542 | 0.4976 |
| local_missing | 4 | pooled_base | 32 | 0.1084 | -0.3798 | 0.6354 | 0.9352 | 0.6305 |
| local_missing | 4 | residual_logvar_base | 32 | 0.1086 | -0.3329 | 0.5810 | 0.8916 | 0.5378 |
| local_missing | 6 | difference_logvar_base | 32 | 0.1122 | -0.2012 | 0.5231 | 0.8600 | 0.4756 |
| local_missing | 6 | difference_logvar_plus | 32 | 0.1100 | -0.2230 | 0.6088 | 0.8526 | 0.4798 |
| local_missing | 6 | plus_bootstrap | 32 | 0.1100 | -0.2996 | 0.5783 | 0.8711 | 0.5115 |
| local_missing | 6 | pooled_base | 32 | 0.1119 | -0.3130 | 0.6181 | 0.9174 | 0.5918 |
| local_missing | 6 | residual_logvar_base | 32 | 0.1122 | -0.2882 | 0.5737 | 0.8954 | 0.5367 |
| mean_missing | 2 | difference_logvar_base | 32 | 0.1404 | -0.0552 | 0.2338 | 0.8256 | 0.4951 |
| mean_missing | 2 | difference_logvar_plus | 32 | 0.0328 | -0.6014 | 0.9198 | 0.9309 | 0.5005 |
| mean_missing | 2 | plus_bootstrap | 32 | 0.0337 | -0.6380 | 0.9101 | 0.9514 | 0.5634 |
| mean_missing | 2 | pooled_base | 32 | 0.1312 | -0.3438 | 0.3391 | 0.9641 | 0.6994 |
| mean_missing | 2 | residual_logvar_base | 32 | 0.1325 | -0.3367 | 0.3434 | 0.9606 | 0.7030 |
| mean_missing | 4 | difference_logvar_base | 32 | 0.1361 | -0.1173 | 0.2234 | 0.8198 | 0.4921 |
| mean_missing | 4 | difference_logvar_plus | 32 | 0.0270 | -0.6458 | 0.9572 | 0.9394 | 0.4968 |
| mean_missing | 4 | plus_bootstrap | 32 | 0.0277 | -0.6640 | 0.9417 | 0.9572 | 0.5396 |
| mean_missing | 4 | pooled_base | 32 | 0.1293 | -0.3452 | 0.3256 | 0.9688 | 0.7070 |
| mean_missing | 4 | residual_logvar_base | 32 | 0.1306 | -0.3436 | 0.3171 | 0.9595 | 0.6869 |
| mean_missing | 6 | difference_logvar_base | 32 | 0.1345 | 0.0598 | 0.1964 | 0.7793 | 0.4512 |
| mean_missing | 6 | difference_logvar_plus | 32 | 0.0290 | -0.6210 | 0.9336 | 0.9190 | 0.4553 |
| mean_missing | 6 | plus_bootstrap | 32 | 0.0295 | -0.6504 | 0.9174 | 0.9336 | 0.4833 |
| mean_missing | 6 | pooled_base | 32 | 0.1316 | -0.3284 | 0.3252 | 0.9695 | 0.7220 |
| mean_missing | 6 | residual_logvar_base | 32 | 0.1321 | -0.3297 | 0.3221 | 0.9660 | 0.7106 |
| normal | 2 | difference_logvar_base | 32 | 0.0300 | -0.5756 | 0.9005 | 0.9074 | 0.4666 |
| normal | 2 | difference_logvar_plus | 32 | 0.0324 | -0.5734 | 0.9035 | 0.9043 | 0.4716 |
| normal | 2 | plus_bootstrap | 32 | 0.0323 | -0.6261 | 0.8993 | 0.9329 | 0.5282 |
| normal | 2 | pooled_base | 32 | 0.0289 | -0.7103 | 0.9468 | 0.9444 | 0.4624 |
| normal | 2 | residual_logvar_base | 32 | 0.0294 | -0.6806 | 0.9363 | 0.9317 | 0.4618 |
| normal | 4 | difference_logvar_base | 32 | 0.0264 | -0.6606 | 0.9456 | 0.9344 | 0.4905 |
| normal | 4 | difference_logvar_plus | 32 | 0.0312 | -0.6457 | 0.9329 | 0.9356 | 0.4951 |
| normal | 4 | plus_bootstrap | 32 | 0.0313 | -0.6598 | 0.9255 | 0.9514 | 0.5322 |
| normal | 4 | pooled_base | 32 | 0.0251 | -0.7077 | 0.9603 | 0.9468 | 0.4741 |
| normal | 4 | residual_logvar_base | 32 | 0.0258 | -0.7026 | 0.9545 | 0.9402 | 0.4679 |
| normal | 6 | difference_logvar_base | 32 | 0.0264 | -0.6735 | 0.9444 | 0.9410 | 0.4808 |
| normal | 6 | difference_logvar_plus | 32 | 0.0309 | -0.6617 | 0.9290 | 0.9406 | 0.4852 |
| normal | 6 | plus_bootstrap | 32 | 0.0309 | -0.6738 | 0.9198 | 0.9525 | 0.5123 |
| normal | 6 | pooled_base | 32 | 0.0258 | -0.7130 | 0.9622 | 0.9433 | 0.4713 |
| normal | 6 | residual_logvar_base | 32 | 0.0262 | -0.7049 | 0.9518 | 0.9402 | 0.4649 |
| shared_batch | 2 | difference_logvar_base | 32 | 0.0607 | 1.6946 | 0.5459 | 0.6578 | 0.4469 |
| shared_batch | 2 | difference_logvar_plus | 32 | 0.0768 | 1.7499 | 0.5390 | 0.6539 | 0.4518 |
| shared_batch | 2 | plus_bootstrap | 32 | 0.0770 | 0.6889 | 0.5258 | 0.6983 | 0.5041 |
| shared_batch | 2 | pooled_base | 32 | 0.0595 | -0.0583 | 0.8765 | 0.9255 | 0.8378 |
| shared_batch | 2 | residual_logvar_base | 32 | 0.0596 | 0.0304 | 0.8488 | 0.9035 | 0.7860 |
| shared_batch | 4 | difference_logvar_base | 32 | 0.0870 | 1.2162 | 0.4664 | 0.6667 | 0.4573 |
| shared_batch | 4 | difference_logvar_plus | 32 | 0.1017 | 1.3229 | 0.4579 | 0.6497 | 0.4617 |
| shared_batch | 4 | plus_bootstrap | 32 | 0.1016 | 0.7444 | 0.4309 | 0.6802 | 0.4939 |
| shared_batch | 4 | pooled_base | 32 | 0.0863 | 0.0899 | 0.6416 | 0.8654 | 0.7175 |
| shared_batch | 4 | residual_logvar_base | 32 | 0.0859 | 0.2439 | 0.5822 | 0.8194 | 0.6466 |
| shared_batch | 6 | difference_logvar_base | 32 | 0.1013 | 1.1529 | 0.3711 | 0.6732 | 0.4760 |
| shared_batch | 6 | difference_logvar_plus | 32 | 0.1207 | 1.2834 | 0.3893 | 0.6613 | 0.4803 |
| shared_batch | 6 | plus_bootstrap | 32 | 0.1217 | 0.7861 | 0.3723 | 0.6821 | 0.5077 |
| shared_batch | 6 | pooled_base | 32 | 0.0987 | 0.2292 | 0.5363 | 0.8326 | 0.6806 |
| shared_batch | 6 | residual_logvar_base | 32 | 0.1006 | 0.4125 | 0.5050 | 0.7901 | 0.6350 |
| within_batch_drift | 2 | difference_logvar_base | 32 | 0.0266 | -0.0109 | 1.0000 | 0.9981 | 1.3409 |
| within_batch_drift | 2 | difference_logvar_plus | 32 | 0.0310 | -0.0024 | 1.0000 | 0.9981 | 1.3552 |
| within_batch_drift | 2 | plus_bootstrap | 32 | 0.0349 | 0.0091 | 1.0000 | 0.9988 | 1.5289 |
| within_batch_drift | 2 | pooled_base | 32 | 0.0266 | -0.2790 | 1.0000 | 0.9715 | 0.7498 |
| within_batch_drift | 2 | residual_logvar_base | 32 | 0.0266 | -0.2570 | 1.0000 | 0.9792 | 0.8159 |
| within_batch_drift | 4 | difference_logvar_base | 32 | 0.0245 | -0.0797 | 0.9745 | 0.8472 | 0.5554 |
| within_batch_drift | 4 | difference_logvar_plus | 32 | 0.0306 | -0.0797 | 0.9630 | 0.8499 | 0.5606 |
| within_batch_drift | 4 | plus_bootstrap | 32 | 0.0307 | -0.1363 | 0.9352 | 0.8796 | 0.6056 |
| within_batch_drift | 4 | pooled_base | 32 | 0.0243 | -0.2583 | 0.9950 | 0.9294 | 0.6353 |
| within_batch_drift | 4 | residual_logvar_base | 32 | 0.0242 | -0.2281 | 0.9977 | 0.9163 | 0.6317 |
| within_batch_drift | 6 | difference_logvar_base | 32 | 0.0266 | 0.1750 | 0.8943 | 0.7728 | 0.4781 |
| within_batch_drift | 6 | difference_logvar_plus | 32 | 0.0315 | 0.1644 | 0.9163 | 0.7735 | 0.4824 |
| within_batch_drift | 6 | plus_bootstrap | 32 | 0.0315 | 0.0296 | 0.9062 | 0.8079 | 0.5130 |
| within_batch_drift | 6 | pooled_base | 32 | 0.0270 | -0.2184 | 0.9653 | 0.9090 | 0.6032 |
| within_batch_drift | 6 | residual_logvar_base | 32 | 0.0270 | -0.1919 | 0.9626 | 0.8974 | 0.5920 |
