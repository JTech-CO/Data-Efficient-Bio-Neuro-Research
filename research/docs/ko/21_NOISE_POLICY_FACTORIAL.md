# 21. F: 잡음 모형과 수집 정책의 분리

## 교차 설계

평균 모형은 모든 방법에서 같은 작은 3차원 기저 $\phi(x)=(1,x,(3x^2-1)/2)$다. 이를 고정해야 더 유연한 평균 모형의 효과를 잡음 추정의 효과로 잘못 해석하지 않는다.

각 세계에서 수집용 잡음 모형 3개(hom Gaussian, log-variance Gaussian, Student-t)와 정책 3개(random, spacefill, IVR)를 교차한다. 그 결과 생긴 **동일 관측을 최종 추정기 3개로 모두 재적합**한다. 따라서 세계당 수집 실행은 9개, 최종 평가 셀은 27개다. random과 spacefill은 수집용 모델을 보지 않으므로 세 controller에서 같은 데이터를 만들며 별도 독립 데이터셋으로 계산하지 않는다.

같은 데이터에서 추정기만 바꾼 비교와, 같은 controller·최종 추정기를 고정한 채 policy만 바꾼 비교를 각각 저장한다. 주어진 세계·좌표·반복·split의 잡음은 질의 키로 결정하므로 두 정책이 같은 질의를 하면 같은 관측이지만 서로 다른 질의에 같은 잡음을 억지로 배정하지 않는다.

## 추정기

일반 측정은 항상 같은 위치의 기술적 쌍이다. $d_i=(y_{i1}-y_{i2})/\sqrt2$의 제곱으로 공통 평균을 제거한 잡음 정보를 얻는다. 이는 반복과 탐색을 함께 다루는 기존 문헌과 연결되지만, 본 코드는 hetGP가 아니다. [T04](../../triad/references/REFERENCES.md#t04) [T05](../../triad/references/REFERENCES.md#t05)

1. **Homoscedastic Gaussian:** $\hat\sigma^2=\mathrm{mean}(d_i^2)$, 같은 기저의 OLS/WLS와 plug-in covariance.
2. **Log-variance Gaussian:** $\log \sigma^2(x)=a+bx$. Gaussian에서 $E[\log(d_i^2)]=\log\sigma_i^2+\psi(1/2)+\log2$를 이용하고 slope에 고정된 약한 ridge를 준다. 실제 loglinear 이분산에는 맞지만 비단조 잡음이나 heavy tail에서는 틀릴 수 있다.
3. **Student-t:** 자유도 4를 미리 고정하고 평균 계수와 scale을 IRLS로 갱신한다. 중단 기준과 반복 상한을 저장하고 미수렴을 숨기지 않는다. Student-t의 견고성은 추론과 수렴 문제를 없애지 않는다. [T06](../../triad/references/REFERENCES.md#t06)

잡음 함수를 적분한 완전 Bayesian posterior는 구현하지 않았다. noise 계수와 scale은 plug-in이고, Student-t 계수 공분산은 기대 정보·IRLS 근사다. 예측에서 Student-t 잡음과 평균 오차를 합하는 단계도 분산을 맞춘 Student-t 근사다. 출력 확률분포 자체를 명시적으로 정의하여 score를 계산하지만 정확한 생성 posterior라고 주장하지 않는다.

## 정책과 예산

초기 다섯 위치 -1,-0.5,0,0.5,1에서 각 두 번 측정한다. 전체 수집 예산은 48, 질의 후보는 [-1,1]의 41점이다. 반복 측정도 후보에 포함된다. 공간 채우기는 기존 위치로부터 최대 거리를 선택한다.

IVR은 공개 uniform target grid의 적분 평균분산을 줄이는 1단계 근사다. 기저 공분산 C, $M=E[\phi\phi^T]$에서

$$U(x)=\frac{\phi(x)^T C M C\phi(x)}{\hat\sigma^2(x)/2+\phi(x)^T C\phi(x)}.$$

쌍의 비용이 모두 같으므로 순서는 비용 정규화와 같다. Student-t의 경우 분산으로 근사한 IVR이지 실제 t 우도의 정확한 정보이득이 아니다. 잡음 추정이 달라지면 수집 위치도 달라질 수 있으므로, 최종 추정기 교체와 이 효과를 분리한다.

## 평가

정상 Gaussian, loglinear 이분산, 비단조 이분산, 같은 분산의 t3, 드문 큰 잡음 오염, 평균식 누락을 각각 시험한다. 평균식 누락은 동일한 작은 기저가 사실을 담지 못하는 경우이며 더 견고한 우도만으로 기전이 발견되었다고 보지 않는다.

모델을 동결한 뒤 81개 새 test 관측을 한 번 연다. latent RMSE, 관측 NLL, CRPS, 관측·latent 포함률, 관측 구간 폭과 수렴 상태를 함께 기록한다. NLL은 밀도이므로 음수가 가능하고 값이 낮을수록 좋다. CRPS는 Gaussian·Student-t의 명시적 식을 사용하며 수치적 적분과 일치하는지 테스트했다. 포함률이나 폭만으로 우월성을 주장하지 않는 이유는 proper scoring rule의 취지와 같다. [T07](../../triad/references/REFERENCES.md#t07)

계획된 쌍 비교의 bootstrap은 같은 합성 세계 ID를 재표집한다. 작은 모형·고정 자유도·관측비·이분산 함수의 선택에 의존하므로 범용 우월성으로 확장하지 않는다. Mean-capacity, calibration transport, biological donor variation은 이 과제에서 함께 추정하지 않는다.

---
[English](../en/21_NOISE_POLICY_FACTORIAL.md) · [v1.3 entry](../../../TRIAD.md)
