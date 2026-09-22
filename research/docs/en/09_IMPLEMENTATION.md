# 09. Executable closed-loop research architecture

**Version 1.1.0 · synthetic research only · 2026-09-22**  
[한국어](../ko/09_IMPLEMENTATION.md) · [Research entry](../../README.en.md) · [Original architecture](../../../docs/en/02_ARCHITECTURE.md)

## Purpose and boundary

This is an additive, executable research slice, not a replacement for the original plan. It tests whether observations, assumptions, and intervention decisions remain distinguishable in code. It does not implement a biological production model, ingest real biological records, reproduce cells or neurons, or establish clinical validity.

The central question is not just whether predictions are accurate, but which measurement distinguishes which assumption, and whether failure is noticed. Restricted parts of H1, H2, and H5 are executable. H3 has provenance guards; H6 has diagnostics. H4, SINDy, PINN, BINN, UDE, and foundation-model adaptation remain future research. The original 01–08 chapters are unchanged.

## Run the implementation

From the repository root:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -r research/requirements.txt
python -m research.closed_loop serve
```

Open `http://127.0.0.1:8765`. The new-experiment button performs an actual Python computation and saves its result under `research/results/local/`. This is a same-computer research server, not a public multi-user service. On Windows, substitute `py` if that is the configured interpreter command.

```bash
python -m research.closed_loop run --scenario mechanism_pair --policy guarded --seed 27 --budget 24 --output research/results/local-run.json
python -m research.closed_loop audit research/results/local-run.json
python -m research.closed_loop suite --config research/configs/pilot.json
```

`run` computes one experiment; `suite` executes the 504-run matrix; `audit` checks internal consistency. Audit accepts both `.json` and `.json.gz`. Reusing an output path replaces that output; use a new `--output` to retain earlier experiments.

For installation-free viewing, extract the entire repository and open `index.html`. Static files and GitHub Pages replay **42 included seed-zero design cells**, with aggregate statistics across all twelve seeds. Replay is not retraining. New seeds or budgets require the local server. The native browser bundle is gzip/base64 and uses `DecompressionStream`; no external dependency or network fetch is needed. Use a browser supporting that API, documented in [implementation sources](../../SOURCES.md). Copying the HTML alone is insufficient.

The bilingual, responsive UI includes prediction/readout views, conditional intervals, provenance, a step-wise assumption register, acquisition decisions, policy comparisons, and the H1–H6 research map. It exports full runs and event logs and imports run JSON. Browser shape checks on imported files are not equivalent to Python audit. Neither imported code nor arbitrary real data is executed.

## The three boundaries

```text
measurement ledger -> training-only fit -> reused diagnostic check
 -> assumption register -> costed query proposal -> synthetic approval
 -> oracle measurement -> ledger append -> repeat or stop
 -> freeze model -> reveal final test once -> report
```

**Observation:** immutable Measurement records contain values, declared measurement noise, cost, split, group, origin, and lineage. A measurement is not silently promoted to an observed latent state.

**Assumption:** a separate register describes the observation operator, declared noise, kernel or finite hypothesis family, likelihood identifiability, and fidelity relation. “Not rejected” is not “true.” A residual alarm does not localize sensor error versus mechanism error.

**Intervention:** Query separates condition, readout, intervention, fidelity, replicate, and group. Proposal, simulator approval, and committed observation are separate events. Approval authorizes only a call inside a finite synthetic design; no instrument or biological intervention is connected.

Oracle reference truth is restricted to evaluation. Policy and model modules do not import the oracle. A test changes final labels without changing earlier query choices. Diagnostics used for model selection are explicitly reusable validation, not a locked final test.

## Implemented models

### Observation-aware linear regression

For latent coefficients \(\theta=(a,b)\), observations follow \(y=h(q)\theta+\epsilon\). Sum readout uses \((x,x)\), selective readout \((x,0)\), and synthetic attenuation of the second component \((x,0.2x)\).

Sum measurements alone have likelihood-design rank one. A proper Gaussian prior can make posterior covariance invertible without making both coefficients data-identifiable. Rank is therefore computed from the observation design without the prior. The identity ablation incorrectly maps every readout to \((x,x)\), deliberately ignoring measurement semantics.

Projected information gain is \(\frac12\log(1+h\Sigma h^T/\sigma_q^2)\), divided by query cost for the information-gain policy. Comparators include uniform eligible-action sampling, sum-only acquisition, and observation-projected variance. Sum-only acquisition is a restricted-action-space comparison, not an equal-information algorithm comparison.

