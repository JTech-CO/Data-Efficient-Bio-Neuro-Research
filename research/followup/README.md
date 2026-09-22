# Diagnostic follow-up module

[한국어](../../FOLLOWUP.md) · [English](../../FOLLOWUP.en.md) · [Static viewer](web/index.html)

| Path | Purpose |
|---|---|
| `../diagnostic_loop/` | Frozen v1.2 numerical implementation |
| `../configs/followup_v120.json` | Executed study configuration |
| `results/v120/` | Development/calibration/lock, every completed evaluation cell and interrupted-run provenance |
| `references/` | Consensus discovery, primary-source checks, metadata corrections and BibTeX |
| `schemas/` | Synthetic run envelope schema |
| `tests/`, `validate_followup.py` | Unit/integration tests and full raw-run auditing |
| `web/` | Saved-outcome viewer, explicitly not a compute endpoint |
| `quality/` | Logs, actual checks, previews and limitations |
| `baseline/` | Byte-exact originals of the three updated root files and v1.1 inventory |

`build_viewer_data.py` regenerates bundle.js from the locked study's complete summary and 60 saved traces. `browser_smoke.py` is a developer QA harness requiring Playwright and Chromium; the supplied run used `/usr/bin/chromium` on Linux. It reports when native URL navigation is blocked rather than claiming deployment passed.

`execute_shards.py` was added only to resume missing acquisition cells after the diagnostic stage of the locked execution completed. It is not part of the sealed numerical implementation, does not tune policies, and records retries with the same world IDs. See execution.resume.json.
