# Verification record | v1.4.0-research.1

Research date: 2026-09-23 (Asia/Seoul). UTC timestamps inside execution logs retain the actual runtime clock. These are software and synthetic numerical checks, not external scientific, biological, clinical or security certification.

## Test suites

| Suite | Tests | Result |
|---|---:|---|
| Original examples (`tests`) | 14 | Passed |
| Initial closed loop (`research/tests`) | 63 | Passed |
| Diagnostic follow-up (`research/followup/tests`) | 43 | Passed |
| Transport / audit / noise triad (`research/triad/tests`) | 61 | Passed |
| New bounded-evidence modules (`research/bounded/tests`) | 32 | Passed |
| Total | **213** | **Passed** |

Logs: [original](tests-original.log), [closed loop](tests-closed-loop.log), [diagnostic](tests-diagnostic.log), [triad](tests-triad.log), [new](tests-bounded.log), [suite return codes](test-suites.json).

## Numerical verification

[validation.json](validation.json) records all 8,208 runs and 1,575,072 serialized observations. Record hashes, evidence roles, synthetic-only flags, costs, freeze order, all aggregate statistics and planned paired contrasts were recalculated. All 105 representative runs were fully replayed and exactly matched. All numerical source/configuration hashes remained frozen. G bias-profile nesting and H identical training data across audit policies were checked. The largest pure-error partition discrepancy was 1.7763568394002505e-15. No I variance-clipping events occurred in the reported evaluation.

The first synchronous full validator invocation exceeded the tool time limit; the validator was subsequently run to completion as a process in the same task. This was not a scientific evaluation failure or a reason to change numerical code. The final report—not the timed-out attempt—is the evidence of completion. The final scientific evaluation completed without rerunning a modified evaluation bank.

New public demo commands for G/H/I, seed 27, were also executed in a separate temporary output directory; those demos do not modify or contribute to the locked evaluation summaries. Overwrite refusal is covered by unit tests.

## Browser and transport

[browser.json](browser.json) contains **126 passed checks** over all 105 representative selector combinations, bilingual controls, data counts, mobile document overflow, JavaScript errors and direct JSON retrieval. Desktop/mobile screenshots are generated from the exact deployment assets.

**A real browser navigation to localhost was attempted and failed with `net::ERR_BLOCKED_BY_ADMINISTRATOR`.** See [initial failure](browser-navigation-failure.log). The smoke script then explicitly injected the HTML/CSS/JS deployment assets into a page for rendering and interaction tests, while checking local HTTP transport separately with Python. It did not certify end-to-end browser-to-localhost navigation, native browser downloads, file-URL navigation, Windows/macOS installation, or GitHub Pages deployment. No remote deployment occurred. The original failure was preserved rather than hidden.

The optional [browser script](../browser_smoke.py) requires Playwright and Chromium; these are QA tools, not runtime requirements for the numerical package. Its current Chromium executable path is environment-specific. On a machine where localhost navigation is allowed, it attempts normal HTTP first.

Screenshots: [Korean desktop](viewer-desktop-ko.png), [English desktop](viewer-desktop-en.png), [Korean mobile](viewer-mobile-ko.png), [replicate view](viewer-I-ko.png). Mobile tables/plots use independent horizontal scroll areas instead of shrinking labels to unreadable sizes.

## README and preservation

The main READMEs have one current version marker each and no previous release bodies. [VERSIONS](../../../VERSIONS.md) / [English history](../../../VERSIONS.en.md) are the active release index. Original README/checksum bytes are archived in [baseline](../baseline/manifest.json); snapshot relative links deliberately preserve original text, so use the active version index for navigation.

Only the two READMEs and root checksum list are changed among baseline files. Previous numerical modules, raw results and original chapters remain unchanged. [documentation-validation.json](documentation-validation.json) records current Markdown path checks and README assertions. Link anchors and live remote URLs are not certified by that local path check.

## Reproducible environment and packaging scope

Runtime: Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0 on Linux x86_64. [Actual environment](../results/v140/environment.json). The dependency ranges in the existing requirements file are preserved; this does not guarantee installation on every operating system.

ZIP CRC, every distributed file checksum and exact base-plus-overlay equality are verified during packaging. The external package-validation JSON records final filenames, sizes and checksums. SHA-256 detects accidental changes; it is not a digital signature or authenticity guarantee. Cached bytecode is not distributed.
