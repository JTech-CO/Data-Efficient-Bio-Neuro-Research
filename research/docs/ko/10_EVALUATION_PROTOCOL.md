# 10. 실행 평가 프로토콜

[English](../en/10_EVALUATION_PROTOCOL.md) · [구현](09_IMPLEMENTATION.md) · [원 평가 계획](../../../docs/ko/03_EVALUATION.md)

## 평가 성격

v1.1.0은 **개발용 합성 파일럿**이다. 독립 사전등록, 외부 생물학 검증, 임상 검증이 아니다. 실행 전 config와 전체 실행 행렬을 해시로 고정했지만, 개발 과정에서 시나리오와 게이트를 검토했다. 따라서 본 결과를 확인적 검정이나 검증된 일반적 개선 효과라고 부르지 않는다. 전반적인 연구 계획과 별개로, 이 구현이 실제 수행한 범위를 한정한다.

## 실행 행렬

| 시나리오 | 설명 | 정책 수 |
|---|---|---:|
| smooth | GP 가정과 비교적 잘 맞는 매끄러운 함수 | 4 |
| narrow_peak | 고정 length보다 훨씬 좁은 봉우리 | 4 |
| confounded | 합산하면 두 계수의 합만 보이는 계 | 5 |
| biased_sensor | 선택 readout의 실제 gain 0.55, 모형은 1 가정 | 5 |
| missing_term | 후보 선형식에 없는 비선형 항 | 5 |
| fidelity_helpful | LF가 HF의 유용한 구조를 공유 | 4 |
| fidelity_deceptive | 입력에 따라 LF 관계가 변하는 불리한 전이 | 4 |
| mechanism_pair | 합산은 같고 선택 측정은 다른 A/B 기전 | 5 |
| mechanism_outside | 실제 함수가 A/B 어느 쪽도 아님 | 5 |

41개 scenario-policy 셀에 confounded의 identity-operator 추가 셀 1개를 합한다. **42셀 × 시드 0~11 = 504실행**이다. 모든 셀을 보고하며 결과가 나쁜 셀을 삭제하지 않는다. 세포·환자·동물 504개가 아니라 같은 합성 함수를 대상으로 한 Monte Carlo 실행이다. truth family와 parameter는 시드에 따라 바뀌지 않는다.

각 실행의 training 비용 상한은 24이다. 비용 단위는 임의의 synthetic 측정 단위다. sum/HF 1, 선택 readout 1.8, attenuation 2.2, LF 0.25로 선언한다. 시뮬레이터 계산 시간이나 실제 실험비를 측정한 값이 아니다.

## 분할과 진단의 재사용

초기 training 측정은 GP/선형/후보 모델의 경우 4개 sum이며, MF는 3위치의 HF/LF 쌍이다. HF-only는 3개 HF만 수집한다. 이후 정책이 유한 후보 격자에서 다음 측정을 고른다. 같은 조건의 두 번째 측정은 명시적 replicate이며 첫 측정 뒤에만 허용한다.

validation은 9개 위치, 최종 test는 61개 위치다. 선형/기전 후보는 각 위치에 sum, selective, attenuation의 3종류 측정이 있다. 각각 27개/183개다. 따라서 검증 오버헤드 비용은 GP/MF에서 70, 선형/후보에서 350이다. 총 측정 비용은 이 비용과 실제 training 비용을 합산한다. 모든 비교 셀은 적합에는 쓰지 않더라도 같은 진단 측정을 확보한다.

validation은 커널 선택, HF-only 전환, 가정 오류 중단에 반복 사용된다. 이를 독립 검증으로 포장하지 않는다. 한 실행의 최종 test는 모델·질의 선택 완료 후 한 번만 공개한다. 같은 test로 다시 threshold를 고르는 코드는 없다. 파일럿 전체의 결과를 본 연구자가 후속 코드를 수정한다면 새 연구 버전과 새 평가 시나리오가 필요하다.

## 지표와 성공의 의미

여기서 잠재 반응은 잡음 없는 관측 반응 함수를 뜻하며, 모든 숨은 상태의 복원을 의미하지 않는다. 예측에는 관측 RMSE/MAE/NLL, 관측 95% 구간의 포함률과 폭, evaluator-only truth에 대한 잠재 RMSE/포함률/폭을 저장한다. 선형식에는 prior를 제외한 관측 설계 rank도 저장한다. 유한 후보에는 최대 posterior, 0.95 결정 여부, 실제 후보 적중 여부, 진단 게이트 통과를 분리한다.

