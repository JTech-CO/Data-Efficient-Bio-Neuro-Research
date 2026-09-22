# v1.2.0-research.1 QA / 검증 기록

[한국어 재현·범위](../../docs/ko/17_REPRODUCTION_QA.md) · [English reproduction/scope](../../docs/en/17_REPRODUCTION_QA.md)

## Performed

- 43 new + 63 prior research + 14 original tests: 120 total, all passed. [New log](new-tests.log), [prior log](prior-research-tests.log), [original log](original-tests.log).
- 1,900 diagnostic trajectories; 1,920 acquisition runs; 413,978 serialized observation records checked for structure, source, splits, costs and technical-replicate lineage. Counts include repeated policy use, not independent biological units.
- 60 full acquisition replays + 10 diagnostic replays exactly match. Full compact records and summary recalculated from raw gzip files. [Validation JSON](validation.json).
- 80 browser-asset checks, all 60 scenario/policy trace selections, Korean/English, 390px layout, plot changes, labels and missing-vs-zero monitoring state. [Browser details](browser-validation.json).
- Four actual HTTP asset transfers compared byte-for-byte with released files, separately from browser tests.
- Frozen numerical source/configuration/calibration values match the protocol lock after evaluation. [Observed environment](environment.json).

## Browser navigation failed due to environment policy

Both file and localhost URL navigation returned `ERR_BLOCKED_BY_ADMINISTRATOR`. Screenshots and interaction checks use actual assets injected into an empty browser page, not normal deployment navigation. Native download completion and browser-to-server end-to-end operation were **not** verified. The environment policy was not disabled. Windows/macOS installation and remote GitHub Pages deployment are untested. Static viewer has no new Python computation API.

[Desktop](viewer-desktop-ko.png) · [Individual trace](viewer-trace-ko.png) · [Mobile](viewer-mobile-ko.png)

## Execution interruption

An initial per-call runtime limit interrupted one acquisition gzip. Completed cells were retained and a recovery helper reran only missing/incomplete cells using unchanged code, thresholds and world IDs. The interrupted file and start/resume/completion metadata are retained under results/v120. This is not outcome-based exclusion or independent repeated validation.

## Scientific boundary

No biological observations, real-world intervention authorization, clinical model, external blind evaluation or distribution-free prediction coverage. Rank checks are conditional on the declared measurement model. Diagnostic flags are not causal source labels. Finite-look correction is not unbounded-time anytime-valid inference. Local lock is a reproducibility record, not independent preregistration or a tamper-proof service.

## Preservation and package checks

The base archive has 626 files, including its checksum inventory. 623 remain unchanged in place; two root READMEs and root CHECKSUMS have byte-exact baseline copies. Original chapters 01–12 and the v1.1 code/results/viewer are preserved. Links and preservation are checked separately. The full archive, additive archive, CRC and base+overlay identity are verified by the external package-validation JSON provided alongside the archives.
