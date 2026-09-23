# 후속 연구 사용 안내 | v1.4.0-research.1

[English](BOUNDED.en.md) · [README](README.md) · [Versions](VERSIONS.md)

G는 기준 편향의 허용 집합, H는 미지 분산의 대조 진단, I는 반복 자료의 잡음·평균 분해를 다룬다. 모든 자료는 합성이며 실험 장치 실행·실제 데이터 업로더가 없다. 세 모듈의 증거를 서로 자동 재사용하는 통합 프로덕션 모델도 아니다.

## Install / 실행

```bash
python -m pip install -r research/requirements.txt
python -m research.bounded_loop demo --study G --scenario common_in_bounds --design triangulated --seed 27 --out research/bounded/results/demo-G.json
python -m research.bounded_loop demo --study H --scenario hetero_null --policy max_gap --audit-fraction 0.5 --seed 27 --out research/bounded/results/demo-H.json
python -m research.bounded_loop demo --study I --scenario combined --repeats 4 --seed 27 --out research/bounded/results/demo-I.json
```
저장소 루트에서 실행한다. API 키·GPU·모델 가중치는 필요 없다. 출력이 이미 있으면 덮어쓰지 않고 종료하므로 새 경로를 사용한다. 공개 demo bank와 수록 평가 bank는 다르다.

## Reproduce / 전체 재현

```bash
python -m research.bounded_loop prepare --out research/bounded/results/new-study
python -m research.bounded_loop evaluate --workers 4 --out research/bounded/results/new-study
python -m research.bounded_loop verify-lock --out research/bounded/results/new-study
python -m unittest discover -s research/bounded/tests -v
python research/bounded/validate_bounded.py
```
`prepare`는 개발 60개와 소스·설정을 고정한다. 평가를 시작한 폴더는 다시 덮어쓰지 않는다. 검증 스크립트는 기본 수록 `v140` 결과를 검사한다. 동일 bank의 재현은 새로운 독립 평가가 아니다. 평가 병렬화에서 필요하면 `OPENBLAS_NUM_THREADS=1`, `OMP_NUM_THREADS=1`을 설정한다.

## Viewer / 결과 화면

```bash
python -m http.server 8766 --bind 127.0.0.1
```

`http://127.0.0.1:8766/research/bounded/web/`

화면은 전체 363셀과 105개 대표 실행을 읽는 정적 뷰어다. 집계와 시드 73000의 한 실행을 구분한다. 새 계산은 CLI에서 수행하며, 화면에 원격 모델 호출·학습 버튼은 없다. 원래 루트 index.html은 과거 폐루프 뷰어로 보존했다.

## Documents

[25. BOUNDED_DESIGN](research/docs/ko/25_BOUNDED_DESIGN.md)  
[26. PARTIAL_IDENTIFICATION](research/docs/ko/26_PARTIAL_IDENTIFICATION.md)  
[27. UNKNOWN_SCALE_AUDIT](research/docs/ko/27_UNKNOWN_SCALE_AUDIT.md)  
[28. REPLICATE_DECOMPOSITION](research/docs/ko/28_REPLICATE_DECOMPOSITION.md)  
[29. BOUNDED_RESULTS](research/docs/ko/29_BOUNDED_RESULTS.md)  
[30. RESEARCH_DECISIONS](research/docs/ko/30_RESEARCH_DECISIONS.md)  
[31. REPRODUCIBILITY](research/docs/ko/31_REPRODUCIBILITY.md)  

[All cells](research/bounded/results/v140/ALL_RESULTS.md) · [References](research/bounded/references/REFERENCES.md) · [QA](research/bounded/quality/QA.md) · [Merge](MERGE_BOUNDED.md)
