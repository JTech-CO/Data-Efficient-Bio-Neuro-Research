# 09. 폐루프 연구 구현 명세

**버전 1.1.0 · 연구용 합성 실험 · 2026-09-22**  
[English](../en/09_IMPLEMENTATION.md) · [연구 입구](../../README.ko.md) · [원 아키텍처](../../../docs/ko/02_ARCHITECTURE.md)

## 1. 이 버전의 목적

기존 문헌 조사와 연구 계획을 대체하지 않는다. 관측·가정·개입을 분리한다는 설계를 실제 코드에서 시험하고, 어떤 연구 질문을 다음에 다룰지 결정하는 실행 가능한 추가 모듈이다. 생물 데이터 없이 작동하며, 모든 측정은 알려진 함수를 이용한 합성 oracle에서 나온다. 실제 세포, 뉴런, 인체 또는 임상 모델을 만들었다는 뜻이 아니다.

핵심 질문은 “정확한 예측을 얻었는가?”에 더해 “어떤 측정으로 어떤 가정을 구분했고, 실패를 알아차렸는가?”이다. 원 문서의 H1·H2·H5 중 제한된 부분을 구현했다. H3는 출처 검사, H6는 진단 지표 수준이며, H4와 SINDy/PINN/BINN/UDE·파운데이션 미세조정은 구현하지 않았다. 원 계획의 완성이 아니라 실행 가능한 연구 단면이다.

## 2. 사용 방법

### Python에서 새 합성 실험 실행

저장소 루트에서 실행한다. Windows에서도 `python`이 올바른 인터프리터를 가리키는지 확인한다. 필요하면 `py`로 바꾼다.

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -r research/requirements.txt
python -m research.closed_loop serve
```

터미널의 `http://127.0.0.1:8765`를 연다. 화면의 “새 합성 실험 실행”은 Python 코어를 실제 호출하며, 결과는 `research/results/local/`에 저장된다. 이 서버는 동일 컴퓨터의 연구용이다. 인터넷 공개나 다중 사용자 서비스를 위한 서버가 아니다.

```bash
python -m research.closed_loop run --scenario mechanism_pair --policy guarded --seed 27 --budget 24 --output research/results/local-run.json
python -m research.closed_loop audit research/results/local-run.json
python -m research.closed_loop suite --config research/configs/pilot.json
```

`run`은 하나의 새 계산, `suite`는 504개 비교 실행, `audit`은 저장된 실행의 내부 일관성 검사다. `.json.gz` 실행 파일도 CLI audit이 직접 읽는다. 재실행하면 지정한 출력 경로의 파일이 갱신된다. 보존할 실험은 다른 `--output`을 지정한다.

### 설치 없이 기록 보기

압축을 모두 풀고 루트 `index.html`을 연다. 정적 모드와 GitHub Pages에서는 이미 계산한 **42개 설계 셀의 시드 0 기록**을 단계별로 재생한다. 12개 시드 전체의 통계도 표시한다. 재생은 새로운 학습이 아니다. 새 시드·예산을 계산하려면 로컬 서버가 필요하다.

UI는 한국어/영어, 반응형 레이아웃, 측정 채널 선택, 관측과 조건부 구간, 단계별 가정 기록, 다음 개입의 이유, 정책 비교, H1~H6 상태를 제공한다. 원시 JSON과 이벤트 로그를 저장하거나 실행 JSON을 가져올 수 있다. 가져온 JSON의 브라우저 형식 확인은 Python `audit`과 동등하지 않다. 외부 코드를 실행하거나 생물 데이터를 자동 업로드하지 않는다.

수록 데이터는 gzip을 base64로 내장하여 외부 요청 없이 푼다. `DecompressionStream`이 있는 현대 브라우저가 필요하다. 관련 공식 문서는 [구현 출처](../../SOURCES.md)에 있다. 전체 폴더를 보존해야 하며 `index.html`만 복사하면 작동하지 않는다.

## 3. 세 경계와 실행 순서

```text
관측 ledger (측정값·잡음·출처·분할)
  -> training만 적합 -> 재사용 diagnostic 점검
  -> 가정 register 갱신 -> 다음 query 제안과 비용 기록
  -> 합성 설계 내 실행 승인 -> oracle 측정 -> ledger 추가
  -> 반복 또는 예산/가정 오류 중단
  -> 모델 동결 -> 최종 test 1회 공개 -> 결과·추적 로그 저장
```

