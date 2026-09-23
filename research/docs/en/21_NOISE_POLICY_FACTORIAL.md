# 21. F: Separating noise models from acquisition policies

## Crossed design

Every estimator shares the same three-dimensional mean basis $\phi(x)=(1,x,(3x^2-1)/2)$. This prevents attributing extra mean-model capacity to a noise-model improvement.

For each world, cross three acquisition controllers (homoscedastic Gaussian, log-variance Gaussian, Student-t) with random, spacefill and IVR. Refit **every acquired dataset with all three final estimators**. Thus each world has 9 collection runs and 27 final-fit cells. Random and spacefill ignore the controller and produce duplicate datasets across its three settings; duplicates are not independent evidence.

Save estimator-only changes on the same data, and policy-only changes at fixed controller/final estimator. Noise is keyed by world, location, replicate and split: matching queries share an observation, but different queries are not forced to share artificial common noise.

## Estimators

Measurements are technical pairs at identical locations. $d_i=(y_{i1}-y_{i2})/\sqrt2$ removes their shared mean and provides noise information. This connects to replication/exploration research but is not hetGP. [T04](../../triad/references/REFERENCES.md#t04) [T05](../../triad/references/REFERENCES.md#t05)

1. **Homoscedastic Gaussian:** $\hat\sigma^2=\mathrm{mean}(d_i^2)$ and common-basis OLS/WLS with plug-in covariance.
2. **Log-variance Gaussian:** $\log\sigma^2(x)=a+bx$, using Gaussian $E[\log(d_i^2)]=\log\sigma_i^2+\psi(1/2)+\log2$ and a fixed weak ridge on slope. It can be misspecified under nonmonotone noise or heavy tails.
3. **Student-t:** predeclared df=4, IRLS updates of mean coefficients and scale, stored iteration cap and convergence flag. Robust likelihoods do not eliminate inference or convergence issues. [T06](../../triad/references/REFERENCES.md#t06)

No full Bayesian posterior integrating noise-function uncertainty is implemented. Noise parameters are plug-in; Student-t coefficient covariance is an expected-information/IRLS approximation. Combining t observation noise with mean uncertainty uses a variance-matched t approximation. The forecast distribution is explicitly defined for scoring, not claimed to be an exact generative posterior.

## Policies and budget

Start with pairs at -1,-0.5,0,0.5,1. Acquisition cost is 48, and the candidate grid has 41 locations in [-1,1]. Replicates remain eligible. Spacefill maximizes distance to observed locations.

IVR is a one-step approximation to integrated mean-variance reduction over a public uniform target grid. With coefficient covariance C and $M=E[\phi\phi^T]$,

$$U(x)=\frac{\phi(x)^T C M C\phi(x)}{\hat\sigma^2(x)/2+\phi(x)^T C\phi(x)}.$$

Pairs have equal cost. For Student-t this is a moment-based IVR proxy, not exact likelihood information gain. Noise estimation can change acquisition, which is why its effect is separated from final refitting.

## Evaluation

Worlds include Gaussian, loglinear heteroscedastic, nonmonotone heteroscedastic, variance-matched t3, rare large-noise contamination, and a missing mean term. A robust likelihood under the latter is not discovery of the missing mechanism.

Freeze all fits before opening 81 new test observations once. Report latent RMSE, observed NLL, CRPS, observed/latent coverage, interval width and convergence. NLL is a density score and may be negative; lower is better. Explicit Gaussian and Student-t CRPS formulas are checked against numerical quadrature. Proper scores complement rather than replace coverage and width. [T07](../../triad/references/REFERENCES.md#t07)

Paired bootstrap resamples synthetic-world IDs. Conclusions depend on the small model, fixed df, costs and chosen variance functions; they do not establish universal superiority. Mean-capacity selection, calibration transport and donor variability are not jointly inferred here.

---
[한국어](../ko/21_NOISE_POLICY_FACTORIAL.md) · [v1.3 entry](../../../TRIAD.en.md)
