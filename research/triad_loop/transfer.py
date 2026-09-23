"""D: transporting calibration to samples, with deliberately fallible anchors.

Linear combinations are fitted without pretending unidentifiable physical
parameters have unique estimates. Orthogonal anchors are simulated measurements,
not access to the hidden truth. Delta-method intervals are approximations.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from .common import Collector, rng_for, require_fit, wls, propagated, jacobian, chi_p

SCENARIOS=('normal','gain_shift','offset_shift','both_shift','nonlinear_sensor',
           'blank_mismatch','spike_recovery','reference_drift','common_anchor_failure')
PROTOCOLS=('external_only','addition_only','addition_blank','orthogonal_only','triangulated')

@dataclass(frozen=True)
class World:
    bank: str
    scenario: str
    seed: int
    theta0: float
    theta1: float
    gain: float
    offset: float
    @property
    def identity(self): return f'D/{self.bank}/{self.scenario}/{self.seed}'
    def latent(self,x): return self.theta0+self.theta1*np.asarray(x)
    def main(self,z):
        return self.gain*z+self.offset+(.16*z*z if self.scenario=='nonlinear_sensor' else 0.)
    def observe(self,kind,x,delta,rep,split):
        r=rng_for(self.identity,split,kind,round(x,10),round(delta,10),rep)
        z=float(self.latent(x)); sd=.08
        if kind=='external': mu=x;sd=.06
        elif kind=='blank': mu=self.offset+(.30 if self.scenario=='blank_mismatch' else 0.)
        elif kind=='orthogonal':
            mu=z;sd=.06
            if self.scenario=='reference_drift': mu=1.2*z+.18
            if self.scenario=='common_anchor_failure': mu=float(self.main(z))
        elif kind in ('sample','spike'):
            recovery=.65 if self.scenario=='spike_recovery' else 1.
            if self.scenario=='common_anchor_failure': recovery=1/self.gain
            mu=float(self.main(z+delta*recovery))
        else: raise ValueError('Unknown transfer readout')
        if kind=='blank' and self.scenario=='common_anchor_failure': mu=0.
        return mu+sd*r.normal()


def make_world(bank,scenario,seed):
    if scenario not in SCENARIOS: raise ValueError('Unknown transfer scenario')
    r=rng_for('D/world',bank,seed) # matched latent values across fault families
    g=1.;b=0.
    if scenario in ('gain_shift','both_shift','blank_mismatch','spike_recovery','common_anchor_failure'):
        g=float(r.uniform(1.18,1.45))
    if scenario in ('offset_shift','both_shift','blank_mismatch','spike_recovery','common_anchor_failure'):
        b=float(r.uniform(.18,.38))
    return World(bank,scenario,int(seed),float(r.uniform(.65,1.15)),float(r.uniform(.6,1.15)),g,b)


def planned_actions(protocol,budget=48):
    if protocol not in PROTOCOLS or type(budget)!=int or budget<40 or budget>200: raise ValueError('Protocol or budget invalid')
    a=[]
    for q in (-1.,1.):
        for _ in range(2): a.append(('external',q,0.,1.,.06))
    for x in np.linspace(-1,1,5):
        for _ in range(2): a.append(('sample',float(x),0.,1.,.08))
    if protocol in ('addition_only','addition_blank','triangulated'):
        for x in (-.8,0.,.8):
            for d in (.35,.7): a.append(('spike',x,d,1.,.08))
    if protocol in ('addition_blank','triangulated'):
        for _ in range(2): a.append(('blank',0.,0.,2.,.08))
    if protocol in ('orthogonal_only','triangulated'):
        for x in np.linspace(-1,1,5): a.append(('orthogonal',float(x),0.,3.,.06))
    spent=sum(q[3] for q in a)
    for i in range(budget-int(spent)): a.append(('sample',float(np.linspace(-1,1,9)[i%9]),0.,1.,.08))
    return a


def row(o):
    if o.kind=='external': return [0,0,0,0,o.x,1]
    if o.kind=='blank': return [0,0,0,1,0,0]
    return [1,o.x,o.delta,0,0,0]


def physical_map(p, obs):
    t0,t1,g,b,gc,bc=p
    vals=[]
    for o in obs:
        if o.kind=='external': v=gc*o.x+bc
        elif o.kind=='blank': v=b
        elif o.kind=='orthogonal': v=t0+t1*o.x
        else: v=g*(t0+t1*o.x+o.delta)+b
        vals.append(v)
    return np.asarray(vals)


def physical_rank(records):
    # Analytic Jacobian at a generic theta1 != 0 point. Finite differences can
    # falsely raise rank through roundoff along exact null directions.
    rows=[]
    for o in records:
        if o.kind=='external': r=[0,0,0,0,o.x,1]
        elif o.kind=='blank': r=[0,0,0,1,0,0]
        elif o.kind=='orthogonal': r=[1,o.x,0,0,0,0]
        else: r=[1,o.x,1+.8*o.x+o.delta,1,0,0]
        rows.append(r)
    return int(np.linalg.matrix_rank(np.asarray(rows,float),tol=1e-8))


def fit_transfer(records):
    require_fit(records)
    base=[o for o in records if o.kind!='orthogonal']; refs=[o for o in records if o.kind=='orthogonal']
    X=np.asarray([row(o) for o in base],float)
    a,C,lr,Q,df=wls(X,[o.value for o in base],[o.nominal_sd**2 for o in base])
    rank=physical_rank(records)
    has_blank=any(o.kind=='blank' for o in records)
    has_add=any(o.kind=='spike' for o in records)
    physical=None; PC=None; ref_p=None
    if has_add and has_blank:
        if abs(a[2])>.15:
            physical,PC=propagated(lambda v:np.array([(v[0]-v[3])/v[2],v[1]/v[2],v[2],v[3],v[4],v[5]]),a,C)
    elif refs:
        R=np.array([[1,o.x] for o in refs]); ry=np.array([o.value for o in refs]); rv=np.array([o.nominal_sd**2 for o in refs])
        t,TC,rr,rQ,rdf=wls(R,ry,rv)
        h=np.array([a[0],a[1],t[0],t[1],a[4],a[5]])
        HC=np.zeros((6,6));ii=[0,1,4,5];HC[np.ix_(ii,ii)]=C[np.ix_(ii,ii)];HC[2:4,2:4]=TC
        if abs(t[1])>.15:
            physical,PC=propagated(lambda v:np.array([v[2],v[3],v[1]/v[3],v[0]-v[1]*v[2]/v[3],v[4],v[5]]),h,HC)
        Q+=rQ;df+=rdf
    if has_add and has_blank and refs and physical is not None:
        R=np.array([[1,o.x] for o in refs]); residual=np.array([o.value for o in refs])-R@physical[:2]
        V=np.diag([o.nominal_sd**2 for o in refs])+R@PC[:2,:2]@R.T
        ref_p=chi_p(residual@np.linalg.solve(V,residual),len(refs))
    fit_p=chi_p(Q,df)
    contradicted=(fit_p is not None and fit_p<.025) or (ref_p is not None and ref_p<.025)
    status='unresolved' if rank<6 or physical is None else ('contradicted' if contradicted else 'identifiable-under-assumptions')
    transfer_p=None;transfer_scope='not_testable'
    if physical is not None:
        L=np.zeros((2,6));L[0,2]=1;L[0,4]=-1;L[1,3]=1;L[1,5]=-1
        diff=L@physical;V=L@PC@L.T
        transfer_p=chi_p(diff@np.linalg.pinv(V)@diff,2);transfer_scope='gain_and_offset'
    elif has_add:
        d=a[2]-a[4];v=C[2,2]+C[4,4]-2*C[2,4]
        transfer_p=chi_p(d*d/v,1);transfer_scope='gain_only_offset_unresolved'
    naive=None
    if abs(a[4])>.15: naive=[float((a[0]-a[5])/a[4]),float(a[1]/a[4])]
    return {'coefficients':a.tolist(),'coefficient_covariance':C.tolist(),'linear_rank':lr,'expanded_physical_rank':rank,
            'physical':None if physical is None else physical.tolist(),'physical_covariance':None if PC is None else PC.tolist(),
            'status':status,'fit_p':fit_p,'orthogonal_contradiction_p':ref_p,'transfer_p':transfer_p,
            'transfer_scope':transfer_scope,'transfer_rejected':None if transfer_p is None else bool(transfer_p<.05),
            'naive_transfer_theta':naive,'approximation':'known-noise WLS; delta method for ratios; no exact coverage claim',
            'causal_source_identified':False}


def run(bank,scenario,seed,protocol,budget=48):
    w=make_world(bank,scenario,seed); c=Collector(w.identity,w.observe)
    for k,x,d,cost,sd in planned_actions(protocol,budget): c.take(k,x,delta=d,cost=cost,sd=sd)
    model=fit_transfer(tuple(c.records));c.freeze(model)
    grid=np.linspace(-1,1,33);truth=w.latent(grid)
    test=[c.take('sample',x,split='test',sd=.08) for x in grid]
    a=np.array(model['coefficients']);C=np.array(model['coefficient_covariance'])
    P=np.array([[1,x,0,0,0,0] for x in grid]);mean=P@a;var=np.einsum('ij,jk,ik->i',P,C,P)+.08**2
    yy=np.array([o.value for o in test]);metrics={
        'sensor_predictive_nll':float(np.mean(.5*(np.log(2*np.pi*var)+(yy-mean)**2/var))),
        'latent_rmse':None,'latent_inclusion':None,'latent_width':None,'gain_abs_error':None,'offset_abs_error':None,
        'naive_transfer_rmse':float(np.sqrt(np.mean((model['naive_transfer_theta'][0]+model['naive_transfer_theta'][1]*grid-truth)**2))) if model['naive_transfer_theta'] else None}
    curve={'x':grid.tolist(),'latent_truth':truth.tolist(),'sensor_test':yy.tolist(),'latent_mean':None,'latent_sd':None}
    if model['physical'] is not None:
        ph=np.array(model['physical']);V=np.array(model['physical_covariance']);B=np.c_[np.ones(len(grid)),grid]
        m=B@ph[:2];s=np.sqrt(np.maximum(0,np.einsum('ij,jk,ik->i',B,V[:2,:2],B)))
        metrics.update(latent_rmse=float(np.sqrt(np.mean((m-truth)**2))),latent_inclusion=float(np.mean(abs(m-truth)<=1.96*s)),
                       latent_width=float(np.mean(3.92*s)),gain_abs_error=abs(float(ph[2])-w.gain),offset_abs_error=abs(float(ph[3])-w.offset))
        curve.update(latent_mean=m.tolist(),latent_sd=s.tolist())
    c.finish()
    return {'version':'1.3.0-research.1','study':'D','bank':bank,'scenario':scenario,'seed':seed,'protocol':protocol,
            'model':model,'metrics':metrics,'curves':curve,'costs':c.costs(),'observations':[o.export() for o in c.records],
            'events':c.trail.events,'evaluator_truth':{'theta':[w.theta0,w.theta1],'gain':w.gain,'offset':w.offset,'scope':'evaluator-only after freeze'}}
