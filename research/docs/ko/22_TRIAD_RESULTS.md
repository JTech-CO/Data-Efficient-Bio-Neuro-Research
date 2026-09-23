# 22. 세 후속 연구의 결과: 새 관측은 정보를 늘리지만, 기준 가정을 없애지는 않는다

**v1.3.0-research.1 · 완료된 평가: D 3,600 + E 10,560 + F 2,160 = 16,320개 실행. 실제 생물학적 관측 0개.** F는 2,160개 수집 실행에 세 최종 추정기를 적용한 6,480개 적합이며, 중복을 제거한 수집 데이터셋은 1,200개다. 재사용·정책 비교·검정 규칙 수를 독립 표본으로 계산하지 않는다.

[English](../en/22_TRIAD_RESULTS.md) · [설계](18_TRIAD_DESIGN.md) · [모든 수치](../../triad/results/v130/summary.json) · [짝지은 비교](../../triad/results/v130/paired_comparisons.json)

이 문서의 수치는 동봉 코드의 실제 실행값이다. 논문 수치를 가져온 것이 아니다. 최종 bank는 `evaluation-v130-c`, 시드는 41000부터다. 부동소수점 좌표 계보 오류로 첫 부분 평가를 중단한 뒤 새 bank에서 전부 재실행했다. 전체 수정 이력은 18장과 QA에 있다. 개발자에게 생성기가 알려진 탐색적 합성 연구이며, 독립 사전등록·외부 블라인드 검증이 아니다.

## 1. D: 표준 첨가, 공백, 독립 기준은 서로 다른 모호성을 없앤다

