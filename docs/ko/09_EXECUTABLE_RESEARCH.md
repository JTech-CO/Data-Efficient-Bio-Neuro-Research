# 09. 관측·가정·개입 폐루프의 실행 가능한 연구 단계

**상태: 합성 데이터 전용 연구 구현 0.1.0. 생물학적 프로덕션 모델이 아니다.**

[연구 입구](../../RESEARCH_LAB.md) · [결과](10_PILOT_RESULTS.md) · [후속 방향](11_NEXT_RESEARCH.md)

## 1. 원래 계획과의 관계

[02_ARCHITECTURE](02_ARCHITECTURE.md)의 관측·모델·실험설계·검증 분리를 구현하고, [03_EVALUATION](03_EVALUATION.md)의 동일 정보 접근, 비용 기록, 분할, 실패 조건을 작은 합성 과제에서 실행했다. 01~08장의 원문은 수정하지 않았다. 원문에 남아 있는 ‘전체 시스템 미구현’ 표현은 원래 연구 단계의 상태이며, 이번 추가 자료가 전 영역의 구현 완료를 의미하지도 않는다.

범위는 H1(경쟁 가정을 구분하는 질의)과 H2(관측 연산자를 잘못 두었을 때의 손실)의 **제한된 검증**이다. 기존 단계표상 P0 계약의 일부와 P2 합성 스트레스, P3 통합 루프의 작은 부분을 실행했다. P1 공개 실제 데이터 회귀시험, P4 실제 prospective 실험은 수행하지 않았다.

이 작업의 결과물은 미래의 큰 모델을 위한 비어 있는 인터페이스만이 아니다. CPU에서 실제로 관측을 생성하고, posterior를 갱신하고, 다음 질의를 선택하고, 비용을 지출하고, 진단에 따라 예측 경로를 바꾸며, 완료된 기록을 독립 평가하는 코드다.

## 2. 의도적으로 작은 동역학

두 상태 A, B와 계수 a, b를 가진 합성 세계를 사용한다. x는 입력 조건, u는 개입 강도, t는 시점이다. 상태나 단위는 특정 세포·뉴런·약물을 뜻하지 않는다.

$$A(t)=a x(1-u)e^{-t}$$

$$B_{parallel}(t)=b x e^{-0.45t}$$

$$B_{compensatory}(t)=bxe^{-0.45t}+0.8aux(1-e^{-0.45t})$$

이는 알려진 선형 ODE의 해다. `A'=-A`, `B'=-0.45B` 또는 `B'=-0.45B+0.45·0.8aux`를 사용한다. 초기조건은 `A(0)=ax(1-u)`, `B(0)=bx`다. 감쇠율과 보상 형태는 학습하지 않는다. 각 후보에서 a,b만 Gaussian prior `N([1,1],0.36 I)`와 Gaussian observation likelihood로 추정한다. Gaussian prior에는 음수 꼬리도 있으므로 생리학적 양성 제약을 보장하지 않는다.

