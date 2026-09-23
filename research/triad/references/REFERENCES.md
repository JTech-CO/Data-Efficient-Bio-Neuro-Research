# v1.3 references / 참고문헌



The studies are original synthetic implementations, not replications of the cited algorithms. Counts are Consensus snapshots on 2026-09-22, not quality rankings.



<a id="t01"></a>

## [T01] Standard additions: myth and reality

Stephen L. R. Ellison; Michael Thompson (2008). *Analyst*, 133, 992-997.

[Primary source](https://pubs.rsc.org/en/content/articlelanding/2008/an/b717660k) · DOI: `10.1039/B717660K`

표준 첨가는 회전형(기울기) matrix effect를 다루지만 이동형(절편) 효과는 별도 정보가 필요하다.

Standard additions address rotational matrix effects; translational effects require separate treatment.

**Boundary:** Conceptual support only; study D is not an analytical chemistry assay.

[Consensus fetched record](https://consensus.app/papers/standard-additions-myth-and-reality-ellison-thompson/e3029837055b5f86ab7491c277114923/?utm_source=chatgpt) · citation-count snapshot: 117.



<a id="t02"></a>

## [T02] Recommendations for Setting a Criterion for Assessing Commutability of Secondary Calibrator Certified Reference Materials

W. Greg Miller et al. (IFCC Working Group) (2023). *Clinical Chemistry*, 69(9), 966-975.

[Primary source](https://pubmed.ncbi.nlm.nih.gov/37566391/) · DOI: `10.1093/clinchem/hvad104`

Commutability는 특정 측정 절차들에서 표준과 표본 사이의 수치적 관계에 대한 제한된 속성이며 사용 목적에 맞는 판정 기준이 필요하다.

Commutability concerns a quantitative relationship across specified measurement procedures and requires fit-for-purpose criteria.

**Boundary:** Not clinical implementation or formal validation against the IFCC recommendations. Publisher metadata was cross-checked via PubMed search; direct open was blocked.

[Consensus fetched record](https://consensus.app/papers/recommendations-for-setting-a-criterion-for-assessing-miller-keller/2eb8e242fccf56fa85245c2a743d940a/?utm_source=chatgpt) · citation-count snapshot: 26.



<a id="t03"></a>

## [T03] An Adaptive Sampling Strategy for Real-Time Anomaly Detection with Unmanned Sensing Vehicles

Yue Jiang; Ana María Estrada Gómez (2024). *Technometrics*, 66(3), 438-454.

[Primary source](https://www.tandfonline.com/doi/abs/10.1080/00401706.2024.2322645) · DOI: `10.1080/00401706.2024.2322645`

탐색·집중과 측정 이동비를 함께 다루는 공간 적응 진단의 기존 사례다.

An existing spatial adaptive monitoring framework balances exploration, exploitation and deployment costs.

**Boundary:** The new one-dimensional audit is not a replication of their tensor or vehicle-path algorithm.

[Consensus fetched record](https://consensus.app/papers/an-adaptive-sampling-strategy-for-realtime-anomaly-jiang-gómez/1af27d65194350ce976465b826c19864/?utm_source=chatgpt) · citation-count snapshot: 5.



<a id="t04"></a>

## [T04] Replication or Exploration? Sequential Design for Stochastic Simulation Experiments

Mickaël Binois; Jiangeng Huang; Robert B. Gramacy; Mike Ludkovski (2019). *Technometrics*, 61(1), 7-23.

[Primary source](https://arxiv.org/abs/1710.03206) · DOI: `10.1080/00401706.2018.1469433`

새 위치 탐색과 기존 위치 반복을 함께 최적화하며 이분산 관측을 다루는 선행 연구다.

Sequential design can consider replication and exploration jointly under input-dependent noise.

**Boundary:** F uses a small linear-basis IVR proxy, not their lookahead GP implementation. Online publication 2018; journal volume 2019.



<a id="t05"></a>

## [T05] Practical Heteroscedastic Gaussian Process Modeling for Large Simulation Experiments

Mickaël Binois; Robert B. Gramacy; Mike Ludkovski (2018). *Journal of Computational and Graphical Statistics*, 27(4), 808-821.

[Primary source](https://www.tandfonline.com/doi/abs/10.1080/10618600.2018.1458625) · DOI: `10.1080/10618600.2018.1458625`

반복 관측은 입력 의존 잡음의 추정과 계산 효율에 중요한 역할을 한다.

Replicates can inform input-dependent noise estimation and computational efficiency.

**Boundary:** Consensus year 2016 corresponds to the preprint. Publisher journal year is 2018. F does not implement hetGP.

[Consensus fetched record](https://consensus.app/papers/practical-heteroscedastic-gaussian-process-modeling-for-binois-gramacy/6aab6350f000539ba633df74f9ede731/?utm_source=chatgpt) · citation-count snapshot: 227.



<a id="t06"></a>

## [T06] Robust Gaussian Process Regression with a Student-t Likelihood

Pasi Jylänki; Jarno Vanhatalo; Aki Vehtari (2011). *Journal of Machine Learning Research*, 12(99), 3227-3257.

[Primary source](https://www.jmlr.org/papers/v12/jylanki11a.html)

Student-t likelihood의 견고성은 근사 추론과 수렴 문제를 함께 요구한다.

Student-t likelihoods require attention to approximate inference and convergence.

**Boundary:** F implements a fixed-df linear IRLS approximation, not GP expectation propagation.



<a id="t07"></a>

## [T07] Strictly Proper Scoring Rules, Prediction, and Estimation

Tilmann Gneiting; Adrian E. Raftery (2007). *Journal of the American Statistical Association*, 102(477), 359-378.

[Primary source](https://doi.org/10.1198/016214506000001437) · DOI: `10.1198/016214506000001437`

확률 예측은 포함률·폭과 함께 로그 점수와 CRPS 같은 proper score로 평가한다.

Probability forecasts should be assessed with proper scores such as log score and CRPS, alongside interval width and coverage.

**Boundary:** A proper score does not validate an incorrect observation model or make plug-in intervals exact.



<a id="t08"></a>

## [T08] Time-uniform, nonparametric, nonasymptotic confidence sequences

Steven R. Howard; Aaditya Ramdas; Jon McAuliffe; Jasjeet Sekhon (2021). *The Annals of Statistics*, 49(2), 1055-1080.

[Primary source](https://arxiv.org/abs/1810.08240) · DOI: `10.1214/20-AOS1991`

반복적으로 결과를 확인하는 추론에는 사용한 순차 규칙의 조건과 보장 범위를 명시해야 한다.

Repeated monitoring requires explicit assumptions and sequential validity conditions.

**Boundary:** E uses elementary alpha spending with conditionally valid fresh p-values, not this paper's confidence-sequence algorithms. Journal 2021; first preprint 2018.

