"""python -m research_lab {run,benchmark,serve}."""
from __future__ import annotations
import argparse, sys
from pathlib import Path
from .contracts import RunConfig, SCENARIOS, POLICIES
from .runner import run_experiment, save_json, benchmark,ROOT

def main():
    parser=argparse.ArgumentParser(description='Synthetic-only closed-loop research lab')
    sub=parser.add_subparsers(dest='command',required=True)
    run=sub.add_parser('run',help='Execute a new synthetic experiment and export a JSON trace')
    run.add_argument('--scenario',choices=SCENARIOS,default='identifiable')
    run.add_argument('--policy',choices=POLICIES,default='guarded_information')
    run.add_argument('--seed',type=int,default=0);run.add_argument('--budget',type=float,default=24)
    run.add_argument('--observer',choices=('calibrated','identity'),default='calibrated')
    run.add_argument('--out',type=Path,default=Path('research_lab/results/my-run.json'))
    run.add_argument('--overwrite',action='store_true')
    bench=sub.add_parser('benchmark',help='Run the documented paired synthetic pilot')
    bench.add_argument('--plan',type=Path,default=ROOT/'research_lab/configs/pilot.json')
    bench.add_argument('--out',type=Path,default=Path('research_lab/results/new-pilot'))
    bench.add_argument('--seeds',type=int,default=None);bench.add_argument('--overwrite',action='store_true')
    server=sub.add_parser('serve',help='Serve the static review UI and enable local Python execution')
    server.add_argument('--port',type=int,default=8765)
    args=parser.parse_args()
    try:
        if args.command=='run':
            cfg=RunConfig(scenario=args.scenario,policy=args.policy,seed=args.seed,budget=args.budget,observer=args.observer)
            result=run_experiment(cfg);save_json(args.out,result,args.overwrite)
            print(f'Saved {args.out} | cost={result["total_cost"]} | biological units=0')
        elif args.command=='benchmark':
            if args.seeds is not None and args.seeds<1:raise ValueError('--seeds must be positive')
            result,_=benchmark(args.plan,args.out,args.seeds,args.overwrite)
            print(f'Saved {result["runs"]} synthetic runs under {args.out}')
        else:
            if not 1024<=args.port<=65535:raise ValueError('port must be 1024..65535')
            from .server import serve
            serve(args.port)
    except (ValueError,TypeError,OSError) as exc:
        print(f'Error: {exc}',file=sys.stderr);return 2
    return 0

if __name__=='__main__':raise SystemExit(main())
