# Bounded-evidence research guide | v1.4.0-research.1

[한국어](BOUNDED.md) · [README](README.en.md) · [Versions](VERSIONS.en.md)

G models bounded reference bias, H diagnoses paired controls with unknown variance, and I separates replicate noise from mean misspecification. All data are synthetic. There is no real-data uploader, laboratory controller or integrated production agent that recycles evidence across modules.

## Install / 실행

```bash
python -m pip install -r research/requirements.txt
python -m research.bounded_loop demo --study G --scenario common_in_bounds --design triangulated --seed 27 --out research/bounded/results/demo-G.json
python -m research.bounded_loop demo --study H --scenario hetero_null --policy max_gap --audit-fraction 0.5 --seed 27 --out research/bounded/results/demo-H.json
python -m research.bounded_loop demo --study I --scenario combined --repeats 4 --seed 27 --out research/bounded/results/demo-I.json
```
Run from the repository root. No API key, GPU or model weights. Existing output paths are rejected; choose a new path. Public demos use a different bank from the bundled evaluation.

## Reproduce / 전체 재현

```bash
python -m research.bounded_loop prepare --out research/bounded/results/new-study
python -m research.bounded_loop evaluate --workers 4 --out research/bounded/results/new-study
python -m research.bounded_loop verify-lock --out research/bounded/results/new-study
python -m unittest discover -s research/bounded/tests -v
python research/bounded/validate_bounded.py
```
`prepare` records 60 development runs and freezes source/configuration. An evaluation-started directory cannot be overwritten. The validator targets the bundled `v140` results. Reproduction of the same bank is not an independent evaluation. Set `OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1` if needed to avoid BLAS oversubscription.

## Viewer / 결과 화면

```bash
python -m http.server 8766 --bind 127.0.0.1
```

`http://127.0.0.1:8766/research/bounded/web/`

The static viewer reads all 363 aggregate cells and 105 representative runs. Aggregates and one seed-73000 run are separate. New calculation uses the CLI, not a fake remote-model or training button. The original root index.html remains the earlier closed-loop viewer.

## Documents

[25. BOUNDED_DESIGN](research/docs/en/25_BOUNDED_DESIGN.md)  
[26. PARTIAL_IDENTIFICATION](research/docs/en/26_PARTIAL_IDENTIFICATION.md)  
[27. UNKNOWN_SCALE_AUDIT](research/docs/en/27_UNKNOWN_SCALE_AUDIT.md)  
[28. REPLICATE_DECOMPOSITION](research/docs/en/28_REPLICATE_DECOMPOSITION.md)  
[29. BOUNDED_RESULTS](research/docs/en/29_BOUNDED_RESULTS.md)  
[30. RESEARCH_DECISIONS](research/docs/en/30_RESEARCH_DECISIONS.md)  
[31. REPRODUCIBILITY](research/docs/en/31_REPRODUCIBILITY.md)  

[All cells](research/bounded/results/v140/ALL_RESULTS.md) · [References](research/bounded/references/REFERENCES.md) · [QA](research/bounded/quality/QA.md) · [Merge](MERGE_BOUNDED.md)
