"""Reproducible run/benchmark artifact generation."""
from __future__ import annotations
from collections import defaultdict
from dataclasses import replace
import hashlib, json, platform, sys, time
from pathlib import Path
import numpy as np
import scipy
from . import __version__
from .contracts import RunConfig
from .simulator import SyntheticOracle
from .engine import execute
from .evaluation import evaluate

ROOT=Path(__file__).resolve().parents[1]

def run_experiment(config: RunConfig, full_curves: bool=True) -> dict:
    oracle=SyntheticOracle(config.scenario,config.seed)
    result=execute(config,oracle.measure)
    # By construction no offline evaluation can influence the acquisition history.
    result['evaluation']=evaluate(result,oracle,full_curves)
    result['software']={'version':__version__,'numpy':np.__version__,'scipy':scipy.__version__,'python':platform.python_version()}
    return result

def save_json(path, payload, overwrite=False):
    path=Path(path)
    if path.exists() and not overwrite: raise FileExistsError(f'{path} already exists; choose a new path or --overwrite')
    path.parent.mkdir(parents=True,exist_ok=True)
    data=json.dumps(payload,ensure_ascii=False,indent=2,allow_nan=False)+'\n'
    temp=path.with_suffix(path.suffix+'.tmp');temp.write_text(data,encoding='utf-8');temp.replace(path)

def compact(run,track='main'):
    final=run['evaluation']['final']
    return {'track':track,'scenario':run['config']['scenario'],'policy':run['config']['policy'],
            'observer':run['config']['observer'],'seed':run['config']['seed'],
            'budget':run['config']['budget'],'cost':run['total_cost'],
            'acquisition_sha256':run['acquisition_sha256'],'gate_suspect':run['gate']['suspect'],
            'stop_reason':run['stop_reason'],'information_budget':run['information_budget'],
            'truth':run['evaluation']['truth'],'final':final,'curves':run['evaluation']['curves']}

def summarize(records):
    groups=defaultdict(list)
    for r in records: groups[(r['track'],r['scenario'],r['policy'],r['observer'])].append(r)
    summary=[]
    for (track,scenario,policy,observer),rows in groups.items():
        def avg(fn):return float(np.mean([fn(r) for r in rows]))
        summary.append({'track':track,'scenario':scenario,'policy':policy,'observer':observer,'n_simulated_worlds':len(rows),
                        'id_rmse':avg(lambda r:r['final']['id']['rmse']),
                        'ood_rmse':avg(lambda r:r['final']['ood']['rmse']),
                        'observation_95_coverage':avg(lambda r:r['final']['id']['observation_95_coverage']),
                        'observation_95_width':avg(lambda r:r['final']['id']['observation_95_width']),
                        'latent_95_coverage':avg(lambda r:r['final']['id']['latent_95_coverage']),
                        'nll':avg(lambda r:r['final']['id']['nll']),
                        'cost':avg(lambda r:r['cost']),
                        'audit_calls':avg(lambda r:r['information_budget']['audit_measurements']),
                        'abstention_rate':avg(lambda r:r['final']['abstained']),
                        'false_candidate_assertion_rate':avg(lambda r:r['final']['false_candidate_assertion']),
                        'alert_rate':avg(lambda r:r['gate_suspect']),
                        'target_reached_rate':avg(lambda r:r['final']['target_reached']),
                        'candidate_correct_rate':None if scenario=='hidden_mechanism' else avg(lambda r:r['final']['candidate_correct'])})
    # Seed-paired bootstrap differences at the same allowed budget, not necessarily same spend.
    paired=[]; rng=np.random.default_rng(20260922)
    base={(r['scenario'],r['seed']):r for r in records if r['track']=='main' and r['policy']=='random'}
    for group in summary:
        if group['track']!='main' or group['policy']=='random':continue
        rows=groups[(group['track'],group['scenario'],group['policy'],group['observer'])]
        for field in ('rmse','observation_95_coverage','observation_95_width'):
            delta=np.array([r['final']['id'][field]-base[(r['scenario'],r['seed'])]['final']['id'][field] for r in rows])
            samples=delta[rng.integers(0,len(delta),size=(2000,len(delta)))].mean(axis=1)
            paired.append({'scenario':group['scenario'],'policy':group['policy'],'against':'random','metric':field,
                           'mean_paired_difference':float(delta.mean()),
                           'bootstrap_95_percentile_interval':np.quantile(samples,[.025,.975]).tolist(),
                           'paired_seeds':len(delta),'resamples':2000,
                           'scope':'synthetic-world Monte Carlo variation; not biological confidence or multiplicity-adjusted inference'})
    return summary,paired

def benchmark(plan_path, out, seed_count=None, overwrite=False):
    plan_path=Path(plan_path);plan=json.loads(plan_path.read_text(encoding='utf-8'))
    out=Path(out)
    if out.exists() and any(out.iterdir()) and not overwrite:
        raise FileExistsError(f'{out} is not empty; choose a fresh output or --overwrite')
    out.mkdir(parents=True,exist_ok=True)
    seeds=plan['seeds'] if seed_count is None else plan['seeds'][:seed_count]
    if not seeds: raise ValueError('At least one seed is required')
    keys=('budget','audit_every','audit_z','audit_hits','audit_window','exploration_every','parameter_weight','decision_threshold','quadrature_nodes')
    kw={k:plan[k] for k in keys}
    jobs=[]
    for scenario in plan['scenarios']:
        for policy in plan['policies']:
            for seed in seeds:jobs.append(('main',RunConfig(scenario=scenario,policy=policy,seed=seed,**kw)))
    for scenario in plan['ablations']['scenarios']:
        for policy in plan['ablations']['policies']:
            for seed in seeds: jobs.append(('ablation',RunConfig(scenario=scenario,policy=policy,seed=seed,**kw)))
    for seed in seeds:
        jobs.append(('ablation',RunConfig(scenario=plan['ablations']['identity_observer_scenario'],observer='identity',seed=seed,**kw)))
    start=time.perf_counter();records=[];demos=[]
    raw_path=out/'runs.jsonl'
    with raw_path.open('w',encoding='utf-8') as stream:
        for i,(track,cfg) in enumerate(jobs):
            run=run_experiment(cfg);row=compact(run,track);records.append(row)
            stream.write(json.dumps(row,ensure_ascii=False,allow_nan=False)+'\n');stream.flush()
            if cfg.seed==seeds[0] and track=='main':demos.append(run)
            if (i+1)%40==0 or i+1==len(jobs):print(f'{i+1}/{len(jobs)} completed',flush=True)
    summary,paired=summarize(records)
    artifact={'experiment_id':plan['experiment_id'],'research_only':True,'runs':len(records),'seeds':seeds,
              'summary':summary,'paired_comparisons':paired,
              'plan_sha256':hashlib.sha256(plan_path.read_bytes()).hexdigest(),
              'interpretation':'Descriptive synthetic pilot; no biological data, external preregistration, or superiority claim.'}
    save_json(out/'summary.json',artifact,True)
    save_json(out/'demos.json',demos,True)
    save_json(out/'execution.json',{'duration_seconds':time.perf_counter()-start,'runs':len(records),'python':sys.version,
                                  'platform':platform.platform(),'numpy':np.__version__,'scipy':scipy.__version__,
                                  'command_plan':str(plan_path.relative_to(ROOT)) if plan_path.is_relative_to(ROOT) else str(plan_path),
                                  'evaluation_after_each_completed_acquisition_run':True,'biological_units':0},True)
    return artifact,demos
