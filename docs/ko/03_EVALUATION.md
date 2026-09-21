# 평가·재현·중단 기준

**아래 수량과 통과 조건은 연구 설계 예시다. 논문에서 검증된 보편적 임계값이나 실제 완료 결과가 아니다.**

## 1. 비교 질문을 사전에 고정

좋지 않은 질문은 ‘적은 데이터에서 AI보다 좋은가’이다. 좋은 질문은 ‘새 기증자에서 특정 오차·coverage 조건을 만족할 때 필요한 실제 assay 비용이, 동일 정보 접근과 튜닝 예산을 가진 기준선보다 작은가’이다.

입력 예산은 `n_independent_groups`, `n_real_measurements`, `n_new_labels`, `annotation_minutes`, `n_pretraining_examples_known`, `n_simulator_calls`, `compute_hours`, `assay_cost`로 나눠 보고한다. 공개 아틀라스의 cell 수나 EEG window 수를 독립 기증자 수로 대체하지 않는다. 정확한 사전학습 수·중복이 공개되지 않았다면 `unknown`으로 쓴다.

초기 예산 곡선은 8/16/32/64개의 독립 실험 조건처럼 정할 수 있다. 단, 사람 수가 적은 데이터에서 이 수치를 억지로 만들지 않는다. Few-shot 분류의 클래스당 라벨 수와 독립 개체 수는 별도로 기록하고, 실제 이용 가능한 집단 수에 따라 계획을 바꾼다.

## 2. 분할을 변환보다 먼저 수행

| 데이터 | 1차 분할 단위 | 추가로 차단할 누수 |
|---|---|---|
| 세포 영상 | donor / organoid / slide / imaging run | 같은 FOV의 crop·증강·중복 이미지 |
| 단일세포 | donor / cell line / perturbation / batch | 같은 유전자 개입이나 기증자의 cell 혼입 |
| EEG | subject / session / recording | 겹치는 window, 미래 filtering, 동일 세션 통계 |
| 동역학 | 독립 trajectory / 초기조건 / 개입 | 같은 궤적의 가까운 시간점을 임의 혼합 |
| 멀티피델리티 | 공통 condition·group 단위 | held-out 고정밀 대상의 저정밀 짝을 학습에서 몰래 사용 |

Transductive 또는 저정밀 관측을 허용하는 테스트 시나리오는 별도 트랙으로 정의한다. 허용 자체가 항상 누수인 것은 아니지만, 그런 정보를 못 쓰는 기준선과 같은 이름의 시험으로 비교해서는 안 된다.

