# 18. Design and boundaries of the three follow-up studies

**v1.3.0-research.1 / zero biological observations.** Chapters 01–17 and the v1.0–v1.2 code are unchanged. This module tests tasks D/E/F from chapter 16 separately; it is not a fully integrated production system.

| Workstream | Question | Comparison | Implemented scope |
|---|---|---|---|
| D | Which observations test calibration transport to samples? | External standards, additions, matrix blank, orthogonal reference, triangulation | Observation/physical-parameter rank, recovery errors, conditional identification and contradiction |
| E | Can the same audit budget find local errors missed by a fixed panel? | Three-point, uniform, stratified, max-gap, adaptive coverage | Fresh matched contrasts, location selection, finite Bonferroni and alpha spending |
| F | Does improvement come from noise estimation or acquisition? | 3 controllers × 3 policies × 3 final estimators | Same-data refitting, fixed-estimator policy changes, NLL, CRPS, coverage and width |

## Evidence and access boundaries

Only runners own a `World`. D fitting receives observations; E location selection receives past contrasts and public domain/budget information; F selection receives a fitted model and past fit observations. Hidden fault locations, true gains, the noise law and final test outcomes are not selection-function arguments.

Records retain original IDs, kind, x, delta, cost, technical replicate, fit/audit/test role, parent ID and simulated origin. Generated/imputed observations, real samples and real-world authorization are rejected. Repeated technical measurements are not independent biological units. Coordinates are canonicalized to 10 decimal places before measurement to avoid inconsistent floating-point replicate identities.

A freeze event precedes opening test data. D and F account separately for 33 and 81 final test measurements. E uses audit measurements only; its final scoring uses numerical simulator truth about the hidden discrepancy. It does not fabricate a clinical endpoint or a physical test cost for numerical truth.

## Lock and amendment history

A local source/config/development-results hash follows 38 development smoke runs. This is not external preregistration, external blinding or independently administered simulation. The developer knows the generator; results are exploratory synthetic research.

The first partial `evaluation-v130-b` stopped because its replicate key rounded coordinates while stored values did not, causing a lineage check to reject numerically equivalent locations. Some D outcomes were inspected while checking progress. The implementation bug was fixed, without tuning inference, policies or thresholds, and the entire evaluation was rerun with bank `evaluation-v130-c` and seeds starting at 41000. The failed log, old code, old lock and hashes of partial outputs are retained in `research/triad/quality/aborted_attempt/`. Partial raw streams are not redundantly bundled. This history precludes describing the final work as untouched confirmatory research.

## Fair comparisons and stopping

D spends 48 acquisition units per protocol; expensive references displace ordinary measurements. E compares location policies under the same audit budget and reference cost. Costs are declared synthetic units, not real preparation or travel expenses. F refits all three estimators to every cost-48 dataset. Random and space-filling policies do not depend on the controller, so their duplicate datasets are not independent evidence.

No workstream automatically stops at its first warning. D qualifies its identification claim. E continues to the common budget while recording first-alarm cost. Worse results and failures are retained. Early warning is not equated with cheaper accurate prediction.

## Statistical interpretation

Parameters, effects and noise vary across worlds, and policies are paired on the same world. Rates have Wilson intervals. Prespecified F contrasts have descriptive 1,000-resample world-bootstrap intervals. These are not multiplicity-adjusted superiority tests or confidence intervals for a donor population. All simple-baseline failures are reported.

Hierarchical biological variation, ODE/SINDy/PINN models, foundation-model adaptation, real-data governance and instrument control remain outside scope. Beyond the limited E audit rule, no distribution-free predictive coverage claim is added.

---
[한국어](../ko/18_TRIAD_DESIGN.md) · [v1.3 entry](../../../TRIAD.en.md)
