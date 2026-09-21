# Evaluation, reproduction, and stopping criteria

**Budgets and gates below are design examples, not universal published thresholds or completed results.**

## 1. Preregister the comparison

“Does it beat AI with little data?” is underspecified. A useful question is whether a workflow meets a defined error-and-coverage target for a new donor at lower real assay cost than a baseline with equal information access and tuning budget.

Report `n_independent_groups`, `n_real_measurements`, `n_new_labels`, `annotation_minutes`, `n_pretraining_examples_known`, `n_simulator_calls`, `compute_hours`, and `assay_cost` separately. Cell or EEG-window counts are not donor counts. Record unavailable pretraining size or overlap as `unknown`.

An example budget curve might use 8/16/32/64 independent experimental conditions, but do not manufacture those sample sizes in a dataset with fewer groups. Few-shot labels per class and independent individuals remain separate quantities. Adapt budgets to the available grouping structure.

## 2. Split before transforming

| Modality | Primary split unit | Additional leakage to prevent |
|---|---|---|
| Cell images | Donor / organoid / slide / imaging run | Crops, augmentations, duplicates from the same field |
| Single-cell | Donor / cell line / perturbation / batch | Cells sharing held-out interventions or donors |
| EEG | Subject / session / recording | Overlapping windows, future-dependent filtering, session statistics |
| Dynamics | Independent trajectory / initial condition / intervention | Randomly mixing nearby points of one trajectory |
| Multifidelity | Shared condition and group | Undisclosed use of held-out targets' low-fidelity partners |

Transductive evaluation or access to low-fidelity test measurements can be legitimate, but must be a separate, declared track with fair information access for baselines.

Fit scaling, feature selection, PCA, batch correction, generators, library selection, and hyperparameter searches inside training. Validation selects models; final real test data remain locked. Add an external institution, device, or date holdout where possible. Audit foundation pretraining overlap separately. [R18](../../references/BIBLIOGRAPHY.md#r18) [D01](../../references/BIBLIOGRAPHY.md#d01)

## 3. Strong, small baselines

| Comparison | Required baseline | Additional candidates |
|---|---|---|
| Scalar prediction | Constant/mean, ridge or elastic net, simple mechanistic fit | GP, trees, small NN |
| Acquisition | Random, space-filling, established experimental design | Information-driven GP AL / BO |
| Dynamics | ODE solver plus likelihood, point-derivative SINDy | Weak/ensemble SINDy, PINN, UDE |
| Transfer | Raw features plus linear head, frozen encoder plus same head | Adapters, partial fine-tuning |
| Gene perturbation | No-change, mean-response, additive/linear | Biological-feature models, selected FM |
| Augmentation | Real-only, no augmentation | Rule-based, calibrated simulator, fitted generator |
| Fidelity | High-only and low-only | Linear and nonlinear multifidelity |

Simple single-cell baselines are substantive competitors, not formalities. [R12](../../references/BIBLIOGRAPHY.md#r12) [R13](../../references/BIBLIOGRAPHY.md#r13) Disclose external information, tuning trials, early stopping, and compute. An unequal search budget confounds claims about modeling methodology.

## 4. Role-specific endpoints

| Role | Example primary endpoint | Supporting or failure endpoint |
|---|---|---|
| Collection | Real cost to reach target accuracy | Failed assays, diversity, repeated queries |
| Regression | Held-out MAE/RMSE | Group error, NLL/CRPS, extrapolation gap |
| Intervals | Empirical versus nominal coverage | Width, group undercoverage, abstention |
| Mechanism | New-intervention/initial-condition rollout | Coefficient stability, identifiability, constraint violations |
| Imaging | Object precision/recall or AP, Dice/IoU | Rare morphology, count and trajectory bias |
| Omics | Error in change from control | Per-perturbation error, effect direction, pathway consistency |
| EEG | Balanced accuracy or macro-F1 | Worst-subject results, latency, artifact dependence |
| Augmentation | Change on a real-only downstream test | Rare-mode loss, source-label shortcuts, privacy risk |

Report coverage together with width; arbitrarily wide intervals are not useful decisions. Calibration error alone does not establish epistemic uncertainty. Keep regression-interval and classification-confidence assessment separate.

Synthetic systems with known equations permit term precision/recall and equivalence tests. Real data without known governing equations do not. Report predictive stability, intervention-based falsification, and identifiability evidence instead. [R06](../../references/BIBLIOGRAPHY.md#r06)

## 5. Essential ablations

**A, acquisition:** hold the GP, initialization, noise model, and total budget fixed; change only random versus active acquisition.

**B, prior:** compare correct, partially wrong, absent, and discrepancy-corrected mechanisms. Separate known-truth synthetic tests from real-data tests.

**C, dynamics:** compare point derivatives, weak forms, ensembles, and observation-aware latent models incrementally.

**D, representation:** use the same downstream head and splits for raw/PCA, frozen foundation, and adapter representations.

**E, augmentation:** compare real-only, simple transformations, calibrated simulations, and generative augmentation with equal access to original information.

**F, fidelity:** test helpful, unrelated, and input-dependent wrong-trend sources, including cases where high-only wins. Nonlinear cross-fidelity structure is a relevant comparison. [R19](../../references/BIBLIOGRAPHY.md#r19)

When a full factorial is too costly, preregister a smaller staged design and report omitted interactions. Do not select only favorable combinations after observing outcomes.

## 6. Statistics and stopping

Use paired comparisons over multiple seeds and independent group splits. Bootstrap donors or trajectories at the intended generalization level. A cell/window bootstrap alone does not produce population-level uncertainty. With very few groups, acknowledge unstable intervals; prioritize effect sizes, all run results, and failures over precise-looking p-values.

If a target is not reached within the observed budget, report non-attainment rather than extrapolating an invented cost. Without a target effect and variance estimate, do not assert a definitive donor requirement. Estimate variability in a pilot and size the main study separately.

**Proposed gates:** baseline reproduction → leakage audit → preserved real held-out performance → acceptable coverage and width → external-condition stress test → approved prospective experiment when needed. Preregister acceptable error and cost improvement according to the downstream use. Distinguish a 95% confidence level, 95% predictive coverage, and a 95% success rate.

Stop for invalid access, unresolved overlap, unassessable bias, harmful transfer versus high-only, serious rare-group degradation, or absent safety review. Complexity is not a substitute for passing these checks.

## 7. Stage-specific deliverables

| Stage | Output | Remaining limitation |
|---|---|---|
| P0, data contract | Data card, group split, provenance, consent and version | Population representativeness |
| P1, retrospective test | Baselines, learning curves, leakage audit | Pool replay does not validate unmeasured experiments |
| P2, synthetic stress | Wrong prior, hidden state, deceptive fidelity | Simulator realism |
| P3, integrated prototype | Acquisition logs and model/equation cards | No independent prospective validation yet |
| P4, approved prospective test | New measurements, cost and errors | Generalization beyond that site and population |

This package supplies P0/P1 designs and an educational synthetic example. It does not report completion of the full P1 benchmark or P4 experiments.
