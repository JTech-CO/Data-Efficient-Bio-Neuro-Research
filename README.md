# 데이터 효율적 생명·뇌과학 AI 연구

[English](README.en.md) · **현재 버전: v1.4.0-research.1** · [버전별 자료](VERSIONS.md)

관측, 모델의 가정, 다음 측정·개입을 분리하는 폐루프 연구 저장소다. 문헌 조사와 실행 가능한 소규모 합성 실험을 함께 관리하며, 데이터 효율성뿐 아니라 잘못된 교정·잡음·모델 가정을 어디까지 알아낼 수 있는지 검토한다.

**현재는 합성 연구 단계다. 실제 생물학적 표본 학습이나 임상·실험 장치 제어 모델이 아니다.**

## 현재 연구

| 주제 | 자료 |
|---|---|
| 기준 편향을 허용한 부분 식별 | [집합·가정·식별 범위](research/docs/ko/26_PARTIAL_IDENTIFICATION.md) |
| 잡음 분산을 모르는 대조 진단 | [검정 조건·위치·예산](research/docs/ko/27_UNKNOWN_SCALE_AUDIT.md) |
| 기술적 반복의 잡음·평균 오류 분해 | [동일 자료 비교·반례](research/docs/ko/28_REPLICATE_DECOMPOSITION.md) |

[시작 및 실행](BOUNDED.md) · [평가 결과](research/docs/ko/29_BOUNDED_RESULTS.md) · [결과 뷰어](research/bounded/web/index.html) · [다음 연구 결정](research/docs/ko/30_RESEARCH_DECISIONS.md)

## 실행

저장소 루트에서 실행한다. Python 환경이 필요하며 API 키·GPU·모델 가중치는 필요 없다.

```bash
python -m pip install -r research/requirements.txt
python -m research.bounded_loop demo --study G --scenario common_in_bounds --design triangulated --out research/bounded/results/demo-G.json
```

결과 화면은 저장된 기록을 읽는 정적 뷰어다. 새 계산과 전체 재현 명령은 [사용 안내](BOUNDED.md)에 있다.

## 연구 기반과 재현성

[종합 조사](docs/ko/01_RESEARCH_REPORT.md) · [원 아키텍처](docs/ko/02_ARCHITECTURE.md) · [원 평가 계획](docs/ko/03_EVALUATION.md) · [현재 검증 범위](research/bounded/quality/QA.md) · [사용권 안내](LICENSE.md)

과거 설계·코드·원시 결과는 보존한다. 릴리스별 변경 내용과 실행 경로는 [VERSIONS.md](VERSIONS.md)에서 확인한다. 합성 결과를 생물학적 성능이나 보편적 통계 보장으로 확대하지 않는다.
