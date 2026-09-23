"""G: exact LP projections for a declared affine inverse-calibration model.

The polytope combines simultaneous technical-replicate mean intervals and
bounded nuisance bias. It is not the sharp identified set of an arbitrary
biological system. Infeasibility is reported, never repaired using truth.
"""
from __future__ import annotations
import numpy as np
from scipy.optimize import linprog
from scipy import stats
from .common import rng, group, seal, costs, native
SCENARIOS=('normal','bounded_bias','common_in_bounds','common_out_of_bounds','nonlinear_sensor','correlated_repeats')
DESIGNS=('reference_only','addition_blank','triangulated')
B_REF=.12; B_BLANK=.08; RECOVERY_HALF=.10
GAIN_RANGE=(.60,1.50)
TARGETS={'theta0':[1,0,0,0,0], 'theta1':[0,1,0,0,0],
         'inverse_gain':[0,0,1,0,0], 'inverse_offset':[0,0,0,1,0],
         'recovery':[0,0,0,0,1], 'z_minus1':[1,-1,0,0,0], 'z_plus1':[1,1,0,0,0]}

def design_groups(design: str, budget: float=72.) -> list:
    if design not in DESIGNS: raise ValueError('Unknown G design')
    groups=[dict(kind='primary',x=-.8,delta=0.,unit_cost=1.),dict(kind='primary',x=.8,delta=0.,unit_cost=1.)]
    if design in ('addition_blank','triangulated'):
        groups += [dict(kind='primary',x=x,delta=.6,unit_cost=1.5) for x in (-.8,.8)]
        groups += [dict(kind='blank',x=0.,delta=0.,unit_cost=1.)]
    if design in ('reference_only','triangulated'):
        groups += [dict(kind='reference',x=x,delta=0.,unit_cost=3.) for x in (-.8,.8)]
    cycle=sum(g['unit_cost'] for g in groups);n=int(budget//cycle)
    if n<4: raise ValueError('Budget must fund at least four repeats per group')
    for g in groups:g['n']=n
    left=budget-n*cycle
    for g in groups:
        if left+1e-9>=g['unit_cost']:g['n']+=1;left-=g['unit_cost']
    return groups

def make_world(bank: str, scenario: str, seed: int) -> dict:
    if scenario not in SCENARIOS: raise ValueError('Unknown G scenario')
    r=rng('G',bank,scenario,seed,'world')
    w=dict(theta0=r.uniform(.7,1.3),theta1=r.uniform(.35,.85),gain=r.uniform(.8,1.25),
           offset=r.uniform(-.12,.12),recovery=1.,ref_bias=0.,blank_bias=0.,quadratic=0.,batch_sd=0.)
    if scenario in ('bounded_bias','correlated_repeats'):
        w.update(recovery=r.uniform(.92,1.08),ref_bias=r.uniform(-.1,.1),blank_bias=r.uniform(-.06,.06))
    if scenario in ('common_in_bounds','common_out_of_bounds'):
        shift=.06 if scenario=='common_in_bounds' else .32
        w.update(ref_bias=shift,blank_bias=-shift)
    if scenario=='nonlinear_sensor':w['quadratic']=.22
    if scenario=='correlated_repeats':w['batch_sd']=.07
    return w

def intervals(groups: list, alpha: float=.05) -> list:
    fit=[g for g in groups if g['role']=='fit'];out=[]
    if not 0<alpha<1:raise ValueError('alpha must be in (0,1)')
    for g in fit:
        y=np.asarray(g['values']);n=len(y)
        if n<2:raise ValueError('Technical repeats required')
        t=stats.t.ppf(1-alpha/(2*len(fit)),n-1)
        half=t*np.std(y,ddof=1)/np.sqrt(n)
        out.append({**{k:g[k] for k in ('kind','x','delta')},'low':float(y.mean()-half),'high':float(y.mean()+half)})
    return out

def constraints(cis: list, multiplier: float=1.) -> tuple:
    if multiplier<0 or not np.isfinite(multiplier):raise ValueError('Invalid bias multiplier')
    if multiplier*RECOVERY_HALF>=1:raise ValueError('Recovery lower bound must remain positive')
    A=[];b=[]
    for g in cis:
        x,lo,hi=g['x'],g['low'],g['high']
        if lo>hi:raise ValueError('Reversed measurement interval')
        if g['kind']=='primary':
            d=g['delta']
            A.extend([[-1,-x,lo,1,-d],[1,x,-hi,-1,d]]);b.extend([0,0])
        elif g['kind']=='reference':
            A.extend([[1,x,0,0,0],[-1,-x,0,0,0]])
            b.extend([hi+multiplier*B_REF,-lo+multiplier*B_REF])
        elif g['kind']=='blank':
            A.extend([[0,0,lo,1,0],[0,0,-hi,-1,0]])
            b.extend([multiplier*B_BLANK,multiplier*B_BLANK])
        else:raise ValueError('Unknown measurement kind')
    bounds=[(None,None),(None,None),(1/GAIN_RANGE[1],1/GAIN_RANGE[0]),(None,None),
            (1-multiplier*RECOVERY_HALF,1+multiplier*RECOVERY_HALF)]
    return np.asarray(A,float),np.asarray(b,float),bounds

def solve(cis: list, multiplier: float=1., objectives: dict|None=None) -> dict:
    A,b,bounds=constraints(cis,multiplier)
    feas=linprog(np.zeros(5),A_ub=A,b_ub=b,bounds=bounds,method='highs')
    if feas.status==2:return {'status':'empty','projections':{},'solver_status':2}
    if not feas.success:raise RuntimeError(f'LP feasibility failed: {feas.message}')
    projections={}
    for key,c in (objectives or TARGETS).items():
        cc=np.asarray(c,float);sol=[]
        for sign in (1,-1):
            result=linprog(sign*cc,A_ub=A,b_ub=b,bounds=bounds,method='highs')
            if result.status==3:sol.append(None)
            elif result.success:sol.append(float(sign*result.fun))
            else:raise RuntimeError(f'LP projection failed: {result.message}')
        projections[key]={'low':sol[0],'high':sol[1], 'width':None if None in sol else sol[1]-sol[0]}
    return {'status':'unbounded' if any(v['width'] is None for v in projections.values()) else 'bounded',
            'projections':projections,'solver_status':0}

def contains(cis: list, q: np.ndarray, multiplier: float) -> bool:
    A,b,bounds=constraints(cis,multiplier)
    return bool(np.all(A@q<=b+1e-8) and all((lo is None or z>=lo-1e-8) and (hi is None or z<=hi+1e-8)
                                         for z,(lo,hi) in zip(q,bounds)))

def run(bank: str,scenario: str,seed: int,design: str,budget: float=72.) -> dict:
    w=make_world(bank,scenario,seed);observations=[];exact=[]
    for i,spec in enumerate(design_groups(design,budget)):
        x=spec['x'];z=w['theta0']+w['theta1']*x;kind=spec['kind'];d=spec['delta']
        if kind=='primary':
            z=z+w['recovery']*d
            m=w['gain']*z+w['offset']+w['quadratic']*z*z;sd=.035
        elif kind=='reference':m=z+w['ref_bias'];sd=.020
        else:m=w['gain']*w['blank_bias']+w['offset'];sd=.030
        rr=rng('G',bank,scenario,seed,kind,x,d,'measure')
        # A fixed group-level error deliberately violates independence in its stress case.
        shift=rng('G',bank,scenario,seed,kind,x,d,'batch').normal(0,w['batch_sd'])
        vals=m+shift+rr.normal(0,sd,spec['n'])
        observations.append(group(f'G:{i}','fit',x,vals,spec['unit_cost'],kind=kind,delta=d))
        exact.append({'kind':kind,'x':x,'delta':d,'low':m,'high':m})
    cis=intervals(observations)
    fits={name:solve(cis,scale) for name,scale in [('assume_unbiased',0.),('bounded',1.),('wide',2.)]}
    # This evaluator-only noiseless projection is NOT supplied to a fit or a selector.
    structural=solve(exact,1.)
    q=np.array([w['theta0'],w['theta1'],1/w['gain'],-w['offset']/w['gain'],w['recovery']])
    evaluation={}
    for name,scale in [('assume_unbiased',0.),('bounded',1.),('wide',2.)]:
        f=fits[name]
        evaluation[name]={'empty':f['status']=='empty','joint_truth_in_set':contains(cis,q,scale),
            'theta0_width':f['projections'].get('theta0',{}).get('width'),
            'theta1_width':f['projections'].get('theta1',{}).get('width')}
        if f['status']!='empty':
            pr=f['projections']['theta0'];evaluation[name]['theta0_in_projection']=bool(pr['low']-1e-8<=w['theta0']<=pr['high']+1e-8)
        else:evaluation[name]['theta0_in_projection']=False
    return seal('G',scenario,seed,bank,observations,{'design':design,'budget':budget,'costs':costs(observations),
        'measurement_intervals':cis,'fits':fits,'evaluation':evaluation,
        'evaluator_only':{'truth':w,'noiseless_identification_set':structural,
          'declared_bias_conditions_hold':scenario not in ('common_out_of_bounds','nonlinear_sensor'),
          'iid_gaussian_repeat_conditions_hold':scenario!='correlated_repeats'},
        'notes':'Projection bounds, not a posterior or a set midpoint estimate. Final evaluation is analytic; no final assay cost.'})
