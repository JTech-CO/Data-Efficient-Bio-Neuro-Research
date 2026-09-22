"""Observe -> fit -> audit -> propose -> authorize -> measure -> append.
No evaluation query, true model id or true parameter is used by the selection loop.
"""
from __future__ import annotations
import copy, hashlib, json
import numpy as np
from .contracts import RunConfig, ObservationAssumptions
from .design import candidate_queries, initial_queries, audit_query
from .ledger import EvidenceLedger
from .models import MechanisticEnsemble
from .diagnostics import AuditGate
from .policies import choose


def execute(config: RunConfig, measure):
    """The measurement callable returns a provenance observation, not oracle internals."""
    observer=ObservationAssumptions(config.observer)
    ledger=EvidenceLedger();gate=AuditGate(config.audit_z,config.audit_hits,config.audit_window)
    observational=config.scenario=='observational_equivalence'
    candidates=candidate_queries(observational)
    used=set();history=[];rng=np.random.default_rng(config.seed+117)
    model=MechanisticEnsemble(observer)

    def acquire(q,role,reason):
        nonlocal model
        if ledger.cost+q.cost>config.budget+1e-8: raise ValueError('Budget exceeded')
        # Synthetic allowlist authorization, not human approval for real experiments.
        approval={'type':'synthetic_allowlist','approved':True,'real_world_authorized':False,
                  'query_key':q.key,'cost':q.cost}
        premean,prevar=model.predict([q],True)
        obs=measure(q,role,len(history))
        ledger.append(obs,q,role)
        audit=None
        if role=='train':
            used.add(q.key);model=MechanisticEnsemble(observer,ledger.training())
        else:
            audit=gate.observe(obs['value'],float(premean[0]),float(prevar[0]),obs['record_id'])
        gated=config.policy.startswith('guarded') and config.policy!='guarded_no_gate' and gate.suspect
        diagnostic=model.diagnostic(candidates)
        mkey=max(model.state()['weights'],key=model.state()['weights'].get)
        maximum=max(model.weights)
        # This is *candidate preference*, never automatically "mechanism-supported".
        claim=None if (gated or maximum<config.decision_threshold or diagnostic['parameter_design_rank'][mkey]<2) else mkey
        history.append({'step':len(history),'phase':role,'query':q.to_dict(),'observation_id':obs['record_id'],
                        'value':obs['value'],'cumulative_cost':ledger.cost,'selection':reason,'approval':approval,
                        'prequential_mean':float(premean[0]),'prequential_variance':float(prevar[0]),
                        'audit':audit,'gate_suspect':gate.suspect,'fallback_active':bool(gated),
                        'fit_n':len(ledger.training()),'posterior':model.state(),'diagnostic':diagnostic,
                        'candidate_preference':claim,'evidence_status':'synthetic_candidate_only'})

    for q in initial_queries(): acquire(q,'train',{'reason':'shared_initial_design'})
    adaptive=0;audit_index=0;stop_reason='budget_exhausted'
    while True:
        due=adaptive>0 and adaptive%config.audit_every==0
        if due:
            q=audit_query(audit_index,observational)
            if ledger.cost+q.cost>config.budget+1e-8:
                stop_reason='audit_budget_unavailable';break
            acquire(q,'audit',{'reason':'fixed_independent_audit'});audit_index+=1
        available=tuple(q for q in candidates if q.key not in used and ledger.cost+q.cost<=config.budget+1e-8)
        if not available:
            stop_reason='candidate_pool_exhausted' if len(used)>=len(candidates) else 'no_affordable_candidate';break
        q,why=choose(config,available,model,ledger.training(),rng,adaptive,gate.suspect)
        acquire(q,'train',why);adaptive+=1
    payload={'schema_version':'research-lab-run-1','research_only':True,'config':config.to_dict(),
             'assumptions':observer.register(),'history':history,'evidence':ledger.export(),
             'stop_reason':stop_reason,'total_cost':ledger.cost,
             'information_budget':{'real_measurements':0,'biological_units':0,'simulator_acquisition_calls':len(history),
                                   'training_measurements':len(ledger.training()),'audit_measurements':audit_index,
                                   'pretraining_examples':0,'synthetic_cost_units':ledger.cost},
             'gate':{'suspect':gate.suspect,'audit_count':len(gate.history),'scope':'heuristic; no type-I error control'},
             'limitations':['synthetic only','known toy rates and nominal sensor metadata','finite candidate set',
                            'no human-subject or wet-lab integration','not a reproduction of a cited algorithm']}
    body=json.dumps(payload,sort_keys=True,allow_nan=False,separators=(',',':'))
    payload['acquisition_sha256']=hashlib.sha256(body.encode()).hexdigest()
    return payload
