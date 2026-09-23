"""Recompute every summary and replay all representatives without altering old versions."""
from __future__ import annotations
import gzip,json,sys,hashlib
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from research.bounded_loop.common import validate,digest,write_json
from research.bounded_loop.study import row_records,summarize,paired,verify_lock,job
BASE=ROOT/'research/bounded/results/v140'

def replay(path):
    r=json.loads(Path(path).read_text());spec={k:r[k] for k in ('study','scenario','bank','seed','budget')}
    if r['study']=='G':spec['design']=r['design']
    elif r['study']=='H':spec.update(policy=r['policy'],fraction=r['audit_fraction'])
    else:spec.update(repeats=r['repeats'],bootstrap=r['bootstrap'])
    fresh=job(spec);assert fresh==r,'Replay mismatch '+str(path);validate(fresh);return str(path.name)

def main():
    verify_lock(BASE);rows=[];nobs=0;counts={};digests=[];clips=0;max_error=0;h_equal={}
    for study in 'GHI':
        count=0
        with gzip.open(BASE/f'raw/{study}.jsonl.gz','rt',encoding='utf-8') as f:
            for line in f:
                r=json.loads(line);nobs+=validate(r);count+=1;digests.append(r['record_digest']);rows.extend(row_records(r))
                if study=='G':
                    for a,b in [('assume_unbiased','bounded'),('bounded','wide')]:
                        if r['fits'][a]['status']=='bounded':
                            assert r['fits'][b]['status']=='bounded'
                            for key,p in r['fits'][a]['projections'].items():
                                q=r['fits'][b]['projections'][key]
                                assert q['low']<=p['low']+1e-7 and q['high']>=p['high']-1e-7
                if study=='H':
                    assert r['acquisition_spend']<=r['budget']+1e-7
                    if r['audit_fraction']:
                        assert r['costs']['audit']+r['setup_cost']<=r['budget']*r['audit_fraction']+1e-7
                    fit=digest([g for g in r['groups'] if g['role']=='fit'])
                    key=(r['scenario'],r['seed'],r['audit_fraction']);h_equal.setdefault(key,set()).add(fit)
                if study=='I':
                    max_error=max(max_error,r['pure_error']['identity_error'])
                    clips+=sum(m['variance_clip_count'] for m in r['models'].values())
                    assert r['costs']['fit']==48
        counts[study]=count
        print('Validated',study,count,'records',flush=True)
    assert rows==json.loads((BASE/'records.json').read_text())
    assert summarize(rows)==json.loads((BASE/'summary.json').read_text())
    assert paired(rows)==json.loads((BASE/'paired.json').read_text())
    assert all(len(x)==1 for x in h_equal.values()),'Training data depend on audit policy'
    complete=json.loads((BASE/'evaluation.complete.json').read_text())
    assert complete['raw_digest_sequence']==digest(digests)
    assert complete['runs']==counts and complete['serialized_observations']==nobs
    paths=sorted((BASE/'traces').glob('*.json'))
    with ProcessPoolExecutor(max_workers=4) as pool:done=list(pool.map(replay,paths,chunksize=2))
    report=dict(all_runs_validated=sum(counts.values()),counts=counts,serialized_observations=nobs,
      all_raw_to_records_equal=True,all_summaries_recomputed=True,all_paired_contrasts_recomputed=True,
      representatives_replayed=len(done),all_replays_exactly_equal=True,source_config_lock_unchanged=True,
      pure_error_partition_max_absolute_error=max_error,I_variance_clipping_events=clips,
      H_training_datasets_unchanged_across_audit_policies=True,G_bias_profile_nesting_checked=True,
      scope='Software and synthetic validation only; no external scientific validation')
    write_json(ROOT/'research/bounded/quality/validation.json',report,overwrite=True)
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
