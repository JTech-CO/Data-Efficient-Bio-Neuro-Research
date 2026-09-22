"""Acquisition policies: fixed baselines and local Gaussian information surrogates.

No function in this module takes a World, scenario tag, final test or truth.
"""
from __future__ import annotations
import numpy as np
from .contracts import Action

POLICIES=("random", "reference_first", "joint_information", "block_targeted", "no_reference", "reference_first_no_audit")

def menu():
    return tuple([Action(k,x,2) for k in ("sample","intervention") for x in (-1.,-.5,0.,.5,1.)]+
                 [Action("reference",x,2) for x in (-1.,0.,1.)])

def ld(a):
    sign,val=np.linalg.slogdet(a+np.eye(a.shape[0])*1e-12)
    if sign<=0: raise ArithmeticError("nonpositive covariance determinant")
    return float(val)

def gains(fit,public,a):
    c=fit.covariance; h=public.row(a)
    ch=c@h; den=fit.noise_variance/a.n+h@ch
    new=c-np.outer(ch,ch)/den
    _,j,_=fit.theta()
    theta_gain=max(0.,0.5*(ld(j@c@j.T)-ld(j@new@j.T)))
    sensor_gain=max(0.,0.5*(ld(c[3:,3:])-ld(new[3:,3:])))
    joint_gain=max(0.,0.5*np.log1p(a.n*(h@c@h)/fit.noise_variance))
    return {"theta_local_information":theta_gain,"sensor_information":sensor_gain,
            "joint_information":joint_gain,"assumed_noise_variance":fit.noise_variance,
            "is_exact_mutual_information_for_theta":False}

def choose(policy,fit,public,records,remaining,rng,diagnosis=None):
    if policy not in POLICIES: raise ValueError("unknown policy")
    options=[a for a in menu() if a.cost<=remaining+1e-9]
    if policy=="no_reference": options=[a for a in options if a.kind!="reference"]
    if not options: return None
    if policy=="random":
        a=options[int(rng.integers(len(options)))]; reason="uniform-eligible-action-not-uniform-cost"
    elif policy in ("reference_first","reference_first_no_audit"):
        # Strong simple baseline: anchor both ends, then cycle measurement types
        # and conditions. No threshold tuning or posterior-based query selection.
        refs={r.action.x for r in records if r.action.kind=="reference"}
        need=[a for a in options if a.kind=="reference" and a.x in (-1.,1.) and a.x not in refs]
        if need: a=need[0]
        else:
            order=[Action(k,x,2) for x in (-1.,1.,0.,-.5,.5) for k in ("sample","intervention")]
            counts={q.key:sum(r.action.key==q.key for r in records) for q in order}
            pool=[q for q in order if q.cost<=remaining+1e-9]
            if not pool: return None
            a=min(pool,key=lambda q:counts[q.key])
        reason="two-point-calibration-then-balanced-regression"
    else:
        weights={"theta":1.,"sensor":0.15}
        if policy=="block_targeted" and diagnosis:
            flags=diagnosis["flags"]
            if flags["sensor_affine"] or flags["sensor_nonlinear"]: weights["sensor"]=1.0
            if flags["mechanism_lack_of_fit"]: weights["theta"]=2.0
        def utility(q):
            g=gains(fit,public,q)
            raw=g["joint_information"] if policy=="joint_information" else (
                weights["theta"]*g["theta_local_information"]+weights["sensor"]*g["sensor_information"])
            return raw/q.cost
        a=max(options,key=utility)
        reason="joint-parameter-information-per-cost" if policy=="joint_information" else "weighted-local-block-information-per-cost"
    meta={"reason":reason,"cost":a.cost,**gains(fit,public,a)}
    if policy=="block_targeted": meta["diagnostic_state_used"]=diagnosis["label"] if diagnosis else "not-yet-observed"
    return a,meta