u=0이면 두 후보가 정확히 같은 관측을 만든다. 따라서 관측만 허용하는 트랙은 후보 모델을 구분하지 못하도록 의도적으로 구성했다. 이는 모든 생물계의 식별 불가능성을 주장하는 예제가 아니라, 특정 관측 설계에서의 정확한 반례다. 후보 모델의 구분과 단일 모델 안의 계수 식별을 구분해야 한다는 동기는 [E03](../../research_lab/provenance/LITERATURE.md#e03)과 연결된다.

## 3. 관측값은 상태가 아니다

명목 관측은 `y = w_A(t) A + w_B(t) B + offset(t) + epsilon`이다. `offset=0.10+0.035t`, 광학 감쇠를 흉내 낸 gain은 `exp(-0.18t)`다. 혼합 readout의 기본 가중치는 `(1,0.4)`, A 전용은 `(1,0)`, B 전용은 `(0,0.8)`이다. noise 표준편차는 각각 0.12, 0.075, 0.055로 둔다.

이 값들은 합성 설계에서 공급한 **명목 메타데이터**다. 실제 장비를 교정하거나 관측 연산자를 데이터에서 추정한 결과가 아니다. `identity` 제거 실험은 감쇠·혼합·offset을 무시한 가정을 사용한다. 관측 가정이 맞는 경우와 틀린 경우의 차이를 보는 것이지, 자동 교정 성공을 입증하는 실험이 아니다.

## 4. 실행 흐름과 모듈

| 계층 | 파일 | 실제 역할 |
|---|---|---|
| 계약 | `contracts.py` | query, 비용, 관측 가정, 실행 설정 검증 |
| 증거 | `ledger.py` | 원본 스키마 호환 기록, 역할 분리, 추가 전용 해시 연결 |
| 가정 모델 | `models.py` | 두 ODE 후보의 베이지안 계수 추정, marginal likelihood, 구간 |
| 설계 | `policies.py`, `design.py` | 모델 정보이득·계수 정보이득·분산·탐색·비용 비교 |
| 진단 | `diagnostics.py` | fit에 쓰지 않는 사전 예측 잔차로 경고 |
| 시뮬레이터 | `simulator.py` | 외부 환경에 해당하는 합성 oracle |
| 루프 | `engine.py` | 제안, 합성 허용 목록 승인, 측정, 기록, 갱신 |
| 사후 평가 | `evaluation.py` | 수집 종료 후 정답·held-out·외삽으로 평가 |
| 실행·표시 | `runner.py`, `server.py`, `web/` | CLI, localhost API, 한·영 검토 화면 |

모델·정책·계약 모듈은 simulator와 evaluator를 import하지 않는다. engine에는 oracle 객체가 아니라 측정 callable만 전달한다. Python 메모리 내부를 악의적으로 조사할 수 없게 만든 보안 격리는 아니며, 정상 실행에서 정보 흐름을 제한하는 소프트웨어 경계다.

## 5. 획득 함수의 실제 의미

`model_information`은 스칼라 관측의 Gaussian mixture에 대해 `I(M;Y|D,q)/cost(q)`를 계산한다. 후보별 posterior predictive 적분에는 20점 Gauss-Hermite quadrature를 쓴다. `guarded_information`의 평상시 score는 다음과 같다.

$$S(q)=\frac{I(M;Y_q\mid D)+0.15\sum_Mp(M\mid D)I(\theta_M;Y_q\mid D,M)}{C(q)}$$

후자의 계수 정보는 선형 Gaussian 모델에서 `0.5 log(1+latent_variance/noise_variance)`로 계산한다. 모델 정보와 계수 정보는 로그에 따로 남긴다. 가중치 0.15와 탐색 주기 4는 연구 설정값이며 검증된 최적값이 아니다. 네 번째 adaptive acquisition마다 공간 채우기 탐색을 수행한다. [E01](../../research_lab/provenance/LITERATURE.md#e01)은 개입을 별도로 표현하는 동기이지, 이 score가 논문의 CIV를 구현했다는 뜻이 아니다.

합성 후보는 x=0.4/0.9/1.4, t=0.4/1.2/2.4, 세 readout, u=0/1로 구성한 54개다. 관측만 허용하는 트랙은 9개다. adaptive 질의는 중복하지 않는다. 반복 관측은 별도 replicate ID를 가진 audit로만 실행한다. 임의의 반복 횟수·fidelity를 능동적으로 최적화하는 기능은 아직 없다.

## 6. 점검과 판단 보류의 범위

초기 네 측정은 모든 정책이 공유한다. adaptive 측정 세 번마다 고정 audit 질의를 하나 수행한다. 그 값은 posterior 적합에서 제외한다. 관측 전 mixture 평균·분산으로 계산한 표준화 잔차의 절댓값이 2.5를 초과한 사례가 최근 세 audit 중 두 개이면 경고를 유지한다.

이는 다중·순차검정을 보정한 통계적 검정이 아니다. 경고는 모델의 어떤 가정이 틀렸는지도 특정하지 못한다. 특히 24 비용 단위에서 audit가 대체로 두 개뿐이므로 ‘경고 없음’을 ‘적합성 통과’로 바꾸어서는 안 된다. 적응적 설계의 가정 불일치 위험은 [E02](../../research_lab/provenance/LITERATURE.md#e02)에서도 동기를 얻지만, 본 규칙에는 그 논문의 보장이 없다.

경고 시 guarded 정책은 두 후보에서 강제로 기전을 고르지 않고, query 좌표상의 고정 RBF GP로 예측을 전환하며 비용당 GP 분산으로 다음 점을 선택한다. 이 GP는 알려지지 않은 생물학적 식을 발견하지 않는다. 학습 데이터에 새 latent state나 pseudo-label을 생성하지도 않는다. fixed kernel, known nominal noise를 사용하므로 GP 자신도 틀릴 수 있다.

최대 후보 posterior가 0.95 이상이고 해당 선형 설계 행렬의 rank가 2이면 `candidate_preference`를 기록할 수 있다. guarded 경고가 있으면 보류한다. 어떤 경우에도 `mechanism-supported`를 자동 부여하지 않는다. rank 진단은 이 작은 선형 계수 문제의 수치 진단이지 일반적 structural-identifiability 검사기가 아니다.

## 7. 출처·분할·비용 계약

모든 simulator 측정은 기존 `schemas/observation.schema.json`에 맞는 `kind=simulated`이고 `counts_as_new_biological_unit=false`다. 외부 envelope에 query, 역할, 비용, 명목 noise, 이전 기록 해시를 붙였다. 생성·대체·실측 데이터를 runner에 넣으려 하면 거절한다. 미래 데이터 어댑터를 개발하지 않고 ‘실측 입력 지원’처럼 표시하지 않는다.

train은 적합, audit는 진단, test/OOD는 사후 평가에만 사용한다. audit를 최종 test로 다시 부르지 않는다. 한 simulator world에서 반복된 synthetic 측정은 서로 다른 생물 개체가 아니다. 총 비용에는 초기·adaptive·audit가 모두 들어간다. 테스트 oracle 호출은 별도 진단 비용으로 공개하되 acquisition 예산에는 넣지 않는다.

## 8. 실행 및 결과 확인

```bash
python -m pip install -r requirements-lab.txt
python -m research_lab serve
python -m research_lab run --scenario sensor_shift --seed 7 --out research_lab/results/sensor-seed7.json
python -m research_lab benchmark --out research_lab/results/new-pilot
```

저장소 루트에서 실행한다. `serve`가 출력한 loopback URL을 연다. 서버는 다운로드한 모델이나 GPU 없이 Python으로 실제 계산한다. JSON 기록을 저장하거나 다시 불러올 수 있다. 파일을 직접 열거나 GitHub Pages로 배포하면 기록 검토 전용이며, 실행 버튼은 비활성화되고 로컬 실행 명령을 안내한다. 정적 모드의 replay는 완료된 기록 재생이다.

Windows용 `research_lab/launch-windows.bat`, Unix용 `launch-unix.sh`도 포함하지만 의존성을 먼저 설치해야 한다. 네이티브 Windows/macOS 실행과 원격 GitHub Pages 배포는 이번 환경에서 검증하지 않았다.

## 9. 확장 계약

새 후보식은 `features`와 별도 model adapter로 추가하되 truth 코드와 learner 코드를 분리한다. 비선형 계수나 latent observation으로 확장하면 현재의 conjugate 계산이 더 이상 정확하지 않을 수 있으므로 추론 방법과 구간 의미를 다시 문서화해야 한다. 새 noise model은 fit, acquisition, audit, evaluation 네 경로 모두에 전달해야 한다. 실제 데이터 지원은 별도 access·consent·group split·원본 계보 검토를 통과한 후 추가한다. 기존 함수의 입력 검사를 풀어서 연결하지 않는다.
