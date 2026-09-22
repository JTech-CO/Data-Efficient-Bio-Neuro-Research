"""Four finite-look diagnostic tests from FIXED audit panels, not adaptive fits.

Bonferroni controls the probability of any false warning across the declared
looks if each tested null yields a superuniform p value. This is not an
unbounded-time confidence sequence or a guarantee under arbitrary noise laws.
"""
from __future__ import annotations
import math
import numpy as np
from scipy.stats import f, chi2
from .contracts import Action, pure_error

CHANNELS=("sensor_affine", "sensor_nonlinear", "mechanism_lack_of_fit", "noise_overdispersion")

def audit_panel():
    return tuple([Action("reference",x,2) for x in (-1.,0.,1.)] +
                 [Action(k,x,2) for k in ("sample","intervention") for x in (-1.,0.,1.)])

PANEL_COST=sum(a.cost for a in audit_panel())

def _fit_sse(h,y):
    coef=np.linalg.lstsq(h,y,rcond=None)[0]
    return float(np.sum((y-h@coef)**2)),int(np.linalg.matrix_rank(h))

def _f_p(numerator, numerator_df, sse, denominator_df):
    if numerator_df<=0 or denominator_df<=0: return 1.
    stat=max(0.,numerator)/numerator_df / max(sse/denominator_df,1e-300)
    return float(f.sf(stat,numerator_df,denominator_df))

def diagnose(records,public):
    if not records or any(r.split!="audit" for r in records):
        raise ValueError("diagnosis requires fixed-panel audit records only")
    ref=[r for r in records if r.action.kind=="reference"]
    sam=[r for r in records if r.action.kind!="reference"]
    # Require a balanced predeclared panel; no data-dependent sensor locations.
    expected={a.key for a in audit_panel()}
    keys={r.action.key for r in records}
    counts=[sum(r.action.key==k for r in records) for k in expected]
    if keys!=expected or len(set(counts))!=1 or counts[0]%2:
        raise ValueError("audit design must be complete cumulative fixed panels")
    ry=np.array([r.value for r in ref]); rx=np.array([r.action.x for r in ref])
    hr=np.column_stack([rx,np.ones_like(rx)])
    sr,rankr=_fit_sse(hr,ry); pr,dfr,gr=pure_error(ref)
    s0=float(np.sum((ry-rx)**2))
    sy=np.array([r.value for r in sam]); sx=np.array([r.action.x for r in sam])
    hs=np.column_stack([np.ones_like(sx),public.phi(sx)])
    ss,ranks=_fit_sse(hs,sy); ps,dfs,gs=pure_error(sam)
    p={"sensor_affine":_f_p(s0-sr,2,sr,len(ref)-rankr),
       "sensor_nonlinear":_f_p(sr-pr,gr-rankr,pr,dfr),
       "mechanism_lack_of_fit":_f_p(ss-ps,gs-ranks,ps,dfs),
       "noise_overdispersion":float(chi2.sf((pr+ps)/public.nominal_sd**2,dfr+dfs))}
    return {"p_values":p,"n_audit":len(records),"pure_error_df":dfr+dfs,
            "pure_error_variance":(pr+ps)/(dfr+dfs),
            "roles":"audit-not-fit-not-final-test","no_assumption_certification":True}

def alarm_summary(history,threshold):
    first={k:None for k in CHANNELS}
    for i,h in enumerate(history,1):
        for k in CHANNELS:
            if first[k] is None and h["p_values"][k] < threshold: first[k]=i
    flags={k:v is not None for k,v in first.items()}
    if flags["sensor_nonlinear"]:
        label="sensor_nonlinearity_or_shared_model_mismatch"
    elif flags["sensor_affine"] and flags["mechanism_lack_of_fit"]:
        label="sensor_and_mechanism_like_signals"
    elif flags["sensor_affine"]: label="sensor_affine_signal"
    elif flags["mechanism_lack_of_fit"]: label="mechanism_like_signal"
    elif flags["noise_overdispersion"]: label="noise_signal"
    else: label="no_detected_violation_not_certified"
    return {"threshold":threshold,"flags":flags,"first_look":first,"label":label,
            "any_alarm":any(flags.values()),"causal_source_identified":False}

def trajectory_score(history):
    return -math.log(max(min(p for h in history for p in h["p_values"].values()),1e-300))

def empirical_threshold(scores,alpha=0.05):
    """Upper order-statistic threshold for a NEW exchangeable null trajectory.

Marginal over calibration and test scores, P(score_new > threshold) <= alpha.
This is not a conditional guarantee for the one realised calibration bank.
"""
    s=sorted(float(v) for v in scores)
    if not s or not 0<alpha<1: raise ValueError("invalid calibration")
    k=math.ceil((len(s)+1)*(1-alpha))
    if k>len(s): raise ValueError("calibration bank too small for finite threshold")
    score=s[k-1]
    return {"n":len(s),"order_statistic_index_1based":k,"alpha":alpha,
            "score_threshold":score,"p_threshold":float(math.exp(-score)),
            "guarantee_scope":"new-exchangeable-global-null-trajectory-marginal-only"}
