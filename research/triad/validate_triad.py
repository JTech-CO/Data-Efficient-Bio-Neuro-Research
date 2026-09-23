"""Recompute summaries, provenance checks, and every representative synthetic trace."""
from __future__ import annotations
import sys, json, gzip, hashlib, platform, importlib.metadata
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from research.triad.archive import iter_records
from research.triad_loop import transfer,spatial,noise
from research.triad_loop.common import validate_run,digest,write_json
from research.triad_loop.study import compact,summarize,paired,verify_lock

BASE=ROOT/'research/triad/results/v130'
def stream(study):
    path=BASE/f'raw/{study}.compact.jsonl.gz'
    if not path.exists(): path=BASE/f'raw/{study}.jsonl.gz'
    records=[];nobs=0;nnconv=0
    for r in iter_records(path):
        nobs+=validate_run(r);records.append(compact(r))
        if r['study']=='F': nnconv+=sum(not h['converged'] for h in r['history'])
    return {'study':study,'records':records,'observations':nobs,'nonconverged_acquisition_fits':nnconv}

def replay(path):
    r=json.loads(Path(path).read_text());kw=(r['bank'],r['scenario'],r['seed'])
    if r['study']=='D': fresh=transfer.run(*kw,r['protocol'],int(r['costs']['fit']))
    elif r['study']=='E': fresh=spatial.run(*kw,r['policy'],r['budget'],r['control_cost'])
    else: fresh=noise.run(*kw,r['controller'],r['policy'],r['budget'])
    if r!=fresh: raise AssertionError('Representative replay mismatch: '+str(path))
    validate_run(fresh);return Path(path).name

def main():
    lock=verify_lock(BASE)
    with ProcessPoolExecutor(max_workers=3) as pool: rr=list(pool.map(stream,'DEF'))
    records=[r for batch in rr for r in batch['records']]
    expected=json.loads((BASE/'records.json').read_text())
    assert records==expected,'Raw-to-compact records mismatch'
    summary=summarize(records,lock['config']);assert summary==json.loads((BASE/'summary.json').read_text())
    assert paired(records)==json.loads((BASE/'paired_comparisons.json').read_text()),'Paired contrast mismatch'
    paths=sorted((BASE/'traces').glob('*.json'))
    with ProcessPoolExecutor(max_workers=4) as pool: done=list(pool.map(replay,paths,chunksize=6))
    f=[r for r in records if r['study']=='F']
    passive={}
    for r in f:
        if r['policy']!='ivr': passive.setdefault((r['scenario'],r['seed'],r['policy']),set()).add(r['data_digest'])
    assert all(len(h)==1 for h in passive.values()),'Passive design depends on controller'
    report={'version':'1.3.0-research.1','all_raw_runs_validated':len(records),
       'all_serialized_observations_checked':sum(r['observations'] for r in rr),
       'source_and_config_lock_unchanged':True,'raw_to_records_equal':True,
       'all_group_summaries_recomputed_equal':True,'all_paired_contrasts_recomputed_equal':True,
       'representatives_completely_reexecuted':len(done),'all_replay_digests_equal':True,
       'passive_world_policy_groups_with_equal_data_across_controllers':len(passive),
       'F_unique_datasets':len({r['data_digest'] for r in f}),
       'F_nonconverged_final_fits_retained':sum(not v['fit_converged'] for r in f for v in r['evaluation'].values()),
       'F_nonconverged_acquisition_fit_snapshots_retained':sum(r['nonconverged_acquisition_fits'] for r in rr),
       'scope':'Synthetic correctness checks; not validation of biology, absolute sensor truth, or general interval coverage'}
    write_json(ROOT/'research/triad/quality/validation.json',report)
    env={'python':sys.version,'platform':platform.platform(),'packages':{m:importlib.metadata.version(m) for m in ['numpy','scipy','jsonschema','playwright']}}
    write_json(ROOT/'research/triad/quality/environment.json',env)
    print(json.dumps(report,indent=2))
if __name__=='__main__': main()
