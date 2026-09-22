# 17. Reproduction, validation and scope

[한국어](../ko/17_REPRODUCTION_QA.md) · [Entry](../../../FOLLOWUP.en.md) · [Results](15_FOLLOWUP_RESULTS.md) · [QA record](../../followup/quality/QA.md)

## Reproduction unit

Bundled outcomes are the locked synthetic v1.2.0-research.1 study under research/followup/results/v120. The protocol lock fixes source/configuration/calibration SHA-256 values. Changed source should not be presented as a new validated result on the same independent bank.

```bash
python -m pip install -r research/requirements.txt
python -m research.diagnostic_loop verify-lock --out research/followup/results/v120
python research/followup/validate_followup.py
python -m research.diagnostic_loop demo --scenario reference_mismatch --policy block_targeted --seed 27 --out research/followup/results/my-demo.json
```

Demo uses a separate public namespace. See the entry document for prepare/evaluate in a fresh directory. The separate execute_shards.py recovery helper supports interrupted acquisition cells **after the diagnostic stage completed**. It is not an arbitrary-stage distributed execution service. Read its docstring and retained execution metadata before reuse.

## Executed checks

| Check | Observed scope |
|---|---|
| New tests | 43 |
| Previous research tests | 63 |
| Original tests | 14 |
| Raw diagnostic trajectories | 1,900, all three detectors recomputed |
| Raw acquisition runs | 1,920, schema/budget/roles/approval/hash chain/freeze/final test ordering |
| Serialized observation records | 413,978 provenance, cost and replicate checks; not independent subjects |
| Full deterministic replay | 10 diagnostic trajectories and 60 acquisition runs |
| Aggregates | Compact records and full summary exactly reconstructed from raw files |
| Browser assets | 80 checks, all 60 scenario/policy pairs, languages/mobile/intervention curves/tables |

Logs remain in research/followup/quality. Passing these checks is not biological validity, external generalization, adversarial security or clinical certification.

## Browser limitations

Managed Chromium policy blocked file and localhost navigation with ERR_BLOCKED_BY_ADMINISTRATOR. The policy was not disabled or circumvented. Actual released HTML/CSS/JS/data assets were injected into an empty browser page for rendering and interaction tests. A separate Python HTTP server and native HTTP requests verified byte-identical delivery of four assets.

Native file navigation, end-to-end browser HTTP navigation, completed native downloads, remote GitHub Pages and native Windows/macOS Python installation were not validated. Previews were rendered through the inline asset harness. The new viewer is explicitly static; no new computation API is claimed.

## Preservation

The base v1.1 archive contains 626 files including its checksum inventory. Of these, 623 remain byte-identical in place; two root READMEs receive additive entries and the root checksum inventory is regenerated. Byte-exact originals of those three files are preserved in baseline. Prior chapters 01–12, 504-run outcomes, numerical code and viewer remain unchanged.

The baseline manifest records the base archive and every base-file hash. A separate package check compares base plus additive payload with the full payload. Archived original README copies intentionally retain their relative-link bytes and are excluded from current-document link checks. No source-paper PDFs or model weights are redistributed.

## Scientific limitations

False-warning statements depend on null-model validity, Gaussian homoscedastic errors and finite prespecified looks. Local delta information is not exact nonlinear mutual information. Calibration propagation is first-order and noise variance is plug-in. Synthetic truth is evaluator-only. Different world IDs and feature families do not establish external blinding; features are public to the model. Passing an audit panel does not certify the entire domain or specimen calibration transport.
