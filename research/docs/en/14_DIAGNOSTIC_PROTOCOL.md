# 14. Mathematical and execution protocol

[한국어](../ko/14_DIAGNOSTIC_PROTOCOL.md) · [Design](13_FOLLOWUP_DESIGN.md) · [Results](15_FOLLOWUP_RESULTS.md)

## Observation model and reparameterization

For dimensionless condition x and a declared synthetic intervention u,

$$z=\theta_0+\theta_1\phi(x)+\theta_2u\psi(x),\quad\psi(x)=1+0.5\phi(x)^2,$$
$$y_{sample}=gz+b+\epsilon,\qquad y_{reference}=gr+b+\epsilon.$$

The diagnostic baseline assumes theta2=0, g=1, b=0 and nominal Gaussian homoscedastic noise. Unknown theta0/theta1 vary across worlds. Reparameterize beta=(g*theta0+b,g*theta1,g*theta2,g,b). Sample rows are [1,phi,u*psi,0,0]; reference rows are [0,0,0,r,1]. Gaussian prior mean (0,1,0,1,0) and SD (1.5,1,.8,.4,.5) produce

$$C=(C_0^{-1}+H^TH/\widehat\sigma^2)^{-1},\qquad m=C(C_0^{-1}m_0+H^Ty/\widehat\sigma^2).$$

Independent beta priors are not independent theta priors. No references implies nonidentifiability despite finite posterior numbers. Full data rank 5 is conditional on the declared likelihood, not evidence that calibration transports. Separating identifiability from fitting follows the established calibration workflow. [D08](../../followup/references/REFERENCES.md#d08)

## Noise and intervals

Actions collect two technical repeats. Within-condition pure-error SSE and df give the shrinkage plug-in estimate

$$\widehat\sigma^2=(\sigma_0^2+SSE_{pure}/2)/(1+df/2).$$

This corresponds to an inverse-gamma a0=2,b0=sigma0² variance prior mean, but the implementation does not integrate variance uncertainty. Conditional posterior intervals after adaptive sampling are not advertised as frequentist coverage guarantees.

Transform theta=((A-b)/g,B/g,C/g) and propagate the full Jacobian covariance. The delta approximation rejects |g|<0.05. The calibration plug-in ablation keeps identical means but removes the Jacobian's g/b columns from variance propagation. Observed intervals add estimated measurement noise; latent and observed coverage are different targets and both are retained in raw results. Same-data estimators also include fixed nominal noise, an identity-sensor baseline and an evaluator-only affine-calibration oracle. The oracle is privileged and cannot be a deployable competitor.

## Fixed audit panel

At each of three looks, collect two repeats for each reference r=-1,0,1 and sample/intervention condition x=-1,0,1: 18 observations per panel. Cumulative audit records are used only for diagnostic statistics, never to update predictive or calibration posteriors.

Four channels are computed: identity-versus-affine reference F test; reference affine lack-of-fit versus saturated reference means; sample [1,phi] lack-of-fit versus six condition means; and an upper chi-square test of pure-error SSE/sigma0². Nuisance fits internal to a diagnostic statistic are distinct from fitting the predictor. Nonlinear sensor response can also trigger a mechanism-like residual. Multiple flags are retained; causal attribution is always false.

## Sequential scope

Naive checks p<.05 for four channels at three looks. Bonferroni checks .05/(4*3). Whenever the null p values are superuniform,

$$P(\text{any false warning})\le\sum_{j,t}P(p_{jt}<\alpha/(4L))\le\alpha.$$

Independence is not needed for the union bound, but fixed-panel Gaussian/homoscedastic assumptions are needed for the component tests. The normal-bank global-null case is the principal validation target. These guarantees are not transferred to arbitrary sensor nonlinearity, heavy tails or heteroscedasticity.

A separate 2,000-world normal calibration bank uses S=-log(min p) per complete trajectory. The k=ceil((n+1)*(1-alpha)) order statistic sets a strict upper-tail threshold for a new exchangeable normal trajectory. The order-statistic statement is marginal over calibration and test trajectories, not a guarantee conditional on this single realised bank or under new noise laws.

Finite-look correction is not an unbounded-time confidence sequence or e-process. Those require separate constructions and assumptions and are not implemented here. [D04](../../followup/references/REFERENCES.md#d04) [D05](../../followup/references/REFERENCES.md#d05)

## Acquisition

The menu has five x values for ordinary/intervention measurements and three reference values. All benchmark actions collect two technical repeats and may revisit a condition. Contracts allow one/four repeats, but adaptive batch-size selection is not evaluated.

For row h and batch size n,

$$C'=C-Chh^TC/(\widehat\sigma^2/n+h^TCh).$$

joint_information maximizes .5*log(1+n*h'C*h/sigma²)/cost. block_targeted combines theta Jacobian logdet reduction and sensor-block logdet reduction per cost. Default weights are theta=1,sensor=.15; a sensor warning changes sensor weight to 1, a mechanism-like warning changes theta weight to 2. This is a local Gaussian information surrogate for nonlinear theta, not exact full EIG. Estimated noise propagates to fitting, acquisition and intervals; it is not a learned general noise function.

Comparators are uniform eligible-action random, reference_first (two endpoint calibrations followed by balanced sampling), joint information, no_reference, and reference_first_no_audit. The last spends diagnostic savings on additional fit data under an equal total acquisition cap. Audit-only standards never repair no_reference's predictive data-rank deficiency.

## Costs and single final opening

Each observation costs sample=1, reference=1.5 or intervention=1.8 synthetic units. Fit cap=36; each audit panel costs25.8; three panels cost77.4; total acquisition cap=113.4. Looks occur near fit-cost12,24 and at completion. Atomic batches may leave a small unused remainder. The no-audit reference baseline can spend the entire113.4 on fitting.

The final test has41 x values for each of two intervention states:82 observations costing114.8. Costs are separated into fit, audit and final evaluation. Noise-free latent truth is privileged simulator output, not free real-world measurement.

Look-prefix and final snapshots are frozen before a single final-test opening. All prespecified estimators and prefixes are evaluated in that opening. This does not mean only one prediction vector is scored. No score affects subsequent fitting or thresholds. Stopping at the first warning is evaluated as an offline counterfactual using a frozen prefix, not mislabelled as a separately run online stopping policy.

## Protocol and statistics

Forty development executions and2,000 null-calibration trajectories precede a SHA-256 lock of config, simulator, estimators, policies and scoring code. Study A then evaluates1,900 trajectories (1,000 normal plus9*100 fault worlds). Study B evaluates1,920 executions (10*6*32); six policies share320 worlds, so1,920 are not independent worlds. A/B index namespaces are disjoint.

This is a local ordering/reproducibility record, not independent preregistration, externally blinded validation or a secret to the author of the generator. Platform timeout recovery recomputes an interrupted cell under unchanged code/worlds, reuses complete cells and records the interruption. No cell is removed for its outcome.

Report warning counts, Wilson intervals, first-detection look and restricted mean look with undetected coded L+1. Paired-policy differences use2,000 descriptive world bootstrap resamples, without multiplicity-adjusted superiority testing or biological-population inference. The balanced known-feature mixture and simulator-only target remain explicit.
