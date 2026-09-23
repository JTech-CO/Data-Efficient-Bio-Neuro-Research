# 24. Reproducibility and verification

[한국어](../ko/24_REPRODUCTION_QA.md) · [Research entry](../../../TRIAD.en.md) · [Full QA](../../triad/quality/QA.md)

Version1.3 publishes16,320 synthetic D/E/F runs. All61 new numerical/contract tests and120 prior tests pass (181 total). Every890,880 serialized observation is checked for lineage, roles, costs and freeze order. All219 representative runs are recomputed identically. Group summaries and planned paired contrasts are recalculated from raw data.

Six of6,480 final fits and267 acquisition snapshots did not meet the configured iterative tolerance and remain in the results. Numerical convergence does not establish an exact posterior or a true model.

Raw logs use lossless event reconstruction without dropping measurements, models or outcomes. `python -m research.triad.archive ... --restore` reconstructs the original JSONL objects. Hashes detect accidental changes, not signed external attestation.

The106 browser/HTTP checks comprise100 injected-asset rendering/DOM checks and6 separate HTTP byte comparisons. Managed policy blocked native localhost/file navigation; actual browser download completion and deployment end-to-end are not claimed. Logs, screenshots and reproduction commands are linked in QA and TRIAD.

Of825 v1.2 baseline files, only two root READMEs and the checksum list are updated; original plans, code and results remain unchanged. Those three originals and a complete baseline manifest are retained. ZIP CRC, per-file SHA and additive-overlay equality are recorded in the package report. No remote GitHub write was performed.

The earlier coordinate-lineage abort/fresh-bank evaluation and a later integer-argument replay-harness fix are documented. The local lock is not independent preregistration. Biology, clinical use and general prediction-interval guarantees require separate validation.
