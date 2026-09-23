"""H: local unknown-scale t tests and a conditional-sign test martingale.

No promise for arbitrary mean-zero noise: the sign monitor tests conditional
sign balance, while the batch t monitor requires fresh iid Gaussian contrasts
within each location. No new control data are reused for fitting.
"""
from __future__ import annotations
import numpy as np
from scipy import stats
from scipy.special import logsumexp
from .common import rng,group,seal,costs,native,normal_metrics
SCENARIOS=('gaussian_null','hetero_null','symmetric_t3_null','skew_mean_null','correlated_repeats',
           'broad_mean','narrow_mean','weak_narrow','common_mode')
POLICIES=('max_gap','adaptive_cover')
METHODS=('nominal_z','local_t_bonferroni','conditional_sign_e')
REPEATS=6

class SignMonitor:
    """Mixture of two-sided fixed bets, global and four fixed spatial bins.

    sign(0)=0 yields a factor of one. Under E[sign(D_t)|past,x_t]=0,
    each capital is a nonnegative martingale. Their fixed mixture is too.
    """
    def __init__(self,alpha: float=.05):
        if not 0<alpha<1:raise ValueError('Invalid alpha')
        self.alpha=alpha;self.stakes=np.array([-.75,-.5,-.25,.25,.5,.75])
        self.logs=np.zeros((5,6));self.n=0;self.max_value=1.
    def update(self,x: float,difference: float) -> float:
        if not (-1<=x<=1) or not np.isfinite(difference):raise ValueError('Invalid contrast')
        sign=np.sign(difference);inc=np.log1p(self.stakes*sign)
        self.logs[0]+=inc;idx=1+min(3,int((x+1)*2));self.logs[idx]+=inc
        components=logsumexp(self.logs,axis=1)-np.log(6)
        val=float(np.exp(logsumexp(components+np.log([.5,.125,.125,.125,.125]))))
        self.n+=1;self.max_value=max(self.max_value,val);return val
    @property
    def alarm(self):return self.max_value>=1/self.alpha

def choose_location(policy: str,history: list) -> float:
    if policy not in POLICIES:raise ValueError('Unknown policy')
    grid=np.linspace(-1,1,81)
    if not history:return 0.
    xs=np.array([h['x'] for h in history]);distance=np.min(abs(grid[:,None]-xs[None,:]),axis=1)
    if policy=='adaptive_cover' and len(history)>=3 and len(history)%2==1:
        h=max(history,key=lambda h:abs(h['mean_difference'])/(h['sd_difference']+.05))
        # Locations/score depend on past AUDIT only. No truth or final-test access.
        score=np.exp(-((grid-h['x'])/.22)**2)+.2*distance
        return round(float(grid[np.argmax(score)]),12)
    return round(float(grid[np.argmax(distance)]),12)

def batch_t_p(d: np.ndarray) -> float:
    if len(d)<2:raise ValueError('At least two fresh technical contrasts required')
    sd=float(np.std(d,ddof=1));mean=float(np.mean(d))
    if sd==0:return 1. if mean==0 else 0.
    return float(2*stats.t.sf(abs(mean)*np.sqrt(len(d))/sd,len(d)-1))

def truth_functions(w: dict,x: np.ndarray) -> tuple:
    x=np.asarray(x);base=w['coef'][0]+w['coef'][1]*x+w['coef'][2]*x*x
    bump=w['effect']*np.exp(-.5*((x-w['centre'])/w['width'])**2)
    if w['scenario']=='broad_mean':bump=np.full_like(x,w['effect'])
    if w['scenario']=='common_mode':return base+bump,base+bump
    return base+bump,base

def sigma(w:dict,x):
    x=np.asarray(x)
    return w['sigma']*np.exp(.9*x) if w['scenario']=='hetero_null' else np.full_like(x,w['sigma'],dtype=float)

def noise_pair(w:dict,x:float,random:np.random.Generator,n:int) -> tuple:
    sd=float(sigma(w,x));s=w['scenario']
    if s=='symmetric_t3_null':return sd*random.standard_t(3,n)/np.sqrt(3),sd*random.standard_t(3,n)/np.sqrt(3)
    if s=='skew_mean_null':return sd*2.5*(random.exponential(1,n)-1),sd*.25*random.normal(size=n)
    a=sd*random.normal(size=n);b=sd*random.normal(size=n)
    if s=='correlated_repeats':a+=random.normal(0,.18)
    return a,b

def make_world(bank,scenario,seed):
    if scenario not in SCENARIOS:raise ValueError('Unknown H scenario')
    r=rng('H',bank,scenario,seed,'world')
    effect={'broad_mean':.28,'narrow_mean':.55,'weak_narrow':.18,'common_mode':.55}.get(scenario,0.)
    return dict(scenario=scenario,coef=r.normal([.4,.7,-.15],[.08,.08,.03]).tolist(),sigma=r.uniform(.08,.14),
                effect=effect,centre=r.uniform(-.7,.7),width=.09)

