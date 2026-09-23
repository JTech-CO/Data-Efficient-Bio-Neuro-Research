# 31. Reproducibility, documentation cleanup and verification boundaries

[한국어](../ko/31_REPRODUCIBILITY.md) · [Guide](../../../BOUNDED.en.md) · [Detailed QA](../../bounded/quality/QA.md)

## Reproduction unit and freeze

`prepare` recorded 60 development runs and froze numerical source, configuration, execution plan and development hashes. Documents and the viewer were written after evaluation; frozen numerical code was unchanged. The 8,208 runs use new seeds from known synthetic families, not independent external preregistration or a biological blind evaluation. G has analytic final truth comparison; H/I release fresh final measurements only after freezing fits and bootstrap.

All records are in `raw/G.jsonl.gz`, `H.jsonl.gz` and `I.jsonl.gz`, with observations, costs, roles, assumptions, evaluations and hashes. `summary.json` contains 363 cells; `paired.json` contains prespecified same-world comparisons. The viewer presents 105 representative runs without deleting other outcomes. Raw data are ordinary gzipped JSON Lines, requiring no custom restoration algorithm.

## Verification

All 181 inherited and 32 new tests passed: 213 total. All 8,208 records, 1,575,072 serialized observations, summaries and paired contrasts were revalidated. All 105 representative runs were fully recomputed and exactly matched. Serialized counts include records reused across designs/policies and are not biological sample sizes. Checks include G set nesting, H identical training data at fixed allocation, I pure-error decomposition and separate public G/H/I demo executions.

Actual localhost browser navigation was attempted but blocked by managed policy. Exact deployment assets were then injected for 126 rendering/interaction/data checks; HTTP JSON transport was checked separately. Full browser URL-to-download operation, native Windows/macOS installation and remote Pages deployment were not validated. Initial failure logs remain public. The first synchronous validator attempt exceeded a tool time limit; the subsequent complete verification is reported separately and no numerical evaluation was modified or selected because of that timeout.

## README cleanup

README.md and README.en.md now contain the current release, project description, current research links and execution entry points. Historical navigation moved to VERSIONS.md and VERSIONS.en.md. Original READMEs and checksum bytes remain in `research/bounded/baseline/`; their relative links were intentionally not rewritten, so use the active version index.

The baseline is the preceding v1.3.0 Transport-Audit-Noise ZIP. Among its 1,132 files, only the two READMEs and root checksum list change. Final file counts, ZIP sizes, checksums and exact overlay equality are recorded by packaging validation. Compare remote/local edits before merging. No remote GitHub read, commit or deployment occurred.

## Scientific and operational scope

The source log distinguishes Consensus search/fetch from author, publisher and NIST material. Abstract-only access is not described as a full-paper reproduction. Existing license/author policies remain. These checks do not certify empirical bias limits, measurement independence, production performance or laboratory automation safety.
