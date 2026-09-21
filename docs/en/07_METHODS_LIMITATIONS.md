# Search methods, dates, and limitations

## Scope

This is a **targeted critical literature investigation** as of 2026-09-22, centered on Consensus and supplemented by publishers, original papers, author repositories, and official documentation. It is not an exhaustive systematic review, meta-analysis, PRISMA study, or inventory of every relevant publication. Effects from incompatible datasets were not pooled into an average saving.

## Search and selection

Workstreams covered GP/acquisition, equation discovery, biological constraints/UDEs, foundation adaptation, and multifidelity/generation. Searches included failures, identifiability, misspecification, leakage, simple baselines, and noise rather than success reports alone. Exact Consensus queries are in the [search log](../../references/search_log.json). Core Consensus records were fetched before use; additional areas were checked through primary web sources. One composite EEG search hit a rate limit and was supplemented with official-source research.

The 35 references include papers, a book, and official software/data documents; they are not 35 experimental studies. DOI, publication status, access date, reading level, and caveats are provided in JSON, BibTeX, and Markdown. `full_text_html` means accessible article text was inspected, not every supplement or experiment reproduced. `abstract_or_primary_page` and `author_repository` represent more limited inspection.

## Metadata corrections

Journal years override inconsistent index/preprint years: Weak SINDy 2021, Ensemble-SINDy 2022, AI-Aristotle 2024, and Wu model discovery 2025. The AI-Aristotle author list was corrected from the publisher, including its first author. scDesign3 distinguishes online 2023 from issue 2024. A 2026 documentation year denotes access, not publication.

R29 is explicitly a July 2026 **preprint**. R28 uses the preprint linked by official documentation; later publication status was not resolved. CellSAM and Cellpose-SAM are distinct projects. A tissue-multifidelity candidate with insufficient fetched content was not promoted to a core evidence record.

## Evidence limitations

Cell, animal, human, synthetic, and retrospective benchmark studies are different evidence types. Results in one dataset are not automatically transferable to another disease or site. Positive original studies and critical external benchmarks are retained together; different tasks need not constitute a contradiction. Numerical claims require attention to estimated versus direct comparisons.

The synthesis is limited to retrieved text, abstracts, and documentation. It does not claim access to unseen paywalled content. Supplements, software releases, upstream licenses, and long-term link availability were not comprehensively audited. Some OpenNeuro/BioModels browser retrievals were insufficient and were not counted as adopted datasets.

## Completed and not completed

Completed: bilingual research documents, evidence/failure maps, proposed architecture, validation plans, provenance schemas, execution of a synthetic-only GP example, and internal link/reference/schema/ZIP checks.

Not completed: biological dataset downloads or model training, foundation fine-tuning, comprehensive upstream reproduction, wet-lab/clinical experiments, or remote GitHub upload. Demo numbers are not biological performance evidence.

Proposed improvements are hypotheses, not proved new theory or validated superiority. Uncertainty is a reason to design a discriminating study, not a claim that further research is impossible.
