# 09. An executable observation–assumption–intervention research slice

**Status: synthetic-only implementation 0.1.0, not a production biological model.**

[Entry point](../../RESEARCH_LAB.md) · [Results](10_PILOT_RESULTS.md) · [Next research](11_NEXT_RESEARCH.md)

## 1. Relationship to the original plan

This adds a small executable slice of [02_ARCHITECTURE](02_ARCHITECTURE.md) and [03_EVALUATION](03_EVALUATION.md). Chapters 01–08 remain byte-for-byte unchanged. Their statements about an unimplemented full system describe the original research stage; this addition does not implement the full proposal either.

The slice addresses H1, selecting experiments that separate candidate mechanisms, and a restricted H2, testing the effect of a wrong observation operator. It implements parts of P0 contracts, P2 synthetic stress tests, and P3 loop integration. P1 real-data regression and P4 prospective experiments were not performed.

This is not merely an interface scaffold: the code generates measurements, updates posteriors, chooses and charges queries, issues diagnostic alerts, changes prediction paths, and evaluates a completed acquisition history.

## 2. Deliberately small dynamics

The toy world has states A and B, coefficients a and b, input x, intervention u, and time t. These names and units do not represent a particular cell, neuron or drug.

$$A(t)=ax(1-u)e^{-t}$$
$$B_{parallel}(t)=bxe^{-0.45t}$$
$$B_{compensatory}(t)=bxe^{-0.45t}+0.8aux(1-e^{-0.45t})$$

These are analytic solutions of known ODEs: `A'=-A`, and either `B'=-0.45B` or `B'=-0.45B+0.45·0.8aux`, with `A(0)=ax(1-u)` and `B(0)=bx`. Rates and candidate structures are not learned. Only a,b are estimated, using prior `N([1,1],0.36 I)` and a Gaussian observation likelihood. The Gaussian prior has negative tails, so it does not enforce physiological positivity.

