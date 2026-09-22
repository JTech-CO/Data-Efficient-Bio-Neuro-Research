"""Stateful synthetic runner. Evaluation is accessible only after freeze.

Audit panels are fixed in advance and are NEVER fitted. Their results can
change query priorities for block_targeted, so they are not final test data.
"""
from __future__ import annotations
from dataclasses import asdict
import numpy as np
from .contracts import Ledger, Action, AuditTrail, digest
from .worlds import make_world, rng_for
from .inference import fit_model, identity_baseline
from .design import choose, POLICIES
from .diagnostics import audit_panel, diagnose, alarm_summary, PANEL_COST

DEFAULT_LOOKS=(12.,24.,36.)

class FinalEvaluator:
    def __init__(self): self._frozen=None; self._used=False

    def freeze(self,snapshots):
        if self._frozen is not None: raise RuntimeError("freeze is single use")
        self._frozen=digest(snapshots)
        return self._frozen

    def evaluate(self,world,records,ledger,snapshots):
        if self._frozen is None or self._used or self._frozen!=digest(snapshots):
            raise RuntimeError("final evaluator requires one unchanged frozen snapshot set")
        self._used=True
        x=np.tile(np.linspace(-1,1,41),2); u=np.repeat([0,1],41)
        test=[]
        for xx,uu in zip(x,u):
            a=Action("intervention" if uu else "sample",float(xx),1)
            test.extend(world.observe(a,"test",ledger))
        y=np.array([r.value for r in test]); z=world.latent(x,u)
        normal=fit_model(records,world.public)
        nominal=fit_model(records,world.public,estimate_noise=False)
        out={}
        def metrics(mu,var,target):
            sd=np.sqrt(np.maximum(var,1e-12)); err=target-mu
            return {"rmse":float(np.sqrt(np.mean(err**2))),
                    "coverage_95":float(np.mean(np.abs(err)<=1.96*sd)),
                    "width_95":float(np.mean(3.92*sd)),
                    "nll_gaussian":float(np.mean(.5*(np.log(2*np.pi*sd**2)+err**2/sd**2)))}
        for key,m,prop in (("propagated",normal,True),("plugin_calibration",normal,False),("nominal_noise",nominal,True)):
            mu,var=m.predict_latent(world.public,x,u,propagate_calibration=prop)
            ym,yv=m.predict_sensor(world.public,x,u)
            out[key]={"latent":metrics(mu,var,z),"observed":metrics(ym,yv+m.noise_variance,y),
                      "interval_type":"conditional-Gaussian-delta-not-formal-coverage"}
        # All estimators see the SAME acquired records. Privileged oracle is
        # labelled and is never used to choose queries or detect assumptions.
        h=np.column_stack([np.ones_like(x),world.public.phi(x),u*world.public.psi(x)])
        theta=identity_baseline(records,world.public)
        rr=[r for r in records if r.action.kind!="reference"]
        hr=np.array([world.public.row(r.action)[:3] for r in rr])
        cov=normal.noise_variance*np.linalg.pinv(hr.T@hr+1e-6*np.eye(3))
        var=np.maximum(np.einsum('ij,jk,ik->i',h,cov,h),1e-12)
        out["identity_baseline"]={"latent":metrics(h@theta,var,z),"known_wrong_units_possible":True}
        ot=np.array([(normal.mean[0]-world.offset)/world.gain,normal.mean[1]/world.gain,normal.mean[2]/world.gain])
        ov=normal.covariance[:3,:3]/world.gain**2
        out["oracle_affine_calibration"]={"latent":metrics(h@ot,np.einsum('ij,jk,ik->i',h,ov,h),z),
                                           "privileged_evaluator_only":True}
        # Counterfactual STOP: all already-frozen prefix models evaluated once
        # after collection. No later action uses any of these outcomes.
        prefix={}
        for key,s in snapshots.items():
            n=s["n_fit"]
            m=fit_model(records[:n],world.public)
            mu,var=m.predict_latent(world.public,x,u)
            prefix[key]={"latent":metrics(mu,var,z),"fit_cost":s["fit_cost"],"audit_cost":s["audit_cost"]}
        mu,var=normal.predict_latent(world.public,x,u)
        return {"estimators":out,"frozen_prefix_evaluations":prefix,
                "curves":{"x":x.tolist(),"u":u.tolist(),"truth_latent":z.tolist(),
                          "mean_latent":mu.tolist(),"sd_latent":np.sqrt(var).tolist()},
                "test_open_count":1,"freeze_digest":self._frozen}

