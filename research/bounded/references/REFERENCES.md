# Sources / 참고문헌

Accessed 2026-09-23. These are methodology sources, not evidence that our synthetic system works on real biology. Citation counts are retrieval snapshots, not quality scores.

문헌 수는 성능 검증의 수가 아니다. 아래의 수학·코드 결합은 자체 제한된 합성 연구이며 각 논문의 직접 재현을 주장하지 않는다.


<a id="b01"></a>
## B01. Partial Identifiability in Discrete Data with Measurement Error

Noam Finkelstein; Roy Adams; Suchi Saria; Ilya Shpitser (2021). UAI / PMLR 161, 1798–1808.

[Primary source](https://proceedings.mlr.press/v161/finkelstein21b.html)

오류가 있는 측정에서 가정별 허용 범위를 보고하는 선행 사례다. 해당 이산모형의 정리를 연속 교정계에 그대로 적용하지 않는다.

Consensus fetch and publisher HTML abstract/metadata. Original paper studies discrete measurement error; our affine continuous LP is a separate construction.

[Consensus record](https://consensus.app/papers/partial-identifiability-in-discrete-data-with-finkelstein-adams/fe060b9cb1145590add820f98a7041e9/?utm_source=chatgpt) · Citation count at retrieval: 13.


<a id="b02"></a>
## B02. Anytime-valid t-tests and confidence sequences for Gaussian means with unknown variance

Hongjian Wang; Aaditya Ramdas (2025). Sequential Analysis 44(1), 56–110.

[Primary source](https://www.tandfonline.com/doi/abs/10.1080/07474946.2024.2428245) · DOI: `10.1080/07474946.2024.2428245`

미지 분산 순차 추론의 전제가 중요함을 확인한다. 이번 local-t + 고정 횟수 보정은 이 논문의 anytime t 절차를 재현한 것이 아니다.

Consensus fetch and publisher HTML abstract/metadata. Publisher year 2025; Consensus year 2023 is preprint-era metadata. Not an implementation of its e-processes.

[Consensus record](https://consensus.app/papers/anytimevalid-ttests-and-confidence-sequences-for-wang-ramdas/812ebbc171d254f193de0878718c730c/?utm_source=chatgpt) · Citation count at retrieval: 12.


<a id="b03"></a>
## B03. Sign tests for dependent observations

Rustam Ibragimov; Donald J. M. Brown (2019). Econometrics and Statistics 10, 1–8.

[Primary source](https://doi.org/10.1016/j.ecosta.2018.11.001) · DOI: `10.1016/j.ecosta.2018.11.001`

조건부 대칭과 부호검정의 관계를 참고했다. 후기 저널 원문은 열람하지 않았으며, 간단한 부호 자본 과정의 조건과 유도는 27장에 직접 제시한다.

Consensus fetch returned metadata without abstract. Primary author-repository precursor abstract read at https://elischolar.library.yale.edu/cowles-discussion-paper-series/1802/ (2005). The publisher search result corroborated the 2019 volume/pages/DOI and abstract, but direct page access returned 403. No full-text review claimed.

[Consensus record](https://consensus.app/papers/sign-tests-for-dependent-observations-ibragimov-brown/2d3652340c0f579384701c88ec9c0def/?utm_source=chatgpt) · Citation count at retrieval: 2.


<a id="b04"></a>
## B04. Game-Theoretic Statistics and Safe Anytime-Valid Inference

Aaditya Ramdas; Peter Grünwald; Vladimir Vovk; Glenn Shafer (2023). Statistical Science 38(4), 576–601.

[Primary source](https://doi.org/10.1214/23-STS894) · DOI: `10.1214/23-STS894`

비음수 자본 과정과 선택 중단의 근거다. 본 구현은 고정 혼합 부호 베팅의 제한된 경우만 다룬다.

Primary publisher search result and author tutorial HTML; abstract/metadata, not a full-paper review.


<a id="b05"></a>
## B05. How can I test whether any significant terms are missing or misspecified in the functional part of the model?

NIST/SEMATECH (n.d.). e-Handbook of Statistical Methods, §4.4.4.6.

[Primary source](https://www.itl.nist.gov/div898/handbook/pmd/section4/pmd446.htm)

반복 내 순수 오차와 평균식 부적합의 고전적 분해 및 F 비교를 사용한다. 정확한 검정 전제는 별도로 명시한다.

Full official HTML section including pure-error and lack-of-fit formulas read.


<a id="b06"></a>
## B06. scipy.optimize.linprog

SciPy contributors (n.d.). Official SciPy documentation.

[Primary source](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html)

LP의 성공·공집합·무한 범위를 구분한다. API 설명과 실행 환경 버전을 혼동하지 않는다.

Official API/status documentation read. Web page labeled 1.18.0; local numerical runtime was SciPy 1.17.0.