A weighted least-squares baseline with the correct observation operator is also fit to exactly the same training queries. Bayesian regression is not assumed to improve on this simple, appropriate baseline.

### Finite mechanism library

Candidate A has components \((x,x^2)\); B has \((x^2,x)\). Sum readout is identical, but selective readout and intervention can separate them. A uniform prior is updated from training likelihoods only.

The acquisition criterion is **observation-space** \(I(M;Y_q\mid D)\), evaluated by twelve-node Gauss–Hermite integration of expected log mixture density. This is information about the declared candidate library, not universal mechanistic truth. Observation intervals invert the Gaussian-mixture CDF; latent intervals use the discrete candidate distribution.

A maximum candidate probability below 0.95 yields `selected_candidate=null`. A 50/50 tie is not counted as successful identification. The out-of-library scenario makes both candidates wrong, separating high posterior confidence from correct mechanism recovery.

### GP and multiple fidelities

An exact Cholesky-based GP uses fixed RBF length 0.20 and amplitude 1. After six training records, the guarded policy also evaluates length 0.06 on reused diagnostics, selecting it when diagnostic RMSE is less than 0.85 of the default. Every fifth guarded GP query is random exploration. This is adaptive model selection, not guaranteed calibration.

The multifidelity model is a **joint GP** with \(f_H=f_L+\delta\) and covariance \(k_L+1_H1'_H k_\delta\). Low-fidelity values are not fixed pseudo-labels at high fidelity. Correlation scale \(\rho=1\), discrepancy length 0.12, and discrepancy amplitude 0.35 are fixed assumptions, not learned quantities. Acquisition scores expected reduction of HF posterior variance on a target grid per cost; every fourth query is an HF anchor.

HF-only performs no initial LF measurements and pays no LF cost. Naive pooling intentionally ignores fidelity. Once at least four HF records exist, guarded compares joint-GP diagnostic RMSE with `1.15 × HF-only RMSE + 0.01`, switching permanently to HF-only if worse. Missed harmful transfer and unnecessary switching remain possible.

## Diagnostic and stop rules

Diagnostics flag standardized squared residual above 4, observation-interval coverage below 0.75, or linear likelihood rank below two. Guarded linear/committee runs stop after at least eight training records when the residual threshold is exceeded; linear runs additionally require rank two. Not every diagnostic flag is an automatic stop.

The final predictive target requires latent RMSE ≤ 0.12, observation coverage ≥ 0.80, and mean observation interval width ≤ 0.80. It is a synthetic prediction criterion, neither a biological accuracy standard nor a mechanism-identification definition. Lower cost after an assumption stop is not successful sample efficiency.

## Modules and extension points

| Module | Responsibility |
|---|---|
| contracts / adapters | Immutable observations, provenance and partition guards, legacy schema bridge |
| design / simulator | Public experiment metadata versus evaluator-only synthetic truth |
| models / committee | Posterior inference, projected prediction, model cards |
| acquisition | Eligibility, cost, and projected query scoring |
| assumptions / evaluation | Revisable assumptions, reused diagnostics, single-use final evaluation |
| runner / suite | State transitions, budgets, audit events, execution matrix, summaries |
| server | Loopback-only synthetic API |
| lab | Dependency-free replay and execution frontend |

`Query.time` reserves an interface field but **rejects values other than 1.0**. There is no continuous-time dynamics model. Measurement noise is known from the oracle, not estimated, and no donor variation exists. Full biological uncertainty propagation and mechanistic discovery are not claimed.

## Provenance, security, and reproducibility

Only directly simulated training observations are eligible for fitting. Generated, imputed, and derived records can pass lineage checks but cannot be used as independent fitting evidence. Real biological input is rejected, and the biological-unit counter is always zero. This strict default prevents evidence laundering without asserting that augmentation can never help.

The server binds 127.0.0.1, checks Host/Origin and a per-server token, limits payload/configuration size, allows one computation at a time, and exposes neither arbitrary paths nor code execution. It lacks TLS, user accounts, execution isolation, an asynchronous queue, and privacy governance. Do not expose it publicly.

Hash-linked events detect inconsistent modification; a file author can recompute the entire chain, so it is not a digital signature or scientific proof. Audit exported files with Python.

Runs record settings, seeds, Python/NumPy/SciPy versions, and a source fingerprint. Execution timing is excluded from deterministic hashes. Determinism is checked within the tested environment, not guaranteed bit-for-bit across all BLAS, OS, or library versions. A CI workflow is provided but remote execution is not claimed. Read the [evaluation protocol](10_EVALUATION_PROTOCOL.md) and [pilot interpretation](11_PILOT_RESULTS.md).
