"""Synthetic research CLI; use a new output path rather than overwriting evidence."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from . import partial,audit,replicates
from .common import write_json,validate
from .study import prepare,evaluate,verify_lock

def main():
    p=argparse.ArgumentParser(description='Partial identification, unknown-scale audit and replicate decomposition (synthetic only)')
    sub=p.add_subparsers(dest='command',required=True)
    for name in ('prepare','evaluate','verify-lock'):
        s=sub.add_parser(name);s.add_argument('--out',type=Path,required=True)
        if name=='evaluate':s.add_argument('--workers',type=int,default=2)
    s=sub.add_parser('demo');s.add_argument('--study',choices=list('GHI'),required=True)
    s.add_argument('--scenario',required=True);s.add_argument('--design',choices=partial.DESIGNS,default='triangulated')
    s.add_argument('--policy',choices=audit.POLICIES,default='max_gap');s.add_argument('--audit-fraction',type=float,default=.5)
    s.add_argument('--repeats',type=int,choices=replicates.REPLICATION,default=4);s.add_argument('--seed',type=int,default=27)
    s.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    try:
        if a.command=='prepare':r=prepare(a.out);print('Local freeze prepared:',r['evaluation_runs'],'planned evaluations')
        elif a.command=='evaluate':print(json.dumps(evaluate(a.out,a.workers),indent=2))
        elif a.command=='verify-lock':verify_lock(a.out);print('Source / config / plan / development hashes match')
        else:
            if a.out.exists():raise FileExistsError('Choose a fresh output path')
            args=('public-demo-v140',a.scenario,a.seed)
            if a.study=='G':r=partial.run(*args,a.design)
            elif a.study=='H':r=audit.run(*args,a.policy,a.audit_fraction)
            else:r=replicates.run(*args,a.repeats)
            validate(r);write_json(a.out,r);print(a.out)
    except (ValueError,RuntimeError,FileExistsError,FileNotFoundError) as e:p.exit(2,f'Error: {e}\n')
if __name__=='__main__':main()
