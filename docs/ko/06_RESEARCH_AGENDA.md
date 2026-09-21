# 개선을 위한 연구 가설과 반증 계획

## 1. 무엇이 새롭고 무엇이 새롭지 않은가

GP+AL, weak/ensemble SINDy, PINN+SR, hybrid UDE, multi-fidelity GP, foundation fine-tuning은 이미 알려진 방향이다. 이들을 연결했다고 새로운 이론의 발명이나 선행기술의 부재를 주장하지 않는다. 본 문서의 독창성 후보는 **관측·가정·계보·반증 실험을 연결하는 문제 정의와 평가 구성**이며, novelty 검증 및 실증은 후속 작업이다. [R05](../../references/BIBLIOGRAPHY.md#r05) [R08](../../references/BIBLIOGRAPHY.md#r08) [R09](../../references/BIBLIOGRAPHY.md#r09) [R19](../../references/BIBLIOGRAPHY.md#r19)

## H1. 가장 불확실한 값 대신 가장 잘 구분되는 가정을 질의한다

가설: 관측 noise가 큰 샘플을 반복하는 대신, 경쟁 기전의 예측 차이가 크고 실제 readout으로 구분 가능한 실험을 선택하면 동일 비용에서 기전 선택 정확도가 높아진다.

가장 가까운 선행방향은 GPAL의 설계와 Ensemble-SINDy의 능동학습이다. 비교군은 random, maximum latent variance, 정보이득, model-discrimination acquisition이다. 참 모델이 후보 집합 안에 있는 시험과 밖에 있는 시험을 모두 둔다. 후보 밖에서 과신하고 false discovery가 늘면 가설의 일반적 이점을 반증한다. [R02](../../references/BIBLIOGRAPHY.md#r02) [R05](../../references/BIBLIOGRAPHY.md#r05)

차별화 후보는 measurement operator와 replicate cost를 포함해 ‘구분될 것으로 보이지만 실제 센서로는 관측되지 않는’ 질의를 제거하는 부분이다. 단순한 ensemble disagreement 재명명만으로 신규성을 주장할 수 없다.

## H2. PINN 제약 강화보다 관측모형 교정이 효과적일 수 있다

가설: 일부 저표본 문제에서는 residual loss를 줄이는 것보다 intensity·count·voltage의 관측 편향을 설명하는 것이, 개입 외삽과 계수 안정성을 더 크게 개선한다.

`known state + noise`, `hidden state + correct observation`, `hidden state + biased observation`의 세 시험을 설계한다. vanilla PINN, reweighted PINN, ordinary solver likelihood, observation-aware UDE를 비교한다. 모든 조건에서 UDE가 이길 필요는 없다. 충분히 정확한 관측과 작은 기전모형에서 복잡한 observation layer가 오히려 손해라면 그 범위를 명시한다. 선행 UDE·BINN 결과가 동기이며, 이 비교 결과는 아직 없다. [R07](../../references/BIBLIOGRAPHY.md#r07) [R10](../../references/BIBLIOGRAPHY.md#r10)

## H3. 생성 데이터의 수보다 독립 증거 예산을 관리한다

가설: provenance-aware weighting과 real-only validation gate를 쓰면, naive synthetic oversampling보다 OOD 성능 악화와 과신을 줄일 수 있다.

같은 training data에서 generator를 적합하고, 생성량을 늘리는 조건·여러 simulator prior를 섞는 조건·외부 pretrained prior를 쓰는 조건을 구분한다. 실제 donor 수는 고정한다. generative augmentation이 더 낫더라도 이득이 새 정보인지 regularization인지 해석을 나눈다. 데이터 계보를 둔다고 통계적 편향이 자동 제거되지는 않으므로, gate가 해로운 증강을 얼마나 실제 탐지했는지도 평가한다. [R21](../../references/BIBLIOGRAPHY.md#r21) [R22](../../references/BIBLIOGRAPHY.md#r22)

## H4. 하나의 전역 방정식보다 공유 구조와 개체차를 분리한다

가설: 모든 개체에 한 방정식을 강요하거나 개체별 독립 모형만 쓰는 것보다, 공유된 후보항과 개인별 계수를 구분하는 계층적 sparse 모델이 적은 donor에서 더 안정적일 수 있다.

비교군은 pooled SINDy, 개인별 SINDy, 계층 mixed-effect 또는 hierarchical GP, 제안 hierarchical sparse dynamics이다. 공통 기전이 맞는 경우와 개체별 구조 자체가 다른 경우를 분리한다. 식별가능성을 먼저 검사하고, 관측하지 않은 개체차를 ‘개인화 성공’으로 포장하지 않는다. 희소 구조가 개체차를 과도하게 평탄화하면 가설이 깨진다. [R06](../../references/BIBLIOGRAPHY.md#r06)

## H5. fidelity를 고정 순위가 아니라 조건부 신뢰 관계로 다룬다

가설: 짝지은 calibration과 입력 의존 discrepancy를 함께 사용하면, 저정밀 소스가 일부 영역에서 잘못된 방향을 보일 때 negative transfer를 줄일 수 있다.

NARGP·cost-aware KG를 기준선으로 두므로, 이 발상 자체는 새롭지 않다. 생물학적 domain shift, 제한된 paired samples, downstream acquisition과 calibration을 결합한 평가가 연구 후보이다. high-only가 항상 비슷하거나 더 좋다면 비용 이득 주장을 철회한다. [R19](../../references/BIBLIOGRAPHY.md#r19) [R20](../../references/BIBLIOGRAPHY.md#r20)

## H6. 적응적 수집 후에도 구간이 의사결정에 쓸모있는가

가설: 목표에 맞는 shift-aware calibration은 과신을 줄이지만, shift가 크면 구간이 너무 넓어져 실용 이득이 사라질 수 있다.

표준 split conformal과 feedback-shift에 맞는 방법, raw GP interval을 비교한다. coverage뿐 아니라 width, abstention, cost-to-decision을 측정한다. 입력 density ratio가 불명확하거나 `P(y|x)`가 변하면 정리의 조건이 깨진 것으로 기록한다. FCS conformal 선행연구의 보장을 무조건적인 온라인 제어 보장으로 확대하지 않는다. [R23](../../references/BIBLIOGRAPHY.md#r23) [R24](../../references/BIBLIOGRAPHY.md#r24)

## 2. 첫 논문화 가능한 질문의 선택

가장 권장하는 좁은 질문은 H1+H2의 조합이다. **‘제한된 관측 연산자와 실험 비용을 고려한 기전 구분 획득 정책이, 표준 불확실성 획득보다 어떤 조건에서 더 유용한가?’** 합성 known-truth 사례, 공개 실제 데이터 replay, 승인된 소규모 prospective 실험을 별도로 설계한다. 데이터 replay만으로 prospective 성공을 주장하지 않는다.

부정 결과도 산출물이다. 어느 잡음·관측·domain 조건에서 복잡한 방법이 단순 회귀보다 나쁜지 경계도를 만드는 것은, 새 알고리즘의 성공 사례만 보이는 것보다 후속 구현 판단에 유용하다.
