"""Small auditable predictive models; no simulator or evaluator imports."""
from __future__ import annotations
import numpy as np
from scipy.linalg import cho_factor, cho_solve
from scipy.special import logsumexp, ndtr
from .contracts import Query, ObservationAssumptions
from .ledger import TrainingDatum

MODELS=("parallel","compensatory")

def features(queries, model: str, observer: ObservationAssumptions):
    if model not in MODELS: raise ValueError('Unknown mechanism')
    rows=[]; offsets=[]
    for q in queries:
        wa,wb,bias=observer.weights_offset(q)
        p=q.condition*np.exp(-q.time)*(1-q.intervention)
        b=q.condition*np.exp(-.45*q.time)
        c=(.8*q.intervention*q.condition*(1-np.exp(-.45*q.time)) if model=='compensatory' else 0.)
        rows.append((wa*p+wb*c,wb*b)); offsets.append(bias)
    return np.asarray(rows,dtype=float).reshape(-1,2), np.asarray(offsets)

class MechanisticEnsemble:
    """Exact conjugate BLR per known ODE candidate, exact Gaussian marginal evidence."""
    def __init__(self, observer: ObservationAssumptions, data=()):
        self.observer=observer
        self.data=tuple(data)
        self.prior_mean=np.array([1.,1.])
        self.prior_cov=np.eye(2)*.6**2
        self.parameters=[]; self.covariances=[]; self.log_evidence=[]
        for model in MODELS:
            X,offset=features([d.query for d in data],model,observer)
            y=np.array([d.value for d in data])-offset
            s2=np.array([d.sigma**2 for d in data])
            if not len(data):
                mean=self.prior_mean.copy(); cov=self.prior_cov.copy(); le=0.
            else:
                precision=np.linalg.inv(self.prior_cov)+(X.T/s2)@X
                cov=np.linalg.inv(precision)
                mean=cov@(np.linalg.solve(self.prior_cov,self.prior_mean)+X.T@(y/s2))
                C=X@self.prior_cov@X.T+np.diag(s2)
                cf=cho_factor(C,lower=True,check_finite=False)
                residual=y-X@self.prior_mean
                le=-.5*(residual@cho_solve(cf,residual)+2*np.log(np.diag(cf[0])).sum()+len(data)*np.log(2*np.pi))
            self.parameters.append(mean); self.covariances.append(cov); self.log_evidence.append(le)
        # Weights have no dependence on ground truth. Uniform prior over the two candidates.
        logw=np.asarray(self.log_evidence)-logsumexp(self.log_evidence)
        self.weights=np.exp(logw)

    def components(self, queries, noisy: bool = True):
        means=[]; variances=[]
        for i,model in enumerate(MODELS):
            X,off=features(queries,model,self.observer)
            means.append(X@self.parameters[i]+off)
            variances.append(np.maximum(np.einsum('ij,jk,ik->i',X,self.covariances[i],X),1e-12))
        means=np.array(means); variances=np.array(variances)
        if noisy: variances+=np.array([q.nominal_sigma**2 for q in queries])[None,:]
        return means,variances

    def predict(self, queries, noisy: bool=True):
        m,v=self.components(queries,noisy)
        mean=self.weights@m
        var=self.weights@(v+m*m)-mean*mean
        return mean,np.maximum(var,1e-12)

    def interval(self, queries, noisy: bool=True, level=.95):
        m,v=self.components(queries,noisy)
        return mixture_interval(m,v,self.weights,level)

    def information(self, queries, nodes: int=20):
        """I(M;Y|D,q), deterministic Gauss-Hermite integration; nats.
        Conditional parameter information is analytic, averaged over M.
        The two quantities are intentionally exposed separately.
        """
        m,v=self.components(queries,True)
        gh,gw=np.polynomial.hermite.hermgauss(nodes)
        score=np.zeros(len(queries))
        logw=np.log(np.maximum(self.weights,1e-300))
        for i in range(2):
            if self.weights[i]<1e-14: continue
            y=m[i,:,None]+np.sqrt(2*v[i,:,None])*gh[None,:]
            lp=-.5*(np.log(2*np.pi*v[:,:,None])+(y[None,:,:]-m[:,:,None])**2/v[:,:,None])
            lmix=logsumexp(logw[:,None,None]+lp,axis=0)
            score+=self.weights[i]*((lp[i]-lmix)@(gw/np.sqrt(np.pi)))
        entropy=-float(np.sum(self.weights*np.log(np.maximum(self.weights,1e-300))))
        # Floating-point/quadrature errors must not produce impossible negative information.
        score=np.clip(score,0.,entropy)
        _,lv=self.components(queries,False)
        noise=np.array([q.nominal_sigma**2 for q in queries])
        param=.5*(self.weights@np.log1p(lv/noise))
        return score,param

    def diagnostic(self, candidates):
        ranks=[]; conditions=[]
        for model in MODELS:
            X,_=features([d.query for d in self.data],model,self.observer)
            rank=int(np.linalg.matrix_rank(X)) if len(X) else 0
            ranks.append(rank)
            conditions.append(float(np.linalg.cond(X)) if rank==2 else None)
        m,_=self.components(candidates,False)
        return {'parameter_design_rank':dict(zip(MODELS,ranks)),
                'parameter_design_condition':dict(zip(MODELS,conditions)),
                'maximum_candidate_mean_gap':float(np.max(np.abs(m[0]-m[1]))) if len(candidates) else 0.,
                'interpretation':'Local linear design diagnostics; not a general structural-identifiability proof.'}

    def state(self):
        return {'weights':dict(zip(MODELS,self.weights.tolist())),
                'parameters':{m:{'mean':self.parameters[i].tolist(),'covariance':self.covariances[i].tolist()}
                              for i,m in enumerate(MODELS)},
                'log_evidence':dict(zip(MODELS,[float(v) for v in self.log_evidence]))}

