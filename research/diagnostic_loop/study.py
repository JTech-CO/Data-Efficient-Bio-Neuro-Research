"""Development -> null calibration -> sealed evaluation -> descriptive summaries.

The seal is a local reproducibility record, not independent preregistration,
external blinding or a cryptographically protected experimental service.
"""
from __future__ import annotations
from pathlib import Path
import gzip, json, hashlib, math, platform, sys
from collections import defaultdict
from datetime import datetime, timezone
import numpy as np
from scipy.stats import norm
from .contracts import Ledger, digest
from .worlds import make_world, SCENARIOS, rng_for
from .diagnostics import audit_panel, diagnose, alarm_summary, trajectory_score, empirical_threshold, CHANNELS, PANEL_COST
from .runner import run_world

ROOT=Path(__file__).resolve().parents[2]
CONFIG=ROOT/'research/configs/followup_v120.json'


def write_json(path,obj):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,allow_nan=False,indent=2)+'\n',encoding='utf-8')


def fingerprint(config):
    paths=sorted((ROOT/'research/diagnostic_loop').glob('*.py'))+[ROOT/'research/closed_loop/contracts.py']
    return {'config':digest(config),'sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}


def diagnostic_trajectory(world,looks=3):
    ledger=Ledger(); history=[]
    for _ in range(looks):
        for a in audit_panel(): world.observe(a,'audit',ledger)
        history.append(diagnose(ledger.view('audit'),world.public))
    return {'world':world.truth_record(),'history':history,'score':trajectory_score(history),
            'observations':ledger.export(),'costs':ledger.counts()}


def prepare(out,config=None):
    out=Path(out); config=json.loads(CONFIG.read_text()) if config is None else config
    if out.exists() and any(out.iterdir()): raise FileExistsError('prepare requires a new empty directory')
    out.mkdir(parents=True,exist_ok=True)
    write_json(out/'config.json',config)
    # Development fixtures are deliberately a separate basis and namespace.
    dev=[]
    for scenario in config['scenarios']:
        for i in range(config['development_worlds_per_scenario']):
            w=make_world('development',scenario,i)
            r=run_world(w,'block_targeted',config['alpha']/(len(CHANNELS)*len(config['looks'])),
                        fit_budget=config['fit_budget'],looks=config['looks'],keep_raw=False)
            dev.append({'world':r['world'],'diagnosis':r['diagnosis'],
                        'latent':r['evaluation']['estimators']['propagated']['latent']})
    write_json(out/'development.json',dev)
    cal=[]
    for i in range(config['calibration_worlds']):
        t=diagnostic_trajectory(make_world('calibration','normal',i),len(config['looks']))
        cal.append({'world_id':t['world']['identity'],'score':t['score']})
    thresholds={'naive':config['alpha'],'bonferroni':config['alpha']/(len(CHANNELS)*len(config['looks']))}
    empirical=empirical_threshold([v['score'] for v in cal],config['alpha'])
    thresholds['calibrated_max']=empirical['p_threshold']
    write_json(out/'calibration.json',{'scores':cal,'order_statistic':empirical,'thresholds':thresholds})
    seal={'created_at_utc':datetime.now(timezone.utc).isoformat(),
          'status':'local-protocol-lock-before-evaluation-not-independent-preregistration',
          'fingerprint':fingerprint(config), 'config':config,
          'calibration_sha256':hashlib.sha256((out/'calibration.json').read_bytes()).hexdigest(),
          'thresholds':thresholds,'n_development':len(dev),'n_calibration':len(cal),
          'truth_namespace_disjoint':True,'basis_supplied_to_model':True,
          'python':sys.version,'numpy':np.__version__,'platform':platform.platform()}
    write_json(out/'protocol.lock.json',seal)
    return seal


def verify_lock(out):
    out=Path(out); seal=json.loads((out/'protocol.lock.json').read_text())
    if fingerprint(seal['config'])!=seal['fingerprint']: raise RuntimeError('source/config changed after lock; create a new version/bank')
    if hashlib.sha256((out/'calibration.json').read_bytes()).hexdigest()!=seal['calibration_sha256']:
        raise RuntimeError('calibration changed after lock')
    return seal


def compact_result(r):
    return {k:r[k] for k in ('version','world','policy','threshold','final_model','diagnosis','costs','first_alarm_look','result_status')} | {
        'estimators':r['evaluation']['estimators'],'prefix':r['evaluation']['frozen_prefix_evaluations']}


def evaluate(out):
    out=Path(out); seal=verify_lock(out); c=seal['config']
    if (out/'evaluation.started.json').exists():
        raise FileExistsError('evaluation already started; do not silently rerun or overwrite a locked bank')
    write_json(out/'evaluation.started.json',{'started_at_utc':datetime.now(timezone.utc).isoformat(),'protocol_digest':digest(seal)})
    thresholds=seal['thresholds']; detection=[]; acquisition=[]
    raw=out/'raw'; raw.mkdir()
    # All detectors see the same predeclared audit observations.
    for scenario in c['scenarios']:
        n=c['normal_detection_worlds'] if scenario=='normal' else c['fault_detection_worlds_per_scenario']
        with gzip.open(raw/f'detection-{scenario}.jsonl.gz','wt',encoding='utf-8') as f:
            for i in range(n):
                t=diagnostic_trajectory(make_world('evaluation',scenario,c['detection_index_offset']+i),len(c['looks']))
                t['detectors']={k:alarm_summary(t['history'],thresholds[k]) for k in c['detectors']}
                f.write(json.dumps(t,ensure_ascii=False,allow_nan=False,separators=(',',':'))+'\n')
                detection.append({'world':t['world'],'detectors':t['detectors'],'score':t['score']})
        print(f'detection {scenario}: {n}',flush=True)
    for scenario in c['scenarios']:
        for policy in c['policies']:
            with gzip.open(raw/f'acquisition-{scenario}-{policy}.jsonl.gz','wt',encoding='utf-8') as f:
                for i in range(c['acquisition_worlds_per_scenario']):
                    r=run_world(make_world('evaluation',scenario,c['acquisition_index_offset']+i),policy,thresholds[c['live_policy_detector']],
                                fit_budget=c['fit_budget'],looks=c['looks'])
                    f.write(json.dumps(r,ensure_ascii=False,allow_nan=False,separators=(',',':'))+'\n')
                    acquisition.append(compact_result(r))
                    if i==0:
                        write_json(out/'traces'/f'{scenario}--{policy}.json',r)
            print(f'acquisition {scenario}/{policy}: {c["acquisition_worlds_per_scenario"]}',flush=True)
    write_json(out/'detection_records.json',detection)
    write_json(out/'acquisition_records.json',acquisition)
    summary=summarize(detection,acquisition,c)
    write_json(out/'summary.json',summary)
    write_json(out/'evaluation.completed.json',{'completed_at_utc':datetime.now(timezone.utc).isoformat(),
        'n_detection_trajectories':len(detection),'n_acquisition_trajectories':len(acquisition),
        'all_configured_cells_present':True,'code_unchanged':fingerprint(c)==seal['fingerprint']})
    return summary


def wilson(success,n):
    if not n: return None
    z=1.959963984540054; p=success/n; den=1+z*z/n
    mid=(p+z*z/(2*n))/den; delta=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [max(0.,mid-delta),min(1.,mid+delta)]


def paired_bootstrap(values,seed_tag):
    a=np.asarray(values,float)
    rng=rng_for('descriptive-world-bootstrap',seed_tag)
    draws=np.mean(a[rng.integers(0,len(a),size=(2000,len(a)))],axis=1)
    return {'mean_difference':float(a.mean()),'descriptive_95_interval':np.quantile(draws,[.025,.975]).tolist(),
            'n_world_pairs':len(a),'not_adjusted_for_multiple_comparisons':True}


def summarize(detection,acquisition,config):
    ds=[]
    for scenario in config['scenarios']:
        rr=[r for r in detection if r['world']['scenario']==scenario]
        for det in config['detectors']:
            dd=[r['detectors'][det] for r in rr]; n=len(dd)
            n_any=sum(d['any_alarm'] for d in dd)
            first=[min(v for v in d['first_look'].values() if v is not None) for d in dd if d['any_alarm']]
            flags={k:sum(d['flags'][k] for d in dd) for k in CHANNELS}
            channel_types={'sensor':'sensor_affine','mechanism':'mechanism_lack_of_fit','noise':'noise_overdispersion'}
            exact=0; type_hits=defaultdict(int)
            for r,d in zip(rr,dd):
                predicted={'sensor':d['flags']['sensor_affine'] or d['flags']['sensor_nonlinear'],
                           'mechanism':d['flags']['mechanism_lack_of_fit'],'noise':d['flags']['noise_overdispersion']}
                # Label agreement is a synthetic scoring aid, not source proof.
                exact+=predicted==r['world']['fault_tags']
                for k in predicted:
                    type_hits[k]+=predicted[k] and r['world']['fault_tags'][k]
            ds.append({'scenario':scenario,'detector':det,'n_worlds':n,'any_alarm_count':n_any,
                       'any_alarm_rate':n_any/n,'any_alarm_wilson_95':wilson(n_any,n),
                       'miss_rate_if_fault':1-n_any/n if scenario!='normal' else None,
                       'channel_flag_counts':flags,'exact_tag_agreement_count':exact,
                       'exact_tag_agreement_rate':exact/n,'target_tag_hit_counts':dict(type_hits),
                       'mean_first_look_among_detected':float(np.mean(first)) if first else None,
                       'restricted_mean_look_undetected_as_L_plus_1':float(np.mean(first+[len(config['looks'])+1]*(n-len(first))))})
    ac=[]
    for scenario in config['scenarios']:
        for policy in config['policies']:
            rr=[r for r in acquisition if r['world']['scenario']==scenario and r['policy']==policy]
            estimates={}
            for estimator in rr[0]['estimators']:
                mm=[r['estimators'][estimator]['latent'] for r in rr]
                estimates[estimator]={k:{'mean':float(np.mean([v[k] for v in mm])),
                                          'sd_world':float(np.std([v[k] for v in mm],ddof=1))} for k in mm[0]}
            costs={k:float(np.mean([r['costs'][k] for r in rr])) for k in ('fit_cost','audit_cost','acquisition_cost','test_cost','all_measurement_cost')}
            alarm=[r['diagnosis']['any_alarm'] for r in rr if r['diagnosis']['any_alarm'] is not None]
            pe=[r['estimators']['propagated']['latent'] for r in rr]
            ac.append({'scenario':scenario,'policy':policy,'n_worlds':len(rr),'estimators':estimates,'mean_costs':costs,
                       'full_data_rank_rate':float(np.mean([r['final_model']['rank']==5 for r in rr])),
                       'alarm_rate':float(np.mean(alarm)) if alarm else None,
                       'rmse_le_012_rate':float(np.mean([m['rmse']<=.12 for m in pe])),
                       'composite_development_target_rate':float(np.mean([m['rmse']<=.12 and m['coverage_95']>=.8 and m['width_95']<=.8 for m in pe]))})
    pairs=[]
    for scenario in config['scenarios']:
        rr=[r for r in acquisition if r['world']['scenario']==scenario]
        refs={r['world']['index']:r for r in rr if r['policy']=='reference_first'}
        for policy in ('block_targeted','joint_information','no_reference','reference_first_no_audit'):
            diff=[r['estimators']['propagated']['latent']['rmse']-refs[r['world']['index']]['estimators']['propagated']['latent']['rmse'] for r in rr if r['policy']==policy]
            pairs.append({'scenario':scenario,'policy':policy,'reference':'reference_first',**paired_bootstrap(diff,scenario+policy)})
    stop=[]
    for policy in config['policies']:
        if policy=='reference_first_no_audit': continue
        for scenario in config['scenarios']:
            rr=[r for r in acquisition if r['world']['scenario']==scenario and r['policy']==policy]
            mm=[]; spent=[]; stopped=0
            for r in rr:
                look=r['first_alarm_look']; key=f'look_{look}' if look is not None else 'final'
                p=r['prefix'][key]; mm.append(p['latent']['rmse']); spent.append(p['fit_cost']+p['audit_cost']); stopped+=look is not None
            stop.append({'scenario':scenario,'policy':policy,'n':len(rr),'would_stop':stopped,
                         'frozen_stop_rmse_mean':float(np.mean(mm)),'spent_until_stop_mean':float(np.mean(spent)),
                         'full_budget_rmse_mean':float(np.mean([r['estimators']['propagated']['latent']['rmse'] for r in rr])),
                         'not_evidence_of_success_cost_reduction':True})
    return {'scope':'synthetic-only locked-bank developmental evaluation','n_biological_units':0,
            'n_detection_trajectories':len(detection),'n_acquisition_trajectories':len(acquisition),
            'n_calibration_trajectories':config['calibration_worlds'],'detection':ds,'acquisition':ac,'paired_rmse':pairs,
            'counterfactual_stop':stop,'panel_cost':PANEL_COST,'config':config}