**관측:** `Measurement`와 `Ledger`가 측정값, 알려진 잡음 크기, 비용, train/validation/test, group, 부모 ID, 출처를 보존한다. 값의 의미는 관측 연산자에 의해 정해지며, 임의로 잠재 상태의 정답으로 승격하지 않는다.

**가정:** `assumptions.py`가 관측 연산자, 알려진 잡음, 커널 또는 유한 후보 집합, 식별성, fidelity 관계를 명시한다. 상태는 `not-rejected`, `challenged` 등이며 실제 참임을 인증하지 않는다. 잔차가 커졌다고 관측계 오류인지 기전 오류인지 자동 진단했다고 표시하지 않는다.

**개입:** `Query`가 조건, readout, 개입, fidelity, 반복, group을 포함한다. 제안과 승인과 측정 완료는 서로 다른 이벤트다. 현재의 승인은 허용된 합성 함수 호출만을 뜻한다. 실험실 장비 제어나 실제 연구 대상에 대한 개입 권한은 없다.

최종 참값은 평가기에서만 사용한다. 정책·모델 모듈은 oracle을 import하지 않는다. 최종 test 값을 바꿔도 앞선 질의가 변하지 않는 테스트가 포함된다. 가정 변경에 쓰는 validation은 최종 test가 아니며 반복 사용한다는 사실을 로그에 남긴다.

## 4. 실제 모델과 정책

### 4.1 관측 인식 선형 모델

잠재 계수는 \(\theta=(a,b)\)이고, 관측은 \(y=h(q)\theta+\epsilon\)이다. 합산 측정에서는 \(h=(x,x)\), 선택 측정에서는 \(h=(x,0)\), 두 번째 성분을 약화하는 합성 개입에서는 \(h=(x,0.2x)\)이다.

합산 측정만으로는 likelihood 설계행렬의 rank가 1이다. Bayesian prior 덕분에 posterior 공분산을 역산할 수 있어도 데이터가 두 계수를 식별했다는 뜻은 아니다. rank는 prior를 빼고 관측 설계 자체에서 계산한다. `identity` 제거 비교는 모든 readout을 \((x,x)\)로 취급하므로 측정 의미를 무시했을 때의 실패를 드러낸다.

후보 질의의 정보 점수는 \(\frac12\log(1+h\Sigma h^T/\sigma_q^2)\)이며 `information_gain`에서는 비용으로 나눈다. 대안으로 uniform random, 합산만 허용한 fixed readout, 관측 투영 분산을 비교한다. fixed readout은 같은 action space의 우열 비교가 아니라 **측정 채널 제한** 비교다.

같은 관측에 대한 알려진 관측 연산자 기반 가중 최소제곱 기준선도 계산한다. Bayesian 모형이 단순 관측 인식 회귀보다 특별히 우월하다는 결론은 전제하지 않는다.

### 4.2 유한 기전 후보

A는 \((x,x^2)\), B는 \((x^2,x)\)이다. 합산하면 동일하지만 선택 readout과 개입 후 관측은 다르다. 균등 prior에서 training likelihood만으로 후보 사후확률을 갱신한다.

획득 함수는 잠재 상태 간 거리 대신 **관측 공간의** \(I(M;Y_q\mid D)\)를 쓴다. 12점 Gauss-Hermite 적분으로 예상 log mixture density를 계산한다. 이는 선언한 두 후보 내부의 정보이득이며 세계 전체의 설명력을 뜻하지 않는다. 관측 예측 구간은 Gaussian 혼합의 CDF를 역산하고, 잠재 구간은 이산 후보 분포의 분위수다.

최대 사후확률이 0.95 미만이면 `selected_candidate=null`이다. 0.5/0.5 tie를 맞춘 것으로 세지 않는다. `mechanism_outside`는 A/B 모두 틀리게 구성하여 높은 사후확률과 실제 정답을 분리한다.

### 4.3 GP와 멀티피델리티

GP는 Cholesky 기반 exact posterior를 사용한다. 기본 RBF length 0.20, amplitude 1은 고정된 실험 가정이다. `guarded`는 최소 6개 관측 후 length 0.06 후보를 동일 diagnostic에서 비교하고, 짧은 커널의 RMSE가 기본의 0.85배 미만일 때 바꾼다. 매 5번째 질의는 무작위 탐색이다. 이 선택은 데이터 재사용을 포함하며 정식 보정 보장이 아니다.

