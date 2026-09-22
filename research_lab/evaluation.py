"""Offline evaluator: called only AFTER the acquisition history is finalized."""
from __future__ import annotations
import numpy as np
from scipy.special import logsumexp
from .contracts import Query, ObservationAssumptions
from .ledger import TrainingDatum
from .models import MechanisticEnsemble, PredictiveGP,MODELS
from .design import evaluation_queries

def reconstruct(run,through):
    obs={e['observation']['record_id']:e for e in run['evidence']}
    train=[]
    for step in run['history'][:through+1]:
        if step['phase']=='train':
            e=obs[step['observation_id']]
            train.append(TrainingDatum(Query(**e['query']),e['observation']['value'],e['nominal_sigma'],e['observation']['record_id']))
    o=ObservationAssumptions(run['config']['observer'])
    mechanistic=MechanisticEnsemble(o,train)
    selected=PredictiveGP(o,train) if run['history'][through]['fallback_active'] else mechanistic
    return selected,mechanistic,train

def score(predictor,queries,truth,noisy):
    mean,var=predictor.predict(queries,True)
    low,high=predictor.interval(queries,True)
    ll,lh=predictor.interval(queries,False)
    if isinstance(predictor,MechanisticEnsemble):
        m,v=predictor.components(queries,True)
        nll=-np.mean(logsumexp(np.log(np.maximum(predictor.weights,1e-300))[:,None]
                              -.5*(np.log(2*np.pi*v)+(noisy[None,:]-m)**2/v),axis=0))
    else: nll=np.mean(.5*(np.log(2*np.pi*var)+(noisy-mean)**2/var))
    return {'rmse':float(np.sqrt(np.mean((mean-truth)**2))),
            'observation_95_coverage':float(np.mean((noisy>=low)&(noisy<=high))),
            'observation_95_width':float(np.mean(high-low)),
            'latent_95_coverage':float(np.mean((truth>=ll)&(truth<=lh))),
            'latent_95_width':float(np.mean(lh-ll)), 'nll':float(nll)}

def evaluate(run,oracle,full_curves=True):
    observational=run['config']['scenario']=='observational_equivalence'
    qid=evaluation_queries(False,observational);qood=evaluation_queries(True,observational)
    tid=oracle.clean(qid);tood=oracle.clean(qood)
    yid=np.array([oracle.observed_value(q,'test') for q in qid]);yood=np.array([oracle.observed_value(q,'external_test') for q in qood])
    indices=range(len(run['history'])) if full_curves else [len(run['history'])-1]
    curves=[]
    for i in indices:
        predictor,mechanism,train=reconstruct(run,i)
        entry={'step':i,'cost':run['history'][i]['cumulative_cost'],
               'id':score(predictor,qid,tid,yid),'ood':score(predictor,qood,tood,yood),
               'predictor':'predictive_gp' if isinstance(predictor,PredictiveGP) else 'candidate_mixture',
               'candidate_preference':run['history'][i]['candidate_preference']}
        curves.append(entry)
    final=curves[-1];pref=final['candidate_preference']
    in_set=oracle.true_model in MODELS
    final['true_candidate_weight']=float(mechanism.weights[MODELS.index(oracle.true_model)]) if in_set else None
    final['candidate_correct']=bool(pref==oracle.true_model) if in_set else None
    final['false_candidate_assertion']=bool(pref is not None and pref!=oracle.true_model)
    final['abstained']=pref is None
    # Fixed target for reporting only. NEVER used as online stopping criteria.
    reached=[e['cost'] for e in curves if e['id']['rmse']<=.10 and e['id']['observation_95_coverage']>=.90
             and e['id']['observation_95_width']<=.60]
    final['first_observed_cost_to_target']=min(reached) if reached else None
    final['target_reached']=bool(reached)
    mean,var=predictor.predict(qid,True);lo,hi=predictor.interval(qid,True)
    return {'access':'post_run_only_not_visible_to_policy','truth':oracle.truth_card(),
            'target':{'rmse_max':.10,'observation_coverage_min':.90,'interval_width_max':.60,
                      'meaning':'arbitrary synthetic reporting target; not a clinical threshold'},
            'test_points':len(qid),'ood_test_points':len(qood),'simulator_test_calls':len(qid)+len(qood),
            'curves':curves,'final':final,
            'prediction_panel':{'queries':[q.to_dict() for q in qid],'truth':tid.tolist(),'noisy_test':yid.tolist(),
                                'mean':mean.tolist(),'lower':lo.tolist(),'upper':hi.tolist(),
                                'interval':'pointwise 95% predictive, not simultaneous'},
            'uncertainty_note':'Coverage across synthetic design points is descriptive, not donor-population inference.'}
