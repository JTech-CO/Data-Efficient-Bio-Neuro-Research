# Executable research extension / 실행 가능한 연구 추가 단계

**한국어:** [09 실행 문서](docs/ko/09_EXECUTABLE_RESEARCH.md) · [10 실제 결과](docs/ko/10_PILOT_RESULTS.md) · [11 다음 연구](docs/ko/11_NEXT_RESEARCH.md) · [12 설계 결정](docs/ko/12_DESIGN_DECISIONS.md)

**English:** [09 implementation](docs/en/09_EXECUTABLE_RESEARCH.md) · [10 actual results](docs/en/10_PILOT_RESULTS.md) · [11 next research](docs/en/11_NEXT_RESEARCH.md) · [12 decisions](docs/en/12_DESIGN_DECISIONS.md)

**Repository extension:** 1.1.0-research.1 · **Python slice:** 0.1.0 · **Date:** 2026-09-22.

기존 연구를 다른 프로젝트로 교체하지 않는다. 기존 01~08장, 예제, 스키마, 문헌은 보존하고 동일 저장소의 `research_lab/`에 H1/H2의 제한된 합성 폐루프를 추가했다. 실제 생명·뇌과학 데이터, 외부 API 또는 사전학습 가중치가 필요하지 않다. 연구 자료의 기존 공개 라이선스 선택 전 상태를 유지한다.

This is an additive research implementation, not a replacement project or a production biological model. It preserves the original research plan and adds a small, executable, falsifiable loop using synthetic data only. The original license-selection status remains unchanged.

## Local execution

From the repository root, use Python 3.11 or newer; the recorded environment was Python 3.13.5 on Linux.

```bash
python -m pip install -r requirements-lab.txt
python -m research_lab serve
```

Open the URL printed by the terminal: `http://127.0.0.1:8765/research_lab/web/`.

The UI supports Korean and English. It shows observation provenance, assumed models, selected queries, audit alerts, prediction intervals and the repeated pilot. The local server runs new synthetic experiments. It binds only to loopback; it is not a production or multi-user server.

## Static review

Open `research_lab/web/index.html` directly, or publish the repository root with GitHub Pages. The root `index.html` points to the lab. Static mode contains 25 seed-0 execution traces and the full 640-run summary; no fake browser inference is performed. New computation requires Python. Imported execution JSON stays in the browser; biological uploads are not supported.

```bash
python -m research_lab run --scenario hidden_mechanism --policy guarded_information --seed 7 --out research_lab/results/my-run.json
python -m research_lab benchmark --out research_lab/results/new-pilot
python -m pytest research_lab/tests -q
python -m unittest discover -s tests -v
python scripts/validate_research_lab.py
```

Existing output paths are not silently overwritten. Use a new path, or explicitly add `--overwrite`.

## What was actually executed

The stored pilot has 32 settings × 20 matched simulator seeds = 640 executions: 500 main comparisons and 140 ablation runs. Costs include initial and audit queries. Independent audit labels influence the gate but never fit the posterior. Test and extrapolation targets are computed only after a completed acquisition run. Zero biological units were used.

The guarded policy is **not uniformly superior**. It sometimes abstains appropriately, sometimes increases error and interval width, and often misses sensor/noise misspecification. These failures are the reason for the next research plan, not hidden exclusions.

See [additional literature](research_lab/provenance/LITERATURE.md), [baseline preservation manifest](research_lab/provenance/baseline_manifest.json), [quality report](research_lab/results/quality/QA.md), and [additive changelog](CHANGELOG-RESEARCH.md).

## Merge into the same repository

See [MERGE_RESEARCH.md](MERGE_RESEARCH.md) before applying the overlay, especially if your repository has changed since the baseline ZIP.
