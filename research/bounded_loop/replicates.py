"""I: same-data noise / mean ablations using independent technical differences.

The model-independent pure-error identity is algebraic. Its F reference law
is only exact under the declared homoscedastic iid Gaussian conditions.
"""
from __future__ import annotations
import numpy as np
from scipy import stats
from scipy.special import digamma,logsumexp,ndtr
from .common import rng,group,seal,costs,native,normal_metrics
SCENARIOS=('normal','heteroscedastic','mean_missing','combined','local_missing','contamination','shared_batch','within_batch_drift')
REPLICATION=(2,4,6)
ESTIMATORS=('pooled_base','residual_logvar_base','difference_logvar_base','difference_logvar_plus','plus_bootstrap')

def basis(x,plus=False):
    x=np.asarray(x,float);a=[np.ones_like(x),x,x*x]
    if plus:a.append(np.sin(np.pi*x))
    return np.column_stack(a)

def variance_fit(x,q,df):
    """log chi-square mean correction is exact only for independent Gaussian noise."""
    V=np.column_stack([np.ones(len(x)),x])
    bias=digamma(df/2)+np.log(2/df)
    target=np.log(np.maximum(q,1e-10))-bias
    penalty=np.diag([.001,.20])
    gamma=np.linalg.solve(V.T@V+penalty,V.T@target)
    return gamma

def noise_variance(gamma,x):
    V=np.column_stack([np.ones(len(x)),x]);raw=V@np.asarray(gamma)
    return np.exp(np.clip(raw,-9,2))

def fit(x,y,method):
    if method not in ESTIMATORS[:-1]:raise ValueError('Unknown fitting method')
    x=np.asarray(x,float);y=np.asarray(y,float)
    if y.ndim!=2 or y.shape[0]!=len(x) or y.shape[1]<2:raise ValueError('Replicate matrix required')
    r=y.shape[1];plus=method=='difference_logvar_plus';X=basis(x,plus);means=y.mean(axis=1)
    if len(x)<=X.shape[1]:raise ValueError('Not enough unique locations')
    initial=np.linalg.lstsq(X,means,rcond=None)[0]
    if method=='pooled_base':
        s2=float(np.sum((y-(X@initial)[:,None])**2)/(y.size-X.shape[1]))
        gamma=np.array([np.log(max(s2,1e-10)),0.])
    elif method=='residual_logvar_base':
        # This baseline deliberately mixes squared mean error into the variance fit.
        gamma=variance_fit(x,np.mean((y-(X@initial)[:,None])**2,axis=1),r)
    else:
        k=r//2;d=(y[:,:2*k:2]-y[:,1:2*k:2])/np.sqrt(2)
        gamma=variance_fit(x,np.mean(d*d,axis=1),k)
    sv=noise_variance(gamma,x);weights=r/sv
    information=X.T@(weights[:,None]*X)
    covariance=np.linalg.inv(information)
    beta=np.linalg.solve(information,X.T@(weights*means))
    return {'method':method,'plus':plus,'beta':beta,'gamma':gamma,'covariance':covariance,
            'variance_clip_count':int(np.sum(abs(np.column_stack([np.ones(len(x)),x])@gamma-np.clip(np.column_stack([np.ones(len(x)),x])@gamma,-9,2))>1e-12))}

def predict(model,x):
    X=basis(x,model['plus']);mu=X@model['beta'];vm=np.einsum('ij,jk,ik->i',X,model['covariance'],X)
    return mu,np.maximum(vm,1e-12),noise_variance(model['gamma'],np.asarray(x))

def pure_error(x,y):
    x=np.asarray(x);y=np.asarray(y);J,r=y.shape;X=basis(x);means=y.mean(1)
    beta=np.linalg.lstsq(X,means,rcond=None)[0];pred=X@beta
    pure=float(np.sum((y-means[:,None])**2));lof=float(r*np.sum((means-pred)**2))
    total=float(np.sum((y-pred[:,None])**2));dfp=y.size-J;dfl=J-X.shape[1]
    if pure<=0:stat=0. if lof<=1e-20 else None;p=1. if stat==0 else 0.
    else:stat=(lof/dfl)/(pure/dfp);p=float(stats.f.sf(stat,dfl,dfp))
    return dict(sse_total=total,sse_pure=pure,sse_lack_of_fit=lof,identity_error=abs(total-pure-lof),
                df_pure=dfp,df_lack_of_fit=dfl,F=stat,p=p,pure_variance=pure/dfp)

