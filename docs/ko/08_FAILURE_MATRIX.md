# 실패 모드 → 점검 → 개선 → 잔여 한계

개선은 문헌에 있는 방법과 본 보고서의 운영 제안을 결합한 것이다. 모든 조합의 효과를 실증한 표가 아니다.

| 실패 | 원인 | 점검 | 개선 | 남는 한계 | 근거 |
|---|---|---|---|---|---|
| GP 과신 | 커널·잡음·집단 구조가 틀림 | coverage/폭, kernel sensitivity, 새 집단 잔차 | 계층/robust likelihood, prior sensitivity, 독립 탐색 | 어떤 보정도 arbitrary shift에 자동 보장 아님 | [R01](../../references/BIBLIOGRAPHY.md#r01) [R23](../../references/BIBLIOGRAPHY.md#r23) |
| 능동학습 잠금 | 예측 불확실성과 목표 정보 혼동 | 질의 중복, noisy point 집중, random 대비 비용 | target information과 replicate cost, 탐색 대조군 | 모든 후보의 shared blind spot | [R02](../../references/BIBLIOGRAPHY.md#r02) [R05](../../references/BIBLIOGRAPHY.md#r05) |
| SINDy 잡음 | 수치 미분이 관측 잡음 증폭 | noise sweep와 coefficient stability | weak/integral, bootstrap ensemble | 미관측 상태·잘못된 dictionary는 남음 | [R04](../../references/BIBLIOGRAPHY.md#r04) [R05](../../references/BIBLIOGRAPHY.md#r05) |
| 짧지만 틀린 식 | 대안 기전·단위·식별성 미검사 | 단위, profile/posterior ridge, 개입 rollout | identifiable reparameterization, equation card | 해석가능성과 인과성을 동일시할 수 없음 | [R06](../../references/BIBLIOGRAPHY.md#r06) [T02](../../references/BIBLIOGRAPHY.md#t02) |
| 강한 잘못된 physics | 경험적 가정을 정확한 법칙처럼 강제 | wrong-prior stress, residual의 체계 패턴 | trustworthy hard constraint만 유지, shrinkage discrepancy | 유연한 residual이 원 계수를 숨길 수 있음 | [R10](../../references/BIBLIOGRAPHY.md#r10) [R27](../../references/BIBLIOGRAPHY.md#r27) |
| 전처리 과확신 | 마스크·보간 point estimate를 사실로 사용 | raw/derived 비교, downstream 민감도 | observation layer와 uncertainty propagation | ensemble 자체가 잘못 보정될 수 있음 | [R07](../../references/BIBLIOGRAPHY.md#r07) [R15](../../references/BIBLIOGRAPHY.md#r15) |
| FM negative transfer | 표현 목표와 downstream task 불일치 | raw/linear/frozen/adapter 동일 조건 비교 | 단계적 적응과 성능 이득 gate | 더 큰 사전학습의 자동 이득 없음 | [R11](../../references/BIBLIOGRAPHY.md#r11) [R12](../../references/BIBLIOGRAPHY.md#r12) [R13](../../references/BIBLIOGRAPHY.md#r13) |
| 평가 누수 | 개체·세션·pretrain overlap | 원본 hash, group manifest, training corpus audit | group split, 외부 holdout, known-overlap 별도 트랙 | 비공개 pretrain의 중복은 unknown일 수 있음 | [R18](../../references/BIBLIOGRAPHY.md#r18) [D01](../../references/BIBLIOGRAPHY.md#d01) |
| 잘못된 fidelity | 다른 domain을 정확도 순서로 간주 | paired bridge 잔차, HF-only 비교 | discrepancy 또는 multi-task domain model | 짝지은 표본이 너무 적으면 관계 불확실 | [R19](../../references/BIBLIOGRAPHY.md#r19) [R20](../../references/BIBLIOGRAPHY.md#r20) |
| 합성 순환 | 모형 출력을 독립 증거로 재투입 | real-only test, provenance, source-label 의존 | 학습 split 안에서 생성, augmentation ablation | 계보 관리만으로 효과를 보장하지 못함 | [R09](../../references/BIBLIOGRAPHY.md#r09) [R21](../../references/BIBLIOGRAPHY.md#r21) |
| 합성 privacy 오해 | 생성물이 원 사람과 무관하다고 가정 | 적절한 privacy attack·원자료 근접성 검사 | 접근 통제, 필요한 경우 DP와 별도 utility 평가 | 익명화와 DP 보장은 서로 다름 | [R22](../../references/BIBLIOGRAPHY.md#r22) |
| 점 추정 기전 집착 | 여러 가능한 파라미터를 하나로 축약 | 다중 posterior mode, predictive check | SBI·계층 Bayesian inference·부분 식별 | simulator bias와 큰 계산량 | [R25](../../references/BIBLIOGRAPHY.md#r25) [R26](../../references/BIBLIOGRAPHY.md#r26) |