train 안에서 scaling, feature selection, PCA, batch correction, 생성기, symbolic library 선택과 hyperparameter search를 적합한다. validation은 선택용이며 최종 real test는 잠근다. 가능한 경우 새 기관·기기·날짜의 external holdout을 추가한다. foundation pretraining overlap은 별도 manifest로 보고한다. [R18](../../references/BIBLIOGRAPHY.md#r18) [D01](../../references/BIBLIOGRAPHY.md#d01)

## 3. 기준선은 작지만 강하게

| 비교 축 | 반드시 포함할 기준선 | 추가 모델 |
|---|---|---|
| 스칼라 예측 | 평균/상수, ridge 또는 elastic net, 단순 기전 적합 | GP, tree 계열, 소형 NN |
| 획득 정책 | 무작위, space-filling, 기존 실험설계 | GP 정보 기반 AL / BO |
| 동역학 | 알려진 ODE solver + 우도 적합, point-derivative SINDy | weak/ensemble SINDy, PINN, UDE |
| 표현 전이 | raw feature + linear head, frozen encoder + 같은 head | adapter와 partial fine-tuning |
| 유전자 개입 | no-change, mean response, additive/linear | 생물 특징 모델, 선택한 FM |
| 데이터 증강 | real-only와 augmentation 없음 | 규칙 변환, calibrated simulation, 생성모형 |
| fidelity | high-fidelity-only / low-fidelity-only | 선형·비선형 multi-fidelity |

단일세포의 강한 단순 기준선은 형식적 절차가 아니라 핵심 비교 대상이다. [R12](../../references/BIBLIOGRAPHY.md#r12) [R13](../../references/BIBLIOGRAPHY.md#r13) 모델마다 외부 데이터 접근량, 탐색 횟수, early stopping, 계산 예산을 공개한다. 더 큰 모델만 훨씬 많이 튜닝한 비교는 회귀 방법의 순수 효과로 해석하지 않는다.

## 4. 역할별 지표

| 역할 | 1차 지표 예시 | 보조·실패 지표 |
|---|---|---|
| 수집 | 목표 정확도에 도달한 실제 비용 | 실패 assay 비율, 집단 다양성, 중복 질의 |
| 연속 예측 | held-out MAE/RMSE | 집단별 오차, NLL/CRPS, 외삽 gap |
| 구간 | 명목 coverage와 실제 coverage | 폭, 집단별 undercoverage, abstention |
| 기전 | 새 개입·초기조건 rollout | coefficient stability, 식별가능성, 물리 위반 |
| 세포 영상 | object-level precision/recall 또는 AP, Dice/IoU | 경계·희귀 형태·count bias, downstream trajectory bias |
| 오믹스 | control 대비 변화량의 예측 오차 | perturbation별 오차, effect direction, pathway 일관성 |
| EEG | balanced accuracy 또는 macro-F1 | subject별 최저 성능, 지연, artifact 의존성 |
| 생성 증강 | real-only test의 downstream 변화 | 희귀 모드 손실, source-label shortcut, privacy risk |

Coverage는 넓이와 같이 보고한다. 무한히 넓은 구간은 coverage가 높아도 의사결정에 쓸모없을 수 있다. Calibration error만으로 epistemic uncertainty를 증명하지 않는다. 회귀구간과 분류 confidence의 평가를 섞지 않는다.

기전의 정답식을 아는 합성 데이터에서는 term precision/recall과 식 동치성을 평가할 수 있다. 실제 생물 데이터에 알려진 정답식이 없으면 같은 지표를 만든 척하지 않고, 예측 안정성·개입 반증·식별가능성의 증거를 보고한다. [R06](../../references/BIBLIOGRAPHY.md#r06)

## 5. 필수 ablation

A: acquisition만 바꾼다. 동일 GP, 초기 샘플, noise model, 전체 예산에서 random과 AL을 비교한다.

B: prior만 바꾼다. 올바른 법칙, 일부 틀린 법칙, 제약 없음, discrepancy 허용을 비교한다. 참 법칙이 알려진 합성 시험과 실제 데이터를 분리한다.

C: 동역학 추정만 바꾼다. point derivatives, weak formulation, ensemble, latent observation model을 순차 비교한다.

D: 표현만 바꾼다. 동일 downstream head와 분할에서 raw/PCA, frozen foundation, adapter를 비교한다.

E: 증강만 바꾼다. real-only, 단순 변환, calibrated simulator, generative augmentation을 비교하고 원본 정보 접근을 맞춘다.

F: fidelity를 바꾼다. helpful, uncorrelated, input-dependent wrong-trend source를 만들고 HF-only가 더 나은 경우를 포함한다. NARGP와 같이 관계가 비선형일 수 있다는 점을 반영한다. [R19](../../references/BIBLIOGRAPHY.md#r19)

모든 조합의 완전 factorial이 너무 비싸면 사전에 작은 단계별 설계를 선택하고, 제거한 상호작용을 한계로 기록한다. 유리한 조합만 사후 골라 보고하지 않는다.

## 6. 통계와 중단 규칙

여러 seed와 여러 독립 group split에서 paired 비교를 한다. bootstrap 단위는 donor·trajectory 등 일반화 단위여야 한다. Cell/window 단위 bootstrap만으로 연구 모집단의 신뢰구간을 만들어서는 안 된다. 유효 표본이 매우 적으면 CI가 불안정함을 그대로 밝히고, 정밀한 p-value보다 효과 크기·모든 실행 결과·실패 사례를 우선 공개한다.

목표 미달의 예산 곡선은 임의 보간으로 ‘도달 비용’을 만들어내지 않는다. 관측 예산 내 미도달로 기록한다. 의도한 성능 차이와 분산 정보가 없으면 필요한 donor 수를 확정 숫자로 제시하지 않는다. 먼저 pilot에서 분산을 추정하고 본시험 크기를 별도로 계획한다.

**제안 gate:** 기준선 재현 → 누수 audit 통과 → 실제 held-out 성능 유지 → coverage/폭 허용 범위 → 외부 조건 스트레스 시험 → 필요시 승인된 신규 실험. 허용 오차와 비용 절감 목표는 downstream 사용 목적에 따라 preregister한다. `95%` 같은 숫자는 CI 수준인지, coverage인지, 성공률인지 반드시 구분한다.

중단 사유는 잘못된 access 권한, unresolved overlap, 진단 불가능한 편향, HF-only 대비 악화, 드문 집단의 중대한 성능 저하, 또는 안전성 검토의 부재다. 방법을 억지로 복잡하게 만들어 통과시키지 않는다.

## 7. 단계별 실행 산출물

| 단계 | 산출물 | 통과 후에도 남는 한계 |
|---|---|---|
| P0 데이터 계약 | data card, group split, 출처·동의·버전 | 표본 자체의 대표성 |
| P1 공개 데이터 회귀시험 | 기준선 표, learning curve, leakage audit | retrospective AL은 실제 미관측 실험을 증명하지 않음 |
| P2 합성 스트레스 | wrong prior, hidden state, deceptive fidelity | simulator의 현실성 |
| P3 통합 prototype | acquisition log, model/equation cards | 독립 실험 검증 전 |
| P4 승인된 prospective 시험 | 신규 관측·비용·오류 기록 | 다른 기관·집단으로의 일반화 |

본 패키지는 P0/P1 설계와 교육용 합성 예제 수준의 자료다. 전체 P1 벤치마크나 P4 실험이 완료되었다는 뜻이 아니다.