def mixture_interval(m,v,w,level=.95):
    """Pointwise quantiles of a scalar Gaussian mixture via vectorized bisection."""
    def quantile(p):
        left=(m-12*np.sqrt(v)).min(axis=0); right=(m+12*np.sqrt(v)).max(axis=0)
        for _ in range(42):
            mid=(left+right)/2
            cdf=w@ndtr((mid[None,:]-m)/np.sqrt(v))
            left=np.where(cdf<p,mid,left); right=np.where(cdf<p,right,mid)
        return (left+right)/2
    alpha=(1-level)/2
    return quantile(alpha),quantile(1-alpha)

def embedding(queries):
    return np.array([[q.condition/1.4,q.time/2.4,q.intervention,
                      float(q.readout=='aggregate'),float(q.readout=='pathway_a'),float(q.readout=='pathway_b')]
                     for q in queries],dtype=float).reshape(-1,6)

class PredictiveGP:
    """Fixed RBF GP on query coordinates. Prediction fallback only, not a mechanism.
    No residual pseudo-labels, fitted hyperparameters, or audit/test labels are used.
    """
    def __init__(self, observer: ObservationAssumptions, data):
        self.observer=observer; self.data=tuple(data)
        self.X=embedding([d.query for d in data])
        self.length=np.array([.65,.6,.7,.8,.8,.8])
        if len(data):
            K=self.kernel(self.X,self.X)+np.diag([d.sigma**2+1e-9 for d in data])
            self.factor=cho_factor(K,lower=True,check_finite=False)
            centered=np.array([d.value-observer.weights_offset(d.query)[2] for d in data])
            self.alpha=cho_solve(self.factor,centered)

    def kernel(self,X,Z):
        distance=((X[:,None,:]-Z[None,:,:])/self.length)**2
        return np.exp(-.5*distance.sum(axis=2))

    def predict(self,queries,noisy=True):
        Q=embedding(queries)
        off=np.array([self.observer.weights_offset(q)[2] for q in queries])
        if len(self.data):
            k=self.kernel(self.X,Q)
            mean=off+k.T@self.alpha
            var=1.-np.einsum('ij,ij->j',k,cho_solve(self.factor,k))
        else: mean=off;var=np.ones(len(queries))
        var=np.maximum(var,1e-10)
        if noisy: var+=np.array([q.nominal_sigma**2 for q in queries])
        return mean,var

    def interval(self,queries,noisy=True,level=.95):
        from scipy.special import ndtri
        m,v=self.predict(queries,noisy)
        z=ndtri(.5+level/2)
        return m-z*np.sqrt(v),m+z*np.sqrt(v)
