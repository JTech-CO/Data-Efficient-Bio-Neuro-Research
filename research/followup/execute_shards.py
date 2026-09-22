"""Resumable process-level execution of the unchanged locked v1.2 protocol.

This file orchestrates independent cells only. It changes no simulator, model,
policy, threshold, metric or world. Incomplete gzip files are archived; a cell
is deterministically recomputed, not selected by its result. No automatic
changes to the code/config seal are permitted.
"""
from __future__ import annotations
import argparse, gzip, json, os, sys, hashlib
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from research.diagnostic_loop.study import verify_lock, write_json, compact_result, summarize
from research.diagnostic_loop.runner import run_world
from research.diagnostic_loop.worlds import make_world

def read_gz(path):
    if not path.exists(): return None
    try:
        with gzip.open(path,'rt',encoding='utf-8') as f: return [json.loads(line) for line in f]
    except (EOFError,OSError,json.JSONDecodeError): return None

def worker(job):
    out,scenario,policy=job;out=Path(out);seal=verify_lock(out);c=seal['config']
    path=out/'raw'/f'acquisition-{scenario}-{policy}.jsonl.gz'
    tmp=path.with_name(path.name+'.tmp')
    with gzip.open(tmp,'wt',encoding='utf-8') as f:
        for i in range(c['acquisition_worlds_per_scenario']):
            r=run_world(make_world('evaluation',scenario,c['acquisition_index_offset']+i),policy,
                        seal['thresholds'][c['live_policy_detector']],fit_budget=c['fit_budget'],looks=c['looks'])
            f.write(json.dumps(r,ensure_ascii=False,allow_nan=False,separators=(',',':'))+'\n')
            if i==0:write_json(out/'traces'/f'{scenario}--{policy}.json',r)
    os.replace(tmp,path)
    return scenario,policy

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--workers',type=int,default=4)
    args=p.parse_args();out=args.out.resolve();seal=verify_lock(out);c=seal['config'];jobs=[];archived=[]
    if (out/'evaluation.completed.json').exists():raise SystemExit('Already completed; no reevaluation.')
    for scenario in c['scenarios']:
        path=out/'raw'/f'detection-{scenario}.jsonl.gz';r=read_gz(path)
        n=c['normal_detection_worlds'] if scenario=='normal' else c['fault_detection_worlds_per_scenario']
        if r is None or len(r)!=n:raise RuntimeError('Detection stage incomplete; not resumed by this acquisition-only wrapper')
    for scenario in c['scenarios']:
        for policy in c['policies']:
            path=out/'raw'/f'acquisition-{scenario}-{policy}.jsonl.gz';r=read_gz(path)
            expected={c['acquisition_index_offset']+i for i in range(c['acquisition_worlds_per_scenario'])}
            if r is not None and {q['world']['index'] for q in r}==expected:continue
            if path.exists():
                archive=out/'execution_interruptions'/path.name;archive.parent.mkdir(exist_ok=True)
                archived.append({'path':str(archive.relative_to(out)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
                os.replace(path,archive)
            jobs.append((str(out),scenario,policy))
    write_json(out/'execution.resume.json',{'reason':'container per-call wall-time limit interrupted sequential driver',
        'protocol_unchanged':True,'started_at_utc':datetime.now(timezone.utc).isoformat(),
        'reused_complete_cells':len(c['scenarios'])*len(c['policies'])-len(jobs),'scheduled_cells':len(jobs),'archived_partial_files':archived})
    print('Remaining cells:',len(jobs),flush=True)
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        fs=[ex.submit(worker,j) for j in jobs]
        for future in as_completed(fs):print('Completed:',future.result(),flush=True)
    detection=[];acquisition=[]
    for scenario in c['scenarios']:
        for t in read_gz(out/'raw'/f'detection-{scenario}.jsonl.gz'):
            detection.append({'world':t['world'],'detectors':t['detectors'],'score':t['score']})
        for policy in c['policies']:
            acquisition.extend(compact_result(r) for r in read_gz(out/'raw'/f'acquisition-{scenario}-{policy}.jsonl.gz'))
    verify_lock(out)
    write_json(out/'detection_records.json',detection);write_json(out/'acquisition_records.json',acquisition)
    write_json(out/'summary.json',summarize(detection,acquisition,c))
    write_json(out/'evaluation.completed.json',{'completed_at_utc':datetime.now(timezone.utc).isoformat(),
        'n_detection_trajectories':len(detection),'n_acquisition_trajectories':len(acquisition),
        'all_configured_cells_present':True,'code_unchanged':True,'executor':'resumable_process_shards'})
    print('All completed:',len(detection),len(acquisition),flush=True)
if __name__=='__main__':main()
