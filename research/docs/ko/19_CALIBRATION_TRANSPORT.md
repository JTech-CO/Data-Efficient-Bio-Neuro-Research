# 19. D: 교정의 표본 전달 가능성

## 기존 동치와 새 정보

잠재 반응을 $z(x)=\theta_0+\theta_1x$, 표본 센서를 $y_s=g_s z+b_s+\epsilon$로 둔다. 외부 표준은 $y_c=g_cq+b_c+\epsilon_c$이다. $g_s=g_c, b_s=b_c$는 편리하지만 검증해야 하는 가정이다. 실제 계측의 commutability는 특정 측정 절차와 허용 편향 범위에 관한 속성이며, 본 합성 비교를 정식 commutability 검증으로 부르지 않는다. [T02](../../triad/references/REFERENCES.md#t02)

표본을 측정하면 $a_0=g_s\theta_0+b_s$, $a_1=g_s\theta_1$만 보인다. 알려진 증가량 $\Delta$를 추가하면 $y_{s,\Delta}=a_0+a_1x+g_s\Delta+\epsilon$여서 gain을 분리할 수 있다. 그러나 $\theta_0\mapsto\theta_0+c$, $b_s\mapsto b_s-g_sc$는 모든 표본·증가량 관측을 보존한다. **gain 식별과 offset 식별은 별개다.** 이 제한은 표준 첨가의 이동형 matrix effect 문제와 연결된다. [T01](../../triad/references/REFERENCES.md#t01)

## 다섯 프로토콜

| 프로토콜 | 추가 정보 | 확장 물리 매개변수 6개의 일반점 rank |
|---|---|---:|
| external_only | 표본 + 외부 표준 | 4 |
| addition_only | 위 + 알려진 표본 내 증가량 | 5 |
| addition_blank | 위 + 표본과 같은 배경의 latent=0 공백 | 6 |
| orthogonal_only | 표본 + 외부 표준 + 독립 교정된 $r=z+\eta$ | 6 |
| triangulated | 증가량 + 공백 + 독립 기준을 함께 검사 | 6 |

매개변수는 $(\theta_0,\theta_1,g_s,b_s,g_c,b_c)$이다. 독립 기준 경로는 $\theta_1\ne0$인 일반점에서의 결과다. 국소 rank는 모든 비선형 모형의 전역 식별성을 증명하지 않는다. 기준센서의 gain·offset까지 모두 자유 미지수로 두면 새로운 관측 열의 수만 늘려서는 잠재 척도를 고정하지 못할 수 있다.

외부 표준 -1/+1 각 두 번과 표본 다섯 위치 각 두 번으로 시작한다. 증가량은 세 위치에서 0.35/0.7, 공백은 두 번, 독립 기준은 다섯 위치를 측정한다. 일반 측정·표준·증가량의 비용은 1, 공백 2, 독립 기준 3이다. 48단위까지 남은 비용을 일반 측정으로 사용한다. 숫자는 무차원 합성 조건이며 실제 wet-lab 지시가 아니다.

## 추론과 검정

먼저 선형 계수 $(a_0,a_1,g_s,b_s,g_c,b_c)$를 알려진 관측분산으로 WLS 적합한다. 외부 표준만 또는 증가량만으로 식별하지 못하는 좌표에 대해 유일한 물리 매개변수 추정값을 반환하지 않는다. 대신 원래 외부 교정을 그대로 적용했을 때의 **가정 의존 baseline 오차**를 따로 보고한다.

공백과 증가량이 있으면 $\hat\theta_0=(\hat a_0-\hat b_s)/\hat g_s$, $\hat\theta_1=\hat a_1/\hat g_s$를 계산한다. 독립 기준 경로는 $r$로 $\theta$를 추정하고 일반 센서 계수와 결합한다. 비율과 교정 불확실성은 delta method로 전파한다. 작은 분모는 추정을 보류한다. 알려진 잡음 가정, Gaussian 근사, 비율의 비선형성 때문에 정확한 posterior나 보장된 95% 구간이라고 부르지 않는다.

관측식 lack-of-fit과 독립 기준의 모순을 각각 p<0.025로 검사한다. 전송 gain/offset의 Wald 비교는 별도의 p<0.05 검사다. 전송이 기각되지 않았다고 동등성이나 허용 오차 내 일치를 증명하지 않는다. 임상적으로 정한 허용 편향의 equivalence test는 구현하지 않았다.

상태는 `unresolved`, `identifiable-under-assumptions`, `contradicted`다. rank가 충분해도 마지막 상태로 갈 수 있고, 공통 오류로 인해 두 번째 상태에서 실제로 틀릴 수도 있다. `causal_source_identified=false`를 유지한다.

## 반증 세계

정상, gain만 변화, offset만 변화, 둘 모두 변화, 비선형 센서, 공백 불일치, 증가량 회수율 오류, 독립 기준 drift, 공통 anchor 오류를 각각 만든다. 하나의 reference도 이상적인 정답 접근권이 아니라 잡음·편향이 가능한 실제 합성 관측이다.

특히 `common_anchor_failure`에서는 표본의 좌표를 $z'=g_sz+b_s$로 바꾸고, 증가량의 실제 latent 변화는 $\Delta/g_s$, 공백은 0, 독립 기준은 $z'$를 반환한다. 모든 허용 관측은 정상 센서가 $z'$를 측정하는 세계와 동일하게 보인다. **같은 원인으로 오염된 여러 기준은 독립적인 척도의 증거를 추가하지 않는다.** 이 반례는 더 많은 센서만으로 보편적 정합성이 확보되지 않는다는 관측적 동치 증명이지 실제 실험실에서 이 정확한 오류가 발생한다는 빈도 추정이 아니다.

모든 프로토콜은 최종 센서 측정 33개의 관측 예측 NLL을 함께 기록한다. 센서 예측이 좋아도 latent 복원이 틀릴 수 있기 때문이다. 실제 latent 오차는 오직 평가기 truth에서 계산한다.

---
[English](../en/19_CALIBRATION_TRANSPORT.md) · [v1.3 entry](../../../TRIAD.md)
