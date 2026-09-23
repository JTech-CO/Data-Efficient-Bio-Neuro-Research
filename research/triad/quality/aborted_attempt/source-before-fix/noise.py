"""F: fully crossed acquisition controller x policy x final estimator.

The same acquired observations are refitted by every final estimator. All mean
models share one small quadratic basis. Thus robustness is not confounded with
mean-model capacity. Noise/parameter uncertainty propagation is approximate.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from scipy.special import ndtr, betaln, digamma
from scipy.stats import t as student
from .common import Collector, rng_for, require_fit, wls, digest

SCENARIOS=('gaussian','loglinear_noise','nonmonotone_noise','student3','contamination','missing_mean')
ESTIMATORS=('hom_gaussian','logvar_gaussian','student_t')
POLICIES=('random','spacefill','ivr')
NU=4.


def basis(x):
    x=np.asarray(x,float)
    return np.stack((np.ones_like(x),x,.5*(3*x*x-1)),axis=-1)

@dataclass(frozen=True)
class World:
    bank: str; scenario: str; seed: int; theta: tuple; tilt: float
    @property
    def identity(self): return f'F/{self.bank}/{self.scenario}/{self.seed}'
    def mean(self,x):
        x=np.asarray(x,float); y=basis(x)@np.asarray(self.theta)
        if self.scenario=='missing_mean': y=y+.24*np.sin(2*np.pi*(x+.1))
        return y
    def observe(self,kind,x,delta,rep,split):
        r=rng_for(self.identity,split,round(x,10),rep)
        sd=.12
        if self.scenario=='loglinear_noise': sd=.12*np.exp(self.tilt*x)
        if self.scenario=='nonmonotone_noise': sd=.055+.24*np.exp(-.5*((x-.25)/.22)**2)
        if self.scenario=='student3': e=sd*r.standard_t(3)/np.sqrt(3)
        elif self.scenario=='contamination': e=sd*(6. if r.random()<.08 else 1.)*r.normal()
        else: e=sd*r.normal()
        return float(self.mean(x))+e


def make_world(bank,scenario,seed):
    if scenario not in SCENARIOS: raise ValueError('Unknown noise scenario')
    r=rng_for('F/world',bank,seed)
    return World(bank,scenario,seed,tuple(r.uniform([.3,.3,-.35],[1.1,.9,.35])),float(r.uniform(.7,1.15)))


def fit(records,estimator):
    require_fit(records)
    if estimator not in ESTIMATORS: raise ValueError('Unknown noise estimator')
    if len(records)%2 or len(records)<6: raise ValueError('Noise estimators require complete technical pairs')
    x=np.array([o.x for o in records]);y=np.array([o.value for o in records]);X=basis(x)
    if not np.allclose(x[0::2],x[1::2]): raise ValueError('Pairs must have identical x')
    d=(y[0::2]-y[1::2])/np.sqrt(2);xp=x[0::2]
    pooled=float(np.clip(np.mean(d*d),.005**2,2.**2))
    noise_coef=np.array([np.log(pooled),0.]); converged=True;iterations=1
    if estimator=='logvar_gaussian':
        Z=np.c_[np.ones(len(xp)),xp]
        # E[log(chi-square_1)] = digamma(1/2) + log(2).
        target=np.log(np.maximum(d*d,1e-12))-(digamma(.5)+np.log(2))
        noise_coef=np.linalg.solve(Z.T@Z+np.diag([1e-8,.8]),Z.T@target)
        vv=np.clip(np.exp(np.clip(noise_coef[0]+noise_coef[1]*x,-20,5)),.005**2,2.**2)
        beta,C,rank,_,_=wls(X,y,vv)
        scale=float(np.sqrt(pooled))
    elif estimator=='hom_gaussian':
        beta,C,rank,_,_=wls(X,y,pooled);scale=float(np.sqrt(pooled))
    else:
        beta=np.linalg.lstsq(X,y,rcond=None)[0]
        residual=y-X@beta
        scale=max(.015,float(np.median(abs(residual-np.median(residual)))/.67448975))
        converged=False
        for iteration in range(40):
            residual=y-X@beta;weights=(NU+1)/(NU+(residual/scale)**2)
            new,_,rank,_,_=wls(X,y,scale**2/weights)
            new_scale=float(np.sqrt(np.clip(np.mean(weights*(y-X@new)**2),.005**2,2.**2)))
            change=max(float(np.max(abs(new-beta))),abs(new_scale-scale))
            beta=new;scale=new_scale;iterations=iteration+1
            if change<1e-7: converged=True;break
        residual=y-X@beta;weights=(NU+1)/(NU+(residual/scale)**2)
        # Expected-information / IRLS approximation, NOT an exact posterior.
        C=scale**2*np.linalg.pinv(X.T@(weights[:,None]*X))*(NU+3)/(NU+1)
        noise_coef=np.array([np.log(scale**2*NU/(NU-2)),0.])
    return {'estimator':estimator,'beta':beta.tolist(),'covariance':C.tolist(),'noise_coef':noise_coef.tolist(),
            'scale':scale,'nu':NU if estimator=='student_t' else None,'converged':converged,'iterations':iterations,
            'noise_uncertainty_integrated':False,'covariance_approximate':True,'rank':int(rank)}


def noise_variance(model,x):
    x=np.asarray(x,float);a,b=model['noise_coef']
    return np.clip(np.exp(np.clip(a+b*x,-20,5)),.005**2,2.**2)


def predict(model,x):
    P=basis(x); C=np.asarray(model['covariance']);mu=P@model['beta']
    latent_var=np.maximum(0,np.einsum('ij,jk,ik->i',P,C,P))
    if model['estimator']=='student_t':
        # Variance-matched t approximation to t noise plus Gaussian mean error.
        scale=np.sqrt(model['scale']**2+latent_var*(NU-2)/NU)
        half=student.ppf(.975,NU)*scale
    else:
        scale=np.sqrt(noise_variance(model,x)+latent_var);half=1.95996398454*scale
    return mu,scale,half,latent_var


def scores(model,x,y,truth):
    mu,s,h,lv=predict(model,x);z=(y-mu)/s
    if model['estimator']=='student_t':
        pdf=student.pdf(z,NU);cdf=student.cdf(z,NU)
        const=2*np.sqrt(NU)/(NU-1)*np.exp(betaln(.5,NU-.5)-2*betaln(.5,NU/2))
        crps=s*(z*(2*cdf-1)+2*pdf*(NU+z*z)/(NU-1)-const)
        nll=-student.logpdf(z,NU)+np.log(s)
    else:
        pdf=np.exp(-z*z/2)/np.sqrt(2*np.pi)
        crps=s*(z*(2*ndtr(z)-1)+2*pdf-1/np.sqrt(np.pi))
        nll=.5*z*z+np.log(s)+.5*np.log(2*np.pi)
    return {'latent_rmse':float(np.sqrt(np.mean((mu-truth)**2))),
            'predictive_nll':float(np.mean(nll)),'crps':float(np.mean(crps)),
            'observed_inclusion':float(np.mean(abs(y-mu)<=h)),'observed_width':float(np.mean(2*h)),
            'latent_inclusion':float(np.mean(abs(truth-mu)<=1.96*np.sqrt(lv))),
            'fit_converged':model['converged']}


def select(model,records,policy,rng):
    grid=np.linspace(-1,1,41)
    if policy=='random': return float(rng.choice(grid))
    used=np.array([o.x for o in records]);dist=np.min(abs(grid[:,None]-used[None,:]),axis=1)
    if policy=='spacefill':
        choices=np.flatnonzero(np.isclose(dist,dist.max()));return float(grid[int(rng.choice(choices))])
    if policy!='ivr': raise ValueError('Unknown acquisition policy')
    C=np.array(model['covariance']);P=basis(grid);T=basis(np.linspace(-1,1,101));M=T.T@T/len(T)
    signal_var=np.einsum('ij,jk,ik->i',P,C,P)
    reduction=np.einsum('ij,jk,ik->i',P,C@M@C,P)/(noise_variance(model,grid)/2+signal_var)
    # Equal-cost pairs. Moment-based IVR proxy, not exact t expected information.
    j=int(np.argmax(reduction));return float(grid[j])


def run(bank,scenario,seed,controller,policy,budget=48):
    if controller not in ESTIMATORS or policy not in POLICIES or type(budget)!=int or budget<12 or budget>200 or budget%2:
        raise ValueError('Invalid controller, policy or even measurement budget')
    w=make_world(bank,scenario,seed);c=Collector(w.identity,w.observe)
    rng=rng_for('F/policy',bank,seed,policy) # deliberately no controller for passive policies
    for x in np.linspace(-1,1,5):
        for _ in range(2): c.take('sample',float(x),sd=.12)
    history=[]
    while len(c.records)<budget:
        m=fit(tuple(c.records),controller)
        x=select(m,tuple(c.records),policy,rng)
        history.append({'fit_n':len(c.records),'x':x,'controller':controller,'policy':policy,
                        'estimated_variance':float(noise_variance(m,np.array([x]))[0]),'converged':m['converged']})
        for _ in range(2): c.take('sample',x,sd=.12)
    data=tuple(c.records);models={k:fit(data,k) for k in ESTIMATORS};c.freeze(models)
    grid=np.linspace(-1,1,81)
    tests=[c.take('sample',x,split='test',sd=.12) for x in grid]
    y=np.array([o.value for o in tests]);truth=w.mean(grid)
    evaluation={k:scores(v,grid,y,truth) for k,v in models.items()}
    c.finish()
    return {'version':'1.3.0-research.1','study':'F','bank':bank,'scenario':scenario,'seed':seed,
            'controller':controller,'policy':policy,'budget':budget,'models':models,'evaluation':evaluation,
            'data_digest':digest([o.export() for o in data]),'history':history,'costs':c.costs(),
            'curves':{'x':grid.tolist(),'truth':truth.tolist(),'test_y':y.tolist(),
                      'predictions':{k:{'mean':predict(v,grid)[0].tolist(),'halfwidth':predict(v,grid)[2].tolist()} for k,v in models.items()}},
            'observations':[o.export() for o in c.records],'events':c.trail.events,
            'evaluator_truth':{'theta':list(w.theta),'tilt':w.tilt,'causal_source_identified':False}}
