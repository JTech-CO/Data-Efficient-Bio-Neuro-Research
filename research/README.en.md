# Closed-loop research lab v1.1.0

[한국어](README.ko.md) · [Original research](../README.en.md) · [Workbench](../index.html)

An executable **synthetic research module** testing separation of observations, assumptions, and interventions. Original chapters 01–08 are preserved. This is not a completed biological, neuroscience, or production model.

| Read first | Contents |
|---|---|
| [09 Implementation](docs/en/09_IMPLEMENTATION.md) | Modules, equations, operation, boundaries |
| [10 Executed protocol](docs/en/10_EVALUATION_PROTOCOL.md) | Design cells, budgets, leakage controls, metrics |
| [11 Pilot results](docs/en/11_PILOT_RESULTS.md) | All cells and negative findings |
| [12 Research direction](docs/en/12_RESEARCH_DIRECTION.md) | H1–H6 status and falsifiable next questions |
| [QA](quality/QA.md) | Checks actually executed and remaining limits |

```bash
python -m pip install -r research/requirements.txt
python -m research.closed_loop serve
```

Run from the repository root and open `http://127.0.0.1:8765`. No API key, GPU, or external dataset is required. Opening `index.html` without Python replays the included seed-zero traces and twelve-seed statistics, not new training. Use a browser supporting `DecompressionStream`.

The [configuration](configs/pilot.json) defines 504 runs. Recompute with `python -m research.closed_loop suite`; compute one run with `python -m research.closed_loop run`; check a saved run with `python -m research.closed_loop audit <path>`. CLI accepts JSON.gz; UI imports uncompressed detailed run JSON.

[Full summary](results/pilot/summary.json) · [Frozen matrix](results/pilot/protocol.lock.json) · [Baseline manifest](baseline/manifest.json) · [Implementation sources](SOURCES.md)

The existing undecided publication-license status is retained. Adding implementation code does not assign a new license to the original material or third-party sources. Remote GitHub upload, Pages deployment, and Actions execution are not performed by this package.