At u=0 the candidates induce exactly the same observations. The observation-only track is therefore deliberately unable to identify the candidate mechanism. This is an exact counterexample for this design, not a statement about all biological systems. Parameter estimation and candidate discrimination are separate questions, consistent with the motivation in [E03](../../research_lab/provenance/LITERATURE.md#e03).

## 3. Measurement is not state

The nominal observation is `y=w_A(t)A+w_B(t)B+offset(t)+epsilon`. The offset is `0.10+0.035t`, the gain includes `exp(-0.18t)`, and base weights are `(1,0.4)` for aggregate, `(1,0)` for A, and `(0,0.8)` for B. Nominal noise standard deviations are 0.12, 0.075 and 0.055 respectively.

These are supplied **nominal synthetic metadata**, not calibration estimates learned from real instruments. The identity-observer ablation ignores gain, mixing and offset. It tests the consequence of a wrong operator, not successful automatic sensor calibration.

## 4. Executable separation

| Layer | Modules | Implemented responsibility |
|---|---|---|
| Contracts | `contracts.py` | Query domain, cost, assumptions and configuration validation |
| Evidence | `ledger.py` | Original-schema-compatible observations, role boundaries and hash chain |
| Models | `models.py` | Conjugate Bayesian coefficients, candidate evidence and predictive intervals |
| Design | `policies.py`, `design.py` | Information, variance, diversity and cost-based query selection |
| Diagnostics | `diagnostics.py` | Prequential residual alerts on non-fitting audit observations |
| Environment | `simulator.py` | Synthetic oracle |
| Loop | `engine.py` | Proposal, simulator allowlist authorization, measurement and update |
| Evaluation | `evaluation.py` | Post-run held-out and extrapolation assessment |
| Delivery | `runner.py`, `server.py`, `web/` | CLI, local API and bilingual review interface |

Model and policy modules do not import the simulator or evaluator. The loop receives a measurement callable rather than an oracle object. This is an information-flow boundary during normal execution, not protection against malicious inspection of Python memory.

## 5. What the acquisition scores mean

`model_information` uses `I(M;Y|D,q)/cost(q)`, integrated over the scalar Gaussian predictive mixture with 20-point Gauss–Hermite quadrature. The normal guarded score is

$$S(q)=\frac{I(M;Y_q\mid D)+0.15\sum_Mp(M\mid D)I(\theta_M;Y_q\mid D,M)}{C(q)}.$$

Conditional parameter information is analytic: `0.5 log(1+latent_variance/noise_variance)`. Both information terms are logged separately. The coefficient 0.15 and every-fourth-query space-filling rule are fixed pilot settings, not proven optimum values. [E01](../../research_lab/provenance/LITERATURE.md#e01) motivates explicit interventions; this implementation does not reproduce its CIV acquisition.

The public pool contains 54 combinations of x=0.4/0.9/1.4, t=0.4/1.2/2.4, three readouts and u=0/1. The restricted track has nine combinations. Adaptive queries are unique. Repeated observations occur only as audits with separate replicate identifiers; active replicate-count and fidelity optimization remain unimplemented.

## 6. Diagnostics and abstention

All policies share four initial observations. A fixed independent audit query follows every three adaptive observations. Audit labels never fit either predictor. An alert becomes sticky when two of the last three standardized prequential residuals exceed 2.5 in absolute value.

This is a screening heuristic, not a calibrated sequential hypothesis test. It does not identify which assumption failed. With a 24-unit budget, most runs have only two audits. No alert is not evidence of validity. [E02](../../research_lab/provenance/LITERATURE.md#e02) motivates stress testing, but its algorithm and guarantees are not transferred to this heuristic.

When alerted, the guarded policy withholds a mechanism preference, uses a fixed RBF GP over public query coordinates for prediction, and acquires by GP variance per cost. This GP does not discover a biological equation or generate pseudo-labels. Its fixed kernel and nominal noise can themselves be wrong.

A `candidate_preference` is recorded only above posterior weight 0.95 with rank-two fitted linear design, and is suppressed when the guarded alert is active. No state is automatically promoted to `mechanism-supported`. Rank diagnostics are limited to the toy linear coefficient design, not general structural identifiability.

## 7. Provenance, splits and budgets

Each measured record satisfies the original observation schema with `kind=simulated` and `counts_as_new_biological_unit=false`. Query, role, nominal noise, cost and previous hash live in an external envelope. The runner rejects real, generated and imputed evidence; an undeveloped real-data adapter is not advertised as implemented.

Training labels fit the models; audit labels affect the gate; held-out and OOD targets are evaluated after acquisition is complete. Audits are not reused as final tests. Measurements within a synthetic world are not independent biological subjects. Acquisition cost includes initial, adaptive and audit measurements. Evaluation oracle calls are reported separately rather than hidden in the acquisition budget.

## 8. Execution

```bash
python -m pip install -r requirements-lab.txt
python -m research_lab serve
python -m research_lab run --scenario sensor_shift --seed 7 --out research_lab/results/sensor-seed7.json
python -m research_lab benchmark --out research_lab/results/new-pilot
```

Run from the repository root and open the printed loopback URL. No GPU, external API or pretrained weights are required. The interface supports JSON import/export. Direct-file or GitHub Pages mode reviews saved traces only and disables fresh execution. Playback is not simulated computation.

Windows and Unix launch scripts are included after dependency installation. Native Windows/macOS and remote GitHub Pages deployment were not verified in this environment.

## 9. Extension contracts

New candidate structures belong in a model adapter with simulator truth kept separate. Nonlinear parameters or latent observations invalidate the current conjugate inference, requiring a new inference and interval specification. A new noise model must propagate through fitting, acquisition, diagnostics and evaluation. Real-data access requires its own permissions, consent, group split and provenance review; weakening existing input validation is not a valid adapter.
