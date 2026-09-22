# 12. Research direction and falsification criteria

[한국어](../ko/12_RESEARCH_DIRECTION.md) · [Original hypotheses](../../../docs/en/06_RESEARCH_AGENDA.md) · [Current results](11_PILOT_RESULTS.md)

## Direction

Narrow the next question to **when assumption failure can be detected, and which next measurement can distinguish its causes**. This follows directly from current failure cases and is more focused than immediately adding a larger regressor or biological foundation model. Preserve the original plan while accumulating small, executable studies.

Do not describe the next version as a completed biological AI. Current experiments are static synthetic examples exposing observation-operator and candidate-library dependence. No neural signal or cell dynamics has been learned. Falsifiable research on assumption diagnostics and experiment selection can continue without biological data.

## Mapping to the original agenda

| Hypothesis | Current implementation | Unsupported extension |
|---|---|---|
| H1: acquire observable mechanism differences | Finite A/B library, projected MI, out-of-library truth | Unknown mechanism discovery, universal optimal design |
| H2: improve observation modeling | Known-H regression, identity ablation, same-query refits | Learning unknown H, outperforming PINN/UDE |
| H3: separate augmentation from independent evidence | Lineage, partition, and fitting guards | Augmentation effect size, privacy protection |
| H4: shared structure and group variation | Not implemented | Donor generalization, hierarchical Bayesian dynamics |
| H5: avoid adverse fidelity transfer | Joint GP, pooling/HF-only baselines, fallback | Automatic fidelity ranking, universal fallback benefits |
| H6: uncertainty after adaptive selection | NLL, coverage, width, diagnostic stops | Conformal, anytime, or distribution-shift guarantees |

## Workstream A: evaluate the assumption detector itself

The present gate uses residual thresholds and a small diagnostic set. It is an operational heuristic that can miss bias or flag a valid model. Construct a hidden synthetic bank separating correct-model worlds from mismatched worlds.

Vary sensor gain/offset, nonlinear readout, heteroscedastic noise, heavy tails, local discontinuities, omitted terms, and changing LF/HF relationships one axis at a time. Separate development and final function families. Measure false alarms as diagnostic opportunities accumulate.

**Falsification:** if gating does not reduce prediction loss and produces frequent unnecessary stops in correct worlds, reject automatic stopping. Compare warning-only and additional-diagnostic-measurement policies. Fix thresholds on a development bank and do not retune on the hidden bank.

**Deliverables:** fixtures with explicit assumption-truth tags; false-positive, false-negative, and detection-delay tables; joint reporting of total cost, added measurements, and prediction loss. Do not retroactively invent a favorable improvement threshold from the current results.

## Workstream B: change what is measured, not only how much

The present selective readout assumes known H. Introduce a small system with both unknown mechanism coefficients and unknown sensor gain. Treat repeated measurement, independent calibration, selective readout, and a declared synthetic intervention as distinct actions.

Separate information about mechanism parameters from information about sensor calibration. Record which uncertainty decreased. Retain examples where replication reduces noise without resolving structural ambiguity. Do not compress all sensor and mechanism uncertainty into an unexplained scalar.

**Falsification:** if the new acquisition rule offers no practical gain over same-query known-H or oracle-H references but increases computational cost, retain a simple calibration-then-regression path. Report equivalence classes rather than single parameter estimates when identification fails.

## Workstream C: introduce time without adding every module at once

After static-loop contracts stabilize, add a two-state ODE toy family with partial observations. Compare fixed-mechanism numerical fitting, a GP or small residual, and then weak-form dynamics candidates. Do not introduce noise estimation and adaptive time selection simultaneously without staged ablations.

Relaxing the current `time=1.0` restriction requires coordinated changes to query semantics, simulation, numerical integration error, temporal targets, and future-extrapolation splits. Do not advertise empty plugin names as implementations.

**Falsification:** if a more complex dynamics model does not improve error, reproducibility, or interpretation against a simple known ODE plus observation likelihood, do not escalate complexity. Discovery of actual biological mechanisms remains a separate question.

## Boundary when real data become available

The current adapter rejects real data. A future ingestion path needs units, device/readout definitions, permission, donor/session/site partitions, preprocessing lineage, incomplete-label treatment, and retention/deletion rules before adding an uploader. Offline pool replay cannot establish the causal effect of a new intervention. Restrict replay to measurements actually available in that pool.

A useful public-data result would still not establish prospective or clinical validity. Those require separately designed, authorized studies. None are performed by this version.

## Repository practice

Do not rewrite original chapters 01–08 to imply that the present implementation completed them. Accumulate decisions and evidence under `research/docs/`. Each version should bind configuration, code fingerprint, all outcomes, and failure cases. Keep development evidence separate from locked final evaluation. The UI must expose what was observed, assumed, and merely planned.

Prioritize A and B next. Adding H4, foundation models, or new biological modalities first may bypass the main failure illustrated by this pilot. This ordering is a research-design judgment from the present results, not a proven universal development sequence.
