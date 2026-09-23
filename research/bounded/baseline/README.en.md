# Data-Efficient Bio-Neuro Research | v1.3.0-research.1

[English research entry](TRIAD.en.md) · [한국어](TRIAD.md) · [D/E/F viewer](research/triad/web/index.html) · [16,320-run results](research/docs/en/22_TRIAD_RESULTS.md)

Calibration transport, audit placement/cost, and noise-model/acquisition separation are implemented and studied. Original research, code, and results remain preserved. Zero biological observations; synthetic research modules only.

---
## Preserved v1.2 and earlier entry points below

# Data-efficient bio/neuro AI research | follow-up v1.2.0-research.1

[한국어](README.md) · **English**

Added studies A/B on observations, assumptions and measurement choice, preserving the prior plan and v1.1 executable research.

[Start here](FOLLOWUP.en.md) · [Follow-up viewer](research/followup/web/index.html) · [3,820 evaluation executions](research/docs/en/15_FOLLOWUP_RESULTS.md) · [Next decisions](research/docs/en/16_RESEARCH_DECISIONS.md) · [QA scope](research/followup/quality/QA.md)

The count is 1,900 diagnostic trajectories plus 1,920 acquisition runs, not biological samples. Raw outcomes and failures are included. This is not a production model.

---

## Preserved v1.1 research introduction

# Data-efficient bio/neuro AI research | v1.1.0

[한국어](README.md) · **English** · [Workbench](index.html)

## Added executable research: Closed-loop Research Lab

An **executable synthetic research module** separates observations, assumptions, and intervention decisions while preserving the original plan. No biological data ingestion, clinical validation, or production model is included.

[Setup](research/README.en.md) · [Implementation](research/docs/en/09_IMPLEMENTATION.md) · [504-run pilot](research/docs/en/11_PILOT_RESULTS.md) · [Research direction](research/docs/en/12_RESEARCH_DIRECTION.md) · [Changes](CHANGELOG.md)

```bash
python -m pip install -r research/requirements.txt
python -m research.closed_loop serve
```

Extract the entire repository and open `index.html` for installation-free replay. New computations require the local Python server. Original bilingual chapters 01–08 are unchanged. Inspect the [preservation manifest](research/baseline/manifest.json) and [QA scope](research/quality/QA.md).

---

## Preserved v1.0.0 research introduction

# Data-Efficient Biological and Neural AI Research

[한국어](README.md) · **English**

Research materials on GP/Bayesian regression, active learning, SINDy/PySR, PINN/BINN/UDE, biological foundation transfer, multifidelity modeling and generative augmentation.

> Main judgment: the extensions are feasible and often implemented. Gains from fewer new observations depend on prior information, measurement design and evaluation; they do not establish a universal new theory that beats general AI at every stage. [R02](references/BIBLIOGRAPHY.md#r02) [R07](references/BIBLIOGRAPHY.md#r07) [R13](references/BIBLIOGRAPHY.md#r13)

**Cut-off:** 2026-09-22 · **Version:** 1.0.0 · **Scope:** literature synthesis and study design, not clinical/wet-lab validation.

## Reading guide

| Document | Chapter |
|---|---|
| [Research report](docs/en/01_RESEARCH_REPORT.md) | 01 |
| [Architecture, equations and contracts](docs/en/02_ARCHITECTURE.md) | 02 |
| [Evaluation, leakage and stopping](docs/en/03_EVALUATION.md) | 03 |
| [Imaging, omics, EEG and SBI](docs/en/04_CASE_STUDIES.md) | 04 |
| [Implementation and data map](docs/en/05_IMPLEMENTATION_MAP.md) | 05 |
| [Six hypotheses and falsification plans](docs/en/06_RESEARCH_AGENDA.md) | 06 |
| [Search methods and evidence limitations](docs/en/07_METHODS_LIMITATIONS.md) | 07 |
| [Twelve failure modes](docs/en/08_FAILURE_MATRIX.md) | 08 |

[Glossary](docs/GLOSSARY.md) · [Evidence map](references/EVIDENCE.en.md) · [Bibliography](references/BIBLIOGRAPHY.md) · [Reference JSON](references/references.json) · [BibTeX](references/references.bib)

## Repository contents

```text
Data-Efficient-Bio-Neuro-Research/
├── README.md / README.en.md
├── docs/ko/ · docs/en/        # 8 paired research chapters
├── references/              # 35 sources, 14 claims, search log, BibTeX
├── diagrams/                # editable Mermaid
├── schemas/                 # provenance + model-card JSON Schemas
├── configs/                 # proposed experiment configuration
├── templates/               # paired preregistration and equation cards
├── examples/                # executable synthetic GP demonstration
│   └── results/             # 20-seed results, 4 figures, environment
├── scripts/                 # internal consistency validation
├── tests/                   # numerical and schema regression tests
└── quality/                 # actual validation report
```

The 35 sources include papers, a book, software documentation and data resources. They are not all experimental studies or independently reproduced results. Preprints and reading levels are explicitly labeled.

## Executable scope

See the [synthetic example](examples/README.en.md) and [executed results](examples/RESULTS.en.md). No original datasets or weights are downloaded. The example illustrates GP misspecification and identifiability, not biological performance.

```bash
python -m pip install -r examples/requirements-tested.txt
python examples/gp_active_learning_demo.py --seeds 20
python scripts/validate_repository.py
python -m unittest discover -s tests -v
```

## Publication and rights

No third-party paper PDFs, datasets or model weights are included. A repository-wide public license is [not yet selected](LICENSE.md), leaving that decision to the owner. See [citation guidance](CITATION.md), [third-party notices](THIRD_PARTY_NOTICES.md), and [validation scope](quality/QA.md). Add accurate owner/author information before publication; do not label the proposed architecture a proved new theory.
