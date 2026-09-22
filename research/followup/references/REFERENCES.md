# Follow-up evidence and implementation sources

Checked 2026-09-22. These are selected research anchors, not an exhaustive systematic review. Numerical findings in this release are our own synthetic executions. Citation counts are the Consensus snapshot, not quality scores. Publisher dates take precedence over preprint/index dates.

<a id="d01"></a>
## D01

**[Bayesian calibration, process modeling and uncertainty quantification in biotechnology](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1009223)**

Laura Marie Helleckes; Michael Osthege; Wolfgang Wiechert; Eric von Lieres; Marco Oldiges. 2022. *PLOS Computational Biology*. DOI: `10.1371/journal.pcbi.1009223`.

Measurement calibration and measurement-noise likelihood belong in the model. calibr8/murefi are prior implementations; this addendum does not reproduce them.

Access/date note: Publisher publication date is 2022-03-07; Consensus returned 2021. Publisher HTML checked.

Consensus: [fetched paper record](https://consensus.app/papers/bayesian-calibration-process-modeling-and-uncertainty-helleckes-osthege/4878f7f14f895345b1ff81a561ee0ecf/?utm_source=chatgpt); returned year 2021; citation-count snapshot 31.

<a id="d02"></a>
## D02

**[Quantification of model uncertainty: Calibration, model discrepancy, and identifiability](https://doi.org/10.1115/1.4007390)**

Paul D. Arendt; Daniel W. Apley; Wei Chen. 2012. *Journal of Mechanical Design*. DOI: `10.1115/1.4007390`.

Calibration parameters and model discrepancy may be confounded; motivates an explicit identifiability counterexample.

Access/date note: Consensus abstract fetched. DOI identified in bibliographic cross-reference; publisher full text was not retrievable. No claim of full-text review.

Consensus: [fetched paper record](https://consensus.app/papers/quantification-of-model-uncertainty-calibration-model-arendt-apley/7036e08a323652a5a82c3aad4414355d/?utm_source=chatgpt); returned year 2012; citation-count snapshot 348.

<a id="d03"></a>
## D03

**[Efficient data collection for establishing practical identifiability via active learning](https://spj.science.org/doi/10.1016/j.csbj.2025.10.058)**

Xiaolu Liu; Linda Wanika; Michael J. Chappell; Juergen Branke. 2025. *Computational and Structural Biotechnology Journal*. DOI: `10.1016/j.csbj.2025.10.058`.

E-ALPIPE targets practical identifiability under a declared model/noise law. Our local block objective is NOT E-ALPIPE.

Access/date note: Consensus fetch lacked abstract; original publisher HTML and PubMed used. Online publication 2025-11-12.

Consensus: [fetched paper record](https://consensus.app/papers/efficient-data-collection-for-establishing-practical-liu-wanika/047aa6052eaa52f29854eb1f20514bf7/?utm_source=chatgpt); returned year 2025; citation-count snapshot 1.

<a id="d04"></a>
## D04

**[Anytime-Valid Inference in Linear Models with Applications to Regression-Adjusted Causal Inference](https://www.tandfonline.com/doi/full/10.1080/01621459.2026.2692052)**

Michael Lindon; D. Ham; M. Tingley; Iavor Bojinov. 2026. *Journal of the American Statistical Association (online record)*. DOI: `10.1080/01621459.2026.2692052`.

Repeated fixed-sample tests need sequential error control. Our implementation uses finite-look Bonferroni, not the article's anytime-valid linear-model tests.

Access/date note: Consensus gave 2022; publisher search record identifies 2026 DOI. Publisher abstract retrieved in search, full-page fetch failed. Online bibliographic record only; no volume/page guessed.

Consensus: [fetched paper record](https://consensus.app/papers/anytimevalid-inference-in-linear-models-with-lindon-ham/aa84583a5c985a02b4f0a14a31b296ab/?utm_source=chatgpt); returned year 2022; citation-count snapshot 11.

<a id="d05"></a>
## D05

**[Time-uniform, nonparametric, nonasymptotic confidence sequences](https://arxiv.org/abs/1810.08240)**

Steven R. Howard; Aaditya Ramdas; Jon McAuliffe; Jasjeet Sekhon. 2021. *Annals of Statistics, 49(2), 1055-1080*. DOI: `10.1214/20-AOS1991`.

Distinguishes an unbounded-time confidence sequence from our bounded-look diagnostic procedure.

Access/date note: Author arXiv record gives published journal reference and DOI. No PDF redistributed or analysed.

<a id="d06"></a>
## D06

**[Negative controls: Concepts and caveats](https://journals.sagepub.com/doi/10.1177/09622802231181230)**

Bas B. L. Penning de Vries; Rolf H. H. Groenwold. 2023. *Statistical Methods in Medical Research, 32(8), 1576-1587*. DOI: `10.1177/09622802231181230`.

A methodological analogy only: a control passing does not certify the main process. We separately construct a measurement-standard transport counterexample.

Access/date note: Consensus abstract fetched; publisher methodological discussion reviewed. This is about causal negative controls, NOT a direct validation of metrology standards.

Consensus: [fetched paper record](https://consensus.app/papers/negative-controls-concepts-and-caveats-vries-groenwold/93aef4cbb0dd5396a2d8b61d4fda4681/?utm_source=chatgpt); returned year 2023; citation-count snapshot 12.

<a id="d07"></a>
## D07

**[Efficient sampling-based Bayesian Active Learning for synaptic characterization](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1011342)**

Camille Gontier; Simone Carlo Surace; Igor Delvendahl; Martin Müller; Jean-Pascal Pfister. 2023. *PLOS Computational Biology, 19(8), e1011342*. DOI: `10.1371/journal.pcbi.1011342`.

Real physiology is an eventual application class. No synaptic recordings or ESB-BAL replication are part of this release.

Access/date note: Publisher date 2023-08-21 supersedes Consensus 2022 preprint year.

Consensus: [fetched paper record](https://consensus.app/papers/efficient-samplingbased-bayesian-active-learning-for-gontier-surace/91f46ebba3c15e3ab87e791e777e0d32/?utm_source=chatgpt); returned year 2022; citation-count snapshot 4.

<a id="d08"></a>
## D08

**[A protocol for dynamic model calibration](https://academic.oup.com/bib/article/23/1/bbab387/6383562)**

Alejandro F. Villaverde; Dilan Pathirana; Fabian Fröhlich; Jan Hasenauer; Julio R. Banga. 2022. *Briefings in Bioinformatics, 23(1), bbab387*. DOI: `10.1093/bib/bbab387`.

Identifiability, observation likelihood, fitting and uncertainty checks should be distinguished. Does not establish this addendum's empirical performance.

Access/date note: Publisher: online 2021-10-09, journal issue January 2022; both dates retained.

## Numerical API documentation

- [SciPy F survival function](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f.html)
- [SciPy chi-square survival function](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2.html)

Used for numerical tail probabilities, not as empirical evidence of biological validity.
