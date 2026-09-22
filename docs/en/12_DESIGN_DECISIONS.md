# 12. Design decisions, non-goals and baseline preservation

## ADR-001: extend the same repository

The original 63-file SHA-256 inventory is stored in `research_lab/provenance/baseline_manifest.json`. Chapters 01–08 and the original examples, schemas, references, tests and quality records remain unchanged. Only an entry section is appended to the two READMEs, and the root checksum inventory is refreshed. Byte copies of the original READMEs and checksum file are preserved. Original quality reports are not overwritten with new test claims.

## ADR-002: begin with known ODE candidates and exact small inference

There are no dummy classes pretending to discover arbitrary equations or train large PINNs. Two candidate models linear in their unknown coefficients permit exact conjugate posterior and marginal-evidence calculations, making observation, information, cost and evaluation boundaries auditable. Dynamic structures are supplied, not learned; outside-candidate laws are not generated automatically.

## ADR-003: leave the original observation schema intact

Respect the original `additionalProperties=false` contract. Query, role, hash and cost are carried in an external envelope. Structural compatibility and semantic split/simulator-only restrictions are tested separately.

## ADR-004: audits are not tests

Audits can influence behavior and therefore are not final tests. Their labels do not fit the predictor, but do affect alerts and fallback selection. Held-out/OOD truth is accessed only after a run is complete. Post-run metrics are not online stopping criteria.

## ADR-005: automatic approval means a simulator allowlist only

Each approval records `type=synthetic_allowlist` and `real_world_authorized=false`. It does not imply institutional authorization, a human approval action or biological safety review. The server binds to loopback and accepts small configuration JSON only. There are no uploads, command-execution endpoints, API keys or experimental-device connections. Do not expose it to the internet.

## ADR-006: prediction may continue while mechanism preference is withheld

Fallback GP predictions still require separate error and interval evaluation. Increasing alerts and abstention is not automatically success. Much of the observed coverage increase came from wider intervals, shown explicitly in the report and UI.

## ADR-007: static review must not impersonate computation

Bundle 25 actual traces and the 640-run summary. Static mode offers review and JSON import/export; new execution is disabled without the Python backend. Timeline playback is labelled differently from computation. No external CDN, fonts or analytics are used.

## ADR-008: distinguish publication metadata from implementation evidence

Three selected Consensus records were fetched and their publication years checked against publisher/conference records. Where Consensus reflected preprint years, both metadata and version-of-record information are retained. This code does not claim to implement CIV, R-IDeA or profile-likelihood optimal control. [Additional literature](../../research_lab/provenance/LITERATURE.md)

## Non-goals

No production biological/neuroscience model, clinical inference, device control, automatic mechanism confirmation, PINN/BINN/SINDy training, foundation fine-tuning, multi-fidelity selection, generative augmentation or real patient/donor ingestion is implemented. A reserved query field is not an implemented feature.

## Remaining engineering limits

Static JSON import is a local research-record viewer, not a general secure data-format service. A hash chain detects changes but does not establish authenticity against an attacker able to recompute the entire chain. Marginal evidence is conditional on candidate structures and priors. Few audits provide no guaranteed detection power. OOD evaluation changes x within the same simulator rather than supplying external biological validation.