확장 물리 매개변수 여섯 개를 기준으로 외부 교정만은 rank 4, 첨가만은 rank 5, 공백 또는 유효 독립 기준을 더하면 rank 6이었다. 더 많은 동일 측정이 이 rank의 모호성을 자동으로 제거하지 않는다. 첨가만에서는 gain은 분리해도 offset과 잠재 절편은 여전히 섞인다. 이 구분은 표준 첨가의 translational matrix effect 한계와 연결된다. [T01](../../triad/references/REFERENCES.md#t01)

표본 gain·offset이 모두 바뀐 세계에서 외부 교정을 그대로 전달한 가정 기준선의 RMSE는 0.5968이었다. 새 관측을 쓰면 첨가+공백 0.0602, 독립 기준 0.0298, 세 기준 교차 점검 0.0624였다. 모두 수집비 48이다. 그러나 정상 세계에서는 단순 외부 교정 가정이 실제로 맞으므로 이 가정 기준선은 0.0399, 첨가+공백은 0.0788이었다. 추가 정보가 비용·잡음까지 무시한 보편적 우위를 뜻하지 않는다. 외부 가정 기준선은 유일한 물리 매개변수 추정으로 승격하지 않았다.

교차 점검은 고장 난 기준을 알아차리는 데 도움을 주지만 자동으로 결과를 고치지는 않는다. 공백 기준이 틀린 세계에서 첨가+공백의 모형 충돌은 2/80, 교차 점검은 63/80이었다. 그럼에도 현재 교차 점검의 점추정은 첨가+공백 경로를 유지하므로 RMSE는 각각 0.2264와 0.2277이다. 독립 기준만 쓰는 경우는 0.0298이었다. 반대로 독립 기준이 드리프트한 세계에서는 독립 기준 RMSE 0.3804, 첨가+공백 0.0780, 교차 점검 0.0840이었다. 하나의 기준을 무조건 신뢰하는 기본값은 채택하지 않는다.

세 기준이 함께 편향된 반례에서 교차 점검도 5/80만 모형 충돌을 표시했고 RMSE는 0.5995였다. 이것은 우연한 구현 실패만이 아니라 19장의 관측적 동치 반례다. `identifiable-under-assumptions`는 그 가정이 진실임을 인증하지 않는다. 모든 기록의 `causal_source_identified=false`를 유지했다. 실제 commutability 판정은 측정 절차와 허용 편향·불확실성 기준에 종속되며, 여기의 통계적 동일성 기각을 그 실무 판정으로 대체하지 않는다. [T02](../../triad/references/REFERENCES.md#t02)

## 2. E: 위치를 분산하면 좁은 오류를 더 자주 만나지만, 비용과 잡음 가정이 남는다

예산 48, 대조 측정비 1의 24쌍 조건에서 좁은 오류의 Bonferroni any-alarm 비율은 고정 3지점 6/64(9.4%), 균일 37/64(57.8%), 층화 46/64(71.9%), 최대 공백 48/64(75.0%), 적응+탐색 46/64(71.9%)였다. 같은 조건의 정상 256세계 경고는 각각 10/256(3.9%), 17/256(6.6%), 10/256(3.9%), 13/256(5.1%), 11/256(4.3%)다. 이 한 bank의 점추정치로 모든 정책이 5% 이하라고 주장하지 않는다. 각 비율의 Wilson 구간은 JSON에 있다.

가장 복잡한 적응 정책이 항상 낮은 누락을 만들지 않았다. 넓은 위치를 우선 탐색하는 단순 최대 공백 정책도 강한 기준선이었다. 약한 오류에서는 최대 공백조차 13/64(20.3%)만 경고했다. 좁은 오류의 위치에 들어가는 것과 유의한 대비를 확보하는 것도 별개의 문제다.

대조 측정비가 1에서 3으로 커지면 같은 예산 48에서 24쌍 대신 12쌍만 얻는다. 최대 공백의 좁은 오류 경고는 48/64에서 31/64로 줄었다. 이는 정책 재현 시 같은 세계에 다른 좌표 난수열이 적용되는 비교도 포함하므로 순수한 단일 난수열의 절반 절단 실험은 아니다. 예산 24·대조비 1도 별도 제공한다. 실제 금액·이동비·장비 세팅비가 아니라 명시한 측정 단위의 비용 실험이다.

여기서 더 중요한 경계는 새로운 **유효 표본–대조 대비**를 가정했다는 사실이다. 단순히 기존 GP 잔차에 새 p값을 붙인 것이 아니다. 새 관측의 위치가 과거에만 의존하고, 귀무 아래 두 평균이 같으며 독립 Gaussian 잡음 분산이 알려지면 `alpha_t=0.05/[t(t+1)]`의 합이 0.05 이하여서 조건부 유효 p값의 누적 오경보를 제한한다. 일반적인 잔차 검정·conformal·e-process를 구현했다고 하지 않는다. 순차 추론의 조건과 위치 선택의 비용을 분리하는 방향은 문헌과 연결된다. [T03](../../triad/references/REFERENCES.md#t03) [T08](../../triad/references/REFERENCES.md#t08)

평균차가 0이어도 Gaussian 규칙에 t3나 이분산 잡음을 넣으면 그 조건이 깨진다. 최대 공백/예산48에서 Bonferroni 경고는 t3 14/64(21.9%), 이분산 59/64(92.2%)였다. 이는 알려진 Gaussian 귀무 전체에는 위반이 있는 세계이지 유효한 귀무에서 수학적 보장이 반증된 것이 아니다. 실무적으로는 이를 기전 평균 오류로 오해하면 잘못된 경고가 된다. 양쪽 대조군에 동일한 물리 오류가 들어가는 경우 대비가 상쇄되므로 위치를 넓혀도 발견할 수 없었다.

## 3. F: 강건함·이분산성·수집 전략은 서로 교환 가능한 개선이 아니다

수집용 추정기 3개 × 수집 정책 3개 × 최종 추정기 3개를 완전히 교차했다. 모든 평균식은 같은 2차 기저다. 무작위와 영역 채우기는 수집 추정기와 무관하게 같은 관측을 제공한다. 아래의 동일 데이터 비교는 수집용 `hom_gaussian`, `random`을 고정한 40세계의 결과다. 반복 관측에서 입력별 잡음을 학습하는 문헌은 구현 동기를 제공하지만, 본 코드는 heteroscedastic GP 논문의 재현이 아니라 작은 회귀 기준선이다. [T04](../../triad/references/REFERENCES.md#t04) [T05](../../triad/references/REFERENCES.md#t05)

| 세계 | 최종 추정기 | RMSE | NLL | CRPS | 관측 포함률 | 구간 폭 |
|---|---|---:|---:|---:|---:|---:|
| 정상 | 등분산 Gaussian | 0.0208 | -0.6626 | 0.0694 | 94.7% | 0.4925 |
| 정상 | Student-t | 0.0245 | -0.6422 | 0.0698 | 96.8% | 0.5468 |
| 드문 큰 잡음 | 등분산 Gaussian | 0.0499 | 0.1895 | 0.1158 | 94.9% | 0.9198 |
| 드문 큰 잡음 | Student-t | 0.0263 | -0.3315 | 0.1052 | 94.0% | 0.6606 |
| 평균식 누락 | 등분산 Gaussian | 0.1659 | 0.4621 | 0.1284 | 70.1% | 0.4661 |
| 평균식 누락 | Student-t | 0.1689 | -0.0744 | 0.1217 | 96.5% | 0.9030 |

드문 큰 잡음에서는 Student-t의 RMSE 차이(Student-t − Gaussian)가 -0.02357, 세계 bootstrap 기술 구간 [-0.03301, -0.01527]이었다. 정상에서는 +0.00362 [0.00143, 0.00623]로 오히려 높았다. 평균식 누락에서도 +0.00294 [0.00142, 0.00474]였다. 마지막 조건에서 관측 구간 포함률과 점수는 개선돼도 평균의 오류는 고쳐지지 않았고 구간 폭이 거의 두 배가 됐다. ‘좋은 확률 예측’과 ‘기전 복구’를 혼동하지 않는다. Student-t 계산은 명시한 IRLS·예측 근사이며 일반 GP posterior가 아니다. [T06](../../triad/references/REFERENCES.md#t06) [T07](../../triad/references/REFERENCES.md#t07)

로그선형 이분산 조건에서 같은 random 데이터의 로그분산 모형은 RMSE 0.0359, 등분산은 0.0391이었다. 그러나 로그분산 수집기·최종 추정기를 고정하고 IVR 정책을 쓰면 RMSE 0.0251로 내려가면서 NLL은 random -0.4757보다 나쁜 -0.4143이었다. 이 NLL 차이의 기술 구간 [-0.08809, 0.22236]은 0을 포함한다. 한 지표의 평균 개선만으로 전체 예측분포가 좋아졌다고 할 수 없다.

평균식이 누락된 경우 고정 Gaussian 추정기의 IVR은 RMSE 0.2058, random은 0.1659였다. 잘못된 작은 평균식의 분산만 줄이려는 수집은 예측 오류를 악화시킬 수 있다. 이분산 함수가 비단조인데 로그선형만 허용하면 그 추가 유연성 자체가 오지정된다. Student-t도 모든 입력별 분산 형태를 학습하지 않는다.

## 4. 재현성과 해석

16,320개 원시 기록, 890,880개 직렬화 관측, 219개 대표 실행을 보존했다. 관측 건수는 정책 재사용·교정·테스트를 포함하며 독립 표본 수가 아니다. 이벤트 해시와 인덱스는 패키지 크기를 줄이기 위해 **손실 없이 재구성 가능한 형식**으로 저장한다. 복원 시 전체 기록과 원 해시를 검증하며 관측·가정·비용·모형·결과를 버리지 않는다. 수치 소스와 임계값은 최종 평가 전에 고정한 그대로다.

아래 표는 유리한 셀만 고르지 않은 전체 결과다. 연속 밀도 NLL, CRPS, 구간의 날카로움과 포함률은 서로 다른 측면을 평가한다. 40·64·80·256개의 합성 세계라는 크기와 국소 생성 규칙의 한계가 있으며, 어떤 결과도 생물학적 효능이나 실제 시료의 참값을 증명하지 않는다.

## 전체 D 결과

| Scenario | Protocol | n | Rank | Latent RMSE ± SD | Latent coverage | Width | Contradicted | Transfer-null rejected |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| blank_mismatch | addition_blank | 80 | 6/6 | 0.2264 ± 0.0473 | 7.9% | 0.2419 | 2/80 | 80/80 |
| blank_mismatch | addition_only | 80 | 5/6 | — ± — | — | — | 0/80 | 78/80 |
| blank_mismatch | external_only | 80 | 4/6 | — ± — | — | — | 0/80 | — |
| blank_mismatch | orthogonal_only | 80 | 6/6 | 0.0298 ± 0.0156 | 95.3% | 0.1352 | 2/80 | 80/80 |
| blank_mismatch | triangulated | 80 | 6/6 | 0.2277 ± 0.0524 | 11.0% | 0.2549 | 63/80 | 80/80 |
| both_shift | addition_blank | 80 | 6/6 | 0.0602 ± 0.0408 | 94.0% | 0.2656 | 2/80 | 79/80 |
| both_shift | addition_only | 80 | 5/6 | — ± — | — | — | 0/80 | 78/80 |
| both_shift | external_only | 80 | 4/6 | — ± — | — | — | 0/80 | — |
| both_shift | orthogonal_only | 80 | 6/6 | 0.0298 ± 0.0159 | 96.7% | 0.1352 | 2/80 | 80/80 |
| both_shift | triangulated | 80 | 6/6 | 0.0624 ± 0.0463 | 93.8% | 0.2821 | 4/80 | 79/80 |
| common_anchor_failure | addition_blank | 80 | 6/6 | 0.5940 ± 0.1549 | 0.6% | 0.4627 | 4/80 | 1/80 |
| common_anchor_failure | addition_only | 80 | 5/6 | — ± — | — | — | 0/80 | 5/80 |
| common_anchor_failure | external_only | 80 | 4/6 | — ± — | — | — | 0/80 | — |
| common_anchor_failure | orthogonal_only | 80 | 6/6 | 0.5965 ± 0.1127 | 0.2% | 0.1352 | 6/80 | 8/80 |
| common_anchor_failure | triangulated | 80 | 6/6 | 0.5995 ± 0.1675 | 0.9% | 0.4946 | 5/80 | 2/80 |
| gain_shift | addition_blank | 80 | 6/6 | 0.0587 ± 0.0398 | 94.2% | 0.2649 | 2/80 | 77/80 |
| gain_shift | addition_only | 80 | 5/6 | — ± — | — | — | 0/80 | 80/80 |
| gain_shift | external_only | 80 | 4/6 | — ± — | — | — | 0/80 | — |
| gain_shift | orthogonal_only | 80 | 6/6 | 0.0313 ± 0.0162 | 95.4% | 0.1352 | 2/80 | 79/80 |
| gain_shift | triangulated | 80 | 6/6 | 0.0643 ± 0.0420 | 93.8% | 0.2819 | 6/80 | 76/80 |
| nonlinear_sensor | addition_blank | 80 | 6/6 | 0.1500 ± 0.0709 | 38.1% | 0.2351 | 46/80 | 80/80 |
| nonlinear_sensor | addition_only | 80 | 5/6 | — ± — | — | — | 0/80 | 80/80 |
| nonlinear_sensor | external_only | 80 | 4/6 | — ± — | — | — | 0/80 | — |
| nonlinear_sensor | orthogonal_only | 80 | 6/6 | 0.0305 ± 0.0162 | 95.3% | 0.1352 | 27/80 | 78/80 |
| nonlinear_sensor | triangulated | 80 | 6/6 | 0.1433 ± 0.0694 | 45.3% | 0.2508 | 50/80 | 79/80 |
| normal | addition_blank | 80 | 6/6 | 0.0788 ± 0.0538 | 94.9% | 0.3644 | 2/80 | 6/80 |
| normal | addition_only | 80 | 5/6 | — ± — | — | — | 0/80 | 4/80 |
| normal | external_only | 80 | 4/6 | — ± — | — | — | 0/80 | — |
| normal | orthogonal_only | 80 | 6/6 | 0.0339 ± 0.0158 | 94.2% | 0.1352 | 2/80 | 5/80 |
| normal | triangulated | 80 | 6/6 | 0.0843 ± 0.0599 | 95.3% | 0.3877 | 8/80 | 5/80 |
| offset_shift | addition_blank | 80 | 6/6 | 0.0696 ± 0.0463 | 97.0% | 0.3541 | 0/80 | 78/80 |
| offset_shift | addition_only | 80 | 5/6 | — ± — | — | — | 0/80 | 4/80 |
| offset_shift | external_only | 80 | 4/6 | — ± — | — | — | 0/80 | — |
| offset_shift | orthogonal_only | 80 | 6/6 | 0.0281 ± 0.0144 | 98.2% | 0.1352 | 1/80 | 80/80 |
| offset_shift | triangulated | 80 | 6/6 | 0.0739 ± 0.0465 | 96.1% | 0.3765 | 2/80 | 78/80 |
| reference_drift | addition_blank | 80 | 6/6 | 0.0780 ± 0.0531 | 97.7% | 0.3577 | 3/80 | 1/80 |
| reference_drift | addition_only | 80 | 5/6 | — ± — | — | — | 0/80 | 4/80 |
| reference_drift | external_only | 80 | 4/6 | — ± — | — | — | 0/80 | — |
| reference_drift | orthogonal_only | 80 | 6/6 | 0.3804 ± 0.0391 | 0.1% | 0.1352 | 2/80 | 80/80 |
| reference_drift | triangulated | 80 | 6/6 | 0.0840 ± 0.0609 | 97.5% | 0.3790 | 60/80 | 3/80 |
| spike_recovery | addition_blank | 80 | 6/6 | 0.5742 ± 0.1638 | 16.0% | 0.5334 | 1/80 | 79/80 |
| spike_recovery | addition_only | 80 | 5/6 | — ± — | — | — | 0/80 | 40/80 |
| spike_recovery | external_only | 80 | 4/6 | — ± — | — | — | 0/80 | — |
| spike_recovery | orthogonal_only | 80 | 6/6 | 0.0308 ± 0.0189 | 91.5% | 0.1352 | 1/80 | 80/80 |
| spike_recovery | triangulated | 80 | 6/6 | 0.5754 ± 0.1707 | 17.3% | 0.5670 | 76/80 | 78/80 |

외부 교정만 / 첨가만은 확장 물리계가 식별되지 않아 잠재 RMSE를 만들지 않는다. 전달 귀무 기각은 모형 충돌과 다르며, 첨가만에서는 gain만 시험한다. full-rank 모형의 오차는 충돌 여부와 무관하게 모두 공개한다. 비용은 모든 셀 적합 48 + 테스트 33 = 81이다.

## 전체 E 결과

| Scenario | Placement | Budget / control cost | n worlds / pairs | Naive alarm | Bonferroni alarm | Spending alarm | Region hit | Restricted cost (Bonferroni) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| boundary | adaptive_cover | 24/1 | 64/12 | 43/64 | 27/64 | 28/64 | 27/64 | 17.5938 |
| boundary | adaptive_cover | 48/1 | 64/24 | 59/64 | 41/64 | 40/64 | 41/64 | 28.5312 |
| boundary | adaptive_cover | 48/3 | 64/12 | 50/64 | 33/64 | 33/64 | 33/64 | 34.4375 |
| boundary | fixed_three | 24/1 | 64/12 | 45/64 | 25/64 | 22/64 | 10/64 | 17.9062 |
| boundary | fixed_three | 48/1 | 64/24 | 55/64 | 23/64 | 22/64 | 10/64 | 35.6562 |
| boundary | fixed_three | 48/3 | 64/12 | 45/64 | 25/64 | 22/64 | 10/64 | 35.8125 |
| boundary | max_gap | 24/1 | 64/12 | 47/64 | 24/64 | 23/64 | 21/64 | 19.8750 |
| boundary | max_gap | 48/1 | 64/24 | 61/64 | 45/64 | 39/64 | 45/64 | 32.3125 |
| boundary | max_gap | 48/3 | 64/12 | 45/64 | 22/64 | 21/64 | 18/64 | 39.6875 |
| boundary | stratified | 24/1 | 64/12 | 51/64 | 29/64 | 27/64 | 28/64 | 18.6875 |
| boundary | stratified | 48/1 | 64/24 | 61/64 | 46/64 | 37/64 | 52/64 | 28.7500 |
| boundary | stratified | 48/3 | 64/12 | 49/64 | 35/64 | 31/64 | 31/64 | 33.4375 |
| boundary | uniform | 24/1 | 64/12 | 52/64 | 32/64 | 26/64 | 26/64 | 18.0625 |
| boundary | uniform | 48/1 | 64/24 | 58/64 | 39/64 | 36/64 | 43/64 | 29.9375 |
| boundary | uniform | 48/3 | 64/12 | 50/64 | 27/64 | 28/64 | 26/64 | 38.0000 |
| broad | adaptive_cover | 24/1 | 64/12 | 63/64 | 56/64 | 56/64 | 54/64 | 11.3750 |
| broad | adaptive_cover | 48/1 | 64/24 | 64/64 | 61/64 | 62/64 | 64/64 | 13.8750 |
| broad | adaptive_cover | 48/3 | 64/12 | 63/64 | 58/64 | 58/64 | 57/64 | 23.0625 |
| broad | fixed_three | 24/1 | 64/12 | 42/64 | 23/64 | 20/64 | 13/64 | 18.4375 |
| broad | fixed_three | 48/1 | 64/24 | 55/64 | 25/64 | 22/64 | 13/64 | 33.4688 |
| broad | fixed_three | 48/3 | 64/12 | 42/64 | 23/64 | 20/64 | 13/64 | 36.8750 |
| broad | max_gap | 24/1 | 64/12 | 64/64 | 61/64 | 59/64 | 64/64 | 10.8438 |
| broad | max_gap | 48/1 | 64/24 | 64/64 | 63/64 | 61/64 | 64/64 | 12.4688 |
| broad | max_gap | 48/3 | 64/12 | 64/64 | 60/64 | 60/64 | 64/64 | 21.6250 |
| broad | stratified | 24/1 | 64/12 | 64/64 | 61/64 | 58/64 | 64/64 | 10.8125 |
| broad | stratified | 48/1 | 64/24 | 64/64 | 64/64 | 63/64 | 64/64 | 12.0312 |
| broad | stratified | 48/3 | 64/12 | 64/64 | 63/64 | 61/64 | 64/64 | 19.3125 |
| broad | uniform | 24/1 | 64/12 | 58/64 | 54/64 | 52/64 | 53/64 | 11.4062 |
| broad | uniform | 48/1 | 64/24 | 64/64 | 60/64 | 60/64 | 61/64 | 16.9688 |
| broad | uniform | 48/3 | 64/12 | 61/64 | 52/64 | 50/64 | 59/64 | 24.5625 |
| common_mode | adaptive_cover | 24/1 | 64/12 | 30/64 | 3/64 | 3/64 | — | 23.3438 |
| common_mode | adaptive_cover | 48/1 | 64/24 | 48/64 | 5/64 | 3/64 | — | 46.2188 |
| common_mode | adaptive_cover | 48/3 | 64/12 | 34/64 | 4/64 | 3/64 | — | 46.5000 |
| common_mode | fixed_three | 24/1 | 64/12 | 37/64 | 2/64 | 1/64 | — | 23.5312 |
| common_mode | fixed_three | 48/1 | 64/24 | 55/64 | 4/64 | 1/64 | — | 47.1562 |
| common_mode | fixed_three | 48/3 | 64/12 | 37/64 | 2/64 | 1/64 | — | 47.0625 |
| common_mode | max_gap | 24/1 | 64/12 | 34/64 | 3/64 | 3/64 | — | 23.3125 |
| common_mode | max_gap | 48/1 | 64/24 | 45/64 | 2/64 | 3/64 | — | 46.6875 |
| common_mode | max_gap | 48/3 | 64/12 | 30/64 | 3/64 | 3/64 | — | 46.7500 |
| common_mode | stratified | 24/1 | 64/12 | 21/64 | 1/64 | 2/64 | — | 23.9688 |
| common_mode | stratified | 48/1 | 64/24 | 45/64 | 4/64 | 2/64 | — | 46.8438 |
| common_mode | stratified | 48/3 | 64/12 | 29/64 | 4/64 | 3/64 | — | 46.3125 |
| common_mode | uniform | 24/1 | 64/12 | 37/64 | 3/64 | 2/64 | — | 23.3750 |
| common_mode | uniform | 48/1 | 64/24 | 50/64 | 4/64 | 2/64 | — | 46.4375 |
| common_mode | uniform | 48/3 | 64/12 | 31/64 | 0/64 | 2/64 | — | 48.0000 |
| hetero_null | adaptive_cover | 24/1 | 64/12 | 63/64 | 49/64 | 48/64 | — | 13.3750 |
| hetero_null | adaptive_cover | 48/1 | 64/24 | 64/64 | 60/64 | 56/64 | — | 17.0938 |
| hetero_null | adaptive_cover | 48/3 | 64/12 | 62/64 | 50/64 | 50/64 | — | 26.2500 |
| hetero_null | fixed_three | 24/1 | 64/12 | 59/64 | 49/64 | 41/64 | — | 15.2812 |
| hetero_null | fixed_three | 48/1 | 64/24 | 63/64 | 58/64 | 52/64 | — | 21.3750 |
| hetero_null | fixed_three | 48/3 | 64/12 | 59/64 | 49/64 | 41/64 | — | 30.5625 |
| hetero_null | max_gap | 24/1 | 64/12 | 61/64 | 49/64 | 46/64 | — | 13.3438 |
| hetero_null | max_gap | 48/1 | 64/24 | 64/64 | 59/64 | 56/64 | — | 18.0938 |
| hetero_null | max_gap | 48/3 | 64/12 | 62/64 | 50/64 | 46/64 | — | 26.6875 |
| hetero_null | stratified | 24/1 | 64/12 | 63/64 | 50/64 | 46/64 | — | 12.5312 |
| hetero_null | stratified | 48/1 | 64/24 | 64/64 | 60/64 | 50/64 | — | 20.3125 |
| hetero_null | stratified | 48/3 | 64/12 | 62/64 | 50/64 | 44/64 | — | 25.8750 |
| hetero_null | uniform | 24/1 | 64/12 | 64/64 | 52/64 | 42/64 | — | 13.0000 |
| hetero_null | uniform | 48/1 | 64/24 | 64/64 | 58/64 | 52/64 | — | 19.8750 |
| hetero_null | uniform | 48/3 | 64/12 | 62/64 | 43/64 | 41/64 | — | 30.1250 |
| narrow | adaptive_cover | 24/1 | 64/12 | 47/64 | 25/64 | 25/64 | 27/64 | 19.2500 |
| narrow | adaptive_cover | 48/1 | 64/24 | 61/64 | 46/64 | 45/64 | 46/64 | 28.5000 |
| narrow | adaptive_cover | 48/3 | 64/12 | 50/64 | 27/64 | 26/64 | 30/64 | 38.7500 |
| narrow | fixed_three | 24/1 | 64/12 | 40/64 | 5/64 | 8/64 | 3/64 | 22.8125 |
| narrow | fixed_three | 48/1 | 64/24 | 51/64 | 6/64 | 8/64 | 3/64 | 45.2812 |
| narrow | fixed_three | 48/3 | 64/12 | 40/64 | 5/64 | 8/64 | 3/64 | 45.6250 |
| narrow | max_gap | 24/1 | 64/12 | 53/64 | 27/64 | 27/64 | 33/64 | 19.5000 |
| narrow | max_gap | 48/1 | 64/24 | 62/64 | 48/64 | 41/64 | 54/64 | 29.1250 |
| narrow | max_gap | 48/3 | 64/12 | 52/64 | 31/64 | 28/64 | 36/64 | 38.8750 |
| narrow | stratified | 24/1 | 64/12 | 50/64 | 34/64 | 26/64 | 30/64 | 17.5000 |
| narrow | stratified | 48/1 | 64/24 | 59/64 | 46/64 | 39/64 | 51/64 | 28.9062 |
| narrow | stratified | 48/3 | 64/12 | 49/64 | 35/64 | 27/64 | 35/64 | 35.6250 |
| narrow | uniform | 24/1 | 64/12 | 44/64 | 25/64 | 23/64 | 23/64 | 19.2188 |
| narrow | uniform | 48/1 | 64/24 | 60/64 | 37/64 | 37/64 | 46/64 | 32.4375 |
| narrow | uniform | 48/3 | 64/12 | 46/64 | 22/64 | 22/64 | 24/64 | 38.8750 |
| normal | adaptive_cover | 24/1 | 256/12 | 110/256 | 10/256 | 10/256 | — | 23.6172 |
| normal | adaptive_cover | 48/1 | 256/24 | 183/256 | 11/256 | 9/256 | — | 46.7109 |
| normal | adaptive_cover | 48/3 | 256/12 | 109/256 | 12/256 | 11/256 | — | 47.2344 |
| normal | fixed_three | 24/1 | 256/12 | 117/256 | 8/256 | 6/256 | — | 23.6016 |
| normal | fixed_three | 48/1 | 256/24 | 171/256 | 10/256 | 8/256 | — | 46.9922 |
| normal | fixed_three | 48/3 | 256/12 | 117/256 | 8/256 | 6/256 | — | 47.2031 |
| normal | max_gap | 24/1 | 256/12 | 116/256 | 14/256 | 10/256 | — | 23.4375 |
| normal | max_gap | 48/1 | 256/24 | 174/256 | 13/256 | 10/256 | — | 46.4219 |
| normal | max_gap | 48/3 | 256/12 | 109/256 | 13/256 | 11/256 | — | 46.9375 |
| normal | stratified | 24/1 | 256/12 | 120/256 | 9/256 | 14/256 | — | 23.3594 |
| normal | stratified | 48/1 | 256/24 | 179/256 | 10/256 | 10/256 | — | 47.1719 |
| normal | stratified | 48/3 | 256/12 | 120/256 | 14/256 | 16/256 | — | 46.5312 |
| normal | uniform | 24/1 | 256/12 | 130/256 | 13/256 | 16/256 | — | 23.4922 |
| normal | uniform | 48/1 | 256/24 | 184/256 | 17/256 | 14/256 | — | 46.7812 |
| normal | uniform | 48/3 | 256/12 | 125/256 | 14/256 | 12/256 | — | 47.0156 |
| t3_null | adaptive_cover | 24/1 | 64/12 | 25/64 | 6/64 | 7/64 | — | 22.8750 |
| t3_null | adaptive_cover | 48/1 | 64/24 | 37/64 | 9/64 | 9/64 | — | 43.8438 |
| t3_null | adaptive_cover | 48/3 | 64/12 | 26/64 | 8/64 | 8/64 | — | 45.4375 |
| t3_null | fixed_three | 24/1 | 64/12 | 33/64 | 12/64 | 9/64 | — | 22.5312 |
| t3_null | fixed_three | 48/1 | 64/24 | 48/64 | 17/64 | 13/64 | — | 41.7188 |
| t3_null | fixed_three | 48/3 | 64/12 | 33/64 | 12/64 | 9/64 | — | 45.0625 |
| t3_null | max_gap | 24/1 | 64/12 | 25/64 | 8/64 | 10/64 | — | 22.8438 |
| t3_null | max_gap | 48/1 | 64/24 | 42/64 | 14/64 | 13/64 | — | 42.8750 |
| t3_null | max_gap | 48/3 | 64/12 | 23/64 | 8/64 | 10/64 | — | 45.4375 |
| t3_null | stratified | 24/1 | 64/12 | 31/64 | 10/64 | 6/64 | — | 22.6875 |
| t3_null | stratified | 48/1 | 64/24 | 45/64 | 13/64 | 8/64 | — | 43.5625 |
| t3_null | stratified | 48/3 | 64/12 | 18/64 | 8/64 | 5/64 | — | 45.6875 |
| t3_null | uniform | 24/1 | 64/12 | 32/64 | 10/64 | 9/64 | — | 22.3750 |
| t3_null | uniform | 48/1 | 64/24 | 43/64 | 20/64 | 15/64 | — | 39.0625 |
| t3_null | uniform | 48/3 | 64/12 | 28/64 | 9/64 | 11/64 | — | 44.1875 |
| weak | adaptive_cover | 24/1 | 64/12 | 40/64 | 12/64 | 7/64 | 34/64 | 22.1250 |
| weak | adaptive_cover | 48/1 | 64/24 | 53/64 | 13/64 | 8/64 | 50/64 | 43.3438 |
| weak | adaptive_cover | 48/3 | 64/12 | 41/64 | 13/64 | 6/64 | 37/64 | 44.8750 |
| weak | fixed_three | 24/1 | 64/12 | 29/64 | 3/64 | 5/64 | 5/64 | 23.4062 |
| weak | fixed_three | 48/1 | 64/24 | 52/64 | 6/64 | 6/64 | 5/64 | 45.9375 |
| weak | fixed_three | 48/3 | 64/12 | 29/64 | 3/64 | 5/64 | 5/64 | 46.8125 |
| weak | max_gap | 24/1 | 64/12 | 40/64 | 10/64 | 5/64 | 39/64 | 22.1562 |
| weak | max_gap | 48/1 | 64/24 | 53/64 | 13/64 | 9/64 | 61/64 | 43.2812 |
| weak | max_gap | 48/3 | 64/12 | 43/64 | 13/64 | 9/64 | 44/64 | 44.1875 |
| weak | stratified | 24/1 | 64/12 | 42/64 | 5/64 | 4/64 | 38/64 | 23.0312 |
| weak | stratified | 48/1 | 64/24 | 52/64 | 9/64 | 9/64 | 57/64 | 45.3125 |
| weak | stratified | 48/3 | 64/12 | 37/64 | 9/64 | 7/64 | 43/64 | 45.9375 |
| weak | uniform | 24/1 | 64/12 | 29/64 | 10/64 | 6/64 | 30/64 | 21.4375 |
| weak | uniform | 48/1 | 64/24 | 51/64 | 9/64 | 6/64 | 49/64 | 44.0938 |
| weak | uniform | 48/3 | 64/12 | 38/64 | 8/64 | 8/64 | 31/64 | 45.0000 |

경고는 any-alarm이며 오류 위치나 원인 적중을 보장하지 않는다. Region hit은 실제 중심으로부터 폭 1배 안에 측정이 들어간 비율이고 효과가 없는 세계/공통모드에서는 해당 없음이다. 미탐지는 예산 소진 비용으로 넣은 제한 탐지비도 함께 제시한다. 오류가 있는 영역의 모든 위치를 보장하지 않는다.

## 전체 F 교차 결과

| Scenario | Controller | Acquisition | Final estimator | n | Latent RMSE ± SD | NLL | CRPS | Observed coverage | Width | Converged |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| contamination | hom_gaussian | ivr | hom_gaussian | 40 | 0.0412 ± 0.0183 | 0.2205 | 0.1134 | 94.6% | 0.8687 | 100.0% |
| contamination | hom_gaussian | ivr | logvar_gaussian | 40 | 0.0410 ± 0.0184 | 0.7997 | 0.1092 | 91.1% | 0.6124 | 100.0% |
| contamination | hom_gaussian | ivr | student_t | 40 | 0.0247 ± 0.0116 | -0.3252 | 0.1056 | 93.3% | 0.6219 | 100.0% |
| contamination | hom_gaussian | random | hom_gaussian | 40 | 0.0499 ± 0.0318 | 0.1895 | 0.1158 | 94.9% | 0.9198 | 100.0% |
| contamination | hom_gaussian | random | logvar_gaussian | 40 | 0.0498 ± 0.0350 | 1.3791 | 0.1125 | 90.9% | 0.6587 | 100.0% |
| contamination | hom_gaussian | random | student_t | 40 | 0.0263 ± 0.0109 | -0.3315 | 0.1052 | 94.0% | 0.6606 | 100.0% |
| contamination | hom_gaussian | spacefill | hom_gaussian | 40 | 0.0521 ± 0.0324 | 0.0949 | 0.1185 | 95.9% | 0.9997 | 100.0% |
| contamination | hom_gaussian | spacefill | logvar_gaussian | 40 | 0.0515 ± 0.0312 | 0.4294 | 0.1121 | 92.1% | 0.6777 | 100.0% |
| contamination | hom_gaussian | spacefill | student_t | 40 | 0.0257 ± 0.0104 | -0.3314 | 0.1054 | 93.7% | 0.6642 | 100.0% |
| contamination | logvar_gaussian | ivr | hom_gaussian | 40 | 0.0388 ± 0.0197 | 0.1099 | 0.1143 | 95.7% | 0.9206 | 100.0% |
| contamination | logvar_gaussian | ivr | logvar_gaussian | 40 | 0.0391 ± 0.0197 | 1.8612 | 0.1099 | 89.1% | 0.5889 | 100.0% |
| contamination | logvar_gaussian | ivr | student_t | 40 | 0.0208 ± 0.0089 | -0.3301 | 0.1052 | 93.5% | 0.6265 | 100.0% |
| contamination | logvar_gaussian | random | hom_gaussian | 40 | 0.0499 ± 0.0318 | 0.1895 | 0.1158 | 94.9% | 0.9198 | 100.0% |
| contamination | logvar_gaussian | random | logvar_gaussian | 40 | 0.0498 ± 0.0350 | 1.3791 | 0.1125 | 90.9% | 0.6587 | 100.0% |
| contamination | logvar_gaussian | random | student_t | 40 | 0.0263 ± 0.0109 | -0.3315 | 0.1052 | 94.0% | 0.6606 | 100.0% |
| contamination | logvar_gaussian | spacefill | hom_gaussian | 40 | 0.0521 ± 0.0324 | 0.0949 | 0.1185 | 95.9% | 0.9997 | 100.0% |
| contamination | logvar_gaussian | spacefill | logvar_gaussian | 40 | 0.0515 ± 0.0312 | 0.4294 | 0.1121 | 92.1% | 0.6777 | 100.0% |
| contamination | logvar_gaussian | spacefill | student_t | 40 | 0.0257 ± 0.0104 | -0.3314 | 0.1054 | 93.7% | 0.6642 | 100.0% |
| contamination | student_t | ivr | hom_gaussian | 40 | 0.0447 ± 0.0250 | 0.2002 | 0.1146 | 94.8% | 0.8974 | 100.0% |
| contamination | student_t | ivr | logvar_gaussian | 40 | 0.0444 ± 0.0248 | 0.8500 | 0.1104 | 90.5% | 0.6139 | 100.0% |
| contamination | student_t | ivr | student_t | 40 | 0.0233 ± 0.0098 | -0.3325 | 0.1052 | 93.5% | 0.6310 | 100.0% |
| contamination | student_t | random | hom_gaussian | 40 | 0.0499 ± 0.0318 | 0.1895 | 0.1158 | 94.9% | 0.9198 | 100.0% |
| contamination | student_t | random | logvar_gaussian | 40 | 0.0498 ± 0.0350 | 1.3791 | 0.1125 | 90.9% | 0.6587 | 100.0% |
| contamination | student_t | random | student_t | 40 | 0.0263 ± 0.0109 | -0.3315 | 0.1052 | 94.0% | 0.6606 | 100.0% |
| contamination | student_t | spacefill | hom_gaussian | 40 | 0.0521 ± 0.0324 | 0.0949 | 0.1185 | 95.9% | 0.9997 | 100.0% |
| contamination | student_t | spacefill | logvar_gaussian | 40 | 0.0515 ± 0.0312 | 0.4294 | 0.1121 | 92.1% | 0.6777 | 100.0% |
| contamination | student_t | spacefill | student_t | 40 | 0.0257 ± 0.0104 | -0.3314 | 0.1054 | 93.7% | 0.6642 | 100.0% |
| gaussian | hom_gaussian | ivr | hom_gaussian | 40 | 0.0195 ± 0.0077 | -0.6517 | 0.0692 | 93.8% | 0.4697 | 100.0% |
| gaussian | hom_gaussian | ivr | logvar_gaussian | 40 | 0.0198 ± 0.0075 | -0.5855 | 0.0700 | 92.5% | 0.4887 | 100.0% |
| gaussian | hom_gaussian | ivr | student_t | 40 | 0.0218 ± 0.0078 | -0.6452 | 0.0693 | 96.6% | 0.5431 | 100.0% |
| gaussian | hom_gaussian | random | hom_gaussian | 40 | 0.0208 ± 0.0102 | -0.6626 | 0.0694 | 94.7% | 0.4925 | 100.0% |
| gaussian | hom_gaussian | random | logvar_gaussian | 40 | 0.0221 ± 0.0118 | -0.6128 | 0.0706 | 94.1% | 0.5179 | 100.0% |
| gaussian | hom_gaussian | random | student_t | 40 | 0.0245 ± 0.0121 | -0.6422 | 0.0698 | 96.8% | 0.5468 | 100.0% |
| gaussian | hom_gaussian | spacefill | hom_gaussian | 40 | 0.0252 ± 0.0099 | -0.6468 | 0.0699 | 93.9% | 0.4899 | 100.0% |
| gaussian | hom_gaussian | spacefill | logvar_gaussian | 40 | 0.0263 ± 0.0098 | -0.5606 | 0.0711 | 93.2% | 0.5211 | 100.0% |
| gaussian | hom_gaussian | spacefill | student_t | 40 | 0.0275 ± 0.0102 | -0.6362 | 0.0701 | 96.5% | 0.5495 | 100.0% |
| gaussian | logvar_gaussian | ivr | hom_gaussian | 40 | 0.0219 ± 0.0099 | -0.6582 | 0.0694 | 93.9% | 0.4727 | 100.0% |
| gaussian | logvar_gaussian | ivr | logvar_gaussian | 40 | 0.0222 ± 0.0098 | -0.5936 | 0.0702 | 92.4% | 0.4758 | 100.0% |
| gaussian | logvar_gaussian | ivr | student_t | 40 | 0.0243 ± 0.0118 | -0.6390 | 0.0697 | 96.4% | 0.5420 | 100.0% |
| gaussian | logvar_gaussian | random | hom_gaussian | 40 | 0.0208 ± 0.0102 | -0.6626 | 0.0694 | 94.7% | 0.4925 | 100.0% |
| gaussian | logvar_gaussian | random | logvar_gaussian | 40 | 0.0221 ± 0.0118 | -0.6128 | 0.0706 | 94.1% | 0.5179 | 100.0% |
| gaussian | logvar_gaussian | random | student_t | 40 | 0.0245 ± 0.0121 | -0.6422 | 0.0698 | 96.8% | 0.5468 | 100.0% |
| gaussian | logvar_gaussian | spacefill | hom_gaussian | 40 | 0.0252 ± 0.0099 | -0.6468 | 0.0699 | 93.9% | 0.4899 | 100.0% |
| gaussian | logvar_gaussian | spacefill | logvar_gaussian | 40 | 0.0263 ± 0.0098 | -0.5606 | 0.0711 | 93.2% | 0.5211 | 100.0% |
| gaussian | logvar_gaussian | spacefill | student_t | 40 | 0.0275 ± 0.0102 | -0.6362 | 0.0701 | 96.5% | 0.5495 | 100.0% |
| gaussian | student_t | ivr | hom_gaussian | 40 | 0.0192 ± 0.0076 | -0.6531 | 0.0691 | 93.5% | 0.4661 | 100.0% |
| gaussian | student_t | ivr | logvar_gaussian | 40 | 0.0195 ± 0.0073 | -0.5819 | 0.0700 | 92.5% | 0.4821 | 100.0% |
| gaussian | student_t | ivr | student_t | 40 | 0.0206 ± 0.0085 | -0.6482 | 0.0691 | 96.6% | 0.5437 | 100.0% |
| gaussian | student_t | random | hom_gaussian | 40 | 0.0208 ± 0.0102 | -0.6626 | 0.0694 | 94.7% | 0.4925 | 100.0% |
| gaussian | student_t | random | logvar_gaussian | 40 | 0.0221 ± 0.0118 | -0.6128 | 0.0706 | 94.1% | 0.5179 | 100.0% |
| gaussian | student_t | random | student_t | 40 | 0.0245 ± 0.0121 | -0.6422 | 0.0698 | 96.8% | 0.5468 | 100.0% |
| gaussian | student_t | spacefill | hom_gaussian | 40 | 0.0252 ± 0.0099 | -0.6468 | 0.0699 | 93.9% | 0.4899 | 100.0% |
| gaussian | student_t | spacefill | logvar_gaussian | 40 | 0.0263 ± 0.0098 | -0.5606 | 0.0711 | 93.2% | 0.5211 | 100.0% |
| gaussian | student_t | spacefill | student_t | 40 | 0.0275 ± 0.0102 | -0.6362 | 0.0701 | 96.5% | 0.5495 | 100.0% |
| loglinear_noise | hom_gaussian | ivr | hom_gaussian | 40 | 0.0334 ± 0.0177 | -0.3413 | 0.0888 | 93.3% | 0.6803 | 100.0% |
| loglinear_noise | hom_gaussian | ivr | logvar_gaussian | 40 | 0.0329 ± 0.0162 | -0.5338 | 0.0828 | 92.4% | 0.5689 | 100.0% |
| loglinear_noise | hom_gaussian | ivr | student_t | 40 | 0.0430 ± 0.0252 | -0.4375 | 0.0876 | 92.3% | 0.6243 | 92.5% |
| loglinear_noise | hom_gaussian | random | hom_gaussian | 40 | 0.0391 ± 0.0244 | -0.3457 | 0.0882 | 92.0% | 0.6163 | 100.0% |
| loglinear_noise | hom_gaussian | random | logvar_gaussian | 40 | 0.0359 ± 0.0205 | -0.4757 | 0.0832 | 90.3% | 0.5440 | 100.0% |
| loglinear_noise | hom_gaussian | random | student_t | 40 | 0.0384 ± 0.0223 | -0.4534 | 0.0867 | 91.7% | 0.5873 | 97.5% |
| loglinear_noise | hom_gaussian | spacefill | hom_gaussian | 40 | 0.0408 ± 0.0261 | -0.3219 | 0.0880 | 91.6% | 0.5892 | 100.0% |
| loglinear_noise | hom_gaussian | spacefill | logvar_gaussian | 40 | 0.0400 ± 0.0256 | -0.4608 | 0.0837 | 89.8% | 0.5412 | 100.0% |
| loglinear_noise | hom_gaussian | spacefill | student_t | 40 | 0.0434 ± 0.0266 | -0.4494 | 0.0869 | 91.4% | 0.5770 | 100.0% |
| loglinear_noise | logvar_gaussian | ivr | hom_gaussian | 40 | 0.0308 ± 0.0176 | -0.2854 | 0.0926 | 95.3% | 0.8441 | 100.0% |
| loglinear_noise | logvar_gaussian | ivr | logvar_gaussian | 40 | 0.0251 ± 0.0106 | -0.4143 | 0.0826 | 89.9% | 0.5608 | 100.0% |
| loglinear_noise | logvar_gaussian | ivr | student_t | 40 | 0.0309 ± 0.0152 | -0.3975 | 0.0886 | 96.6% | 0.8647 | 100.0% |
| loglinear_noise | logvar_gaussian | random | hom_gaussian | 40 | 0.0391 ± 0.0244 | -0.3457 | 0.0882 | 92.0% | 0.6163 | 100.0% |
| loglinear_noise | logvar_gaussian | random | logvar_gaussian | 40 | 0.0359 ± 0.0205 | -0.4757 | 0.0832 | 90.3% | 0.5440 | 100.0% |
| loglinear_noise | logvar_gaussian | random | student_t | 40 | 0.0384 ± 0.0223 | -0.4534 | 0.0867 | 91.7% | 0.5873 | 97.5% |
| loglinear_noise | logvar_gaussian | spacefill | hom_gaussian | 40 | 0.0408 ± 0.0261 | -0.3219 | 0.0880 | 91.6% | 0.5892 | 100.0% |
| loglinear_noise | logvar_gaussian | spacefill | logvar_gaussian | 40 | 0.0400 ± 0.0256 | -0.4608 | 0.0837 | 89.8% | 0.5412 | 100.0% |
| loglinear_noise | logvar_gaussian | spacefill | student_t | 40 | 0.0434 ± 0.0266 | -0.4494 | 0.0869 | 91.4% | 0.5770 | 100.0% |
| loglinear_noise | student_t | ivr | hom_gaussian | 40 | 0.0302 ± 0.0171 | -0.3420 | 0.0895 | 94.6% | 0.7393 | 100.0% |
| loglinear_noise | student_t | ivr | logvar_gaussian | 40 | 0.0298 ± 0.0162 | -0.4749 | 0.0829 | 90.0% | 0.5533 | 100.0% |
| loglinear_noise | student_t | ivr | student_t | 40 | 0.0364 ± 0.0177 | -0.4384 | 0.0869 | 94.0% | 0.7015 | 100.0% |
| loglinear_noise | student_t | random | hom_gaussian | 40 | 0.0391 ± 0.0244 | -0.3457 | 0.0882 | 92.0% | 0.6163 | 100.0% |
| loglinear_noise | student_t | random | logvar_gaussian | 40 | 0.0359 ± 0.0205 | -0.4757 | 0.0832 | 90.3% | 0.5440 | 100.0% |
| loglinear_noise | student_t | random | student_t | 40 | 0.0384 ± 0.0223 | -0.4534 | 0.0867 | 91.7% | 0.5873 | 97.5% |
| loglinear_noise | student_t | spacefill | hom_gaussian | 40 | 0.0408 ± 0.0261 | -0.3219 | 0.0880 | 91.6% | 0.5892 | 100.0% |
| loglinear_noise | student_t | spacefill | logvar_gaussian | 40 | 0.0400 ± 0.0256 | -0.4608 | 0.0837 | 89.8% | 0.5412 | 100.0% |
| loglinear_noise | student_t | spacefill | student_t | 40 | 0.0434 ± 0.0266 | -0.4494 | 0.0869 | 91.4% | 0.5770 | 100.0% |
| missing_mean | hom_gaussian | ivr | hom_gaussian | 40 | 0.2058 ± 0.0115 | 1.0484 | 0.1535 | 62.9% | 0.4717 | 100.0% |
| missing_mean | hom_gaussian | ivr | logvar_gaussian | 40 | 0.2056 ± 0.0115 | 1.2968 | 0.1541 | 61.7% | 0.4653 | 100.0% |
| missing_mean | hom_gaussian | ivr | student_t | 40 | 0.2108 ± 0.0127 | 0.3728 | 0.1526 | 76.8% | 0.6257 | 100.0% |
| missing_mean | hom_gaussian | random | hom_gaussian | 40 | 0.1659 ± 0.0063 | 0.4621 | 0.1284 | 70.1% | 0.4661 | 100.0% |
| missing_mean | hom_gaussian | random | logvar_gaussian | 40 | 0.1660 ± 0.0074 | 0.5242 | 0.1283 | 70.6% | 0.4915 | 100.0% |
| missing_mean | hom_gaussian | random | student_t | 40 | 0.1689 ± 0.0103 | -0.0744 | 0.1217 | 96.5% | 0.9030 | 100.0% |
| missing_mean | hom_gaussian | spacefill | hom_gaussian | 40 | 0.1631 ± 0.0031 | 0.4097 | 0.1267 | 71.0% | 0.4640 | 100.0% |
| missing_mean | hom_gaussian | spacefill | logvar_gaussian | 40 | 0.1630 ± 0.0033 | 0.6696 | 0.1276 | 69.5% | 0.4658 | 100.0% |
| missing_mean | hom_gaussian | spacefill | student_t | 40 | 0.1647 ± 0.0043 | -0.0961 | 0.1195 | 97.9% | 0.9371 | 100.0% |
| missing_mean | logvar_gaussian | ivr | hom_gaussian | 40 | 0.2007 ± 0.0217 | 0.8569 | 0.1493 | 64.9% | 0.4791 | 100.0% |
| missing_mean | logvar_gaussian | ivr | logvar_gaussian | 40 | 0.2006 ± 0.0218 | 1.1853 | 0.1502 | 63.7% | 0.4721 | 100.0% |
| missing_mean | logvar_gaussian | ivr | student_t | 40 | 0.2072 ± 0.0250 | 0.2964 | 0.1486 | 80.3% | 0.6592 | 100.0% |
| missing_mean | logvar_gaussian | random | hom_gaussian | 40 | 0.1659 ± 0.0063 | 0.4621 | 0.1284 | 70.1% | 0.4661 | 100.0% |
| missing_mean | logvar_gaussian | random | logvar_gaussian | 40 | 0.1660 ± 0.0074 | 0.5242 | 0.1283 | 70.6% | 0.4915 | 100.0% |
| missing_mean | logvar_gaussian | random | student_t | 40 | 0.1689 ± 0.0103 | -0.0744 | 0.1217 | 96.5% | 0.9030 | 100.0% |
| missing_mean | logvar_gaussian | spacefill | hom_gaussian | 40 | 0.1631 ± 0.0031 | 0.4097 | 0.1267 | 71.0% | 0.4640 | 100.0% |
| missing_mean | logvar_gaussian | spacefill | logvar_gaussian | 40 | 0.1630 ± 0.0033 | 0.6696 | 0.1276 | 69.5% | 0.4658 | 100.0% |
| missing_mean | logvar_gaussian | spacefill | student_t | 40 | 0.1647 ± 0.0043 | -0.0961 | 0.1195 | 97.9% | 0.9371 | 100.0% |
| missing_mean | student_t | ivr | hom_gaussian | 40 | 0.2073 ± 0.0126 | 1.0215 | 0.1542 | 63.5% | 0.4764 | 100.0% |
| missing_mean | student_t | ivr | logvar_gaussian | 40 | 0.2072 ± 0.0126 | 1.2634 | 0.1547 | 62.5% | 0.4741 | 100.0% |
| missing_mean | student_t | ivr | student_t | 40 | 0.2119 ± 0.0138 | 0.3704 | 0.1531 | 77.0% | 0.6322 | 100.0% |
| missing_mean | student_t | random | hom_gaussian | 40 | 0.1659 ± 0.0063 | 0.4621 | 0.1284 | 70.1% | 0.4661 | 100.0% |
| missing_mean | student_t | random | logvar_gaussian | 40 | 0.1660 ± 0.0074 | 0.5242 | 0.1283 | 70.6% | 0.4915 | 100.0% |
| missing_mean | student_t | random | student_t | 40 | 0.1689 ± 0.0103 | -0.0744 | 0.1217 | 96.5% | 0.9030 | 100.0% |
| missing_mean | student_t | spacefill | hom_gaussian | 40 | 0.1631 ± 0.0031 | 0.4097 | 0.1267 | 71.0% | 0.4640 | 100.0% |
| missing_mean | student_t | spacefill | logvar_gaussian | 40 | 0.1630 ± 0.0033 | 0.6696 | 0.1276 | 69.5% | 0.4658 | 100.0% |
| missing_mean | student_t | spacefill | student_t | 40 | 0.1647 ± 0.0043 | -0.0961 | 0.1195 | 97.9% | 0.9371 | 100.0% |
| nonmonotone_noise | hom_gaussian | ivr | hom_gaussian | 40 | 0.0231 ± 0.0195 | -0.3478 | 0.0782 | 90.3% | 0.5027 | 100.0% |
| nonmonotone_noise | hom_gaussian | ivr | logvar_gaussian | 40 | 0.0231 ± 0.0191 | -0.1359 | 0.0781 | 85.5% | 0.4036 | 100.0% |
| nonmonotone_noise | hom_gaussian | ivr | student_t | 40 | 0.0280 ± 0.0213 | -0.5637 | 0.0783 | 90.2% | 0.4946 | 100.0% |
| nonmonotone_noise | hom_gaussian | random | hom_gaussian | 40 | 0.0274 ± 0.0157 | -0.3825 | 0.0789 | 91.2% | 0.5438 | 100.0% |
| nonmonotone_noise | hom_gaussian | random | logvar_gaussian | 40 | 0.0272 ± 0.0153 | -0.1792 | 0.0781 | 86.0% | 0.4104 | 100.0% |
| nonmonotone_noise | hom_gaussian | random | student_t | 40 | 0.0205 ± 0.0129 | -0.5797 | 0.0766 | 90.2% | 0.4924 | 100.0% |
| nonmonotone_noise | hom_gaussian | spacefill | hom_gaussian | 40 | 0.0245 ± 0.0116 | -0.3920 | 0.0786 | 91.5% | 0.5561 | 100.0% |
| nonmonotone_noise | hom_gaussian | spacefill | logvar_gaussian | 40 | 0.0240 ± 0.0110 | -0.0548 | 0.0777 | 84.9% | 0.3908 | 100.0% |
| nonmonotone_noise | hom_gaussian | spacefill | student_t | 40 | 0.0174 ± 0.0091 | -0.5842 | 0.0762 | 89.9% | 0.4849 | 100.0% |
| nonmonotone_noise | logvar_gaussian | ivr | hom_gaussian | 40 | 0.0233 ± 0.0153 | -0.2107 | 0.0781 | 87.7% | 0.4457 | 100.0% |
| nonmonotone_noise | logvar_gaussian | ivr | logvar_gaussian | 40 | 0.0232 ± 0.0151 | 0.3503 | 0.0787 | 81.1% | 0.3467 | 100.0% |
| nonmonotone_noise | logvar_gaussian | ivr | student_t | 40 | 0.0217 ± 0.0136 | -0.5485 | 0.0776 | 88.5% | 0.4533 | 100.0% |
| nonmonotone_noise | logvar_gaussian | random | hom_gaussian | 40 | 0.0274 ± 0.0157 | -0.3825 | 0.0789 | 91.2% | 0.5438 | 100.0% |
| nonmonotone_noise | logvar_gaussian | random | logvar_gaussian | 40 | 0.0272 ± 0.0153 | -0.1792 | 0.0781 | 86.0% | 0.4104 | 100.0% |
| nonmonotone_noise | logvar_gaussian | random | student_t | 40 | 0.0205 ± 0.0129 | -0.5797 | 0.0766 | 90.2% | 0.4924 | 100.0% |
| nonmonotone_noise | logvar_gaussian | spacefill | hom_gaussian | 40 | 0.0245 ± 0.0116 | -0.3920 | 0.0786 | 91.5% | 0.5561 | 100.0% |
| nonmonotone_noise | logvar_gaussian | spacefill | logvar_gaussian | 40 | 0.0240 ± 0.0110 | -0.0548 | 0.0777 | 84.9% | 0.3908 | 100.0% |
| nonmonotone_noise | logvar_gaussian | spacefill | student_t | 40 | 0.0174 ± 0.0091 | -0.5842 | 0.0762 | 89.9% | 0.4849 | 100.0% |
| nonmonotone_noise | student_t | ivr | hom_gaussian | 40 | 0.0225 ± 0.0163 | -0.3767 | 0.0786 | 91.6% | 0.5503 | 100.0% |
| nonmonotone_noise | student_t | ivr | logvar_gaussian | 40 | 0.0227 ± 0.0161 | -0.2561 | 0.0780 | 88.0% | 0.4476 | 100.0% |
| nonmonotone_noise | student_t | ivr | student_t | 40 | 0.0258 ± 0.0190 | -0.5720 | 0.0780 | 92.1% | 0.5565 | 100.0% |
| nonmonotone_noise | student_t | random | hom_gaussian | 40 | 0.0274 ± 0.0157 | -0.3825 | 0.0789 | 91.2% | 0.5438 | 100.0% |
| nonmonotone_noise | student_t | random | logvar_gaussian | 40 | 0.0272 ± 0.0153 | -0.1792 | 0.0781 | 86.0% | 0.4104 | 100.0% |
| nonmonotone_noise | student_t | random | student_t | 40 | 0.0205 ± 0.0129 | -0.5797 | 0.0766 | 90.2% | 0.4924 | 100.0% |
| nonmonotone_noise | student_t | spacefill | hom_gaussian | 40 | 0.0245 ± 0.0116 | -0.3920 | 0.0786 | 91.5% | 0.5561 | 100.0% |
| nonmonotone_noise | student_t | spacefill | logvar_gaussian | 40 | 0.0240 ± 0.0110 | -0.0548 | 0.0777 | 84.9% | 0.3908 | 100.0% |
| nonmonotone_noise | student_t | spacefill | student_t | 40 | 0.0174 ± 0.0091 | -0.5842 | 0.0762 | 89.9% | 0.4849 | 100.0% |
| student3 | hom_gaussian | ivr | hom_gaussian | 40 | 0.0238 ± 0.0115 | -0.4929 | 0.0635 | 93.3% | 0.4554 | 100.0% |
| student3 | hom_gaussian | ivr | logvar_gaussian | 40 | 0.0238 ± 0.0116 | -0.4378 | 0.0631 | 90.6% | 0.3959 | 100.0% |
| student3 | hom_gaussian | ivr | student_t | 40 | 0.0174 ± 0.0083 | -0.8118 | 0.0613 | 92.5% | 0.4089 | 100.0% |
| student3 | hom_gaussian | random | hom_gaussian | 40 | 0.0256 ± 0.0143 | -0.5820 | 0.0633 | 92.7% | 0.4332 | 100.0% |
| student3 | hom_gaussian | random | logvar_gaussian | 40 | 0.0248 ± 0.0124 | -0.4311 | 0.0630 | 90.2% | 0.3811 | 100.0% |
| student3 | hom_gaussian | random | student_t | 40 | 0.0182 ± 0.0077 | -0.8132 | 0.0613 | 92.3% | 0.3973 | 100.0% |
| student3 | hom_gaussian | spacefill | hom_gaussian | 40 | 0.0281 ± 0.0201 | -0.5559 | 0.0654 | 94.7% | 0.5069 | 100.0% |
| student3 | hom_gaussian | spacefill | logvar_gaussian | 40 | 0.0274 ± 0.0169 | -0.3882 | 0.0637 | 90.5% | 0.3985 | 100.0% |
| student3 | hom_gaussian | spacefill | student_t | 40 | 0.0179 ± 0.0075 | -0.8172 | 0.0611 | 92.6% | 0.4093 | 100.0% |
| student3 | logvar_gaussian | ivr | hom_gaussian | 40 | 0.0221 ± 0.0118 | -0.5629 | 0.0631 | 93.1% | 0.4423 | 100.0% |
| student3 | logvar_gaussian | ivr | logvar_gaussian | 40 | 0.0220 ± 0.0119 | -0.3714 | 0.0630 | 90.3% | 0.3825 | 100.0% |
| student3 | logvar_gaussian | ivr | student_t | 40 | 0.0171 ± 0.0079 | -0.8157 | 0.0612 | 92.9% | 0.4223 | 100.0% |
| student3 | logvar_gaussian | random | hom_gaussian | 40 | 0.0256 ± 0.0143 | -0.5820 | 0.0633 | 92.7% | 0.4332 | 100.0% |
| student3 | logvar_gaussian | random | logvar_gaussian | 40 | 0.0248 ± 0.0124 | -0.4311 | 0.0630 | 90.2% | 0.3811 | 100.0% |
| student3 | logvar_gaussian | random | student_t | 40 | 0.0182 ± 0.0077 | -0.8132 | 0.0613 | 92.3% | 0.3973 | 100.0% |
| student3 | logvar_gaussian | spacefill | hom_gaussian | 40 | 0.0281 ± 0.0201 | -0.5559 | 0.0654 | 94.7% | 0.5069 | 100.0% |
| student3 | logvar_gaussian | spacefill | logvar_gaussian | 40 | 0.0274 ± 0.0169 | -0.3882 | 0.0637 | 90.5% | 0.3985 | 100.0% |
| student3 | logvar_gaussian | spacefill | student_t | 40 | 0.0179 ± 0.0075 | -0.8172 | 0.0611 | 92.6% | 0.4093 | 100.0% |
| student3 | student_t | ivr | hom_gaussian | 40 | 0.0229 ± 0.0109 | -0.5353 | 0.0630 | 93.0% | 0.4437 | 100.0% |
| student3 | student_t | ivr | logvar_gaussian | 40 | 0.0229 ± 0.0111 | -0.4307 | 0.0627 | 90.8% | 0.3870 | 100.0% |
| student3 | student_t | ivr | student_t | 40 | 0.0170 ± 0.0072 | -0.8167 | 0.0611 | 92.3% | 0.4072 | 100.0% |
| student3 | student_t | random | hom_gaussian | 40 | 0.0256 ± 0.0143 | -0.5820 | 0.0633 | 92.7% | 0.4332 | 100.0% |
| student3 | student_t | random | logvar_gaussian | 40 | 0.0248 ± 0.0124 | -0.4311 | 0.0630 | 90.2% | 0.3811 | 100.0% |
| student3 | student_t | random | student_t | 40 | 0.0182 ± 0.0077 | -0.8132 | 0.0613 | 92.3% | 0.3973 | 100.0% |
| student3 | student_t | spacefill | hom_gaussian | 40 | 0.0281 ± 0.0201 | -0.5559 | 0.0654 | 94.7% | 0.5069 | 100.0% |
| student3 | student_t | spacefill | logvar_gaussian | 40 | 0.0274 ± 0.0169 | -0.3882 | 0.0637 | 90.5% | 0.3985 | 100.0% |
| student3 | student_t | spacefill | student_t | 40 | 0.0179 ± 0.0075 | -0.8172 | 0.0611 | 92.6% | 0.4093 | 100.0% |

NLL·CRPS는 작을수록 좋다. 연속 밀도의 NLL은 음수일 수 있다. 관측 구간과 잠재 평균 구간은 다르다. 잡음 계수의 추정 불확실성은 적분하지 않았고 Student-t 공분산·합성 예측분포는 근사다. 각 셀 적합 48 + 테스트 81 = 129. 최종 적합 6/6,480개는 설정한 수렴 기준을 충족하지 못했으며 제거하지 않았다. 중복된 passive 수집 결과를 독립 증거로 세지 않는다.

