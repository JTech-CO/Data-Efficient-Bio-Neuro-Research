# Modality-specific implementation scenarios

**These are proposed studies, not results from training the listed biological models or datasets in this package.**

## A. Cell images → density trajectories → migration/growth candidates

**Question:** can fewer expert segmentations support prediction of temporal changes in unseen culture conditions? Annotation savings and kinetic identification are separate objectives.

Compare CellSAM and task-specific segmentation under frozen and selectively adapted settings. Do not choose a winner by model name. CellSAM, Cellpose3, and the organoid comparison address different contexts. [R14](../../references/BIBLIOGRAPHY.md#r14) [R15](../../references/BIBLIOGRAPHY.md#r15) [R16](../../references/BIBLIOGRAPHY.md#r16)

Keep raw images and manual masks. Generate alternative density trajectories reflecting segmentation uncertainty instead of passing mean counts as unquestioned observations. Where reaction-diffusion is appropriate, consider `∂t c = ∇·(D(c)∇c)+R(c)`. BINN application to real assays provides relevant prior work. [R07](../../references/BIBLIOGRAPHY.md#r07)

Begin with an established segmentation baseline, logistic growth/constant diffusion, and ordinary solver fitting. Then test weak-form discovery or a constrained BINN. Compare acquisition based on segmentation ambiguity with acquisition sensitive to downstream density or parameter uncertainty.

Split donors, organoids, and slides. Report object AP, count bias, and boundary errors separately from density rollout. If migration and proliferation compensate, report only identifiable combinations. Design additional readouts or conditions capable of discriminating the explanations; this is an information requirement, not a wet-lab protocol.

Explicit alternative explanations include bleaching mistaken for loss of cells, merged masks mistaken for suppressed proliferation, and cells leaving the field mistaken for death. Preserve raw intensity and field geometry so these alternatives remain testable.

## B. Single-cell omics → perturbation-response prediction

**Question:** how well can a model predict change from control in new donors, cell lines, or interventions? Cell-type recognition and intervention forecasting are different endpoints.

Census supports reference-cell and metadata discovery. Pin the release and record duplicate metadata such as `is_primary_data`. An observational atlas is not automatically a paired perturbation dataset. Interventional evaluation needs original measurements and designs, such as those linked by R13. [D01](../../references/BIBLIOGRAPHY.md#d01) [R13](../../references/BIBLIOGRAPHY.md#r13)

Fit count preprocessing within training. Compare no-change, mean-change, additive/linear, biological-feature regression, and frozen embeddings with the same head before testing adapters. Hold donor and perturbation splits fixed. An unseen gene intervention is different from a known intervention in a new donor.

As a constructed illustration, 10,000 cells from five donors do not become 10,000 independent donors. Record actual transformations because ranking, binning, and normalization encode different information.

Evaluate `Δexpression = response - matched control`, per-perturbation errors, direction of effect, and preregistered gene panels. Do not inspect test labels and then choose a favorable primary gene subset. High correlation in total expression can coexist with a near-no-change prediction; score both separately. R13 motivates the strong simple baselines. [R13](../../references/BIBLIOGRAPHY.md#r13)

Pseudotime from snapshots of different cells is not a longitudinal measurement of one cell. Without validated time, lineage, or intervention information, label the result trajectory-inspired rather than assigning physical kinetic rates. Generated scRNA can stress-test estimators but cannot establish the response of an unobserved cell type. [R21](../../references/BIBLIOGRAPHY.md#r21)

## C. EEG → fewer personal labels for new-user prediction

**Question:** can personal calibration labels be reduced while retaining balanced performance and latency for unseen users? Successful EEG classification does not establish anatomical connectivity or a diagnostic mechanism.

The PhysioNet Motor Movement/Imagery dataset is a candidate public starting point. Map T1/T2 labels using run type, because the official documentation assigns different meanings across run types. Preserve original sampling, channels, reference, and artifact-processing records. [D03](../../references/BIBLIOGRAPHY.md#d03)

Compare spectral features with a ridge/logistic head, a small network, frozen LaBraM with the same head, and a limited adapter. Verify sampling, amplitude scaling, and channel-order compatibility with the pretrained model contract. Overlapping windows do not add independent subjects.

Audit whether pretrained weights already include evaluation data. NeuralBench warns about overlap for PhysioNet Motor Imagery and TUAR. Do not use those data with affected weights as the clean primary demonstration of external-dataset generalization; label a known-overlap track or obtain independent recordings. Preserve the documentation's distinctions for other datasets, including TUAB/TUEV. [R17](../../references/BIBLIOGRAPHY.md#r17) [R18](../../references/BIBLIOGRAPHY.md#r18)

Report macro-F1 against label budget, the subject-level distribution, worst-group performance, and measured inference latency. Check whether acquisition overselects movement artifacts or neighboring windows. Distinguish regression intervals from classification confidence. Provide abstention and version preprocessing, model, and decision threshold together.

## D. Neural/biochemical simulators → compatible parameter distributions

SBI is an alternative when simulator likelihoods are difficult to evaluate. Sample parameters, simulate observations, and estimate a distribution of parameters compatible with measurements; neural dynamics supplies established examples. [R25](../../references/BIBLIOGRAPHY.md#r25)

Start with a small checkable model and genuinely measurable readouts. Budget simulator calls separately. Perform posterior predictive checks and simulator-misspecification stress tests. An artificially narrow posterior is not success. Preserve multiple compatible explanations rather than forcing one optimum.

Apply multifidelity first where correspondence is explicit, such as resolution or approximation levels of the same model. For species, tissue, or device differences, decide whether the problem is instead domain transfer. Check for misleading low-fidelity posterior modes and retain a high-only baseline. [R19](../../references/BIBLIOGRAPHY.md#r19) [R26](../../references/BIBLIOGRAPHY.md#r26)

## Suggested starting point

For a small first study, fix segmentation in scenario A and compare only density dynamics, or test identification and acquisition on known synthetic dynamics in D. Omics and EEG introduce additional representation, batch, and overlap variables. Do not begin by claiming a unified cross-modality result. Actual priority depends on available independent observations and authorized experimental access.