def run(bank:str,scenario:str,seed:int,policy:str,fraction:float=.5,budget:int=144) -> dict:
    if policy not in POLICIES:raise ValueError('Unknown H policy')
    if fraction not in (0.,.25,.5,.75):raise ValueError('Audit fractions are 0, .25, .5, .75')
    w=make_world(bank,scenario,seed);groups=[];history=[]
    train_n=int(budget*(1-fraction));audit_budget=budget-train_n
    if train_n<4:raise ValueError('Insufficient training allocation')
    xx=rng('H',bank,scenario,seed,'train-x').uniform(-1,1,train_n)
    yy=[]
    for i,x in enumerate(xx):
        mean,_=truth_functions(w,np.array([x]));eps,_=noise_pair(w,x,rng('H',bank,scenario,seed,'train-y',i),1)
        yy.append(float(mean[0]+eps[0]))
    for i,(x,y) in enumerate(zip(xx,yy)):groups.append(group(f'fit:{i}','fit',x,[y]))
    X=np.column_stack([np.ones(train_n),xx,xx*xx]);y=np.asarray(yy)
    beta=np.linalg.lstsq(X,y,rcond=None)[0];s2=float(np.sum((y-X@beta)**2)/(train_n-3))
    covariance=s2*np.linalg.inv(X.T@X)
    # fit fixed before audit; no warning-triggered model repair or policy-family switching.
    monitor=SignMonitor();spent=0.;previous_x=None;max_looks=audit_budget//(2*REPEATS)
    first={m:None for m in METHODS}
    for look in range(int(max_looks)):
        x=choose_location(policy,history)
        setup=0. if previous_x is None else 1.+.5*abs(x-previous_x)
        batch_cost=2*REPEATS+setup
        if spent+batch_cost>audit_budget+1e-9:break
        mu,ctrl=truth_functions(w,np.array([x]));es,ec=noise_pair(w,x,rng('H',bank,scenario,seed,'audit',look,x),REPEATS)
        a=mu[0]+es;b=ctrl[0]+ec;d=a-b
        groups.append(group(f'audit:{look}:sample','audit',x,a,1.,channel='sample',batch=look))
        groups.append(group(f'audit:{look}:control','audit',x,b,1.,channel='control',batch=look))
        # Setup is charged in a separate explicit cost ledger, never as a measurement.
        spent+=batch_cost
        pt=batch_t_p(d)
        pz=float(2*stats.norm.sf(abs(np.mean(d))*np.sqrt(REPEATS)/(.12*np.sqrt(2))))
        ev=[]
        for di in d:ev.append(monitor.update(x,float(di)))
        alarms={'nominal_z':pz<=.05/max_looks,'local_t_bonferroni':pt<=.05/max_looks,'conditional_sign_e':monitor.alarm}
        for k,v in alarms.items():
            if v and first[k] is None:first[k]={'look':look+1,'cost':spent,'pairs':(look+1)*REPEATS}
        history.append(native(dict(x=x,mean_difference=np.mean(d),sd_difference=np.std(d,ddof=1),
             p_t=pt,p_nominal_z=pz,e_values=ev,maximum_e=monitor.max_value,
             alpha_per_batch=.05/max_looks,cumulative_audit_cost=spent,setup_cost=setup,alarms=alarms)))
        previous_x=x
    # Final independent labels generated only after prediction/audit procedure is finished.
    xt=np.linspace(-1,1,81);truth,_=truth_functions(w,xt);test=[]
    for i,x in enumerate(xt):
        ep,_=noise_pair(w,x,rng('H',bank,scenario,seed,'final',i),1);test.append(float(truth[i]+ep[0]))
        groups.append(group(f'final:{i}','final',x,[test[-1]]))
    T=np.column_stack([np.ones(len(xt)),xt,xt*xt]);prediction=T@beta
    metrics=normal_metrics(prediction,np.einsum('ij,jk,ik->i',T,covariance,T),np.full(len(xt),s2),truth,test)
    c=costs(groups);overhead=sum(h['setup_cost'] for h in history)
    methods={k:{'alarm':None if fraction==0 else first[k] is not None,'first':first[k],
        'restricted_cost_to_alarm':None if fraction==0 else (first[k]['cost'] if first[k] else audit_budget)} for k in METHODS}
    return seal('H',scenario,seed,bank,groups,dict(policy=policy,audit_fraction=fraction,budget=budget,
      costs=c,setup_cost=overhead,acquisition_spend=c['fit']+c['audit']+overhead,
      full_spend_including_final=c['total']+overhead,history=history,methods=methods,evaluation=metrics,
      fitted=dict(beta=beta,covariance=covariance,noise_variance=s2),
      evaluator_only=dict(truth=w,conditional_sign_null_valid=scenario in ('gaussian_null','hetero_null','symmetric_t3_null','common_mode'),
          local_t_null_valid=scenario in ('gaussian_null','hetero_null','common_mode'),
          mean_contrast_zero=scenario not in ('broad_mean','narrow_mean','weak_narrow'),
          common_mode_unobservable=scenario=='common_mode'),
      notes='Diagnostics are shadow monitors, not an OR-combined test. Failed detection is censored at allocated audit budget.'))
