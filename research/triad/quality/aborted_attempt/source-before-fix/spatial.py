"""E: equal-cost spatial audits using fresh matched-control contrasts.

This is NOT a calibrated residual test for an arbitrary learned surrogate.
Under the stated null, the two streams have equal conditional means, fresh
independent Gaussian noise and known variances. Adaptive location selection is
predictable. Under those conditions conditional p-values are super-uniform.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from scipy.special import ndtr
from .common import Collector, rng_for

SCENARIOS=('normal','narrow','weak','broad','boundary','t3_null','hetero_null','common_mode')
POLICIES=('fixed_three','uniform','stratified','max_gap','adaptive_cover')
SETTINGS=((24,1),(48,1),(48,3)) # (diagnostic budget, cost per matched-control observation)
SD=.10

@dataclass(frozen=True)
class World:
    bank: str; scenario: str; seed: int; center: float; width: float; amplitude: float
    @property
    def identity(self): return f'E/{self.bank}/{self.scenario}/{self.seed}'
    def fault(self,x):
        x=np.asarray(x,float)
        if self.scenario in ('normal','t3_null','hetero_null'): return np.zeros_like(x)
        return self.amplitude*np.exp(-.5*((x-self.center)/self.width)**2)
    def contrast(self,x):
        return np.zeros_like(np.asarray(x,float)) if self.scenario=='common_mode' else self.fault(x)
    def observe(self,kind,x,delta,rep,split):
        r=rng_for(self.identity,split,kind,round(x,10),rep)
        baseline=.8+.45*x+.10*x*x
        mu=baseline+(float(self.fault(x)) if kind=='audit_sample' or self.scenario=='common_mode' else 0.)
        if self.scenario=='t3_null': noise=SD*r.standard_t(3)/np.sqrt(3)
        elif self.scenario=='hetero_null': noise=SD*(1+1.5*(x+1)/2)*r.normal()
        else: noise=SD*r.normal()
        return mu+noise


def make_world(bank,scenario,seed):
    if scenario not in SCENARIOS: raise ValueError('Unknown spatial scenario')
    r=rng_for('E/world',bank,seed)
    center=float(r.uniform(-.85,.85));width=float(r.uniform(.025,.06));amp=float(r.uniform(.48,.80))
    if scenario=='weak': amp=float(r.uniform(.18,.32));width=float(r.uniform(.04,.08))
    if scenario=='broad': width=float(r.uniform(.12,.22))
    if scenario=='boundary': center=float(r.choice([-1,1])*r.uniform(.88,.98));width=float(r.uniform(.025,.055))
    return World(bank,scenario,seed,center,width,amp)


def alpha_at(rule,t,max_looks,alpha=.05):
    if t<1 or max_looks<1 or t>max_looks: raise ValueError('Invalid look count')
    if rule=='bonferroni': return alpha/max_looks
    if rule=='spending': return alpha/(t*(t+1))
    if rule=='naive': return alpha
    raise ValueError('Unknown threshold rule')


def choose(policy, history, t, n, rng, stratified):
    """Only past contrasts and public domain/costs; no World or fault location."""
    if policy=='fixed_three': return [-1.,0.,1.][t%3]
    if policy=='uniform': return float(rng.uniform(-1,1))
    if policy=='stratified': return float(stratified[t])
    grid=np.linspace(-1,1,401)
    if not history: return 0.
    xs=np.array([h['x'] for h in history])
    distance=np.min(abs(grid[:,None]-xs[None,:]),axis=1)
    if policy=='adaptive_cover' and t%3!=0:
        winner=max(history,key=lambda h:abs(h['z']))
        if abs(winner['z'])>1.8:
            # A local repeat or neighbour is chosen before observing the next pair.
            step=[0.,-.045,.045][t%3]
            return float(np.clip(winner['x']+step,-1,1))
    elif policy not in ('max_gap','adaptive_cover'): raise ValueError('Unknown audit policy')
    choices=np.flatnonzero(np.isclose(distance,distance.max()))
    return float(grid[int(rng.choice(choices))])


def run(bank,scenario,seed,policy,budget=24,control_cost=1):
    if policy not in POLICIES or budget<=0 or control_cost<=0: raise ValueError('Invalid spatial experiment')
    n=int(budget//(1+control_cost))
    if not 1<=n<=200: raise ValueError('Audit supports 1..200 pairs')
    w=make_world(bank,scenario,seed);c=Collector(w.identity,w.observe)
    rng=rng_for('E/locations',bank,seed,policy,budget,control_cost)
    strat=-1+2*(np.arange(n)+rng.uniform(size=n))/n;rng.shuffle(strat)
    history=[]
    for t in range(n):
        x=choose(policy,history,t,n,rng,strat)
        o=c.take('audit_sample',x,cost=1,sd=SD,split='audit')
        ref=c.take('matched_control',x,cost=control_cost,sd=SD,split='audit')
        d=o.value-ref.value;z=d/(np.sqrt(2)*SD);p=float(2*ndtr(-abs(z)))
        history.append({'look':t+1,'x':x,'contrast':d,'z':z,'p':p,
                        'source_ids':[o.record_id,ref.record_id],
                        'spent':(t+1)*(1+control_cost),
                        'reject':{rule:bool(p<alpha_at(rule,t+1,n)) for rule in ('naive','bonferroni','spending')}})
    c.freeze({'null':'zero matched contrast','variance':2*SD*SD,'looks':n,'history':history})
    outcomes={}
    for rule in ('naive','bonferroni','spending'):
        alarms=[h for h in history if h['reject'][rule]]
        outcomes[rule]={'alarm':bool(alarms),'first_look':alarms[0]['look'] if alarms else None,
                        'first_alarm_cost':alarms[0]['spent'] if alarms else None,
                        'restricted_detection_cost':alarms[0]['spent'] if alarms else n*(1+control_cost)}
    xs=np.array([h['x'] for h in history]);grid=np.linspace(-1,1,201)
    hit=bool(np.any(abs(xs-w.center)<=w.width)) if scenario not in ('normal','t3_null','hetero_null','common_mode') else None
    maxdist=float(np.max(np.min(abs(grid[:,None]-xs[None,:]),axis=1)))
    c.finish()
    return {'version':'1.3.0-research.1','study':'E','bank':bank,'scenario':scenario,'seed':seed,'policy':policy,
            'budget':budget,'control_cost':control_cost,'n_pairs':n,'outcomes':outcomes,'history':history,
            'metrics':{'hit_one_width_region':hit,'domain_covering_radius':maxdist},
            'evaluator_truth':{'center':w.center,'width':w.width,'amplitude':w.amplitude,
                  'contrast_fault':scenario in ('narrow','weak','broad','boundary'),
                  'gaussian_null_assumptions_hold':scenario not in ('t3_null','hetero_null'),
                  'common_mode_unidentifiable':scenario=='common_mode','causal_source_identified':False},
            'curves':{'x':grid.tolist(),'contrast_truth':w.contrast(grid).tolist(),'physical_fault':w.fault(grid).tolist()},
            'costs':c.costs(),'observations':[o.export() for o in c.records],'events':c.trail.events}
