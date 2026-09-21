# 용어 / Glossary

| Term | 한국어 설명 | English explanation |
|---|---|---|
| Estimand | 무엇을 추정하는지 정의한 대상 | The explicitly defined quantity being estimated |
| GP | 함수에 대한 확률분포로 하는 회귀 | Regression through distributions over functions |
| Bayesian nonparametric | 고정 소수 계수만으로 복잡도를 제한하지 않는 베이지안 모형 | Bayesian modeling without fixing complexity to a small parameter vector |
| Active learning | 다음에 확인할 라벨·관측을 고르는 정책 | A policy for selecting observations or labels |
| Bayesian optimization | 비싼 평가로 좋은 조건을 찾는 순차 최적화 | Sequential optimization of expensive objectives |
| Aleatoric uncertainty | 측정·현상 자체의 변동 | Variability in observations or the process |
| Epistemic uncertainty | 데이터·모형 지식의 부족에 관한 불확실성 | Uncertainty from limited knowledge and modeling |
| Structural identifiability | 이상적인 관측으로도 원 파라미터를 구분할 수 있는가 | Whether ideal observations distinguish parameters |
| Practical identifiability | 실제 제한된 데이터에서 충분히 정밀하게 구분되는가 | Whether available data constrain parameters sufficiently |
| Observability | 측정으로 숨은 상태를 구분할 수 있는가 | Whether measurements distinguish hidden states |
| Weak form | 점별 미분 대신 적분 관계를 사용하는 표현 | An integral formulation avoiding pointwise derivatives |
| SINDy | 후보 함수 중 소수 항으로 동역학을 표현 | Sparse identification in a candidate function library |
| PINN | 관측 적합과 방정식 제약을 학습에 결합 | Learning with data and differential-equation constraints |
| BINN | 이 자료에서는 Lagergren 등의 biological reaction-diffusion network | Here, the biological reaction-diffusion approach of Lagergren et al.; the acronym is not globally unique |
| UDE | 알려진 동역학과 학습 가능한 미지 항의 결합 | Known differential equations combined with learned components |
| Few-shot | 새 과제에서 소수의 라벨로 적응 | Adaptation using few new-task labels |
| Multifidelity | 서로 대응하는 정확도·비용 수준의 정보 결합 | Combining corresponding information at different accuracy/cost levels |
| Discrepancy | 모형·시뮬레이터와 대상 현상의 체계적 차이 | Systematic mismatch between model and target |
| Calibration | 선언한 확률·구간이 관측 빈도와 맞는 정도 | Agreement of stated probabilities or intervals with empirical outcomes |
| Conformal prediction | 특정 통계적 조건에서 예측집합을 보정하는 방법 | Prediction-set calibration under stated statistical conditions |
| SBI | 직접 우도 대신 시뮬레이션으로 하는 통계적 추론 | Statistical inference using simulations rather than tractable likelihoods |
| Provenance | 데이터가 어디에서 어떤 변환으로 왔는지 | The origin and transformation history of data |

Definitions are operational for this package; see [references](../references/BIBLIOGRAPHY.md) for formal treatments.
