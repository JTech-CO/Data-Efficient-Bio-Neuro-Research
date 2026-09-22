# 10. Executed synthetic pilot results

**2026-09-22 · 640 runs · 20 paired seeds per setting · biological units = 0**

[Implementation](09_EXECUTABLE_RESEARCH.md) · [Next research](11_NEXT_RESEARCH.md)

These are executed outputs under `research_lab/results/pilot/`, not forecasts. The pilot contains 500 main runs (5 scenarios × 5 policies × 20 seeds) and 140 ablation runs. All planned settings and seeds are retained. This is neither externally preregistered nor a biological experiment.

A seed identifies a shared synthetic world and reproducible noise conditions. The same query and role use identical noise across policies. The 640 runs are not 640 biological units. Every policy has a 24-unit cost ceiling, but actual spending can differ.

## 1. Main comparison: random and guarded information

| Scenario | Policy | ID RMSE | Obs. coverage | Width | Alert rate | Abstention | Actual cost |
|---|---|---:|---:|---:|---:|---:|---:|
| Intervention-identifiable | random | 0.0220 | 96.1% | 0.371 | 0% | 10% | 23.63 |
| Intervention-identifiable | guarded_information | 0.0104 | 95.7% | 0.348 | 0% | 0% | 23.60 |
| Observational equivalence | random | 0.0283 | 97.9% | 0.490 | 0% | 100% | 10.00 |
| Observational equivalence | guarded_information | 0.0283 | 97.9% | 0.490 | 0% | 100% | 10.00 |
| Outside candidate set | random | 0.3278 | 49.6% | 0.382 | 70% | 10% | 23.63 |
| Outside candidate set | guarded_information | 0.3487 | 97.5% | 1.992 | 95% | 95% | 23.22 |
| Sensor misspecification | random | 0.2672 | 57.5% | 0.381 | 45% | 20% | 23.63 |
| Sensor misspecification | guarded_information | 0.2564 | 66.5% | 0.781 | 25% | 25% | 23.50 |
| Noise misspecification | random | 0.0887 | 47.1% | 0.372 | 25% | 30% | 23.63 |
| Noise misspecification | guarded_information | 0.0834 | 58.1% | 0.689 | 20% | 20% | 23.53 |

Coverage refers to nominal pointwise 95% observation-predictive intervals, evaluated at the final state. Latent-function coverage and OOD results are recorded separately in JSON.

## 2. Important negative findings

**The combined policy was not best even in the correctly specified setting.** On `identifiable`, maximum latent variance had RMSE 0.0098, guarded information 0.0104, and model-only information 0.0151. Mechanism discrimination and prediction error are distinct objectives. Adding modules does not establish improvement. These are setting-specific means, not a general ranking.

**Outside-candidate truth triggered abstention without fixing prediction.** Guarded alerts and abstention occurred in 95% of runs, but RMSE 0.3487 was worse than random 0.3278. Width increased to 1.992. Coverage of 97.5% is not evidence of better accuracy. The remaining 5% still recorded an incorrect candidate preference.

**Sensor bias was often missed.** Guarded alerts occurred in only 25% of runs; incorrect candidate preferences occurred in 50% of all runs. The gate cannot attribute disagreement to sensor versus dynamics and cannot serve as a reliability certificate.

**Noise mismatch was poorly detected with roughly two audits.** The guarded alert rate was 20%, and observation coverage was 58.1%, far from nominal 95% despite intervals wider than the random baseline.

**Observational equivalence is an intended test, not a bug.** Every policy ended with weights 0.5/0.5 and withheld candidate selection. The nine-query training pool was exhausted at total cost 10. Identical final predictions reflect eventually observing the same pool; missing higher-budget values were not interpolated.

## 3. Observation and removal ablations

In the same `identifiable` world, guarded inference with the nominal operator had mean RMSE 0.0104, versus 0.1339 with an identity operator. Supplied correct observation knowledge helped in this world; calibration was not automatically discovered.

`guarded_no_gate` logged the same alerts but did not react. For `hidden_mechanism`, its alert rate was 95%, abstention 0%, and incorrect candidate preference 100%, compared with 5% under the full guard. This reduction includes the direct effect of a withholding rule; it does not demonstrate improved discovery of the true mechanism.

`guarded_no_exploration` had lower hidden-mechanism RMSE than the full guard (0.3255 versus 0.3487). The current pilot does not establish the value of its scheduled exploration term. Other simulator families and domains remain future hypotheses.

## 4. Metric limitations

`false_candidate_assertion` is an internal synthetic metric indicating a preference inconsistent with the known toy truth. It does not measure clinical harm or false claims in actual papers. `abstained` refers to mechanism preference; the predictive GP may still output numbers.

Cost-to-target is the first **observed** stage satisfying RMSE≤0.10, observation coverage≥0.90 and width≤0.60. There is no interpolation; unreached targets are null. Early chance passage followed by degradation is possible, so this is neither sustained success nor an online stopping rule. All curves are retained.

Paired bootstrap intervals use 2,000 resamples of 20 synthetic worlds. They do not establish biological or institutional generalization, adjust for multiple comparisons, or replace power calculations.

## 5. Reproduction

`research_lab/configs/pilot.json` is the executed plan, with its SHA-256 recorded in `summary.json`. `runs.jsonl` contains 640 compact runs and cost-indexed evaluations. `demos.json` holds 25 seed-0 full ledgers and selection traces. Full ledgers are not stored for every one of the 640 runs, but each is regenerable from configuration and seed. Web data are generated from recorded files, not hand-entered.

Development unit and smoke tests preceded the pilot. This is exploratory, not externally preregistered confirmatory research, and has no independent biological test set. Its purpose is to narrow the next research question from auditable failures.

```bash
python -m research_lab benchmark --out research_lab/results/new-pilot
```
