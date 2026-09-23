# 26. Partial identification allowing reference bias

[한국어](../ko/26_PARTIAL_IDENTIFICATION.md) · [Sources](../../bounded/references/REFERENCES.md) · [Research entry](../../../BOUNDED.md)


## Model and external bounds

The latent response is $z(x)=\theta_0+\theta_1x$. The primary sensor observes $y=g[z(x)+R\Delta]+b+\epsilon$. The reference observes $y_{ref}=z(x)+c_{ref}+\epsilon_{ref}$, and the blank observes $y_{blank}=g c_{blank}+b+\epsilon_{blank}$. Reference biases may differ across observations but satisfy $|c_{ref}|\le0.12$; the blank satisfies $|c_{blank}|\le0.08$. Main gain is restricted to $[0.6,1.5]$ and recovery to $[0.9,1.1]$.

These are externally declared sensitivity assumptions, not bounds learned or certified from the data. Reference gain remains one. The implementation does not solve arbitrary unknown gains and nonlinear laws for every reference. Partial-identification literature motivates assumption-indexed bounds; the discrete model in B01 is not directly reproduced. [B01](../../bounded/references/REFERENCES.md#b01)

## Linear inverse-calibration polytope

Set $u=1/g>0$, $v=-b/g$ and $q=(\theta_0,\theta_1,u,v,R)$. A primary mean $m$ satisfies

$$um+v=\theta_0+\theta_1x+R\Delta.$$

For a simultaneous mean interval $[L,U]$, impose

$$uL+v\le\theta_0+\theta_1x+R\Delta\le uU+v.$$

Reference constraints are $L_{ref}-B_{ref}\le z(x)\le U_{ref}+B_{ref}$. Blank constraints are $uL_{blank}+v\le B_{blank}$ and $uU_{blank}+v\ge-B_{blank}$. Together with gain/recovery ranges, these are linear inequalities in $q$. Linear programs compute coordinate extrema; empty, bounded, unbounded and numerical-failure states are distinct. Truth is never used to relax a failed problem. [B06](../../bounded/references/REFERENCES.md#b06)

These are exact projections of this specified polytope, not universal sharp biological bounds. Marginal endpoints need not be simultaneously attainable. The physical-offset ratio $b=-v/u$ is not separately optimized; inverse-calibration coordinate intervals must not be mislabelled as independent physical-parameter intervals.

## Sampling uncertainty versus identification uncertainty

Each of the fixed $K$ measurement groups contains fresh iid Gaussian technical repeats, with unknown variance. Construct

$$\bar y_j\pm t_{n_j-1,1-\alpha/(2K)}s_j/\sqrt{n_j}.$$

On the Bonferroni simultaneous-coverage event, every true mean lies in its interval. Under the declared physical bounds, true $q$ then satisfies every linear inequality. This establishes an outer confidence envelope for the true parameter. Cross-group independence is not needed for a union bound, but within-group iid Gaussian repeats and fixed sample counts are. The procedure is not automatically valid after adaptive stopping.

The evaluator separately substitutes noiseless true means. Its remaining width illustrates identification uncertainty that increasing technical replication cannot remove. This is a simulation-only reference, never extra fitting evidence or a confidence interval.

## Designs and same-data comparisons

`reference_only` measures primary and reference at two locations. `addition_blank` uses primary, additions at two locations, and a blank. `triangulated` combines them. A cap of 72 funds at least four repeats per group, then a fixed remainder allocation. Actual observation counts differ across designs.

For identical acquired data, bias profiles are zero, declared and doubled. The gain range is unchanged; recovery/reference/blank ranges change. All projected sets are checked for nesting. Midpoints are not presented as a preferred estimator.

## Counterexamples and metrics

Common bias can preserve the alternative explanation $\theta'_0=\theta_0+c$, $v'=v+c$. When true bias exceeds declared bounds, a nonempty set can exclude truth. Feasibility is therefore not a universal assumption test.

A shared group-level error also defeats within-group standard errors even if reference bias bounds hold. Increasing the bias bound alone cannot repair invalid sampling intervals. Report joint $q$ containment separately from $\theta_0$ projection containment. Empty sets remain failures in denominators; conditional width means disclose their available count.

## Additional boundary

Bias limits are applied to each measurement interval; no extra equality forces reference bias at different locations to equal one common nuisance value. This can be a conservative outer relaxation of a fixed-common-bias model. Exact LP projection of the declared polytope is not a claim of the sharpest set under every available biological assumption.
