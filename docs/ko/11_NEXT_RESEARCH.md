# 11. 다음 연구 방향: 경고의 원인을 분리하고 실패를 계측한다

[원래 연구 가설 H1~H6](06_RESEARCH_AGENDA.md)은 보존한다. 아래는 [합성 파일럿 결과](10_PILOT_RESULTS.md)로부터 도출한 **새 후속 계획**이며, 이미 구현하거나 입증한 결과가 아니다.

## 1. 질문의 변경

초기 질문은 ‘정보이득에 점검과 탐색을 붙이면 좋은가’였다. 파일럿은 그렇게 일반화할 근거를 주지 않았다. 이제 첫 질문을 다음처럼 좁힌다.

> **같은 점검 비용에서, 기전 불일치·관측 연산자 불일치·잡음 불일치를 구분할 수 있는 audit 설계가, 단순 잔차 경고보다 얼마나 유용한가?**

이는 큰 신경망을 먼저 도입해야 하는 질문이 아니다. 현재 가장 분명한 장애는 모델 용량보다 잘못된 관측·noise를 후보 기전 차이로 오해하거나, 두 번의 audit로 통과처럼 읽는 것이다. 단순 수집 기준선이 정상 조건에서 더 좋았다는 결과도 유지한다.

## 2. S2a: 원인 분리 점검 설계

기존 점검과 별도로 다음 세 readout family를 정의하는 simulator extension을 제안한다. 알려진 불변 입력을 관측하는 sensor-reference probe, 같은 조건을 반복하는 noise probe, 후보 동역학이 다르게 반응하는 intervention probe다. 새로운 probe에는 비용을 부여하고 초기·학습·진단 비용을 모두 동일 예산에 포함한다.

현재 코드에는 이 구분에 필요한 별도 reference 장치나 계측 채널이 없다. 기존 `pathway_b`를 이름만 바꿔 ‘교정 채널’이라고 부르지 않는다. 정답을 알려주는 특별한 probe도 허용하지 않는다. 각 probe에서 현실적으로 관측 가능한 정보와 알고 있는 reference 값을 simulator specification으로 먼저 정의한다.

비교는 고정 round-robin audit, 임의 audit, model-discrimination audit, 원인별 정보이득 audit를 같은 비용으로 한다. 문제 유형은 sensor-only, noise-only, dynamics-only, 두 요인의 동시 변화, 변화 없음으로 분리한다. 고정된 후보 모형이 여러 오차를 똑같이 설명할 수 있는 경우에는 원인 미확정 상태를 허용한다.

주요 지표는 오경보, 미탐지, 원인 혼동행렬, 경고 지연, 소모된 점검 비용이다. 최종 예측의 risk–coverage와 구간 폭도 함께 평가한다. 순차 threshold의 오류율을 주장하려면 별도 null simulation과 온라인 검정 이론 검토가 필요하다.

**중단 조건:** 원인 분리 probe가 없는 환경에서는 원인별 정확도를 꾸며내지 않는다. 원인 구분이 과도한 비용을 요구하면 ‘알 수 없음’과 예측 범위 제한을 유지한다.

## 3. S2b: 잡음 추정을 네 경로에 함께 전달

현재는 고정 noise를 fit, acquisition, audit, evaluation 모두가 사용한다. 다음 후보는 readout별 variance posterior 또는 계층적 variance pooling이다. 소표본에서 heteroscedastic GP를 즉시 학습시키기보다 일정 noise·readout별 noise·강건 likelihood를 단계적으로 비교한다.

중요한 점은 noise를 크게 잡아 모든 경고를 없애는 해법을 허용하지 않는 것이다. coverage만이 아니라 interval width, NLL, 예측 오차, 획득 가치의 변화를 함께 본다. noise와 unknown dynamics가 서로 보상하는 비식별성도 기록한다. 참 noise를 공개한 oracle-noise 기준선은 upper-information baseline으로 별도 표시하고 일반 방법과 같은 정보 접근으로 비교하지 않는다.

## 4. S2c: GP 전환 전에 보정 가능한 부분을 구분

이번 GP fallback은 넓고, 많은 경우 정확하지 않았다. 다음 단계에서는 세 가지를 같은 획득 데이터로 비교한다. 작은 observation correction, 후보 ODE에 제한된 discrepancy를 넣는 방식, 현재의 prediction-only GP다. 무엇이 바뀌었는지 식별할 수 없으면 기전 계수의 의미를 유지했다고 주장하지 않는다.

