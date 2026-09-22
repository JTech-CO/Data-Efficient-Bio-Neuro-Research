"""Portable CLI; no networking, real-data ingestion, or model download."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from .study import prepare,evaluate,write_json,verify_lock
from .runner import run_world
from .worlds import make_world,SCENARIOS
from .design import POLICIES

def main():
    p=argparse.ArgumentParser(description='Synthetic diagnostic research, v1.2.0')
    sub=p.add_subparsers(dest='command',required=True)
    for cmd in ('prepare','evaluate','verify-lock'):
        q=sub.add_parser(cmd); q.add_argument('--out',required=True,type=Path)
    q=sub.add_parser('demo');q.add_argument('--scenario',choices=SCENARIOS,default='gain_offset')
    q.add_argument('--policy',choices=POLICIES,default='block_targeted');q.add_argument('--seed',type=int,default=27)
    q.add_argument('--out',required=True,type=Path)
    args=p.parse_args()
    try:
        if args.command=='prepare':
            s=prepare(args.out);print(json.dumps({'prepared':str(args.out),'thresholds':s['thresholds']},indent=2))
        elif args.command=='evaluate':
            s=evaluate(args.out);print(json.dumps({'completed':str(args.out),'n_acquisition':s['n_acquisition_trajectories'],'n_detection':s['n_detection_trajectories']}))
        elif args.command=='verify-lock': verify_lock(args.out);print('Source, config and calibration match the lock.')
        else:
            if args.out.exists(): raise FileExistsError('choose a new output path; no silent overwrite')
            r=run_world(make_world('demo',args.scenario,args.seed),args.policy,0.05/12)
            write_json(args.out,r);print(json.dumps({'saved':str(args.out),'diagnosis':r['diagnosis'],'costs':r['costs']},indent=2))
    except (ValueError,RuntimeError,FileExistsError,FileNotFoundError) as exc:
        p.exit(2,f'{type(exc).__name__}: {exc}\n')

if __name__=='__main__': main()
