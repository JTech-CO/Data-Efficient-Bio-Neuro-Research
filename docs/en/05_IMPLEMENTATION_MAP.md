# Implementation and public-data map

## 1. Entry points and verification level

These are official documents or implementation paths supplied by the reviewed papers. **This is not a list of repositories that were cloned, installed, and independently reproduced.** Check APIs and licenses at the adopted release/commit. No third-party weights, papers, or original datasets are redistributed in this ZIP.

| Tool or prior implementation | Role | Entry point | Before adoption |
|---|---|---|---|
| GPAL | Behavioral active design reference | [Paper and code statement](https://doi.org/10.1016/j.cogpsych.2020.101360) | Task and acquisition objective |
| BoTorch qMFKG | Cost-aware multifidelity BO | [Versioned example](https://botorch.org/docs/v0.16.1/tutorials/multi_fidelity_bo) | Target fidelity and cost assumptions |
| PySINDy | Sparse/weak dynamics | [Documentation](https://pysindy.readthedocs.io/en/stable/) | Derivative estimator, library, optimizer |
| PySR | Restricted expression search | [Physical-unit examples](https://ai.damtp.cam.ac.uk/pysr/dev/examples/physics) | Julia, operators, complexity, units |
| DeepXDE | PINN/BINN-style training | [Documentation](https://deepxde.readthedocs.io/en/latest/) | Backend, loss scales, BC/IC |
| AI-Aristotle | Gray-box plus symbolic discovery | [Repository](https://github.com/mariodeflorio/AI-Aristotle) | Predominantly synthetic validation |
| Wu model-discovery | Hybrid-to-sparse selection | [Repository](https://github.com/maclean-lab/model-discovery) | Lineage of simulated trajectories |
| Massonis identifiability | Reparameterizing sparse models | [Code archive](https://zenodo.org/records/7713048) | MATLAB/toolbox requirements |
| NARGP | Nonlinear fidelity relationships | [Repository](https://github.com/paraklas/NARGP) | Fidelity correspondence, older dependencies |
| LaBraM | Frozen EEG representations | [Repository](https://github.com/935963004/LaBraM) | Montage, scaling, overlap |
| SBI/sbibm | Likelihood-free inference evaluation | [Benchmark](https://github.com/sbi-benchmark/sbibm) | Simulator adequacy and posterior diagnostics |

Sources: [R02](../../references/BIBLIOGRAPHY.md#r02) [R08](../../references/BIBLIOGRAPHY.md#r08) [R09](../../references/BIBLIOGRAPHY.md#r09) [R17](../../references/BIBLIOGRAPHY.md#r17) [R19](../../references/BIBLIOGRAPHY.md#r19) [R20](../../references/BIBLIOGRAPHY.md#r20) [R26](../../references/BIBLIOGRAPHY.md#r26) [T01](../../references/BIBLIOGRAPHY.md#t01) [T02](../../references/BIBLIOGRAPHY.md#t02) [T03](../../references/BIBLIOGRAPHY.md#t03). PySR dimensional penalties require a separate equation-validity check; they are not hard proofs. [T02](../../references/BIBLIOGRAPHY.md#t02)

## 2. Begin with a small manifest, not a large download

| Resource | Initial use | Required checks |
|---|---|---|
| [CELLxGENE Census](https://chanzuckerberg.github.io/cellxgene-census/) | Metadata-filtered reference slices | Original-study citations, release, duplicates, donors |
| [DANDI](https://dandiarchive.org/) | Neurophysiology and optophysiology discovery | Dandiset terms, species, readout and version |
| [PhysioNet EEG](https://physionet.org/content/eegmmidb/1.0.0/) | Basic EEG decoding evaluation | Run-specific labels, group split, pretraining overlap |
| Data linked by R07/R14 | Cell images and assays | Images versus independent experiments |
| Perturbation data linked by R13 | Control/response evaluation | Cell lines, interventions, replicates and licenses |
| GEO data linked by R09 | Trace the biological-dynamics example | Accession, physical time and lineage definitions |

Census supplies slice-based access and duplicate metadata. DANDI covers several neurophysiology modalities. The cited PhysioNet release specifies ODC-By 1.0. A public portal does not imply identical licensing for every downstream use. [D01](../../references/BIBLIOGRAPHY.md#d01) [D02](../../references/BIBLIOGRAPHY.md#d02) [D03](../../references/BIBLIOGRAPHY.md#d03)

OpenNeuro and BioModels were additional discovery candidates, but the browser session returned an empty dynamic page or an error. They are therefore not included in the verified dataset inventory. This is not a statement that either resource is unavailable.

## 3. Build sequence

Start with ingestion manifests, group splits, simple baselines, and serializable metrics. Add acquisition next, observation-aware dynamics afterward, and foundation adapters/multifidelity last. Pin run IDs, seeds, code commits, and package versions so each stage remains comparable.

Prefer typed schemas, small validators, and explicit approval boundaries over allowing an LLM to freely download, transform, and interpret everything. An LLM can assist metadata extraction, document navigation, and equation-card explanations, but should not invent numerical evidence or source claims.

## 4. Compute planning

Run small exact GPs, simple regression, and modest sparse libraries on CPU first. Evaluate cached frozen embeddings before repeated encoder fine-tuning. Cache provenance includes training release and transform hashes. GPU needs depend on resolution, sequence length, batch size, and optimizer state; this report does not promise full-stack execution on an untested laptop.

Actual demo dependencies appear in `examples/requirements-tested.txt`, with environment metadata in `examples/results/environment.json`. These are not a compatibility lock for the entire upstream research stack.
