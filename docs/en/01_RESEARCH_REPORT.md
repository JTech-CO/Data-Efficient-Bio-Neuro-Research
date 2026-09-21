# Can fewer observations support more trustworthy biological and neural AI?

**Evidence cut-off: 2026-09-22 · Critical literature investigation · Not a wet-lab or clinical validation report**

## 1. Answer and scope

All four proposed extensions are feasible, and many already have research implementations and application examples. They do not, however, constitute a single new theory of regression. Probabilistic function estimation, sparse equation discovery, differential-equation-constrained learning, and large-scale pretraining use different sources of prior information. Their strength is not inference without information; it is making explicit **which information can substitute for additional experiments**. [R01](../../references/BIBLIOGRAPHY.md#r01) [R04](../../references/BIBLIOGRAPHY.md#r04) [R07](../../references/BIBLIOGRAPHY.md#r07) [R11](../../references/BIBLIOGRAPHY.md#r11)

The supported conclusion is conditional: when a task and its prior information align, fewer new observations, annotations, or assay expenditures may reach a specified target. A universal advantage over “general AI” is not established. That comparator must be defined: linear regression, a network trained from scratch, and a pretrained model are materially different baselines. Collection, processing, prediction, explanation, and visualization also require different endpoints. Lower prediction RMSE does not establish better collection automation or a correct mechanism.

### First identify the scarce resource

| Scarce resource | Underlying problem | Promising response | What it cannot establish |
|---|---|---|---|
| Independent donors, animals, or cultures | Biological diversity rather than row count | Hierarchical models, partial pooling, new groups | Thousands of windows are not thousands of new subjects |
| Expensive labels | Expert masks or annotations | Active labeling, frozen encoders, few-shot adaptation | Generalization to an unseen disease or device |
| Temporal or interventional measurements | Many states but weak evidence of change or cause | Dynamics, experimental design, state-space models | A unique causal mechanism from association |
| High-accuracy assays | Abundant cheap simulations | Multifidelity modeling and discrepancy estimation | Turning a wrong simulator into reality |
| Access permissions | Restricted or conditional data | Metadata catalogs, authorized APIs, collaboration | Replacing consent or access rights with regression |

Large public cell atlases and neurophysiology archives coexist with shortages of independent observations for a particular question. It is unhelpful to classify all biology as either data-rich or data-poor. [D01](../../references/BIBLIOGRAPHY.md#d01) [D02](../../references/BIBLIOGRAPHY.md#d02)

## 2. Existing combinations and their evidence boundaries

| Combination | Located example | What is demonstrated | Invalid extrapolation |
|---|---|---|---|
| GP plus active design | GPAL; cell-culture-media BO | Iterative behavioral and culture-condition design | A universal reduction factor across biology |
| Sparse equations plus ensembles and acquisition | Ensemble-SINDy | Stability estimates and active data selection | Inclusion frequency as causal truth probability |
| Noise-robust equation discovery | Weak SINDy | Integral estimation rather than point derivatives | Automatic recovery of hidden states or missing terms |
| BINN | Wound-healing reaction-diffusion assays | Mechanism candidates from real in-vitro data | Validation of complete human wound healing |
| PINN/X-TFC plus symbolic regression | AI-Aristotle | A gray-box research workflow | Treating predominantly synthetic evaluation as clinical validation |
| Hybrid dynamics followed by sparse extraction | Wu and colleagues | Denoising and equation candidates | Treating fitted-model trajectories as fresh evidence |
| Biological foundation transfer | scGPT, CellSAM, LaBraM | Modality-specific representations and adaptation | Ignoring the upstream pretraining information budget |
| Multifidelity GP/BO | NARGP; BoTorch qMFKG | Related fidelity levels and cost-aware queries | Assuming species or cell lines have a simple accuracy ordering |

Sources: [R02](../../references/BIBLIOGRAPHY.md#r02) [R03](../../references/BIBLIOGRAPHY.md#r03) [R04](../../references/BIBLIOGRAPHY.md#r04) [R05](../../references/BIBLIOGRAPHY.md#r05) [R07](../../references/BIBLIOGRAPHY.md#r07) [R08](../../references/BIBLIOGRAPHY.md#r08) [R09](../../references/BIBLIOGRAPHY.md#r09) [R11](../../references/BIBLIOGRAPHY.md#r11) [R14](../../references/BIBLIOGRAPHY.md#r14) [R17](../../references/BIBLIOGRAPHY.md#r17) [R19](../../references/BIBLIOGRAPHY.md#r19) [R20](../../references/BIBLIOGRAPHY.md#r20). Locating a paper or implementation is not independent reproduction. Only the separate synthetic GP demonstration in this package was executed here.

## 3. GP/Bayesian regression plus active learning

A GP places a distribution over functions and updates predictive means and covariances after observations. With a Gaussian observation model,

$$
\mu_* = m_* + K_{*X}(K_{XX}+\Sigma)^{-1}(y-m_X),
$$
$$
V_* = K_{**}-K_{*X}(K_{XX}+\Sigma)^{-1}K_{X*}.
$$

This is latent-function variance. Predicting a new measurement additionally requires observation noise. An incorrect heteroscedastic or correlated-noise model can invalidate practical calibration even when the algebra is correct. Nonparametric does not mean assumption-free. [R01](../../references/BIBLIOGRAPHY.md#r01)

Acquisition must match the scientific objective. Learning a response surface calls for uncertainty reduction over the target domain; parameter inference calls for information about parameters; optimizing an assay calls for expected improvement or knowledge gradient. Finding a good optimum is not the same as reconstructing the whole response curve. Replicates inform noise, whereas new conditions inform shape; their respective costs belong in the decision. [R02](../../references/BIBLIOGRAPHY.md#r02) [R20](../../references/BIBLIOGRAPHY.md#r20)

**Recommended design:** start with low-dimensional, scientifically meaningful inputs, such as concentrations, measurement time, stimulation strength, or validated representations. Represent donor and batch effects explicitly. Do not automatically feed entire images or gene vectors into a small exact GP. Standard exact GP factorization is generally cubic in the number of training observations, with quadratic covariance storage. Approximations change the computational burden but also require calibration checks. [R01](../../references/BIBLIOGRAPHY.md#r01)

A central failure is confidence conditional on a wrong model. If a fixed kernel cannot express a sharp transition, acquisition can repeatedly reinforce that blind spot. The proposed safeguards are kernel sensitivity checks, group-specific errors, replicates, and a small independently specified exploration component. These are operational recommendations, not a newly proved optimal algorithm.

## 4. Mechanistic and symbolic methods: falsifiable equations, not attractive curves

SINDy commonly selects sparse coefficients in `dx/dt = Theta(x,u) Xi`. PySR searches expression structures and operators, producing accuracy-complexity trade-offs. A PINN combines observation fitting with differential-equation residuals. A Neural ODE integrates a learned continuous vector field; its name alone implies neither mechanistic constraints nor biological interpretability. UDEs combine known dynamics with learnable unknown components. [T01](../../references/BIBLIOGRAPHY.md#t01) [R28](../../references/BIBLIOGRAPHY.md#r28) [T03](../../references/BIBLIOGRAPHY.md#t03) [R10](../../references/BIBLIOGRAPHY.md#r10)

A typical PINN objective is

$$
\mathcal L = \mathcal L_{obs} + \lambda_{dyn}\mathcal L_{dyn} + \lambda_{bc}\mathcal L_{bc}.
$$

Collocation locations are locations at which an equation is checked, not additional biological observations. Strongly established conservation laws may warrant hard constraints. Empirical kinetics and uncertain boundary conditions need room to be wrong. Increasing a constraint weight does not itself improve mechanistic correctness. Optimization failures in PINNs and sparse-data training problems in biological UDEs are documented. [R27](../../references/BIBLIOGRAPHY.md#r27) [R10](../../references/BIBLIOGRAPHY.md#r10)

**Recommended progression:** define the observation model and the smallest mechanistic model first. Fit an ordinary numerical solver with a measurement likelihood as a baseline. Use weak/integral estimation when differentiation amplifies noise. Add a small residual GP or neural component only when needed, and extract symbolic candidates afterward. Adding every flexible component at once is not a default improvement.

### Identifiability is not predictive accuracy

Consider the constructed counterexample `y=(a+b)x`. Observations identify the sum but cannot distinguish `(a,b)=(1,2)` from `(2,1)` for any x. More observations of the same type cannot separate the parameters. A different measurement, an independently informative intervention, or the honest reparameterization `c=a+b` is required. Sparse, readable biological models can likewise be structurally unidentifiable. [R06](../../references/BIBLIOGRAPHY.md#r06)

The output should therefore be an equation card containing candidates, units, validity domain, coefficient uncertainty, unobserved states, and proposed falsification experiments. A short equation, high R², and a convincing phase portrait do not individually establish causality. Observational association and interventional effects remain separate claims.

## 5. Few-shot and biological foundation models

Pretraining can save new labels without making the total information budget small. Upstream data, annotations, and representation design supply information. “Twenty new labels” is not equivalent to “the model has seen twenty examples.” scGPT explicitly combines large-scale single-cell pretraining with downstream adaptation. [R11](../../references/BIBLIOGRAPHY.md#r11)

Images emphasize object masks, omics emphasizes counts and cell states, and EEG emphasizes temporal, channel, and device structure. Obtaining a latent vector does not make the downstream scientific tasks interchangeable. The recommended escalation is **raw-feature baseline → frozen encoder plus ridge/GP/linear probe → small adapter → selective fine-tuning**. Retain the smaller model when independent validation provides no improvement. Training fewer parameters does not prove that fewer independent biological samples suffice.

Contradictory evidence is informative rather than inconvenient. Some single-cell zero-shot evaluations and gene-perturbation benchmarks found simple methods highly competitive or better. Neither result warrants rejecting all fine-tuned foundation models. CellSAM offers an image-domain example, while a particular organoid-imaging study illustrates the value of task-specific adaptation. [R12](../../references/BIBLIOGRAPHY.md#r12) [R13](../../references/BIBLIOGRAPHY.md#r13) [R14](../../references/BIBLIOGRAPHY.md#r14) [R16](../../references/BIBLIOGRAPHY.md#r16)

A July 2026 cross-modality benchmark preprint similarly reports task-dependent rankings. It is an update motivating further scrutiny, not peer-reviewed confirmation. [R29](../../references/BIBLIOGRAPHY.md#r29)

For EEG, audit overlap between pretraining and evaluation data. The LaBraM implementation and NeuralBench documentation should be read together. A warning about particular datasets is not evidence that every reported LaBraM result is contaminated. [R17](../../references/BIBLIOGRAPHY.md#r17) [R18](../../references/BIBLIOGRAPHY.md#r18)

## 6. Multifidelity and generative augmentation

A simple multifidelity structure is `f_H(x)=rho f_L(x)+delta(x)`: learn both transferable structure and disagreement. Nonlinear, input-dependent relationships are also possible. However, a cheap source is not necessarily a lower-accuracy measurement of the same target. Different cell lines or species may instead require a domain-transfer model. [R19](../../references/BIBLIOGRAPHY.md#r19)

The proposed progression is paired bridge observations, a high-fidelity-only baseline, cost-aware query selection, and a negative-transfer check on separately held-out high-fidelity data. Harmful sources need a down-weighting or exclusion path. A large synthetic sample count must not overwhelm a small real-data likelihood merely by duplication. [R20](../../references/BIBLIOGRAPHY.md#r20)

Distinguish label-preserving image transformations, mechanistic simulations, and fitted generative distributions. scDesign3 illustrates statistical simulation for single-cell and spatial data. Its generated observations remain consequences of fitted assumptions, not independent experiments. [R21](../../references/BIBLIOGRAPHY.md#r21)

Preserve `real / simulated / generated / imputed` provenance and keep raw data immutable. Fit generators inside the training split. Evaluate on unaltered held-out real data. Check rare states, source-label shortcuts, multivariate structure, and downstream utility separately. Synthetic data do not automatically provide privacy protection. [R22](../../references/BIBLIOGRAPHY.md#r22)

## 7. An alternative: an auditable, intervention-oriented loop

The proposed architecture is **observation-aware, assumption-checking, and intervention-oriented**. It is a synthesis of existing methods, not a new theorem or an empirically superior finished system.

1. Specify what the instrument measures, separating intensity, counts, or voltage from hidden biological states.
2. Separate predictor, mechanistic candidates, measurement noise, and individual variation, while propagating their uncertainty.
3. Choose a query over time, readout, replicate status, fidelity, and intervention, not merely the next input point.
4. Permit scientific claims only after independent real-data and identifiability checks.

Adaptive selection changes calibration conditions. Conformal methods for feedback covariate shift already exist, but their weighting and stable-conditional-distribution assumptions must hold. Their guarantees do not automatically cover arbitrary shifts or every sequential biomedical deployment. [R23](../../references/BIBLIOGRAPHY.md#r23) [R24](../../references/BIBLIOGRAPHY.md#r24)

When a neural simulator has an intractable likelihood, simulation-based inference is another option. It can infer a distribution of compatible parameters rather than one best fit, at potentially substantial simulation cost. Simulator adequacy and computational efficiency must be evaluated separately from the number of new observations. [R25](../../references/BIBLIOGRAPHY.md#r25) [R26](../../references/BIBLIOGRAPHY.md#r26)

## 8. Decision

The practical first target is not an AI that solves all biology from almost no data. It is **one well-defined observation system and estimand in which the new workflow reduces real experimental cost without sacrificing accuracy, uncertainty quality, or interpretive validity**. Prioritize GP-based querying, observation and group separation, weak-form dynamics, and real-data validation gates. Add a foundation model where its representation provides demonstrated modality-specific value.

See [architecture](02_ARCHITECTURE.md), [evaluation](03_EVALUATION.md), [case studies](04_CASE_STUDIES.md), [implementation map](05_IMPLEMENTATION_MAP.md), [research agenda](06_RESEARCH_AGENDA.md), and [methods and limitations](07_METHODS_LIMITATIONS.md).