def run_world(world,policy,threshold,*,fit_budget=36.,looks=DEFAULT_LOOKS,keep_raw=True):
    if policy not in POLICIES: raise ValueError("unknown policy")
    ledger=Ledger(); trail=AuditTrail(); evalr=FinalEvaluator()
    rng=rng_for(world.identity,"policy",policy)
    planned_total=fit_budget+PANEL_COST*len(looks)
    active_looks=() if policy=="reference_first_no_audit" else tuple(looks)
    budget=planned_total if not active_looks else fit_budget
    history=[]; steps=[]; snapshots={}; diagnosis=None; next_look=0
    trail.add("start",{"version":"1.2.0-research.1","synthetic_only":True,"policy":policy,
                       "public_design":asdict(world.public),"fit_budget":budget,
                       "planned_acquisition_cap":planned_total})
    for a in (Action("sample",-1.,2),Action("sample",1.,2)):
        world.observe(a,"fit",ledger)
        trail.add("initial_measurement",{"action":asdict(a),"cost":a.cost})
    while True:
        fit_records=ledger.view("fit"); fit=fit_model(fit_records,world.public)
        spent=ledger.counts()["fit_cost"]
        # An audit is a declared finite look, not a data-dependent stopping time.
        # Training may cross a cost checkpoint by one atomic batch; panel count,
        # panel inputs and number of looked-at p values are fixed in advance.
        while next_look<len(active_looks) and spent>=active_looks[next_look]-1e-9:
            for a in audit_panel(): world.observe(a,"audit",ledger)
            h=diagnose(ledger.view("audit"),world.public); h["fit_cost_at_look"]=spent
            history.append(h); diagnosis=alarm_summary(history,threshold)
            next_look+=1
            counts=ledger.counts()
            snapshots[f"look_{next_look}"]={"n_fit":len(fit_records),"fit_cost":spent,
                                              "audit_cost":counts["audit_cost"],"model":fit.summary()}
            trail.add("diagnostic_look",{"look":next_look,"diagnosis":diagnosis,"n_audit":h["n_audit"]})
        result=choose(policy,fit,world.public,fit_records,budget-spent,rng,diagnosis)
        if result is None: break
        a,meta=result
        trail.add("propose",{"action":asdict(a),"selection":meta})
        trail.add("approve",{"authority":"synthetic-action-allowlist","real_world_authorized":False})
        obs=world.observe(a,"fit",ledger)
        trail.add("measure",{"record_ids":[r.record_id for r in obs],"cost":a.cost})
        steps.append({"action":asdict(a),"selection":meta,"spent_after":ledger.counts()["fit_cost"],
                      "values":[r.value for r in obs],"pre_fit":fit.summary()})
    # Guarantee all planned audit looks exist even if small budget residue is
    # not enough for the next batch. No policy gets free/extra training budget.
    while next_look<len(active_looks):
        for a in audit_panel(): world.observe(a,"audit",ledger)
        h=diagnose(ledger.view("audit"),world.public); h["fit_cost_at_look"]=ledger.counts()["fit_cost"]
        history.append(h); next_look+=1; diagnosis=alarm_summary(history,threshold)
        counts=ledger.counts(); fit=fit_model(ledger.view("fit"),world.public)
        snapshots[f"look_{next_look}"]={"n_fit":len(ledger.view("fit")),"fit_cost":counts["fit_cost"],
                                          "audit_cost":counts["audit_cost"],"model":fit.summary()}
        trail.add("diagnostic_look",{"look":next_look,"diagnosis":diagnosis,"n_audit":h["n_audit"]})
    fit_records=ledger.view("fit"); fit=fit_model(fit_records,world.public)
    counts=ledger.counts()
    snapshots["final"]={"n_fit":len(fit_records),"fit_cost":counts["fit_cost"],"audit_cost":counts["audit_cost"],"model":fit.summary()}
    freeze=evalr.freeze(snapshots); trail.add("freeze",{"digest":freeze})
    results=evalr.evaluate(world,fit_records,ledger,snapshots)
    trail.add("final_test",{"open_count":1,"freeze_digest":freeze})
    diagnosis=alarm_summary(history,threshold) if history else {
        "label":"not_monitored","flags":None,"first_look":None,"any_alarm":None,"causal_source_identified":False}
    result={"version":"1.2.0-research.1","world":world.truth_record(),"policy":policy,
            "public_design":asdict(world.public),"threshold":threshold,"final_model":fit.summary(),
            "diagnosis":diagnosis,"audit_history":history,"steps":steps,"evaluation":results,
            "costs":ledger.counts(),"events":trail.events,"snapshots":snapshots,
            "n_biological_units":0,"result_status":"completed"}
    result["first_alarm_look"]=min((i for i in (diagnosis.get("first_look") or {}).values() if i is not None),default=None)
    result["observations"]=ledger.export() if keep_raw else []
    return result