화면의 최종 목표는 잠재 RMSE ≤ 0.12 AND 관측 구간 포함률 ≥ 0.80 AND 폭 ≤ 0.80이다. **명목 95% 구간의 80% 포함률을 정확한 95% 보장이라고 주장하지 않는다.** 이 느슨한 threshold는 실패를 가르는 파일럿용 복합 기준일 뿐이다. 수치 전체를 확인해야 한다. `selected_candidate=null`을 성공으로 세지 않으며, 후보 밖 참값을 posterior confidence로 복구했다고 표시하지 않는다.

최종 test를 반복 열지 않으므로 최초 목표 도달 비용은 계산하지 않는다. `cost_to_target=null`이 의도된 결과다. 학습 예산 내 조기 중단과 목표 달성 비용은 다르다. 별도의 순차 검증 또는 시뮬레이터 전용 분석이 필요하다.

## 비교의 공정성과 제한

Uniform random은 **적격 action 전체**에서 뽑는다. 정보이득 정책은 비용으로 정규화하고 관측 분산 정책은 분산을 직접 최대로 한다. fixed readout은 다른 readout을 금지한다. guarded는 기본 정책에 커널 선택·탐색·진단 중단을 결합한 복합 정책이다. 따라서 guarded와 기본 정책의 차이가 특정 한 기능의 순수 인과효과라고 해석할 수 없다.

H2에 대해서는 두 비교를 모두 제공한다. 별도 identity 셀은 정책까지 잘못된 연산자를 사용한다. 추가로 각 선형 실행에서 **동일한 획득 관측**에 aware/identity 모형을 맞추어 측정 설계 효과와 fitting 효과를 분리한다. 상수·릿지·관측 인식 최소제곱의 같은-data 기준선도 포함한다.

GP의 길이척도, noise_sd, MF discrepancy와 선형 prior는 알려진 설정이다. hyperparameter uncertainty, 추정한 관측잡음, 실제 센서 drift, 생물학적 계층, causal intervention validity는 본 평가에 없다. 유한 두 후보는 symbolic discovery가 아니다.

## 통계

셀별 mean, seed SD, min, max, 목표 충족·가정 중단·fallback 횟수를 공개한다. guarded와 해당 기본 정책 간 RMSE 차이는 동일 seed를 짝지어 2,000회 bootstrap한 기술적 구간을 제공한다. 이는 **고정된 함수에서 시드 변동**의 요약이다. donor 모집단의 신뢰구간, 다중 비교 보정 검정, 일반적 모델 우열의 증명은 아니다. CPU 시간은 기록하지만 공정한 계산 비용 벤치마크로 사용하지 않는다.

동일한 scenario/seed/split/query의 잡음은 질의 ID에서 결정한다. 여러 정책이 같은 조건을 측정하면 같은 잡음을 받는다. 서로 다른 질의의 동일 번호 측정을 억지로 같은 관측으로 만들지 않는다. split별 독립 noise stream이 있고 group crossing은 거부한다. 이러한 group은 실제 피험자 ID가 아니다.

## 저장 결과와 재검사

[실행 설정](../../configs/pilot.json), [실행 전 행렬](../../results/pilot/protocol.lock.json), [전체 요약](../../results/pilot/summary.json)을 함께 본다. 세부 504개 결과는 runs/에 있다. 42개 시드 0은 `.json`, 나머지는 `.json.gz`이며 latter에도 비용·측정·이벤트·scalar snapshot은 모두 남는다. 그림용 81점 배열만 생략한다.

```bash
python -m unittest discover -s research/tests -v
python -m unittest discover -s tests -v
python research/validate_research.py
```

검증은 비용, 출처, hash chain, 테스트 접근 순서, JSON schema, 원 문서 보존, UI 실행 경로에 관한 것이다. 테스트 통과가 과학적 타당성이나 보안 무결성을 일반적으로 증명하지 않는다. 실제 실행 범위와 결과는 [QA](../../quality/QA.md)에 기록한다.

## 후속 연구의 고정 조건

이번 시나리오와 threshold를 보고 다음 버전을 만들었다면 이를 training/development 자원으로 취급한다. 다음 평가에서는 다른 함수 family, effect size, noise law, 센서 gain, 가정 오류 강도와 위치를 숨긴 별도 synthetic test bank를 먼저 고정한다. 고정 정책과 가정 탐지기의 false alarm, missed detection, stop delay, 총 비용, 최종 예측 손실을 함께 보고한다. 이 작업은 제안 단계이며 현재 504개 결과에 이미 포함되었다고 말하지 않는다.
