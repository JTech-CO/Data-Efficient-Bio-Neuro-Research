# 30. Decisions: assumption ranges and the value of independent information

[한국어](../ko/30_RESEARCH_DECISIONS.md) · [Results](29_BOUNDED_RESULTS.md) · [Previous decisions](23_RESEARCH_DECISIONS.md)

These are **post-result design decisions**, not hypotheses claimed to have been independently preregistered. Original chapters 01–24 and previous numerical modules remain unchanged.

| Question | Decision | Evidence / boundary |
|---|---|---|
| Collapse partial-identification sets to a single number? | Not by default | Set midpoints have no automatic accuracy guarantee |
| Accept calibration whenever the set is nonempty? | No | All 40 common-out-of-bounds worlds remain feasible |
| Replace every unknown-scale test with signs? | Retain as comparator | Conditional sign balance is required and narrow-effect power is low |
| Declare 75% auditing optimal? | No | Detection, training, movement cost and prediction conflict |
| Increase technical repeats to identify all noise? | No | Shared batch errors cancel in repeat differences |
| Treat bootstrap as restoring all uncertainty? | No | It propagates the assumed model, not absent mean or batch structure |

## G: external support for bias limits and value of measurements

Retain sensitivity maps over externally declared bounds instead of shrinking B to fit observed results. Compare extra technical repeats, independent calibration batches and distinct measurement operators. Repeats reduce sampling uncertainty; independent evidence may change identification uncertainty. Preserve common-bias counterexamples. Relaxing the reference-gain-equals-one assumption requires a separately designed nonlinear/linear-fractional optimization problem and calibration information, not a placeholder plugin.

**Falsification:** reject a method that frequently excludes the full true parameter under valid declared bounds, or that claims technical repeats alone shrink intervals below the noiseless identification limit. Model fit cannot certify external bounds.

## H: jointly design the target null, power and cost

The sign method targets conditional sign balance, whereas local t requires location-wise Gaussian repeats. Assign distinct null IDs to location/scale hypotheses. State the weaker conclusion or extra observations needed when allowing asymmetry, heteroscedasticity and common-mode effects simultaneously. A new localized sign-accumulation comparator must be tested on a new bank rather than tuned on this one.

**Falsification:** do not promote a method with high alarms in premise-valid null worlds, or worse detection and prediction at the same actual cost than local t/maximum-gap baselines. Preserve movement/setup accounting. Passing a control comparison does not validate the entire model.

## I: cross technical and independent-batch replication

A minimal next model is Y_ijr=m(x_i)+a_ij+epsilon_ijr, not an immediate foundation model. Distinguish within-batch technical repeats r from independent batches j. At fixed cost, cross input locations, batches and repeats. Do not label technical variance as total variance without observations that identify batch variance. Compare a base mean, a prespecified residual and selection using additional independent validation.

**Falsification:** retain the simpler model if extra variance merely hides mean misspecification, or if added structure harms error and proper scores on normal/weak-effect worlds. Bias shared by all batches remains a G-style identification issue.

## Scope and repository practice

G/H/I are separate modules and do not circularly reuse each other's evidence. This is not an integrated autonomous laboratory, real-data experiment, prospective intervention or clinical system. ODE/SINDy/PINN/BINN and foundation-model training remain outside scope. No new efficacy evaluation of augmentation, donor generalization or multifidelity was added.

The main README retains only the current release and entry points. Add historical releases to VERSIONS instead of appending old README bodies. Preserve previous documents, numbers and raw results.
