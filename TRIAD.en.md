# D/E/F follow-up research | v1.3.0-research.1

[한국어](TRIAD.md) · [Bilingual viewer](research/triad/web/index.html) · [All results](research/docs/en/22_TRIAD_RESULTS.md) · [Research decisions](research/docs/en/23_RESEARCH_DECISIONS.md) · [QA](research/triad/quality/QA.md)

All three workstreams are implemented and evaluated synthetically: calibration transport to samples, audit placement and cost, and separation of noise models from acquisition policies. Earlier v1.2 plans and results are preserved. This is not a completed biological AI, clinical device, or real-data-trained model.

| Workstream | Implementation | Evaluation |
|---|---|---|
| D | External calibration, addition, blank, orthogonal reference, triangulation | 9 scenarios × 5 designs × 80 = 3,600 runs |
| E | Fixed, random, stratified, largest-gap and adaptive audits, equal cost and alpha rules | Normal256 + 7×64 worlds, 5 policies × 3 cost settings = 10,560 trajectories |
| F | Full acquisition-controller × policy × final-estimator crossing | 6×40 worlds × 3 controllers × 3 policies = 2,160 collection runs, 6,480 final fits |

There are 16,320 runs/trajectories and zero biological observations. F has 1,200 unique acquired datasets; refitting duplicated passive datasets does not create independent samples.

## Main findings

Addition separates gain but not sample offset from the latent intercept. Additional valid anchors can supply rank, but shared anchor bias remains invisible. Broad spatial coverage detects narrow faults more often than three fixed sites at equal audit cost. Student-t helps under contamination but does not universally improve normal-noise estimation or repair a missing mean function. Chapter22 reports every cell and unfavorable result.

## Install and run new synthetic experiments

Run from the repository root. No GPU, API key, weights, or external dataset is required. No real-sample upload or instrument-execution API is provided. See QA for the environment actually tested.

```bash
python -m pip install -r research/requirements.txt
python -m research.triad_loop demo --study D --scenario both_shift --policy triangulated --seed 27 --out research/triad/results/demo-D.json
python -m research.triad_loop demo --study E --scenario narrow --policy adaptive_cover --seed 27 --out research/triad/results/demo-E.json
python -m research.triad_loop demo --study F --scenario contamination --policy ivr --controller student_t --seed 27 --out research/triad/results/demo-F.json
```

Existing output files are never overwritten. Demos use a separate public demo bank and do not alter the bundled evaluation.

## View saved results

Extract the complete repository and open `research/triad/web/index.html`, or serve it statically:

```bash
python -m http.server 8766 --bind 127.0.0.1
```

Open `http://127.0.0.1:8766/research/triad/web/`. The same subdirectory can be served statically by GitHub Pages; remote Pages deployment was not performed in this session.

The viewer shows aggregate results and 219 representative runs. Aggregates summarize multiple worlds; plots show the seed41000 run. Original run JSON is downloadable. New computation is CLI-only; the viewer does not retrain a model or import arbitrary demo JSON in this version.

## Reproduce the complete evaluation

```bash
python -m research.triad_loop prepare --out research/triad/results/new-study
python -m research.triad_loop evaluate --workers 4 --out research/triad/results/new-study
python -m research.triad_loop verify-lock --out research/triad/results/new-study
```

`prepare` records38 development smoke runs and source/configuration hashes. A started evaluation folder cannot be silently overwritten. This is not independent preregistration or externally blinded validation. [Design](research/docs/en/18_TRIAD_DESIGN.md) documents the earlier coordinate-lineage abort, implementation fix, and complete rerun on a fresh bank.

## Raw archive and validation

All raw measurements, models, costs, and scores are retained. Redundant event hashes/indices are distributed losslessly with full-record digest verification on restoration.

```bash
python -m research.triad.archive research/triad/results/v130/raw/D.compact.jsonl.gz research/triad/results/restored-D.jsonl.gz --restore
python research/triad/validate_triad.py
python -m unittest discover -s research/triad/tests -v
```

Use the same pattern for E/F. Newly generated readable JSONL and the bundled compact archive represent identical records. Hashes check reproducibility and accidental modification, not signed authentication.

## Documentation

Chapters18–24 add design, calibration transport/rank, spatial audits, the noise factorial, all results, decisions, and reproducibility/QA under both `research/docs/ko/` and `en/`. [Eight new references](research/triad/references/REFERENCES.md) distinguish Consensus discovery/fetch from primary-source verification. No paper full texts or weights are redistributed.

[Merge instructions](MERGE_TRIAD.md) · [Change log](CHANGELOG-TRIAD.md)
