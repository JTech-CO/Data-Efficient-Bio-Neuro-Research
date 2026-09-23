"""Locally frozen synthetic banks; exhaustive rows and paired descriptive contrasts."""
from __future__ import annotations
import gzip,json,hashlib,platform,sys,time
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import scipy
from . import partial,audit,replicates
from .common import digest,native,write_json,read_json,validate,rng,wilson,VERSION
ROOT=Path(__file__).resolve().parents[2]
CONFIG_PATH=ROOT/'research/bounded/configs/protocol.json'

def sources():
    files=sorted((ROOT/'research/bounded_loop').glob('*.py'))+[CONFIG_PATH]
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}

def job(spec:dict) -> dict:
    study=spec['study'];args=(spec['bank'],spec['scenario'],spec['seed'])
    if study=='G':return partial.run(*args,spec['design'],spec.get('budget',72))
    if study=='H':return audit.run(*args,spec['policy'],spec['fraction'],spec.get('budget',144))
    if study=='I':return replicates.run(*args,spec['repeats'],spec.get('budget',48),spec.get('bootstrap',64))
    raise ValueError('Unknown study')

def jobs(config):
    bank=config['evaluation_bank'];start=config['seed_start']
    out=[]
    for s in partial.SCENARIOS:
        for i in range(config['G']['worlds_per_scenario']):
            for d in partial.DESIGNS:out.append(dict(study='G',bank=bank,scenario=s,seed=start+i,design=d,budget=72))
    for s in audit.SCENARIOS:
        n=config['H']['valid_null_worlds'] if s in ('gaussian_null','hetero_null','symmetric_t3_null') else config['H']['other_worlds']
        for i in range(n):
            out.append(dict(study='H',bank=bank,scenario=s,seed=start+i,policy='max_gap',fraction=0.,budget=144))
            for p in audit.POLICIES:
                for f in (.25,.5,.75):out.append(dict(study='H',bank=bank,scenario=s,seed=start+i,policy=p,fraction=f,budget=144))
    for s in replicates.SCENARIOS:
        for i in range(config['I']['worlds_per_scenario']):
            for r in replicates.REPLICATION:out.append(dict(study='I',bank=bank,scenario=s,seed=start+i,repeats=r,budget=48,bootstrap=config['I']['bootstrap']))
    return out

def row_records(r):
    common={k:r[k] for k in ['study','scenario','seed','record_digest']}
    if r['study']=='G':
        return [native({**common,'design':r['design'],'variant':v,**m,
              'structural_theta0_width':r['evaluator_only']['noiseless_identification_set']['projections'].get('theta0',{}).get('width'),
              'fit_cost':r['costs']['fit']}) for v,m in r['evaluation'].items()]
    if r['study']=='H':
        return [native({**common,'policy':r['policy'],'audit_fraction':r['audit_fraction'],'variant':v,
              'alarm':m['alarm'],'restricted_cost_to_alarm':m['restricted_cost_to_alarm'],
              'audit_spend':r['costs']['audit']+r['setup_cost'],'fit_cost':r['costs']['fit'],
              'acquisition_spend':r['acquisition_spend'],**r['evaluation']}) for v,m in r['methods'].items()]
    return [native({**common,'repeats':r['repeats'],'variant':v,**m,
            'pure_variance':r['pure_error']['pure_variance'],'lack_of_fit_alarm':r['pure_error']['p']<=.05,
            'partition_error':r['pure_error']['identity_error'],'variance_clip_count':sum(z['variance_clip_count'] for z in r['models'].values()),
            'fit_cost':r['costs']['fit']}) for v,m in r['evaluation'].items()]

def summarize(rows):
    grouped=defaultdict(list)
    for r in rows:
        key=tuple((k,r[k]) for k in ('study','scenario','design','policy','audit_fraction','repeats','variant') if k in r)
        grouped[key].append(r)
    out=[]
    for key,rs in sorted(grouped.items(),key=lambda kv:str(kv[0])):
        fixed=dict(key);n=len(rs);metrics={}
        for k in rs[0]:
            if k in fixed or k in ('seed','record_digest'):continue
            values=[r[k] for r in rs if r[k] is not None]
            if not values:metrics[k]={'n':0,'mean':None};continue
            if isinstance(values[0],bool):
                count=sum(values);metrics[k]={'n':len(values),'count':count,'mean':count/len(values),'wilson95':wilson(count,len(values))}
            elif isinstance(values[0],(int,float)):
                a=np.array(values,float);metrics[k]={'n':len(a),'mean':float(a.mean()),'sd':float(a.std(ddof=1)) if len(a)>1 else 0.,'min':float(a.min()),'max':float(a.max())}
        out.append({**fixed,'runs':n,'metrics':metrics})
    return out

