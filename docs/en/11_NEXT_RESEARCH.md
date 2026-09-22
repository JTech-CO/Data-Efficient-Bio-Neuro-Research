# 11. Next research: separate failure causes and measure diagnostic value

The original [H1–H6 agenda](06_RESEARCH_AGENDA.md) is preserved. This is a **new prospective plan** derived from [the pilot](10_PILOT_RESULTS.md), not work already implemented or proven.

## 1. Narrow the question

The pilot does not support “add audits and exploration, then improve everything.” The next question is:

> **At equal diagnostic cost, can an audit design that separates mechanism, observation-operator and noise misspecification be more useful than a simple residual alert?**

A larger neural network is not the first requirement. The clearest bottlenecks are confusing measurement errors with candidate mechanism differences and treating few audits as adequate assurance. Retain the finding that a simpler acquisition baseline performed better in the correctly specified setting.

## 2. S2a: cause-separating audit design

Propose three new probe families: a sensor-reference probe observing a known invariant input, a same-condition replicate noise probe, and an intervention probe separating candidate dynamics. Charge each probe and include initial, training and diagnostic costs in the same budget.

The current simulator has no separate reference instrument. Relabelling its B readout as “calibration” would not implement one. A probe that reveals hidden truth is not allowed. Specify what each probe can actually observe and which reference values are externally known before coding it.

Compare fixed round-robin, random, candidate-discrimination and cause-oriented information audits under identical budgets. Cross sensor-only, noise-only, dynamics-only, combined failures and no-change cases. Allow an unresolved cause when the available observations cannot distinguish explanations.

Primary metrics are false alerts, misses, cause-confusion matrices, detection delay and diagnostic cost. Evaluate predictive risk–coverage and interval width alongside them. Sequential error-control claims require their own null simulations and statistical analysis.

**Stop rule:** without cause-separating observations, do not invent attribution accuracy. When diagnostic cost is prohibitive, preserve “unknown” and restrict the prediction domain.

## 3. S2b: propagate noise inference through all four paths

Current nominal noise is fixed in fitting, acquisition, audits and evaluation. Next candidates include a readout-specific variance posterior or hierarchical variance pooling. Compare constant noise, readout-dependent noise and robust likelihoods before fitting a highly flexible heteroscedastic GP to a tiny sample.

Inflating noise until all alerts vanish is not success. Jointly report coverage, width, NLL, error and acquisition value. Record compensation between noise and missing dynamics. A true-noise oracle baseline has privileged information and must be labelled separately rather than presented as an equal-information competitor.

## 4. S2c: correction before unrestricted GP fallback

The current fallback often produced broad, inaccurate intervals. Next compare a small observation correction, a restricted ODE discrepancy, and the existing prediction-only GP on identical acquired data. If the source of the change is unidentifiable, do not claim preserved mechanistic coefficient meaning.

Do not make observation and dynamics corrections unrestricted simultaneously. Fix amplitude, dimension and regularization rules, then examine profile likelihood or posterior correlations for parameter compensation. If no useful gain appears, retain the smaller model or abstain in the affected domain.

## 5. S2d: disentangle acquisition and predictor effects

The policy comparison changes both query paths and, under alerts, the predictor. The no-gate ablation only partially separates these effects. Add a crossed evaluation that fits the same small predictor bank to each saved training ledger after acquisition. Keep audit/test roles unchanged.

Fix predictors and information access when studying acquisition. Fix queries and observations when studying model effects. A small, explicitly scoped factorial design is preferable to an undocumented selection of favorable combinations. Include simple mechanistic, ridge and GP baselines.

## 6. Conditions for returning to H3–H6

| Original hypothesis | Entry condition | Do not claim |
|---|---|---|
| H3 synthetic evidence budget | Separate provenance and real-versus-derived learning effects | Generated rows are biological units |
| H4 shared dynamics and individual variation | Add independent simulator individuals and validate hierarchical inference | Repeated observations of one world are personalization |
| H5 conditional fidelity | Define LF/HF targets, paired information, cost and validation | Renaming the reference field implements multi-fidelity learning |
| H6 adaptive intervals | Specify target distribution, feedback shift and calibration-data roles | A nominal 95% interval guarantees OOD coverage |

Add PINN/BINN/SINDy or a foundation encoder only after demonstrating a bottleneck in its intended role. Importing a library does not implement a learning and evaluation path.

## 7. Research record discipline

Freeze `pilot/` as the current raw result. Use a new experiment ID and configuration hash, such as `results/s2a-*`, for subsequent work. Retain hypotheses, anticipated failure, changed code, seed lists, outcomes and refutations. External preregistration has not occurred and should only be claimed if actually performed.

Do not tune on the 20 development seeds and present success on the same seeds as independent evidence. Separate development worlds from unseen simulator families, parameter ranges and noise processes. Choosing realistic ranges needs domain expertise; toy ranges are not biological operating ranges.

## 8. When real data become available

Start with restricted retrospective replay, not automated prospective experimentation. Establish permissions, donor/trajectory splits, instrument/batch metadata and preprocessing fit scope. Do not query an unobserved intervention as though a public dataset were a complete oracle. Specify the available query pool and selection bias.

This repository adds neither real-data ingestion nor a wet-lab executor. S2a–S2d can nevertheless proceed using synthetic falsification, diagnostic assessment and information-flow tests. The goal is to expose when the system should not be trusted before expanding its model capacity.
