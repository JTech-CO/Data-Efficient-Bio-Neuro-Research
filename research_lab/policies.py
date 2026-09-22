"""Acquisition policies can see only public queries, models and diagnostics."""
from __future__ import annotations
import numpy as np
from .models import embedding, PredictiveGP


def choose(config, candidates, model, training, rng, step, suspect):
    if not candidates: raise ValueError('No affordable candidate')
    costs=np.array([q.cost for q in candidates])
    mi,pi=model.information(candidates,config.quadrature_nodes)
    _,variance=model.predict(candidates,False)
    reason=config.policy
    active=embedding([d.query for d in training]); proposed=embedding(candidates)
    diversity=np.min(((proposed[:,None,:]-active[None,:,:])**2).sum(-1),axis=1) if len(active) else np.ones(len(candidates))
    guard=config.policy.startswith('guarded')
    gate_on=guard and config.policy!='guarded_no_gate'
    exploration_on=guard and config.policy!='guarded_no_exploration'
    if config.policy=='random':
        scores=rng.random(len(candidates))
    elif config.policy=='space_filling': scores=diversity
    elif config.policy=='max_variance': scores=variance
    elif config.policy=='model_information': scores=mi/costs
    elif gate_on and suspect:
        gp=PredictiveGP(model.observer,training)
        _,gv=gp.predict(candidates,False)
        scores=gv/costs;reason='audit_alert_gp_exploration'
    elif exploration_on and (step+1)%config.exploration_every==0:
        scores=diversity;reason='scheduled_space_filling'
    else:
        scores=(mi+config.parameter_weight*pi)/costs;reason='model_plus_parameter_information_per_cost'
    i=int(np.argmax(scores))
    # Include the top alternatives to make decisions auditable, not just the winning score.
    ranked=np.argsort(-scores,kind='stable')[:5]
    details={'reason':reason,'score':float(scores[i]),'model_information_nats':float(mi[i]),
             'conditional_parameter_information_nats':float(pi[i]),'latent_variance':float(variance[i]),
             'cost':float(costs[i]),'candidate_count':len(candidates),
             'alternatives':[{'query_key':candidates[j].key,'score':float(scores[j]),'cost':float(costs[j]),
                               'model_information_nats':float(mi[j])} for j in ranked]}
    return candidates[i],details