def paired(rows):
    """Seed-paired descriptive bootstrap; no multiplicity-adjusted superiority claims."""
    groups=defaultdict(dict)
    for r in rows:
        key=tuple((k,r[k]) for k in ('study','scenario','design','policy','audit_fraction','repeats') if k in r)
        groups[key].setdefault(r['variant'],{})[r['seed']]=r
    out=[]
    for key,variants in groups.items():
        st=dict(key)['study'];reference={'G':'assume_unbiased','H':'local_t_bonferroni','I':'pooled_base'}[st]
        fields={'G':['joint_truth_in_set','theta0_width'],'H':['alarm'],'I':['rmse','nll','latent_coverage','observed_width']}[st]
        for name,values in variants.items():
            if name==reference:continue
            for metric in fields:
                differences=[]
                for seed,r in sorted(values.items()):
                    ref=variants[reference][seed]
                    if r.get(metric) is not None and ref.get(metric) is not None:differences.append(float(r[metric])-float(ref[metric]))
                if not differences:continue
                a=np.array(differences);rr=rng('paired-v140',key,name,metric)
                boot=a[rr.integers(0,len(a),(2000,len(a)))].mean(1)
                out.append({**dict(key),'variant':name,'reference':reference,'metric':metric,'n':len(a),
                      'mean_difference':float(a.mean()),'descriptive_bootstrap95':np.quantile(boot,[.025,.975]).tolist()})
    return out

def prepare(out:Path):
    out=Path(out)
    if out.exists():raise FileExistsError('Choose a fresh study directory')
    out.mkdir(parents=True);config=read_json(CONFIG_PATH);source=sources()
    development=[]
    for s in partial.SCENARIOS:
        for d in partial.DESIGNS:development.append(job(dict(study='G',bank='development-v140',scenario=s,seed=17,design=d)))
    for s in audit.SCENARIOS:
        for p in audit.POLICIES:development.append(job(dict(study='H',bank='development-v140',scenario=s,seed=17,policy=p,fraction=.5)))
    for s in replicates.SCENARIOS:
        for r in replicates.REPLICATION:development.append(job(dict(study='I',bank='development-v140',scenario=s,seed=17,repeats=r)))
    for r in development:validate(r)
    write_json(out/'development.json',development)
    plan=jobs(config);write_json(out/'plan.json',plan)
    lock=dict(version=VERSION,research_date='2026-09-23',recorded_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
        config=config,source_sha256=source,plan_digest=digest(plan),development_digest=digest(development),
        development_runs=len(development),evaluation_runs=len(plan),
        limitations='Local prospective freeze; not independent preregistration, not a blind bank. Families known to developer.')
    write_json(out/'protocol.lock.json',lock)
    write_json(out/'environment.json',dict(python=sys.version,platform=platform.platform(),numpy=np.__version__,scipy=scipy.__version__))
    return lock

def verify_lock(out:Path):
    lock=read_json(Path(out)/'protocol.lock.json')
    if lock['source_sha256']!=sources():raise RuntimeError('Numerical source/config differs from the local freeze')
    if digest(read_json(Path(out)/'plan.json'))!=lock['plan_digest']:raise RuntimeError('Plan changed')
    if digest(read_json(Path(out)/'development.json'))!=lock['development_digest']:raise RuntimeError('Development record changed')
    return lock

def evaluate(out:Path,workers:int=2):
    out=Path(out);lock=verify_lock(out)
    if (out/'evaluation.started.json').exists():raise FileExistsError('Evaluation already started; preserve it and choose another path/bank')
    if not 1<=workers<=8:raise ValueError('workers must be 1..8')
    write_json(out/'evaluation.started.json',{'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'source_digest':digest(lock['source_sha256'])})
    plan=read_json(out/'plan.json');(out/'raw').mkdir();(out/'traces').mkdir()
    handles={s:gzip.open(out/f'raw/{s}.jsonl.gz','wt',encoding='utf-8',compresslevel=6) for s in 'GHI'}
    rows=[];nobs=0;digests=[];count=defaultdict(int);start=time.monotonic()
    try:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            for i,r in enumerate(pool.map(job,plan,chunksize=8)):
                nobs+=validate(r);count[r['study']]+=1;digests.append(r['record_digest']);rows.extend(row_records(r))
                handles[r['study']].write(json.dumps(r,separators=(',',':'),ensure_ascii=False,allow_nan=False)+'\n')
                if r['seed']==lock['config']['seed_start']:
                    label=r.get('design') or (r.get('policy','')+'_'+str(r.get('audit_fraction'))) if r['study']!='I' else f"r{r['repeats']}"
                    write_json(out/'traces'/f"{r['study']}_{r['scenario']}_{label}.json",r)
                if (i+1)%250==0:print(f"Completed {i+1}/{len(plan)}",flush=True)
    except Exception as e:
        write_json(out/'evaluation.failed.json',{'type':type(e).__name__,'message':str(e),'completed':dict(count)})
        raise
    finally:
        for h in handles.values():h.close()
    verify_lock(out)
    write_json(out/'records.json',rows);write_json(out/'summary.json',summarize(rows));write_json(out/'paired.json',paired(rows))
    report={'version':VERSION,'runs':dict(count),'total_runs':sum(count.values()),'serialized_observations':nobs,
         'I_final_estimators':count['I']*5,'I_parametric_bootstrap_fits':count['I']*lock['config']['I']['bootstrap'],
         'real_biological_observations':0,'representative_runs':len(list((out/'traces').glob('*.json'))),
         'raw_digest_sequence':digest(digests),'wall_seconds':time.monotonic()-start}
    write_json(out/'evaluation.complete.json',report);return report
