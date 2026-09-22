"""Verify every completed raw run; replay fixed records without policy retuning."""
from pathlib import Path
import sys,json,gzip,math,hashlib
from collections import Counter
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import numpy as np
from jsonschema import Draft202012Validator
from research.diagnostic_loop.contracts import Observation,Action,Ledger,digest,AuditTrail
from research.diagnostic_loop.worlds import make_world
from research.diagnostic_loop.runner import run_world
from research.diagnostic_loop.study import verify_lock,summarize,diagnostic_trajectory,compact_result,write_json
from research.diagnostic_loop.diagnostics import alarm_summary

def check(cond,msg):
 if not cond:raise AssertionError(msg)

def validate(out):
 out=Path(out);seal=verify_lock(out);c=seal['config'];schema=json.loads((ROOT/'research/followup/schemas/run.schema.json').read_text());validator=Draft202012Validator(schema)
 counts=Counter();detection=[];acquisition=[];worldsA=set();worldsB=set();split_ids={k:set() for k in ['fit','audit','test']}; cells=Counter();sample_runs=[]
 def observations(rr):
  led=Ledger()
  for o in rr:
   kw={k:o[k] for k in ['record_id','value','split','replicate_index','parent_id','origin','real_world_authorized']}
   v=Observation(action=Action(**o['action']),**kw);check(not o['counts_as_new_biological_unit'],'biological unit claim')
   check(abs(o['cost']-v.cost)<1e-10,'unit cost');led.append(v);split_ids[o['split']].add(o['record_id']);counts['observation_records_checked']+=1
  return led
 for p in sorted((out/'raw').glob('*.jsonl.gz')):
  with gzip.open(p,'rt',encoding='utf-8') as f:
   for line in f:
    r=json.loads(line);led=observations(r['observations'])
    for k,v in led.counts().items():
     got=r['costs'][k];check(math.isclose(v,got,abs_tol=1e-8) if isinstance(v,(int,float)) else v==got,'ledger totals')
    sc=r['world']['scenario'];idx=r['world']['index']
    if p.name.startswith('detection-'):
     check(len(led.view('audit'))==54 and not led.view('fit') and not led.view('test'),'detector split')
     for d in c['detectors']:check(r['detectors'][d]==alarm_summary(r['history'],seal['thresholds'][d]),'detector recomputation')
     detection.append({k:r[k] for k in ['world','detectors','score']});worldsA.add(r['world']['identity']);counts['detection_trajectories']+=1
     if idx==c['detection_index_offset']:
      fresh=diagnostic_trajectory(make_world('evaluation',sc,idx),len(c['looks']));check(digest(fresh['history'])==digest(r['history']),'detector replay');counts['detector_replays']+=1
    else:
     validator.validate(r);policy=r['policy'];cells[(sc,policy)]+=1
     check(AuditTrail.verify(r['events']),'event chain');check(r['evaluation']['freeze_digest']==digest(r['snapshots']),'freeze record')
     types=[e['type'] for e in r['events']];check(types.count('freeze')==1 and types.count('final_test')==1 and types.index('freeze')<types.index('final_test')==len(types)-1,'final ordering')
     check(all(e['payload'].get('real_world_authorized') is False for e in r['events'] if e['type']=='approve'),'real approval')
     check(len(led.view('test'))==82,'test panel');check(r['costs']['acquisition_cost']<=113.4+1e-8,'cap exceeded')
     check(len(led.view('audit'))==(0 if policy=='reference_first_no_audit' else 54),'audit panel')
     check(r['diagnosis']['any_alarm'] is None if policy=='reference_first_no_audit' else r['diagnosis']==alarm_summary(r['audit_history'],r['threshold']),'diagnostic role')
     if policy=='no_reference':check(not any(o.action.kind=='reference' for o in led.view('fit')) and r['final_model']['rank']<5,'ablation leak')
     check(r['threshold']==seal['thresholds'][c['live_policy_detector']],'threshold mismatch')
     acquisition.append(compact_result(r));worldsB.add(r['world']['identity']);counts['acquisition_runs']+=1
     if idx==c['acquisition_index_offset']:sample_runs.append(r)
 check(counts['detection_trajectories']==1900 and counts['acquisition_runs']==1920,'incomplete design')
 check(len(cells)==60 and set(cells.values())=={32},'missing cells');check(len(worldsA)==1900 and len(worldsB)==320,'world counts');check(not worldsA&worldsB,'world leakage')
 check(all(not split_ids[a]&split_ids[b] for a,b in [('fit','audit'),('audit','test'),('fit','test')]),'split overlap')
 # Aggregate order matches the fixed design order to avoid floating summation drift.
 keyA=lambda r:(c['scenarios'].index(r['world']['scenario']),r['world']['index'])
 keyB=lambda r:(c['scenarios'].index(r['world']['scenario']),c['policies'].index(r['policy']),r['world']['index'])
 detection.sort(key=keyA);acquisition.sort(key=keyB)
 check(digest(detection)==digest(json.loads((out/'detection_records.json').read_text())),'compact diagnostic records')
 check(digest(acquisition)==digest(json.loads((out/'acquisition_records.json').read_text())),'compact acquisition records')
 check(digest(summarize(detection,acquisition,c))==digest(json.loads((out/'summary.json').read_text())),'summary recalculation')
 for old in sample_runs:
  fresh=run_world(make_world('evaluation',old['world']['scenario'],old['world']['index']),old['policy'],old['threshold'],fit_budget=c['fit_budget'],looks=c['looks'])
  check(digest(fresh)==digest(old),'full replay mismatch');counts['acquisition_replays']+=1
 counts.update(unique_diagnostic_worlds=len(worldsA),unique_acquisition_worlds=len(worldsB),acquisition_cells=len(cells),diagnostic_summary_cells=30)
 result={'status':'passed','counts':dict(counts),'all_run_schema_valid':True,'all_ledger_costs_recomputed':True,'event_chains_verified':True,'sequential_test_roles_verified':True,'summary_exactly_recomputed':True,'locked_code_unchanged':True,'scientific_validity_or_security_certification':False}
 write_json(ROOT/'research/followup/quality/validation.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':validate(sys.argv[1] if len(sys.argv)>1 else ROOT/'research/followup/results/v120')
