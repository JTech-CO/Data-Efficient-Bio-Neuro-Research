# 28. Separating noise and mean misspecification with technical repeats

[한국어](../ko/28_REPLICATE_DECOMPOSITION.md) · [Sources](../../bounded/references/REFERENCES.md) · [Research entry](../../../BOUNDED.md)


## Differences and means carry different information

At fixed $x_j$, observe $Y_{jk}=m(x_j)+\epsilon_{jk}$. Non-overlapping differences $D_{jl}=(Y_{j,2l-1}-Y_{j,2l})/\sqrt2$ remove the shared mean. With independent equal-variance errors, $E[D_{jl}^2]=\sigma_j^2$. This provides noise information without automatically absorbing omitted mean terms.

Replicate means expose structural residuals. For any fitted group mean,

$$\sum_{j,k}(Y_{jk}-\hat m_j)^2=\sum_{j,k}(Y_{jk}-\bar Y_j)^2+\sum_jr(\bar Y_j-\hat m_j)^2.$$

This algebraic identity separates total SSE, pure error and lack of fit. Its F reference law additionally requires independent homoscedastic Gaussian repeats, a correct mean null and fixed design. For the quadratic base, degrees of freedom are $N-J$ and $J-3$. [B05](../../bounded/references/REFERENCES.md#b05)

## Five analyses of identical data

| Method | Mean | Noise source | Further uncertainty |
|---|---|---|---|
| pooled_base | Quadratic | Single variance from all residuals | Plug-in |
| residual_logvar_base | Quadratic | Squared preliminary-model residuals | Plug-in |
| difference_logvar_base | Quadratic | Non-overlapping differences | Plug-in |
| difference_logvar_plus | Quadratic + sin(pi*x) | Same differences | Plug-in |
| plus_bootstrap | Expanded mean | Re-estimated differences | 64 conditional parametric fits |

The extra mean basis is fixed before evaluation, not discovered from truth. A separate narrow `local_missing` family is intentionally not represented well by it.

For $K=\lfloor r/2\rfloor$ difference pairs and $Q_j$ their mean square, independent Gaussian noise gives $KQ_j/\sigma_j^2\sim\chi_K^2$. Correct $\log Q_j$ by $\psi(K/2)+\log(2/K)$, then fit $\log\sigma^2(x)=\gamma_0+\gamma_1x$ with small fixed ridge stabilization. The residual-noise comparator uses the same two variance coefficients but learns from residuals that can include mean error. No GP or neural network is silently added.

## Fixed cost and bootstrap

Allocate 48 measurements as 24 locations × 2 repeats, 12 × 4, or 8 × 6. More replication reduces spatial coverage. Technical repeats do not create independent subjects or batches. Mean coefficients and noise scale vary across synthetic worlds.

After fitting the expanded mean and variance, simulate independent Gaussian repeats at the same fixed inputs and re-estimate both noise and mean 64 times. Latent intervals use bootstrap percentiles; observation intervals invert the Gaussian-mixture CDF. NLL is calculated under the same mixture. This is a conditional parametric bootstrap, not a Bayesian posterior or distribution-free 95% guarantee. Tail-quantile Monte Carlo resolution is limited.

Generate 81 fresh final labels only after all fits and bootstrap fits. Final outcomes never select the extra basis or variance law. Post-result selection would require a new study.

## Retained failures

A shared batch term $U_j$ cancels in differences, so difference-based noise estimation can omit $Var(U_j)$. A large lack-of-fit statistic need not identify a missing biological mean law. Merely recording batch IDs does not remove the uncertainty.

The ordered-drift stress case includes training phases from -0.14 to +0.14, whereas each final singleton is the first phase of a fresh batch (-0.14). It therefore includes a measurement-phase shift, not only a noise-estimation comparison. Its prediction-coverage loss is not attributed to variance fitting alone.

Logvariance stabilization clips to [-9,2], fixed before evaluation and counted. Failures, clipping and unfavorable scores remain in denominators. Better proper scores without lower latent mean error are not mechanistic recovery.
