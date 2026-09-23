# 28. 기술적 반복을 이용한 잡음·평균 오지정 분리

[English](../en/28_REPLICATE_DECOMPOSITION.md) · [Sources](../../bounded/references/REFERENCES.md) · [Research entry](../../../BOUNDED.md)


## 같은 입력의 차이와 평균은 다른 정보를 담는다

동일 위치 $x_j$에서 $r$회 관측 $Y_{jk}=m(x_j)+\epsilon_{jk}$를 얻는다. 겹치지 않는 쌍의 차이 $D_{jl}=(Y_{j,2l-1}-Y_{j,2l})/\sqrt2$는 공통 평균을 지운다. 독립이며 같은 분산인 오차라면 $E[D_{jl}^2]=\sigma_j^2$다. 이는 추정 평균식에 없는 항까지 잡음으로 흡수하지 않고 noise 정보를 얻는 통로다.

반복 평균은 평균식의 잔차를 드러낸다. 다음 항등식은 모든 적합 평균 $\hat m_j$에 성립한다.

$$\sum_{j,k}(Y_{jk}-\hat m_j)^2
=\sum_{j,k}(Y_{jk}-\bar Y_j)^2+\sum_j r(\bar Y_j-\hat m_j)^2.$$

왼쪽은 전체 SSE, 오른쪽 첫 항은 pure error, 둘째는 lack of fit이다. 항등식 자체와 F 검정의 정확한 참조분포를 구분한다. 후자는 독립·등분산 Gaussian 반복, 올바른 평균 귀무와 고정 설계가 필요하다. 이번 base 평균의 매개변수 수는 3이며 자유도는 각각 $N-J$, $J-3$이다. [B05](../../bounded/references/REFERENCES.md#b05)

## 동일 자료의 다섯 분석

| 이름 | 평균 | 잡음 정보 | 추가 불확실성 |
|---|---|---|---|
| pooled_base | 2차 | 전체 잔차의 단일 분산 | plug-in |
| residual_logvar_base | 2차 | 예비 평균의 제곱잔차를 logvariance로 적합 | plug-in |
| difference_logvar_base | 2차 | 독립 쌍 차이의 제곱 | plug-in |
| difference_logvar_plus | 2차 + sin(pi*x) | 동일한 쌍 차이 | plug-in |
| plus_bootstrap | 위의 확장 평균 | 쌍 차이를 다시 추정 | 조건부 모수 bootstrap 64회 |

앞의 네 분석은 같은 데이터셋에 적용한다. 추가 평균 기저는 평가 전에 고정했다. 정답 함수를 보고 검색한 식도 아니고 미지 기전 발견도 아니다. `local_missing`은 이 기저로 설명하기 어려운 좁은 변화를 별도로 넣는다.

$K=\lfloor r/2\rfloor$개의 제곱 차이 평균을 $Q_j$라 하면 독립 Gaussian 아래 $KQ_j/\sigma_j^2\sim\chi_K^2$다. 따라서 $\log Q_j$에 $\psi(K/2)+\log(2/K)$의 기대 편향을 보정하고, $\log\sigma^2(x)=\gamma_0+\gamma_1x$를 작은 ridge로 적합한다. 잔차 기반 비교도 같은 두 logvariance 계수를 사용하되 평균 오지정을 포함한 잔차에서 학습한다. 이 비교는 복잡한 GP나 원리 불명의 새로운 신경망이 아니다.

## 고정 총비용과 bootstrap

관측 48개를 24위치×2반복, 12위치×4반복, 8위치×6반복으로 나눈다. 반복 수가 늘수록 unique 위치는 줄어든다. 같은 피험자나 배치의 반복을 독립 생물 표본 수로 세지 않는다. 위치별 noise law와 평균 계수는 세계에 따라 달라진다.

bootstrap은 확장 평균과 분산 함수를 적합한 뒤, 동일한 입력에서 독립 Gaussian 합성 자료를 만들어 분산·평균을 함께 다시 적합한다. 평균 구간은 64개 적합 평균의 percentile, 새로운 관측은 64개 Gaussian 성분의 혼합 CDF로 계산한다. 혼합 NLL도 평가한다. 이것은 sampling uncertainty를 근사하는 **조건부 모수 bootstrap**이지 Bayesian posterior나 분포무관 95% 보장이 아니다. 64개의 재적합은 표본 수가 아니며 tail quantile의 Monte Carlo 분해능도 제한된다.

관측 81개짜리 final grid는 모든 fitting과 bootstrap 이후 새로 생성한다. 같은 final 자료를 평균 기저나 분산 함수를 선택하는 데 쓰지 않는다. 기본·확장 모델을 모두 보고하며 결과 이후 하나를 선택했다면 차기 연구 가설이다.

## 반드시 남긴 실패 조건

공유 배치오차 $U_j$가 반복 전체에 더해지면 차이에서는 지워진다. 따라서 $D^2$는 독립 noise만 추정하고 $Var(U_j)$를 놓칠 수 있다. 평균식의 잔차가 커졌다고 모두 생물학적 mean law 누락으로 단정할 수 없다. 데이터에 배치 ID가 있다고 이 불확실성이 자동으로 제거되지 않는다.

반복 내 순서 드리프트도 넣었다. 구현에서 학습은 -0.14~+0.14의 전체 단계를 포함하지만 최종 단일 관측은 새 배치의 첫 단계(-0.14)를 사용한다. 따라서 이 셀은 순수 잡음 비교가 아니라 **측정 단계의 이동도 포함한 스트레스 시험**이다. 관측 포함률의 저하를 분산 추정 하나의 효과로 해석하지 않는다.

분산 안정화를 위한 logvariance clip은 [-9,2]로 사전 고정하고 횟수를 남긴다. 수치 실패와 clip, 모든 불리한 성능은 분모에 유지한다. proper score가 좋아져도 latent 평균 오차가 줄지 않았다면 기전 개선이라고 부르지 않는다.