관측 보정과 기전 보정을 무제한 동시에 넣지 않는다. 각각의 amplitude·차원·정규화 규칙을 먼저 고정하고 profile likelihood 또는 posterior correlation으로 보상 관계를 점검한다. 이 비교에서 유의미한 오차 감소가 없으면 현재의 간단한 후보/GP 구조를 유지하거나 그 영역의 예측을 보류한다.

## 5. S2d: 같은 데이터와 같은 정책 효과를 분리

이번 policy comparison은 획득 경로와 모델 전환 효과가 함께 바뀐다. `guarded_no_gate`는 일부를 분리하지만, 예측 개선과 질의 개선 전체를 분해하지는 못한다. 후속에는 각 정책의 저장된 training ledger에 동일한 predictor bank를 사후 적합하는 crossed evaluation을 추가한다. 이때 audit/test의 역할은 그대로 유지한다.

획득 효과만 비교할 때 predictor와 학습 정보는 고정한다. 모델 효과만 비교할 때 query sequence와 관측은 고정한다. 완전 factorial이 부담되면 2~3개 predictor와 명시한 두 acquisition에 한정하고 생략한 상호작용을 문서화한다. 항상 단순 기전·릿지·GP 기준선을 포함한다.

## 6. 원래 H3~H6로 확장하는 조건

| 원래 가설 | 다음 진입 조건 | 아직 하지 않는 것 |
|---|---|---|
| H3 생성 정보 예산 | 관측 lineage와 실제/파생 학습 효과를 분리하는 기준선 확립 | 합성 수를 생물학적 표본 수로 계산 |
| H4 공유 구조·개체차 | 독립 simulator individual과 계층 추론의 검증 추가 | 한 세계의 반복 측정을 개인화라고 표시 |
| H5 조건부 fidelity | LF/HF의 관측 대상·paired 정보·비용·독립 검증 명세 | reference 필드를 low/high로 바꾼 것만으로 구현 선언 |
| H6 적응적 구간 | 타깃 분포와 feedback shift, 보정 데이터 역할 명시 | 명목 95%라는 이유만으로 OOD 보장 |

PINN/BINN/SINDy 또는 foundation encoder는 해당 역할의 작은 모델이 명확한 병목으로 확인된 다음 추가한다. 라이브러리를 import할 수 있다는 사실은 동작 경로·학습·평가가 구현되었다는 의미가 아니다.

## 7. 연구 기록 운영

이번 결과 `pilot/`은 원시 결과로 동결한다. 새 실험은 `results/s2a-*`처럼 별도 experiment ID와 설정 hash로 저장하고, 이전 결과를 덮어쓰지 않는다. configuration, hypothesis, expected failure, 실제 변경 코드, seed 목록, 결과 및 반증 여부를 함께 기록한다. external preregistration은 현재 없으며 추후 수행했을 때만 그렇게 부른다.

20개 개발 시드에 맞추어 gate를 튜닝한 뒤 같은 시드에서 성공했다고 발표하지 않는다. 개발 simulator와 unseen simulator family, parameter range, noise process를 구분한 검증을 둔다. 설정 범위 선택에는 분야 지식이 필요하며, 현재의 toy 범위를 실제 생물학적 작동 범위로 옮기지 않는다.

## 8. 실제 데이터가 가능한 시점

처음 실제 데이터 트랙은 폐루프 자동 실험이 아니라 제한된 retrospective replay로 시작한다. 데이터 접근 권한, donor/trajectory split, 장비·batch 메타데이터, preprocessing fit scope를 확정한다. 공개 데이터의 관측되지 않은 개입에 답이 있다고 가정해서 oracle처럼 질의하지 않는다. 가능한 질의 집합과 선택편향을 명시한다.

현재 저장소에 실측 ingestion이나 wet-lab executor를 추가하지 않았다. 데이터셋을 확보하기 전까지도 위 S2a~S2d의 합성 반증·진단 정확도·정보 경계 검증은 독립적으로 진행할 수 있다. 목표는 ‘어떤 조건에서 믿을 수 없는가’를 먼저 드러내는 연구 기반이다.
