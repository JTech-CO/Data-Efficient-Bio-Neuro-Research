# 27. Control diagnostics without known noise variance

[한국어](../ko/27_UNKNOWN_SCALE_AUDIT.md) · [Sources](../../bounded/references/REFERENCES.md) · [Research entry](../../../BOUNDED.md)


## Separate the tested claims

At location $x$, acquire fresh technical contrasts $D_i(x)=Y_{S,i}(x)-Y_{C,i}(x)$. Three monitors share observations for comparison, but their alarms are never OR-combined and labelled a single 5% procedure. Location policies see past audit records only, not final outcomes or truth.

`nominal_z` intentionally uses a fixed assumed scale. `local_t_bonferroni` estimates scale from six fresh contrasts per location: under iid Gaussian contrasts within that batch, its statistic has five degrees of freedom. A cap of $J$ looks gives threshold $0.05/J$. Variance may vary between locations under these batch conditions. `conditional_sign_e` uses signs without estimating variance, but does not follow from a mean-zero assumption alone.

More sophisticated anytime t procedures for unknown variance exist. Our local-t comparator is a finite-batch correction, not a reproduction of those procedures. [B02](../../bounded/references/REFERENCES.md#b02)

## Implemented sign capital

Let $S_t=\operatorname{sign}(D_t)$, with a zero sign giving multiplier one. For fixed $\lambda\in\{-0.75,-0.5,-0.25,0.25,0.5,0.75\}$, set

$$E_t^\lambda=\prod_{i=1}^t(1+\lambda S_i).$$

Under $\mathbb E[S_t\mid\mathcal F_{t-1},x_t]=0$, each multiplier has conditional mean one and the capital is a nonnegative martingale. Mix six stakes equally within each component; give weight one half to the global component and one eighth to each of four fixed spatial bins. Bin capital does not change outside its bin. This fixed mixture remains a nonnegative martingale, yielding $P_0(\sup_t E_t\ge1/\alpha)\le\alpha$. Unit tests check initialization, zero signs and the conditional averaging identity. [B03](../../bounded/references/REFERENCES.md#b03) [B04](../../bounded/references/REFERENCES.md#b04)

Conditional symmetry is sufficient for sign balance; mean-zero is not. A variable equal to 1 with probability .9 and -9 with probability .1 has mean zero but violates sign balance. Symmetric heavy tails require no known variance for this construction. A shared replicate-level error can invalidate the conditional premise. The code does not reproduce the specific e-processes in B02.

## Location and cost factors

Acquisition cap is 144, with audit fractions 0/25/50/75%. The zero-audit comparator is not monitored, not a zero-alarm success. `max_gap` fills the largest unsampled gap; `adaptive_cover` alternates coverage and revisiting regions suggested by previous contrasts.

A batch of six pairs costs 12 measurements. After the first location, setup costs one unit plus .5 times travel distance. When the next atomic batch is unaffordable, the leftover is not retrospectively reassigned to fitting. Both cap and actual spending are reported; these are synthetic costs, not measured laboratory prices.

The complementary training allocation fits a separate quadratic predictor. Audits do not refit or calibrate it. More audit spending can therefore yield more detections and worse predictions together. The 81 final measurements are separately charged. Undetected trajectories receive allocated audit budget in the restricted-cost metric; this is not an unbiased survival estimate of detection delay.

## Interpretation boundaries

A broad contrast shift can already be represented by the fitted predictor's intercept. An alarm is not automatically a defect in that predictor. A narrow local shift may not provide enough signs for the mixture to accumulate evidence. Low false-alarm frequency alone is not dominance.

Common-mode effects cancel from sample-minus-control measurements. Results under heteroscedasticity, symmetric heavy tails, skew mean-zero noise and correlated repeats are labelled by the actual validity conditions, rather than pooled as one valid-null false-positive rate.
