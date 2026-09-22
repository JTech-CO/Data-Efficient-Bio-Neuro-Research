# Implementation literature / 구현 추가 근거

Retrieved / 확인일: 2026-09-22. Citation counts are transient Consensus metadata, not evidence weights. 원 논문 PDF·초록 전문을 재배포하지 않는다.

Consensus 검색 → fetch 확인 → 출판사/학회 기록으로 발행 연도 확인. 이 문서는 문헌 동기를 기록하며 알고리즘 재현이나 성능 보증을 뜻하지 않는다.

<a id="e01"></a>
## E01
**[Active learning for optimal intervention design in causal models](https://consensus.app/papers/active-learning-for-optimal-intervention-design-in-causal-zhang-cammarata/99cfb1cdc83b5da997232d8ece4a9cd9/?utm_source=chatgpt)**
Jiaqi Zhang, Louis Cammarata, Chandler Squires, Themistoklis P. Sapsis, Caroline Uhler. 2023. Nature Machine Intelligence 5, 1066–1075.
Primary record: https://www.nature.com/articles/s42256-023-00719-0
DOI: 10.1038/s42256-023-00719-0. Consensus citation count: 53.
Read scope: Consensus abstract/metadata and publisher abstract, scope and publication metadata.
Consensus indexed 2022 preprint year; version of record is 2023. This implementation does not reproduce CIV.

<a id="e02"></a>
## E02
**[Representative, Informative, and De-Amplifying: Requirements for Robust Bayesian Active Learning under Model Misspecification](https://consensus.app/papers/representative-informative-and-deamplifying-tang-sloman/4b0681ea376650118bd3a2d69fa45fca/?utm_source=chatgpt)**
Roubing Tang, Sabina J. Sloman, Samuel Kaski. 2026. AISTATS, Proceedings of Machine Learning Research 300, 3016–3024.
Primary record: https://proceedings.mlr.press/v300/tang26d.html
DOI: Not provided by the verified record. Consensus citation count: 1.
Read scope: Consensus abstract/metadata and PMLR indexed publication record/abstract; direct page open failed.
Consensus indexed 2025; 2026 conference publication verified separately. R-IDeA is not implemented here.

<a id="e03"></a>
## E03
**[Optimal experiment design for practical parameter identifiability and model discrimination](https://consensus.app/papers/optimal-experiment-design-for-practical-parameter-liu-maini/4f489205cf885aa4b8140fac406a8639/?utm_source=chatgpt)**
Yue Liu, Philip K. Maini, Ruth E. Baker. 2026. Mathematical Biosciences 399, 109710.
Primary record: https://www.sciencedirect.com/science/article/pii/S0025556426001008
DOI: 10.1016/j.mbs.2026.109710. Consensus citation count: 2.
Read scope: Consensus metadata (fetch had no abstract), publisher abstract/introduction/section snippets and Oxford metadata.
Preprint 2025; published online 2026-05-22, September 2026 issue. Profile-likelihood and Pontryagin algorithms are not implemented here.

## Evidence-to-implementation boundary

| Evidence | Design implication here | Explicitly not claimed |
|---|---|---|
| E01: causal structure can inform intervention design | Represent intervention separately from readout | Reproduction of the published acquisition function or biological transfer |
| E02: informativeness alone can be brittle under misspecification | Retain exploration and record negative results | R-IDeA implementation or a robustness guarantee |
| E03: parameter identifiability and model discrimination are related but distinct | Report parameter design rank and candidate weights separately | General structural-identifiability analysis or optimal-control implementation |

이 근거들은 설계 동기를 제공한다. 아래 합성 실험의 효과 크기는 이 논문들의 결과를 복사한 것이 아니라 저장소 코드의 자체 실행 결과다.
