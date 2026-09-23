# 23. Decisions: distinguish calibratability, detectability, and predictability

[한국어](../ko/23_RESEARCH_DECISIONS.md) · [Completed results](22_TRIAD_RESULTS.md) · [Prior decisions](16_RESEARCH_DECISIONS.md)

**These follow-up decisions were written after inspecting v1.3 results; they are not presented as preregistered hypotheses.** Chapters 01–17 and the original agenda remain unchanged. All D/E/F workstreams were implemented and evaluated in limited synthetic settings, not integrated into a finished autonomous biological scientist.

## Current decisions

| Question | Decision | Evidence in this version | Remaining condition |
|---|---|---|---|
| Use standard addition as complete calibration recovery? | No | Rank 5/6; offset–intercept equivalence persists | Report only identified gain information |
| Do three anchors guarantee truth? | No | Common-anchor RMSE 0.5995; contradictions 5/80 | Independent anchors or externally justified bias bounds |
| Default to the orthogonal reference alone? | Withhold | Strong in many scenarios; RMSE 0.3804 under reference drift | Independently assess reference stability |
| Prefer adaptive auditing over largest-gap coverage? | Withhold | Narrow-fault alarms 46/64 versus 48/64 at equal budget | Account for complexity, weak effects, and cost |
| Treat passing three sites as domain-wide validity? | No | Narrow-fault alarms 6/64 | Display coverage and testing power separately |
| Default to Student-t everywhere? | No | Gains under contamination; worse normal-noise RMSE | Separate robustness cost from mean misspecification |
| Select acquisition solely by mean error? | No | IVR can lower RMSE while worsening NLL | Jointly inspect proper scores, coverage, width, and cost |

## Next D experiment: partial identification with fallible anchors

Current full identification depends on a correct anchor assumption. Next, allow bounded reference offset, gain ranges, and recovery-rate ranges rather than fixing reference bias to zero. Compute the set of latent and sensor parameters consistent with the observations and bounds, reporting **an admissible set rather than one point**.

The present WLS/delta-method implementation does not solve this bounded-bias problem. A future fixed-data, equal-cost comparison should test reference-only, addition/blank, and triangulated sets for inclusion, width, and reduction by additional measurements. Bias bounds must not be tightened after seeing outcomes.

**Falsification:** reject a method that frequently excludes true parameters while bias remains within the declared bounds, or returns spuriously narrow sets under shared-anchor counterexamples. A provenance declaration that standards and samples share a measurement law is not evidence that the law actually transfers.

## Next E experiment: matched controls with unknown noise and explicit budget allocation

Current E assumes known Gaussian contrast variance. Add one change at a time: local variance estimation from new technical replicates, a contrast test under sign-symmetry assumptions, or an e-process with explicitly stated validity conditions. Alpha spending consumes valid conditional p-values; it does not correct a misspecified noise model.

Separately vary the fraction of a fixed total budget assigned to prediction versus auditing. Current E isolates audit location and cost; it does not establish prediction improvement or an optimal audit fraction. A new locked bank should add travel/setup costs and test whether the largest-gap baseline remains competitive.

**Falsification:** do not promote an adaptive policy if valid-null errors violate its claimed conditions or if it simultaneously increases misses and prediction loss relative to uniform/largest-gap designs at equal cost. Common-mode faults that disappear in contrasts remain mandatory counterexamples.

## Next F experiment: distinguish noise misspecification from mean misspecification

Technical replicate differences remove a shared mean and inform noise, while replicate means across inputs inform mean-function residuals. Next, model these sources separately and ablate one small residual basis. Increasing noise flexibility to absorb mean error remains a comparator rather than a mechanistic explanation.

Treat bootstrap or hierarchical propagation of estimated variance and calibration parameters as an independent ablation. Student-t degrees of freedom currently remain fixed at four; input-dependent degrees of freedom and posterior integration are not implemented. Retain unconverged fits in denominators rather than selectively removing difficult cases.

**Falsification:** better predictive scores do not establish mechanistic improvement when systematic latent-mean error or calibration ambiguity worsens. Retain simple Gaussian or context-specific selection when robustness is costly under normal conditions. Do not tune that choice on the final test set.

## Relation to the original hypotheses

H1/H2 gain limited measurement-design and small-regression evidence. H3 covers lineage and role separation, not new augmentation efficacy. H4 donor/individual hierarchy remains unimplemented. H5 multi-fidelity is preserved from the earlier version and not newly tested. H6 supports only the conditional audit rule in E; D/F prediction intervals gain no distribution-free guarantee.

Real-data permissions, retention and donor/site splitting, ethics approval, ODE/SINDy/PINN/BINN learning, and foundation-model fine-tuning remain out of scope. No empty plug-ins are added to imply those capabilities. The next step prioritizes small experiments that can falsify the remaining assumptions, not larger models.
