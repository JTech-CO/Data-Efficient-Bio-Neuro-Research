from __future__ import annotations
import argparse
import json
from pathlib import Path
from .runner import RunConfig, run_experiment, save_run, audit_run, load_run

def main() -> None:
    parser = argparse.ArgumentParser(description="Closed-loop synthetic research lab; not a biological production model")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="execute one actual Python synthetic experiment")
    run.add_argument("--scenario", default="confounded")
    run.add_argument("--policy", default="guarded")
    run.add_argument("--seed", type=int, default=0)
    run.add_argument("--budget", type=float, default=24)
    run.add_argument("--observation-model", choices=("aware", "identity"), default="aware")
    run.add_argument("--output", type=Path, default=Path("research/results/local-run.json"))
    suite = sub.add_parser("suite", help="run the recorded pilot comparison protocol")
    suite.add_argument("--config", type=Path, default=Path("research/configs/pilot.json"))
    suite.add_argument("--output", type=Path, default=Path("research/results/pilot"))
    audit = sub.add_parser("audit", help="verify a saved run")
    audit.add_argument("path", type=Path)
    server = sub.add_parser("serve", help="serve the local web workbench with a synthetic-only execution API")
    server.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    try:
        if args.command == "run":
            result = run_experiment(RunConfig(args.scenario, args.policy, args.seed, args.budget, args.observation_model))
            save_run(result, args.output)
            print(json.dumps({"path": str(args.output), "run_id": result["run_id"],
                              "stop_reason": result["stop_reason"], "final": result["final"],
                              "audit": audit_run(result)}, ensure_ascii=False, indent=2))
        elif args.command == "suite":
            from .suite import run_suite
            run_suite(args.config, args.output)
        elif args.command == "audit":
            report = audit_run(load_run(args.path))
            print(json.dumps(report, indent=2))
            if report["errors"]:
                raise SystemExit(1)
        else:
            from .server import serve
            serve(args.port)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.exit(2, f"Error: {exc}\n")

if __name__ == "__main__":
    main()
