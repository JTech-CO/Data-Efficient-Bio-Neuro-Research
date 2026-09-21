# Research hypotheses and falsification plans

## 1. Novelty boundary

GP+AL, weak/ensemble SINDy, PINN+SR, UDEs, multifidelity GPs, and foundation adaptation already exist. Connecting them is not evidence of a new regression theory or absence of prior art. Candidate contributions here are the **observation-, assumption-, provenance-, and falsification-aware problem definition and evaluation**. Novelty and empirical value remain to be established. [R05](../../references/BIBLIOGRAPHY.md#r05) [R08](../../references/BIBLIOGRAPHY.md#r08) [R09](../../references/BIBLIOGRAPHY.md#r09) [R19](../../references/BIBLIOGRAPHY.md#r19)

## H1. Query discriminating assumptions, not merely uncertain values

Hypothesis: experiments where competing mechanisms disagree and their differences are observable provide more mechanism-selection value per cost than repeatedly querying noisy points.

Closest directions include GPAL and active Ensemble-SINDy. Compare random, maximum latent variance, information gain, and model-discrimination acquisition. Test both truth-inside-library and truth-outside-library settings. Overconfidence and false discovery outside the library would falsify a broad superiority claim. [R02](../../references/BIBLIOGRAPHY.md#r02) [R05](../../references/BIBLIOGRAPHY.md#r05)

A possible contribution is accounting for measurement operators and replicate costs to reject apparently discriminating experiments whose differences the instrument cannot observe. Renaming ensemble disagreement is not novelty.

## H2. Correcting observations may matter more than strengthening PINN constraints

Hypothesis: in some low-sample problems, modeling intensity/count/voltage bias improves intervention extrapolation and coefficient stability more than reducing equation residuals.

Use known-state/noisy, hidden-state/correct-observation, and hidden-state/biased-observation tests. Compare vanilla and reweighted PINNs, ordinary solver likelihood fitting, and observation-aware UDEs. Do not require UDEs to win everywhere. Accurately observed simple systems may make the extra observation layer harmful. BINN/UDE work motivates this experiment but does not supply its results. [R07](../../references/BIBLIOGRAPHY.md#r07) [R10](../../references/BIBLIOGRAPHY.md#r10)

## H3. Budget independent evidence instead of generated rows

Hypothesis: provenance-aware weighting and a real-only validation gate reduce OOD degradation and overconfidence compared with naive synthetic oversampling.

Separate more draws from one fitted generator, multiple simulator priors, and an external pretrained prior. Hold real donor counts fixed. Distinguish regularization benefits from additional external information. Provenance alone cannot eliminate statistical bias; measure how often the gate actually detects harmful augmentation. [R21](../../references/BIBLIOGRAPHY.md#r21) [R22](../../references/BIBLIOGRAPHY.md#r22)

## H4. Separate shared structure from individual dynamics

Hypothesis: a hierarchical sparse model with shared candidate terms and individual coefficients can be more stable with few donors than complete pooling or independent per-donor fitting.

Compare pooled and individual SINDy, mixed-effect/hierarchical GP baselines, and hierarchical sparse dynamics. Include both common-mechanism and truly different-mechanism settings. Check identifiability first. Overshrinking genuine individual differences would contradict the intended advantage; unobserved variation is not personalized validation. [R06](../../references/BIBLIOGRAPHY.md#r06)

## H5. Treat fidelity as conditional reliability

Hypothesis: paired calibration and input-dependent discrepancy reduce negative transfer when cheap sources predict the wrong direction in part of the domain.

Use NARGP and cost-aware KG as baselines: the underlying idea is not new. A candidate contribution is an evaluation combining biological domain shift, limited bridge observations, acquisition, and calibration. Retract a cost-saving claim when high-only is consistently comparable or better. [R19](../../references/BIBLIOGRAPHY.md#r19) [R20](../../references/BIBLIOGRAPHY.md#r20)

## H6. Are intervals useful after adaptive acquisition?

Hypothesis: appropriate shift-aware calibration reduces overconfidence, but sufficiently large shifts may make intervals too wide for practical decisions.

Compare raw GP intervals, standard split conformal, and an appropriate feedback-shift method. Measure width, abstention, and cost-to-decision in addition to coverage. Record violated assumptions when input density ratios are unavailable or `P(y|x)` changes. FCS guarantees are not universal guarantees for online control. [R23](../../references/BIBLIOGRAPHY.md#r23) [R24](../../references/BIBLIOGRAPHY.md#r24)

## 2. A narrow first research question

A useful starting combination is H1+H2: **under limited observation operators and experimental costs, when does mechanism-discriminating acquisition improve on standard uncertainty acquisition?** Separate known-truth synthetic tests, public-data replay, and approved prospective experiments. Replay alone cannot establish prospective success.

Negative results are deliverables. Mapping where a complex approach loses to simple regression can be more useful for implementation decisions than presenting only favorable demonstrations.
