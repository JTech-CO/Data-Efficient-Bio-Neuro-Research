"""CLI: prepare, evaluate, verify-lock, or separate synthetic demo."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from . import transfer,spatial,noise
from .study import prepare,evaluate,verify_lock,job
from .common import write_json,validate_run


def main():
    p=argparse.ArgumentParser(description='Synthetic calibration / audit / noise research, no real-data adapter')
    sub=p.add_subparsers(dest='command',required=True)
    for name in ('prepare','evaluate','verify-lock'):
        s=sub.add_parser(name);s.add_argument('--out',type=Path,required=True)
        if name=='evaluate':s.add_argument('--workers',type=int,default=1)
    s=sub.add_parser('demo');s.add_argument('--study',choices=list('DEF'),required=True)
    s.add_argument('--scenario',required=True);s.add_argument('--policy',required=True)
    s.add_argument('--controller',default='hom_gaussian',choices=noise.ESTIMATORS)
    s.add_argument('--seed',type=int,default=27);s.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    try:
        if a.command=='prepare':r=prepare(a.out);print('Prepared:',r['development_runs'],'development runs')
        elif a.command=='evaluate':
            if not 1<=a.workers<=16: raise ValueError('workers must be 1..16')
            r=evaluate(a.out,a.workers);print(json.dumps(r['counts'],indent=2))
        elif a.command=='verify-lock':verify_lock(a.out);print('Source, config and development record match the local lock')
        else:
            if a.out.exists():raise FileExistsError('Choose a new output path; no implicit overwrite')
            if a.study=='D':r=transfer.run('demo-v130',a.scenario,a.seed,a.policy)
            elif a.study=='E':r=spatial.run('demo-v130',a.scenario,a.seed,a.policy)
            else:r=noise.run('demo-v130',a.scenario,a.seed,a.controller,a.policy)
            validate_run(r);write_json(a.out,r);print(a.out)
    except (ValueError,RuntimeError,FileExistsError,FileNotFoundError) as e:p.exit(2,f'Error: {e}\n')

if __name__=='__main__':main()
