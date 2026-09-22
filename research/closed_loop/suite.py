"""Pilot suite orchestration and paired Monte Carlo summaries, not donor inference."""
from __future__ import annotations
from dataclasses import asdict
from pathlib import Path
import json
import gzip
import base64
import time
import numpy as np
from .contracts import digest
from .design import SCENARIOS, policies_for
from .runner import RunConfig, run_experiment, save_run, audit_run, runtime_fingerprint


def summarize(rows: list[dict], seeds: list[int]) -> dict:
    groups = []
    for scenario in SCENARIOS:
        keys = sorted({(r["policy"], r["observation_model"]) for r in rows if r["scenario"] == scenario})
        for policy, operator in keys:
            selected = [r for r in rows if (r["scenario"], r["policy"], r["observation_model"]) == (scenario, policy, operator)]
            if not selected:
                continue
            stats = {}
            for metric in ("rmse_latent", "rmse_observed", "observation_95_coverage", "observation_95_mean_width", "train_cost", "total_measurement_cost"):
                values = np.array([r[metric] for r in selected], dtype=float)
                stats[metric] = {"mean": float(values.mean()), "sd": float(values.std(ddof=1)) if len(values) > 1 else None,
                                 "min": float(values.min()), "max": float(values.max())}
            groups.append({"scenario": scenario, "policy": policy, "observation_model": operator,
                           "n_seeds": len(selected), "metrics": stats,
                           "target_passes": sum(r["final_target_passed"] for r in selected),
                           "rank2_runs": sum(r.get("data_design_rank") == 2 for r in selected),
                           "assumption_stops": sum(r["stop_reason"].startswith("assumption-challenged") for r in selected),
                           "fallback_runs": sum(r["fallback_used"] for r in selected)})
    contrasts = []
    for scenario in SCENARIOS:
        reference_policy = "multifidelity" if scenario.startswith("fidelity_") else "information_gain" if scenario in ("confounded", "biased_sensor", "missing_term", "mechanism_pair", "mechanism_outside") else "max_variance"
        a = {r["seed"]: r for r in rows if r["scenario"] == scenario and r["policy"] == "guarded" and r["observation_model"] == "aware"}
        b = {r["seed"]: r for r in rows if r["scenario"] == scenario and r["policy"] == reference_policy and r["observation_model"] == "aware"}
        common = sorted(a.keys() & b.keys())
        if not common:
            continue
        diff = np.array([a[s]["rmse_latent"] - b[s]["rmse_latent"] for s in common])
        rng = np.random.default_rng(19037)
        boot = diff[rng.integers(0, len(diff), size=(2000, len(diff)))].mean(axis=1)
        contrasts.append({"scenario": scenario, "contrast": f"guarded minus {reference_policy}", "metric": "rmse_latent",
                          "paired_mean_difference": float(diff.mean()), "paired_seed_bootstrap_95": np.quantile(boot, [0.025, 0.975]).tolist(),
                          "n_seeds": len(common), "scope": "descriptive Monte Carlo seed variation; not biological-population inference or multiplicity-adjusted testing"})
    return {"schema_version": "1.1.0", "evidence_status": "synthetic-pilot-only", "n_runs": len(rows),
            "seed_values": seeds, "groups": groups, "contrasts": contrasts, "runs": rows,
            "sequential_test_cost_to_target_estimated": False, "real_data_validation": False}


def run_suite(config_path: Path, output: Path) -> dict:
    protocol = json.loads(config_path.read_text(encoding="utf-8"))
    seeds = protocol["seeds"]
    if not seeds or len(seeds) > 100 or len(seeds) != len(set(seeds)):
        raise ValueError("suite requires 1-100 unique seeds")
    tasks = []
    for scenario in protocol["scenarios"]:
        for policy in policies_for(scenario):
            for seed in seeds:
                tasks.append(RunConfig(scenario, policy, seed, protocol["training_budget"]))
    for scenario in protocol.get("identity_operator_ablations", []):
        for seed in seeds:
            tasks.append(RunConfig(scenario, "information_gain", seed, protocol["training_budget"], "identity"))
    # Validate the complete execution matrix before any outcome is observed.
    matrix = [asdict(task) for task in tasks]
    output.mkdir(parents=True, exist_ok=True)
    protocol_snapshot = {"protocol": protocol, "config_sha256": digest(protocol),
                         "execution_matrix_sha256": digest(matrix), "matrix": matrix,
                         "runtime": runtime_fingerprint(),
                         "scope": "frozen before this pilot execution; not an independently registered confirmatory study"}
    (output / "protocol.lock.json").write_text(json.dumps(protocol_snapshot, indent=2) + "\n")
    rows, browser_runs = [], []
    started = time.perf_counter()
    for index, task in enumerate(tasks):
        detailed = task.seed == seeds[0]
        result = run_experiment(task, detailed=detailed)
        suffix = ".json" if detailed else ".json.gz"
        destination = output / "runs" / f"{result['run_id']}{suffix}"
        save_run(result, destination, compact=True)
        final, budget = result["final"], result["budget"]
        row = {**asdict(task), "run_id": result["run_id"],
               "rmse_latent": final["rmse_latent"], "rmse_observed": final["rmse_observed"],
               "observation_95_coverage": final["observation_95_coverage"],
               "observation_95_mean_width": final["observation_95_mean_width"],
               "train_cost": budget["train_cost"], "total_measurement_cost": budget["total_measurement_cost"],
               "final_target_passed": final["final_target_passed"],
               "data_design_rank": final.get("data_design_rank"), "stop_reason": result["stop_reason"],
               "fallback_used": any(s["fallback"] for s in result["snapshots"]),
               "audit_status": audit_run(result)["status"], "relative_path": f"runs/{result['run_id']}{suffix}",
               "deterministic_payload_sha256": result["deterministic_payload_sha256"]}
        rows.append(row)
        if detailed:
            browser_runs.append(result)
        if (index + 1) % 30 == 0:
            print(f"Completed {index + 1}/{len(tasks)} synthetic runs", flush=True)
    summary = summarize(rows, seeds)
    summary["protocol_hash"] = digest(protocol)
    summary["execution_seconds"] = time.perf_counter() - started
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    root = Path(__file__).resolve().parents[2]
    bundle = {"summary": summary, "protocol": protocol, "runs": browser_runs}
    public = root / "lab/data/pilot-data.js"
    public.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(bundle, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")
    encoded = base64.b64encode(gzip.compress(raw, mtime=0)).decode("ascii")
    public.write_text(
        "/* Generated synthetic pilot. Native gzip decoding; no network or CDN. */\n"
        "window.CLOSED_LOOP_READY = (async () => {\n"
        "  if (typeof DecompressionStream === 'undefined') throw Error('Browser requires DecompressionStream support.');\n"
        "  const bytes = Uint8Array.from(atob('" + encoded + "'), c => c.charCodeAt(0));\n"
        "  const stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'));\n"
        "  return JSON.parse(await new Response(stream).text());\n"
        "})();\n", encoding="utf-8")
    print(json.dumps({"runs": len(rows), "browser_runs": len(browser_runs), "seconds": summary["execution_seconds"],
                      "summary": str(output / "summary.json"), "all_audits_pass": all(r["audit_status"] == "pass" for r in rows)}, indent=2))
    return summary
