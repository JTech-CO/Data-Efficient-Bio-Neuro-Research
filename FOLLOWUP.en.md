# Follow-up research v1.2.0-research.1

[한국어](FOLLOWUP.md) · [Result viewer](research/followup/web/index.html) · [Design](research/docs/en/13_FOLLOWUP_DESIGN.md) · [Full results](research/docs/en/15_FOLLOWUP_RESULTS.md) · [Decisions](research/docs/en/16_RESEARCH_DECISIONS.md)

## Added scope

This implements bounded tasks A/B from the prior observation/assumption/intervention architecture. **No real biological observations, trained biological model or clinical diagnostic system is included.** Synthetic worlds test unknown sensor gain/offset, latent coefficients, replicate-based noise estimation, false warnings and calibration-transport failures.

Forty development runs and 2,000 null calibration trajectories preceded a local protocol lock. Study A uses 1,900 diagnostic trajectories (1,000 normal plus 100 for each of nine faulty settings); study B uses 320 worlds × six policies = 1,920 runs. The biological sample count is zero. Numerical source and thresholds were not changed after evaluation. A local hash is not independent preregistration.

## Findings to read first

Normal-world warning rates were 38.5% for naive repeated testing, 5.5% for Bonferroni and 6.1% for maximum-score calibration. Reducing false warnings did not solve source identification. Corrected monitoring warned in only 4% of reference/specimen mismatch worlds, and its mechanism channel hit none of the localized faults between fixed audit locations. Block-targeted information did not always outperform joint-information. Full results report failures, cost and same-data estimator ablations.

## Viewing is not computation

After extracting the complete folder, `research/followup/web/index.html` is designed to show saved study tables and 60 representative runs (index 20000). It is a **static viewer**, not a new-training API. Individual curves are distinguished from 32-world averages. The original root index and v1.1 lab remain intact.

Managed browser policy in the execution environment blocked file and localhost navigation. The actual assets were tested through an inline browser harness, with native HTTP transfer checked separately. Native user-browser navigation and completed downloads were not validated here. See [QA](research/followup/quality/QA.md).

## Run a fresh synthetic experiment

From the repository root; no external API key, GPU, weights or biological dataset is required:

```bash
python -m pip install -r research/requirements.txt
python -m research.diagnostic_loop demo --scenario gain_offset --policy block_targeted --seed 27 --out research/followup/results/my-demo.json
```

Existing output paths are not silently overwritten. Demo runs use a separate public bank and do not alter the locked evaluation. New results are JSON; this viewer does not import arbitrary run files.

Reproduce the full protocol in a fresh folder:

```bash
python -m research.diagnostic_loop prepare --out research/followup/results/new-study
python -m research.diagnostic_loop evaluate --out research/followup/results/new-study
python -m research.diagnostic_loop verify-lock --out research/followup/results/new-study
```

Prepare first computes 40 development runs and 2,000 calibration trajectories. `OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1` can avoid BLAS oversubscription. See the [execution environment](research/followup/quality/environment.json). Exact package pins aid reproduction of the observed environment, not a claim of installation testing on every OS.

## Validation

```bash
python -m unittest discover -s research/followup/tests -v
python -m unittest discover -s research/tests -v
python -m unittest discover -s tests -v
python research/followup/validate_followup.py
```

43 new + 63 previous research + 14 original tests passed. Validation checked 413,978 serialized observation records, all 1,920 acquisition logs and 1,900 diagnostic trajectories, costs, provenance, event chains and all summaries. The record count includes reuse across policies, not independent evidence. Sixty acquisition runs and ten diagnostic trajectories were fully replayed.

## Merge and preserve

The base is `Data-Efficient-Bio-Neuro-Research_v1.1.0_Closed-Loop-Lab_KO-EN.zip`, not the older alternative using a research_lab directory. See [merge instructions](MERGE_FOLLOWUP.md). No remote repository was queried, modified or deployed. New chapters 13–17 are in the Korean/English research/docs folders; prior chapters 01–12 are unchanged. Existing [license guidance](LICENSE.md) continues to apply.
