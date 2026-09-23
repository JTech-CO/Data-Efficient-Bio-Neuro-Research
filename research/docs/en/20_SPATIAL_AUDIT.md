# 20. E: Audit location and cost

## A different test target

Rather than repeatedly reusing the v1.2 fitted residual, this study uses a fresh **sample-minus-matched-control contrast** at each location. The two streams share a baseline mean; a local discrepancy is introduced only in the sample stream. The control is a separate synthetic measurement obeying the nominal law, not merely another sensor viewing the same system.

$$D_t=Y_{sample,t}(x_t)-Y_{control,t}(x_t),\qquad Z_t=D_t/\sqrt{\sigma_s^2+\sigma_c^2}.$$

Under the declared null, noises are fresh, independent Gaussian with known standard deviations 0.1. If $x_t$ is selected using past records only, $p_t=2\Phi(-|Z_t|)$ is conditionally super-uniform. **Arbitrary fitted GP/PINN residuals do not inherit this property.** Constructing such controls for real data requires separate measurement design.

## Location and resources

Five policies repeat -1/0/1, sample uniformly, use pre-randomized strata, fill the largest gap, or adapt coverage. Adaptive coverage retains a global step every third step and can repeat or sample a neighbour of a past |Z|>1.8 location. It chooses before observing the new contrast. This is an explicit simple heuristic, not a replication of the cited spatial/path algorithm. [T03](../../triad/references/REFERENCES.md#t03)

A sample costs 1 and its control costs 1 or 3. Settings (budget, control cost) are (24,1), (48,1), and (48,3), giving 12, 24 and 12 contrasts. Controls are not free. Travel and preparation time are not modeled.

Metrics include final-grid covering radius, visiting the actual one-width bump region, alarm rate, first-alarm cost, and restricted cost with non-detection censored at the budget. A detected-only mean is not a standalone ranking. Audit data do not enter training; this study makes no claim to repair prediction errors. Predictor comparisons are performed separately in F.

## A limited guarantee under adaptive location choice

For a fixed maximum N, allocating $\alpha/N$ to each fresh contrast gives $P(\exists t\le N:p_t\le\alpha/N)\le\alpha$ by a union bound under the assumptions above. Past-residual-driven selection does not itself invalidate this statement. The essential requirements are predictable selection and conditionally valid p-values.

The implementation also uses $\alpha_t=\alpha/[t(t+1)]$, whose infinite sum is $\alpha$, supporting optional stopping under the same assumptions. This is elementary alpha spending, not an e-process, a confidence sequence or an implementation of Howard et al.'s specific methods. [T08](../../triad/references/REFERENCES.md#t08)

Multiplicity correction cannot fix invalid conditional p-values. Equal conditional means, known Gaussian variances and fresh independent noise are explicitly flagged. `t3_null` and `hetero_null` stress these assumptions despite zero mean contrast. No formal error-rate guarantee is claimed there.

## Irreducible blind spots

Between a finite set S of locations lies an unmeasured interval. A smooth local bump can be supported there and equal zero on S. The measured distributions then match a normal world despite a different global function. Randomized coverage may reduce misses but cannot guarantee detection of arbitrarily narrow changes with finite cost.

If sample and control share the same fault, the contrast is zero. `common_mode` retains this failure and does not interpret no alarm as absence of a physical error. It connects conceptually to D's shared-anchor failure; the modules are not claimed to be fully integrated.

---
[한국어](../ko/20_SPATIAL_AUDIT.md) · [v1.3 entry](../../../TRIAD.en.md)
