# 19. D: Transporting calibration to samples

## Existing equivalence and new information

Let the latent response be $z(x)=\theta_0+\theta_1x$, the sample sensor $y_s=g_sz+b_s+\epsilon$, and external standards $y_c=g_cq+b_c+\epsilon_c$. Assuming $g_s=g_c$ and $b_s=b_c$ is convenient but requires evidence. Metrological commutability is specific to measurement procedures and tolerances; this toy is not formal commutability validation. [T02](../../triad/references/REFERENCES.md#t02)

Samples identify only $a_0=g_s\theta_0+b_s$ and $a_1=g_s\theta_1$. A known within-sample increment gives $y_{s,\Delta}=a_0+a_1x+g_s\Delta+\epsilon$, separating gain. Yet $\theta_0\mapsto\theta_0+c$, $b_s\mapsto b_s-g_sc$ preserves every sample/addition observation. **Identifying gain does not identify offset.** This parallels the translational matrix-effect limitation of standard addition. [T01](../../triad/references/REFERENCES.md#t01)

| Protocol | Information | Generic rank of 6 expanded physical parameters |
|---|---|---:|
| external_only | Samples and external standards | 4 |
| addition_only | Plus known sample increments | 5 |
| addition_blank | Plus a matrix-matched latent-zero blank | 6 |
| orthogonal_only | Samples, standards, independently calibrated $r=z+\eta$ | 6 |
| triangulated | Additions, blank and orthogonal reference | 6 |

Parameters are $(\theta_0,\theta_1,g_s,b_s,g_c,b_c)$. The orthogonal route assumes a generic $\theta_1\ne0$. Local rank is not a global-identifiability proof for arbitrary nonlinear models. Making the second sensor's gain and offset fully unknown can leave the latent scale unidentified despite more columns of observations.

All protocols start with two replicates at each external level -1/+1 and two at each of five sample positions. Additions are 0.35/0.7 at three positions, blanks have two replicates, and orthogonal references have five positions. Sample/standard/addition costs are 1, blanks 2, references 3. Remaining cost up to 48 is spent on ordinary samples. These are dimensionless simulations, not wet-lab instructions.

## Inference and testing

First fit $(a_0,a_1,g_s,b_s,g_c,b_c)$ by known-variance WLS. Unidentified physical coordinates are not assigned unique estimates for external-only or addition-only designs. A separate assumption-dependent baseline reports the error from blindly transporting external calibration.

With blank and additions, recover $\hat\theta_0=(\hat a_0-\hat b_s)/\hat g_s$ and $\hat\theta_1=\hat a_1/\hat g_s$. The orthogonal route estimates $\theta$ from $r$ before combining it with sample coefficients. Ratio and calibration uncertainty are propagated by the delta method; small denominators trigger withholding. Known-noise assumptions, Gaussian approximations and nonlinear ratios preclude claiming an exact posterior or guaranteed 95% coverage.

Observation lack-of-fit and orthogonal contradiction are separately tested at p<0.025. A separate p<0.05 Wald comparison examines transport of gain/offset. Nonrejection is not proof of equivalence or acceptable bias. A clinically specified equivalence margin is not implemented.

States are `unresolved`, `identifiable-under-assumptions`, and `contradicted`. Full rank can coexist with contradiction, or with a wrong but apparently consistent result under shared failure. `causal_source_identified=false` remains explicit.

## Falsification worlds

Worlds include normal, gain shift, offset shift, both shifts, nonlinear sensor, mismatched blank, incorrect spike recovery, drifting orthogonal reference and common-anchor failure. A reference is a noisy, potentially biased measurement, not hidden-truth access.

In `common_anchor_failure`, define $z'=g_sz+b_s$, let actual latent additions be $\Delta/g_s$, let the blank read zero, and let the orthogonal reference report $z'$. All permitted observations then match a valid sensor measuring $z'$. **Multiple anchors corrupted in the same way add no independent absolute-scale evidence.** This is an observational-equivalence counterexample, not a prevalence estimate for laboratories.

Each protocol also records predictive NLL on 33 final sensor measurements: accurate sensor prediction can coexist with incorrect latent recovery. Latent error is computed only by the evaluator.

---
[한국어](../ko/19_CALIBRATION_TRANSPORT.md) · [v1.3 entry](../../../TRIAD.en.md)
