# 모달리티별 적용 시나리오

**모든 파이프라인은 후속 구현·검증을 위한 제안이다. 공개 데이터나 생물학적 모델을 이 패키지에서 학습한 결과가 아니다.**

## A. 세포 영상 → 밀도 궤적 → 이동·증식 기전 후보

### 연구 질문

적은 전문가 segmentation으로 얻은 밀도 추정이, 보지 않은 배양 조건의 시간 변화 예측에 충분한가? 라벨링을 줄이는 것과 동역학 파라미터를 알아내는 것은 별도 목표다.

### 구성

CellSAM 또는 task-specific segmentation을 frozen/부분 미세조정 조건에서 비교한다. 모델의 이름만으로 승자를 고르지 않는다. CellSAM, Cellpose3, 특정 오가노이드 영상 비교는 서로 다른 연구 범위의 자료다. [R14](../../references/BIBLIOGRAPHY.md#r14) [R15](../../references/BIBLIOGRAPHY.md#r15) [R16](../../references/BIBLIOGRAPHY.md#r16)

원본 이미지와 수동 마스크를 보존하고, 객체별 불확실성으로 여러 밀도 궤적을 만든다. mask count를 평균으로만 합쳐 확정 관측처럼 넘기지 않는다. 반응·확산이 과제에 타당한 경우 `∂t c = ∇·(D(c)∇c)+R(c)`를 후보 구조로 둔다. BINN의 실제 assay 적용은 이 방향의 선행 사례다. [R07](../../references/BIBLIOGRAPHY.md#r07)

최초 기준선은 단순 segmentation 또는 검증된 기성 모델, logistic growth/상수 diffusion 모형, 일반 solver 적합이다. 이후 weak-form 식 추정 또는 제한된 BINN을 추가한다. 활성 라벨링은 segmentation ambiguity뿐 아니라 downstream density·parameter 변화에 민감한 프레임을 고르는 정책과 비교한다.

### 평가와 반증

평가는 donor/organoid/slide별로 분리한다. 객체 AP·count bias·경계 오류와 별개로 density rollout error를 보고한다. 예측이 좋아도 migration과 proliferation이 보상되어 식별되지 않으면 그 조합만 보고한다. 추가 readout이나 관측 조건 변화가 두 가설을 구분할 수 있는지 설계한다. 이는 직접 실험 프로토콜이 아니라 식별 정보의 요구사항이다.

주요 실패는 photobleaching을 세포 감소로, 병합된 마스크를 증식 억제로, 시야 밖 유출을 cell death로 잘못 해석하는 것이다. raw intensity, field geometry, observation process를 남겨 이 대안을 검토할 수 있게 한다.

## B. 단일세포 오믹스 → perturbation response 예측

### 연구 질문

새 기증자·세포주·개입에서 control 대비 변화량을 얼마나 맞추는가? cell-type classification이 좋은 것과 intervention forecasting이 좋은 것은 다른 문제다.

CELLxGENE Census는 관련 reference cells와 메타데이터의 탐색에 유용하다. 버전과 `is_primary_data` 등 중복 관련 메타데이터를 기록한다. 그러나 관찰 아틀라스가 곧 paired perturbation dataset은 아니다. 실제 개입 평가에는 R13 같은 benchmark가 연결하는 원자료와 실험 설계가 별도로 필요하다. [D01](../../references/BIBLIOGRAPHY.md#d01) [R13](../../references/BIBLIOGRAPHY.md#r13)

### 비교 설계

원 count의 preprocessing을 train에서 적합하고, no-change, 평균 변화, additive/linear, 생물 특징 기반 회귀, frozen foundation embedding + 동일 head를 비교한다. 그 다음에만 adapter를 켠다. donor·perturbation별로 나눈 train/test를 고정하고, 실제 보지 않은 gene intervention과 이미 보았지만 새 donor인 경우를 다른 task로 구분한다.

단순 예시로 기증자 5명에서 cell 10,000개를 얻었더라도 모집단 일반화의 독립 기증자가 10,000명인 것은 아니다. 이 수치는 설명을 위한 구성 예시다. gene ranking, binning, normalization이 입력 의미를 바꾸므로 같은 이름의 preprocessing이라고 가정하지 않고 실제 transform을 기록한다.

### 지표

`Δexpression = response - matched control`의 오차, perturbation별 결과, effect direction, 사전 지정된 gene panel에서의 변화량을 보고한다. 실제 test label을 본 뒤 가장 유리한 gene subset을 골라 primary score를 만들지 않는다. 전체 발현의 상관이 높아도 perturbation effect가 0에 가까운 no-change prediction일 수 있으므로 두 점수를 나눈다. 단순 기준선과 비교해야 하는 실증적 이유는 R13에 있다. [R13](../../references/BIBLIOGRAPHY.md#r13)

### 동역학 확장 조건

서로 다른 세포의 snapshot에서 얻은 pseudotime은 같은 세포를 연속 측정한 실제 시간과 다르다. 실시간·lineage·개입 정보를 확인하지 못한 경우 ‘trajectory-inspired model’이라고 부르고 kinetic rate의 실제 시간 단위를 임의로 부여하지 않는다. 생성 scRNA는 sensitivity analysis와 estimator stress test에 쓸 수 있지만, 반응하지 않는 새 cell type의 증거를 만들어내지는 않는다. [R21](../../references/BIBLIOGRAPHY.md#r21)

## C. EEG → 적은 개인 라벨로 새 사용자 예측

### 연구 질문

개인별 calibration label을 줄이면서 보지 않은 사용자에서 균형 정확도와 latency를 유지할 수 있는가? EEG 분류의 성공으로 해부학적 연결이나 질환 진단 기전을 주장하지 않는다.

초기 공개 데이터 후보는 PhysioNet EEG Motor Movement/Imagery 데이터다. 공식 문서상 event의 T1/T2 의미가 run 종류에 따라 달라지므로 label mapping을 run별로 작성한다. 원래 sampling rate·채널 이름·reference·artifact 처리 내역을 보존한다. [D03](../../references/BIBLIOGRAPHY.md#d03)

### 비교 설계

단순 spectral feature + ridge/logistic head, 소형 신경망, frozen LaBraM + 같은 head, 제한 adapter를 비교한다. 입력 sampling rate, amplitude scaling, channel order가 pretrained model 계약과 맞는지 먼저 검사한다. overlapping window로 늘어난 표본은 독립 관측 수에 포함하지 않는다.

LaBraM pretrained weights에 시험용 공개 데이터가 포함되었는지는 별도 audit 항목이다. NeuralBench의 PhysioNet Motor Imagery/TUAR 관련 overlap 경고를 반영한다. 이 데이터와 해당 pretrained weights의 조합은 완전히 새 dataset으로의 external generalization을 증명하는 primary track으로 쓰지 않고, contaminated/known-overlap track으로 표시하거나 다른 독립 세션·데이터를 확보한다. TUAB/TUEV 등 다른 데이터의 상태는 해당 문서의 구분을 따른다. [R17](../../references/BIBLIOGRAPHY.md#r17) [R18](../../references/BIBLIOGRAPHY.md#r18)

### 지표·획득·시각화

label budget별 macro-F1, subject별 성능 분포, worst-group, 실제 inference latency를 보고한다. AL이 움직임 artifact가 강한 구간만 선택하지 않는지, 같은 세션의 근접 구간을 중복 질의하지 않는지 확인한다. 신경신호의 예측구간과 분류 confidence를 혼동하지 않는다. 불확실한 샘플은 abstain 경로를 만들고, 전처리·모델·decision threshold를 함께 버전 관리한다.

## D. 신경·생화학 시뮬레이터 → 유일한 정답 대신 가능한 파라미터 분포

관측 우도를 직접 계산하기 어려운 simulator에는 SBI가 대안이다. 파라미터를 샘플링해 시뮬레이션하고, 관측과 양립하는 파라미터 분포를 추정한다. 신경 동역학에서의 선행 연구가 있다. [R25](../../references/BIBLIOGRAPHY.md#r25)

추가 연구 설계는 먼저 소형 검증 가능한 모델과 실제로 측정 가능한 readout을 고르는 것이다. 시뮬레이터 호출 예산을 따로 세고, posterior predictive check와 simulator misspecification stress test를 수행한다. 가짜로 좁은 posterior는 좋은 결과가 아니다. 서로 다른 파라미터가 관측을 똑같이 설명하면 그 다중해를 남긴다.

멀티피델리티는 동일 모델의 해상도·근사 정도처럼 correspondence가 정의된 경우부터 적용한다. 종·조직·장비가 달라지면 domain 문제인지부터 판단한다. 낮은 fidelity에서 posterior에 없는 잘못된 mode를 학습하지 않는지 확인하고 high-only 기준선을 유지한다. [R19](../../references/BIBLIOGRAPHY.md#r19) [R26](../../references/BIBLIOGRAPHY.md#r26)

## 추천 착수 순서

가장 작게 시작하려면 A에서 segmentation을 이미 검증된 도구로 고정하고 밀도 동역학만 비교하거나, D에서 known synthetic dynamics로 identification·acquisition을 시험한다. 오믹스와 EEG는 representation, batch, overlap이라는 별도 변수가 많으므로 처음부터 전 모달리티 통합 성과를 주장하지 않는다. 실제 어느 과제가 최선인지는 이용 가능한 독립 관측과 실험 접근권한으로 결정한다.
