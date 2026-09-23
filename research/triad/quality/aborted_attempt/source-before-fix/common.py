"""Shared evidence contracts, deterministic streams and numerical utilities."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from collections import Counter
from pathlib import Path
import json, math, hashlib
import numpy as np
from scipy.stats import chi2, norm
from research.closed_loop.contracts import digest, AuditTrail


def rng_for(*keys):
    return np.random.default_rng(int(digest(list(keys))[:16],16))


def write_json(path, obj):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,allow_nan=False,indent=2)+'\n',encoding='utf-8')


@dataclass(frozen=True)
class Observation:
    record_id: str
    kind: str
    x: float
    value: float
    cost: float
    replicate: int
    split: str='fit'
    delta: float=0.0
    nominal_sd: float=0.10
    origin: str='simulated'
    parent_id: str | None=None
    counts_as_biological_unit: bool=False
    real_world_authorized: bool=False

    def __post_init__(self):
        if self.split not in ('fit','audit','test') or self.origin!='simulated':
            raise ValueError('Only split-tagged simulated measurements are accepted')
        if self.counts_as_biological_unit or self.real_world_authorized:
            raise ValueError('No biological observations or authorized physical experiments')
        if not self.record_id or self.replicate<0 or type(self.replicate)!=int:
            raise ValueError('Invalid record identity or replicate')
        if not all(math.isfinite(v) for v in (self.x,self.value,self.cost,self.delta,self.nominal_sd)):
            raise ValueError('Non-finite measurement')
        if self.cost<=0 or self.nominal_sd<=0 or not -1<=self.x<=1:
            raise ValueError('Invalid measurement cost, domain or noise metadata')

    def export(self): return asdict(self)


class Collector:
    """Runner-owned measurement construction. Policies only receive its record view."""
    def __init__(self, identity, observe):
        self.identity=identity; self.observe_fn=observe
        self.records=[]; self.counts=Counter(); self.last={}; self.frozen=False
        self.trail=AuditTrail()
        self.trail.add('start',{'world_id':identity,'data_kind':'simulated','biological_units':0})

    def take(self, kind, x, *, delta=0.,cost=1.,sd=.1,split='fit'):
        if self.frozen and split!='test': raise RuntimeError('Acquisition after freeze is forbidden')
        if not self.frozen and split=='test': raise RuntimeError('Freeze before opening test')
        x=float(x); key=(split,kind,round(x,10),round(delta,10)); rep=self.counts[key]
        self.trail.add('proposal',{'kind':kind,'x':x,'delta':delta,'cost':cost,'split':split})
        value=float(self.observe_fn(kind,x,delta,rep,split))
        rid=digest([self.identity,*key,rep])[:24]
        o=Observation(rid,kind,x,value,float(cost),rep,split,float(delta),float(sd),parent_id=self.last.get(key))
        self.records.append(o); self.counts[key]+=1; self.last[key]=rid
        self.trail.add('measured',{'record':rid,'record_digest':digest(o.export())})
        return o

    def freeze(self, fitted_payload):
        if self.frozen: raise RuntimeError('Already frozen')
        self.frozen=True
        self.trail.add('freeze',{'model_digest':digest(fitted_payload),'acquisition_digest':digest([r.export() for r in self.records])})

    def finish(self):
        if not self.frozen: raise RuntimeError('Cannot evaluate an unfrozen run')
        if any(e['type']=='evaluation_complete' for e in self.trail.events): raise RuntimeError('Test reused')
        self.trail.add('evaluation_complete',{'n_test':sum(o.split=='test' for o in self.records)})

    def costs(self):
        d={s:float(sum(o.cost for o in self.records if o.split==s)) for s in ('fit','audit','test')}
        return {**d,'total':sum(d.values()),'unit':'synthetic_measurement_unit','n_real':0}


def require_fit(records):
    if not records or any(r.split!='fit' or r.origin!='simulated' for r in records):
        raise ValueError('Only nonempty original simulated fit records may be fitted')


def wls(X, y, variance):
    X=np.asarray(X,float); y=np.asarray(y,float); v=np.broadcast_to(np.asarray(variance,float),len(y))
    if not np.all(np.isfinite(X)) or np.any(v<=0): raise ValueError('Invalid linear likelihood')
    A=X/np.sqrt(v[:,None]); b=y/np.sqrt(v)
    coef=np.linalg.lstsq(A,b,rcond=None)[0]; rank=int(np.linalg.matrix_rank(A))
    cov=np.linalg.pinv(A.T@A, rcond=1e-12)
    q=float(np.sum((y-X@coef)**2/v)); df=len(y)-rank
    return coef,cov,rank,q,df


def jacobian(fn, x):
    x=np.asarray(x,float); out=np.asarray(fn(x)); J=np.empty((out.size,len(x)))
    for k in range(len(x)):
        h=1e-5*max(1.,abs(x[k])); a=x.copy(); b=x.copy(); a[k]+=h;b[k]-=h
        J[:,k]=(np.asarray(fn(a)).ravel()-np.asarray(fn(b)).ravel())/(2*h)
    return J


def propagated(fn, mean, cov):
    v=np.asarray(fn(mean)); J=jacobian(fn,mean)
    return v, J@cov@J.T


def wilson(k,n,alpha=.05):
    if n==0: return [None,None]
    z=norm.ppf(1-alpha/2); p=k/n; d=1+z*z/n
    m=(p+z*z/(2*n))/d; w=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return [float(max(0,m-w)),float(min(1,m+w))]


def mean_sd(a):
    a=np.asarray([v for v in a if v is not None],float)
    return {'n':len(a),'mean':float(np.mean(a)) if len(a) else None,
            'sd':float(np.std(a,ddof=1)) if len(a)>1 else None}


def chi_p(q,df): return float(chi2.sf(max(0,float(q)),df)) if df>0 else None


def validate_run(r):
    """Serialized checks; no claim of cryptographic security or scientific validity."""
    obs=[Observation(**o) for o in r['observations']]
    ids=set(); keys=set(); previous={}
    for o in obs:
        key=(o.split,o.kind,round(o.x,10),round(o.delta,10),o.replicate)
        if o.record_id in ids or key in keys: raise AssertionError('Duplicate measurement')
        if o.parent_id is not None:
            if o.parent_id not in previous: raise AssertionError('Unknown replicate parent')
            p=previous[o.parent_id]
            if (p.kind,p.x,p.delta,p.split)!=(o.kind,o.x,o.delta,o.split): raise AssertionError('Cross-condition parent')
        previous[o.record_id]=o;ids.add(o.record_id);keys.add(key)
    for s in ('fit','audit','test'):
        if abs(sum(o.cost for o in obs if o.split==s)-r['costs'][s])>1e-8: raise AssertionError('Cost mismatch')
    prev='0'*64; freezes=[]; evaluations=[]
    for i,e in enumerate(r['events']):
        bare={k:v for k,v in e.items() if k!='hash'}
        if e['hash']!=digest(bare) or e['previous']!=prev or e['index']!=i: raise AssertionError('Event integrity')
        prev=e['hash']
        if e['type']=='measured':
            oid=e['payload']['record']
            if oid not in previous or e['payload']['record_digest']!=digest(previous[oid].export()):
                raise AssertionError('Measurement does not match event digest')
        if e['type']=='freeze':
            freezes.append(i)
            if e['payload']['acquisition_digest']!=digest([o.export() for o in obs if o.split!='test']):
                raise AssertionError('Frozen acquisition mismatch')
        if e['type']=='proposal' and e['payload']['split']!='test' and freezes:
            raise AssertionError('Acquisition after freeze')
        if e['type']=='evaluation_complete': evaluations.append(i)
        if e['type']=='proposal' and e['payload']['split']=='test' and not freezes: raise AssertionError('Early test access')
    if len(freezes)!=1 or len(evaluations)!=1 or evaluations[0]<=freezes[0]: raise AssertionError('Freeze/test order')
    return len(obs)