def mixture_metrics(mus,variances,truth,obs):
    mus=np.asarray(mus);variances=np.maximum(variances,1e-12);sd=np.sqrt(variances)
    nll=float(-np.mean(logsumexp(-.5*np.log(2*np.pi*variances)-.5*(np.asarray(obs)[None,:]-mus)**2/variances,axis=0)-np.log(len(mus))))
    quantiles=[]
    for p in (.025,.975):
        left=np.min(mus-9*sd,axis=0);right=np.max(mus+9*sd,axis=0)
        for _ in range(36):
            mid=(left+right)/2;cdf=ndtr((mid[None,:]-mus)/sd).mean(0)
            left=np.where(cdf<p,mid,left);right=np.where(cdf>=p,mid,right)
        quantiles.append((left+right)/2)
    lo,hi=quantiles;latentlo,latenthi=np.quantile(mus,[.025,.975],axis=0)
    m=mus.mean(0)
    return native(dict(rmse=np.sqrt(np.mean((m-truth)**2)),nll=nll,
          observed_coverage=np.mean((obs>=lo)&(obs<=hi)),observed_width=np.mean(hi-lo),
          latent_coverage=np.mean((truth>=latentlo)&(truth<=latenthi)),latent_width=np.mean(latenthi-latentlo),
          interval_score=np.mean(hi-lo+40*np.maximum(lo-obs,0)+40*np.maximum(obs-hi,0))))

def make_world(bank,scenario,seed):
    if scenario not in SCENARIOS:raise ValueError('Unknown I scenario')
    rr=rng('I',bank,scenario,seed,'world')
    return dict(scenario=scenario,beta=rr.normal([.5,.65,-.2],[.08,.07,.03]),
       sine=.28 if scenario in ('mean_missing','combined') else 0.,
       bump=.5 if scenario=='local_missing' else 0.,centre=rr.uniform(-.5,.5),
       sigma=rr.uniform(.09,.14))

def mean_truth(w,x):return basis(x)@w['beta']+w['sine']*np.sin(np.pi*x)+w['bump']*np.exp(-.5*((x-w['centre'])/.065)**2)
def true_sigma(w,x):
    return w['sigma']*np.exp(.9*x) if w['scenario'] in ('heteroscedastic','combined') else np.full(len(x),w['sigma'])
def measure(w,x,r,random):
    sv=true_sigma(w,x);eps=random.normal(size=(len(x),r))*sv[:,None]
    if w['scenario']=='contamination':
        mask=random.uniform(size=eps.shape)<.10;eps=np.where(mask,eps*6.,eps)
    if w['scenario']=='shared_batch':eps+=random.normal(0,.18,(len(x),1))
    if w['scenario']=='within_batch_drift':
        eps+=.14*np.linspace(-1,1,r)[None,:]
    return mean_truth(w,x)[:,None]+eps

def run(bank:str,scenario:str,seed:int,repeats:int=4,budget:int=48,bootstrap:int=64) -> dict:
    if repeats not in REPLICATION:raise ValueError('repeats must be 2,4,6')
    if bootstrap<20:raise ValueError('Bootstrap count must be at least 20')
    if budget%repeats:raise ValueError('Budget must be divisible by repetitions')
    n=budget//repeats;w=make_world(bank,scenario,seed)
    xx=np.linspace(-.95,.95,n)+rng('I',bank,scenario,seed,'locations',n).uniform(-.15/n,.15/n,n)
    yy=measure(w,xx,repeats,rng('I',bank,scenario,seed,'measure',repeats))
    groups=[group(f'fit:{i}','fit',x,yy[i]) for i,x in enumerate(xx)]
    models={m:fit(xx,yy,m) for m in ESTIMATORS[:-1]}
    base=models['difference_logvar_plus'];mu_x,_,sv_x=predict(base,xx)
    boot_models=[]
    for b in range(bootstrap):
        ystar=mu_x[:,None]+rng('I',bank,scenario,seed,repeats,'parametric-bootstrap',b).normal(size=yy.shape)*np.sqrt(sv_x[:,None])
        boot_models.append(fit(xx,ystar,'difference_logvar_plus'))
    # Every fit and every bootstrap fit is completed before final labels are drawn.
    xt=np.linspace(-1,1,81);yt=measure(w,xt,1,rng('I',bank,scenario,seed,'final'))[:,0];truth=mean_truth(w,xt)
    groups += [group(f'final:{i}','final',x,[yt[i]]) for i,x in enumerate(xt)]
    evaluation={};curves={}
    for name,m in models.items():
        mu,vm,vn=predict(m,xt);evaluation[name]=normal_metrics(mu,vm,vn,truth,yt)
        curves[name]=native(dict(mean=mu,latent_sd=np.sqrt(vm),noise_sd=np.sqrt(vn)))
    boot_preds=[predict(m,xt) for m in boot_models];bm=np.array([a[0] for a in boot_preds]);bv=np.array([a[2] for a in boot_preds])
    evaluation['plus_bootstrap']=mixture_metrics(bm,bv,truth,yt)
    pe=pure_error(xx,yy)
    return seal('I',scenario,seed,bank,groups,dict(repeats=repeats,unique_locations=n,budget=budget,bootstrap=bootstrap,
        costs=costs(groups),models=models,bootstrap_models=boot_models,pure_error=pe,
        evaluation=evaluation,curves=curves,
        evaluator_only=dict(truth=w,grid=xt,latent_response=truth,
          exact_pure_error_F_null_valid=scenario=='normal',
          independent_gaussian_variance_model_correct=scenario in ('normal','heteroscedastic','mean_missing','combined','local_missing'),
          plus_mean_family_correct=scenario not in ('local_missing',),
          repeat_independence=scenario!='shared_batch'),
        notes='Fixed basis on/off ablation, not equation discovery. Conditional parametric bootstrap, not distribution-free coverage.'))