멀티피델리티는 \(f_H=f_L+\delta\), \(\operatorname{Cov}=k_L+1_H1'_Hk_\delta\)인 **공동 GP**다. 저정밀 값을 고정된 가짜 HF label로 바꾸지 않는다. \(\rho=1\), discrepancy length 0.12/amplitude 0.35는 고정이며 학습되지 않는다. 획득 기준은 HF 목표 격자의 예상 분산 감소/비용이다. 네 번째마다 HF anchor를 넣는다.

`hf_only`는 초기 단계에서도 LF를 측정하거나 비용을 청구하지 않는다. `naive_pool`은 fidelity를 무시하는 의도적인 실패 기준선이다. `guarded`는 HF가 4개 이상일 때 diagnostic RMSE가 `1.15 × HF-only + 0.01`보다 나쁘면 HF-only로 전환한다. 잘못된 전환과 누락 가능성을 결과에 포함한다.

## 5. 가정 오류와 중단

진단은 standardized squared residual > 4, 관측 95% 구간 포함률 < 0.75, 선형 설계 rank < 2를 기록한다. 선형/기전 후보 `guarded`에서는 training 관측이 8개 이상이고 잔차 기준을 넘으면 중단한다. 선형 모델은 rank 2도 필요하다. 모든 진단 경고가 자동 중단으로 연결되는 것은 아니다.

최종 “목표 충족”은 잠재 RMSE ≤ 0.12, 관측 포함률 ≥ 0.80, 관측 구간 평균 폭 ≤ 0.80의 교집합이다. 이는 합성 예측 기준이지 생물학적 정확도 기준이나 기전 식별 성공 정의가 아니다. 중단에 따른 낮은 비용도 성공적 실험 절감으로 해석하지 않는다.

## 6. 경로와 확장 지점

| 코드 | 책임 |
|---|---|
| `contracts.py` / `adapters.py` | 불변 관측, 출처·분할 검사, 원 observation schema 연결 |
| `design.py` / `simulator.py` | 공개 설계와 숨긴 합성 참값의 분리 |
| `models.py` / `committee.py` | posterior, 관측 예측, 모델 카드 |
| `acquisition.py` | 비용·적격성·관측 공간 기반 질의 선택 |
| `assumptions.py` / `evaluation.py` | 가정 register, 재사용 진단, 최종 단회 평가 |
| `runner.py` / `suite.py` | 상태 전이, 비용, 이벤트, 실행 행렬, 집계 |
| `server.py` | loopback 전용 synthetic 실행 API |
| `lab/` | 외부 의존성이 없는 기록·실행 UI |

`Query.time`은 형식만 마련하고 **1.0 이외는 거부**한다. 연속 시간 동역학은 없다. 현재 noise_sd는 oracle가 제공하는 알려진 측정잡음이며 추정 결과가 아니다. 개체차도 없다. source별 불확실성 전파나 기전 학습 전체가 구현되었다고 확대 해석하지 않는다.

## 7. 데이터·보안 경계

훈련에는 `origin=simulated`이며 split=train인 직접 관측만 허용한다. generated/imputed/derived 기록은 부모·분할 검사를 통과해도 독립 증거처럼 fitting에 넣을 수 없다. 실제 생물학적 관측 수는 항상 0이며 real 입력을 거부한다. 이는 유용한 augmentation 자체를 부정하는 것이 아니라, 향후 그 효과를 별도 추정하기 위한 엄격한 기본값이다.

서버는 127.0.0.1에만 바인딩하고 Host/Origin/토큰을 검사한다. JSON 크기와 실행 설정을 제한하고 임의 경로·코드 실행을 제공하지 않는다. 단일 계산만 허용한다. TLS, 사용자 계정, 격리 컨테이너, 작업 큐, 개인정보 거버넌스는 없다. 외부에 노출하지 않는다.

로그의 hash chain은 정합성·변경 탐지용이다. 파일 작성자가 전체 체인을 다시 계산할 수 있으므로 서명이나 과학적 증명과 다르다. 저장 결과를 읽을 때 `audit`으로 재검사한다.

## 8. 재현 범위

알고리즘·seed·설정·Python/NumPy/SciPy 버전과 코드 fingerprint를 기록한다. 실행 시간은 결정성 해시에서 제외한다. 같은 환경에서 같은 입력은 같은 기록을 생성한다. 다른 BLAS/OS/라이브러리 버전의 마지막 비트까지 보장하지 않는다. CI 구성은 제공하지만 원격 실행 결과로 주장하지 않는다. [평가 계획](10_EVALUATION_PROTOCOL.md)과 [결과 해석](11_PILOT_RESULTS.md)을 함께 읽는다.
