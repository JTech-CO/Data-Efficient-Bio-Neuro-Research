"""Synthetic oracle. Imported by runner/evaluator, NEVER by model or policy modules.
This separation is a software access boundary, not a cryptographic secret.
"""
from __future__ import annotations
import hashlib
import numpy as np
from .contracts import Query,ObservationAssumptions

class SyntheticOracle:
    version='two-pathway-analytic-v1'
    def __init__(self,scenario,seed):
        self.scenario=scenario;self.seed=seed
        rng=np.random.default_rng(seed+9127)
        self.theta=np.maximum([1.2,.85]+rng.normal(0,.12,2),.2)
        self.true_model='none_of_candidates' if scenario=='hidden_mechanism' else ('parallel' if seed%2 else 'compensatory')

    def latent(self,queries):
        values=[]
        for q in queries:
            a,b=self.theta
            A=a*q.condition*(1-q.intervention)*np.exp(-q.time)
            B=b*q.condition*np.exp(-.45*q.time)
            if self.true_model in ('compensatory','none_of_candidates'):
                B+=.8*a*q.intervention*q.condition*(1-np.exp(-.45*q.time))
            if self.scenario=='hidden_mechanism':
                # Deliberately outside both candidate laws. No learner sees this term.
                B+=1.2*(q.intervention*q.condition)**2*(1-np.exp(-1.4*q.time))
            values.append((A,B))
        return np.asarray(values)

    def clean(self,queries):
        states=self.latent(queries);out=[]
        for q,(A,B) in zip(queries,states):
            wa,wb,bias=ObservationAssumptions().weights_offset(q)
            val=wa*A+wb*B+bias
            if self.scenario=='sensor_shift':
                # Misspecified input/time-dependent gain; not disclosed to the learner.
                val=bias+(val-bias)*(1+.75*q.condition*q.time)
            out.append(val)
        return np.asarray(out)

    def observed_value(self,q,role):
        # Deterministic independent channels. Identical query/role across policies has identical noise.
        key=f'{self.version}:{self.scenario}:{self.seed}:{role}:{q.key}'
        seed=int.from_bytes(hashlib.sha256(key.encode()).digest()[:8],'little')
        factor=3. if self.scenario=='noise_shift' else 1.
        return float(self.clean([q])[0]+np.random.default_rng(seed).normal(0,q.nominal_sigma*factor))

    def measure(self,q,role,index):
        return {'record_id':f'{role}-{index:04d}-{q.key}','kind':'simulated',
                'independent_group_id':f'synthetic-world-{self.seed}',
                'counts_as_new_biological_unit':False,
                'split':{'train':'train','audit':'validation','test':'test'}[role],
                'unit':'arbitrary_signal','value':self.observed_value(q,role),
                'source_uri':f'urn:research-lab:{self.version}:{self.scenario}:{self.seed}',
                'license_status':'original_synthetic_output; see repository LICENSE.md','parent_ids':[],
                'producer':{'artifact_id':self.version,'version':'1','fit_split':'not_fitted','seed':self.seed}}

    def truth_card(self):
        return {'scenario':self.scenario,'candidate_truth':self.true_model,'theta':self.theta.tolist(),
                'access':'evaluation_only_after_run','biological_units':0,'simulator_version':self.version}
