"""Versioned protocol, evaluation, all-cell summaries and paired contrasts."""
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ProcessPoolExecutor
from collections import defaultdict
import gzip, json, hashlib, platform, sys
import numpy as np
from . import transfer, spatial, noise
from .common import write_json, digest, validate_run, mean_sd, wilson, rng_for

ROOT=Path(__file__).resolve().parents[2]
DEFAULT=ROOT/'research/triad/configs/v130.json'


def fingerprint(config):
    paths=sorted((ROOT/'research/triad_loop').glob('*.py'))+[ROOT/'research/closed_loop/contracts.py']
    return {'config':digest(config),'sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}


def job(arg):
    study,args=arg
    if study=='D': return transfer.run(*args)
    if study=='E': return spatial.run(*args)
    if study=='F': return noise.run(*args)
    raise ValueError('Unknown workstream')


def compact(r):
    return {k:v for k,v in r.items() if k not in ('observations','events','curves','history','models','model','evaluator_truth')} | (
        {'model_status':r['model']['status'],'rank':r['model']['expanded_physical_rank'],
         'transfer_rejected':r['model']['transfer_rejected'],'transfer_scope':r['model']['transfer_scope'],
         'fit_p':r['model']['fit_p'],'orthogonal_p':r['model']['orthogonal_contradiction_p']} if r['study']=='D' else {})


def prepare(out, config=None):
    out=Path(out); c=json.loads(DEFAULT.read_text()) if config is None else config
    if out.exists() and any(out.iterdir()): raise FileExistsError('Use a new empty result folder')
    out.mkdir(parents=True,exist_ok=True)
    jobs=[]
    for scenario in ('normal','common_anchor_failure'):
        for protocol in transfer.PROTOCOLS: jobs.append(('D',('development-v130',scenario,7,protocol,c['D']['budget'])))
    for scenario in ('normal','narrow'):
        for policy in spatial.POLICIES: jobs.append(('E',('development-v130',scenario,7,policy,24,1)))
    for scenario in ('gaussian','student3'):
        for controller in noise.ESTIMATORS:
            for policy in noise.POLICIES: jobs.append(('F',('development-v130',scenario,7,controller,policy,c['F']['budget'])))
    dev=[]
    for j in jobs:
        r=job(j);validate_run(r);dev.append(compact(r))
    write_json(out/'development.json',dev);write_json(out/'config.json',c)
    seal={'created_utc':datetime.now(timezone.utc).isoformat(),'config':c,'fingerprint':fingerprint(c),
          'development_runs':len(dev),'development_digest':digest(dev),
          'status':'local reproducibility lock, not independent preregistration or external blinding',
          'thresholds':'D 0.025 lack-of-fit and anchor consistency, 0.05 transfer Wald; E alpha/N or alpha/[t(t+1)]',
          'environment':{'python':sys.version,'numpy':np.__version__,'platform':platform.platform()}}
    write_json(out/'protocol.lock.json',seal)
    return seal


def verify_lock(out):
    out=Path(out);s=json.loads((out/'protocol.lock.json').read_text())
    if s['fingerprint']!=fingerprint(s['config']): raise RuntimeError('Changed source/config: use a new version and bank')
    if digest(json.loads((out/'development.json').read_text()))!=s['development_digest']: raise RuntimeError('Changed development record')
    return s


def all_jobs(c):
    bank=c['evaluation_bank'];start=c['evaluation_seed_start'];jobs=[]
    for s in transfer.SCENARIOS:
        for p in transfer.PROTOCOLS:
            for i in range(c['D']['worlds_per_scenario']): jobs.append(('D',(bank,s,start+i,p,c['D']['budget'])))
    for s in spatial.SCENARIOS:
        n=c['E']['normal_worlds'] if s=='normal' else c['E']['other_worlds']
        for p in spatial.POLICIES:
            for budget,cost in c['E']['settings']:
                for i in range(n): jobs.append(('E',(bank,s,start+i,p,budget,cost)))
    for s in noise.SCENARIOS:
        for ctrl in noise.ESTIMATORS:
            for p in noise.POLICIES:
                for i in range(c['F']['worlds_per_scenario']): jobs.append(('F',(bank,s,start+i,ctrl,p,c['F']['budget'])))
    return jobs


def evaluate(out,workers=1):
    out=Path(out);seal=verify_lock(out);c=seal['config'];jobs=all_jobs(c)
    if (out/'evaluation.started.json').exists(): raise FileExistsError('Evaluation already started: never silently overwrite')
    write_json(out/'evaluation.started.json',{'utc':datetime.now(timezone.utc).isoformat(),'planned_runs':len(jobs),'protocol_digest':digest(seal)})
    raw=out/'raw';raw.mkdir();traces=out/'traces';traces.mkdir()
    handles={s:gzip.open(raw/f'{s}.jsonl.gz','wt',encoding='utf-8',compresslevel=6) for s in 'DEF'}
    records=[];seen=set();obs_count=0
    executor=ProcessPoolExecutor(max_workers=workers) if workers>1 else None
    results=executor.map(job,jobs,chunksize=12) if executor else map(job,jobs)
    try:
        for index,r in enumerate(results,1):
            obs_count+=validate_run(r)
            records.append(compact(r))
            name='--'.join(str(r.get(k,'')) for k in ('study','scenario','protocol','controller','policy','budget','control_cost'))
            if name not in seen:
                seen.add(name);write_json(traces/f'{name}.json',r)
            # Keep all observations, fits, events and outcomes; large plot arrays in traces only.
            rr={k:v for k,v in r.items() if k!='curves'}
            handles[r['study']].write(json.dumps(rr,ensure_ascii=False,allow_nan=False,separators=(',',':'))+'\n')
            if index%400==0 or index==len(jobs): print(f'{index}/{len(jobs)} runs; current study {r["study"]}',flush=True)
    finally:
        for f in handles.values(): f.close()
        if executor: executor.shutdown()
    write_json(out/'records.json',records)
    summary=summarize(records,c)
    write_json(out/'summary.json',summary)
    write_json(out/'paired_comparisons.json',paired(records))
    verify_lock(out)
    write_json(out/'evaluation.completed.json',{'utc':datetime.now(timezone.utc).isoformat(),'runs':len(records),
        'serialized_observations_checked':obs_count,'representative_traces':len(seen),
        'records_digest':digest(records),'summary_digest':digest(summary),'n_biological_observations':0})
    return summary


def rate(values):
    vals=[v for v in values if v is not None];n=len(vals);k=int(sum(vals))
    return {'k':k,'n':n,'rate':k/n if n else None,'wilson95':wilson(k,n)}


def summarize(records,c):
    D=defaultdict(list);E=defaultdict(list);F=defaultdict(list)
    for r in records:
        if r['study']=='D':D[(r['scenario'],r['protocol'])].append(r)
        if r['study']=='E':E[(r['scenario'],r['policy'],r['budget'],r['control_cost'])].append(r)
        if r['study']=='F':F[(r['scenario'],r['controller'],r['policy'])].append(r)
    d=[]
    for (s,p),rr in sorted(D.items()):
        d.append({'scenario':s,'protocol':p,'n':len(rr),'rank':rr[0]['rank'],
                  'conditional_identifiable':rate([v['model_status']=='identifiable-under-assumptions' for v in rr]),
                  'contradicted':rate([v['model_status']=='contradicted' for v in rr]),
                  'transfer_rejected':rate([v['transfer_rejected'] for v in rr]),
                  'metrics':{k:mean_sd([v['metrics'][k] for v in rr]) for k in rr[0]['metrics']},
                  'fit_cost':mean_sd([v['costs']['fit'] for v in rr]),'test_cost':mean_sd([v['costs']['test'] for v in rr])})
    e=[]
    for (s,p,b,cost),rr in sorted(E.items()):
        e.append({'scenario':s,'policy':p,'budget':b,'control_cost':cost,'n':len(rr),'n_pairs':rr[0]['n_pairs'],
                  'detection':{rule:{'alarm':rate([v['outcomes'][rule]['alarm'] for v in rr]),
                       'first_alarm_cost_detected_only':mean_sd([v['outcomes'][rule]['first_alarm_cost'] for v in rr]),
                       'restricted_detection_cost':mean_sd([v['outcomes'][rule]['restricted_detection_cost'] for v in rr])}
                        for rule in ('naive','bonferroni','spending')},
                  'hit_region':rate([v['metrics']['hit_one_width_region'] for v in rr]),
                  'covering_radius':mean_sd([v['metrics']['domain_covering_radius'] for v in rr]),
                  'audit_cost':mean_sd([v['costs']['audit'] for v in rr])})
    f=[]
    for (s,ctrl,p),rr in sorted(F.items()):
        for est in noise.ESTIMATORS:
            f.append({'scenario':s,'controller':ctrl,'policy':p,'estimator':est,'n':len(rr),
                      'metrics':{k:mean_sd([v['evaluation'][est][k] for v in rr]) for k in rr[0]['evaluation'][est]},
                      'fit_cost':mean_sd([v['costs']['fit'] for v in rr]),'test_cost':mean_sd([v['costs']['test'] for v in rr])})
    return {'version':'1.3.0-research.1','config':c,'D':d,'E':e,'F':f,
            'counts':{'D_runs':sum(map(len,D.values())),'E_runs':sum(map(len,E.values())),
                      'F_collection_runs':sum(map(len,F.values())),'F_final_fits':3*sum(map(len,F.values())),
                      'F_unique_datasets':len({r['data_digest'] for r in records if r['study']=='F'}),
                      'n_biological_observations':0}}


def bootstrap_delta(d,key):
    d=np.asarray(d,float);rng=rng_for('paired-bootstrap-v130',key)
    means=np.mean(d[rng.integers(0,len(d),(1000,len(d)))],axis=1)
    return {'n_worlds':len(d),'mean_delta':float(np.mean(d)),'descriptive95':np.quantile(means,[.025,.975]).tolist()}


def paired(records):
    rows=[r for r in records if r['study']=='F'];result=[]
    # Same dataset: estimator differences, never collected as independent evidence.
    for s in noise.SCENARIOS:
        for ctrl in noise.ESTIMATORS:
            for p in noise.POLICIES:
                rr=sorted([r for r in rows if r['scenario']==s and r['controller']==ctrl and r['policy']==p],key=lambda r:r['seed'])
                for est in ('logvar_gaussian','student_t'):
                    for metric in ('latent_rmse','predictive_nll','crps'):
                        d=[r['evaluation'][est][metric]-r['evaluation']['hom_gaussian'][metric] for r in rr]
                        key=(s,ctrl,p,est,metric)
                        result.append({'type':'same_dataset_estimator','scenario':s,'controller':ctrl,'policy':p,
                              'comparison':f'{est} minus hom_gaussian','metric':metric,**bootstrap_delta(d,key)})
        # Fixed controller and fixed final estimator: switch policy only.
        for ctrl in noise.ESTIMATORS:
            for est in noise.ESTIMATORS:
                groups={p:{r['seed']:r for r in rows if r['scenario']==s and r['controller']==ctrl and r['policy']==p} for p in noise.POLICIES}
                for baseline in ('random','spacefill'):
                    for metric in ('latent_rmse','predictive_nll','crps'):
                        seeds=sorted(groups['ivr'])
                        d=[groups['ivr'][i]['evaluation'][est][metric]-groups[baseline][i]['evaluation'][est][metric] for i in seeds]
                        key=(s,ctrl,est,baseline,metric)
                        result.append({'type':'fixed_estimator_policy','scenario':s,'controller':ctrl,'estimator':est,
                               'comparison':f'ivr minus {baseline}','metric':metric,**bootstrap_delta(d,key)})
    return {'interpretation':'paired synthetic-world bootstrap; descriptive; no multiple-comparison superiority test','comparisons':result}
