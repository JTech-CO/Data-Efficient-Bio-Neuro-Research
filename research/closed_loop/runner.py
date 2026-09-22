"""The executable closed loop. No real-data or wet-lab adapter is installed.

observe -> fit -> diagnose -> propose -> simulated approval -> observe;
freeze -> one final held-out evaluation -> report.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
import hashlib
import gzip
import importlib.metadata
import json
from pathlib import Path
import platform
import time
import numpy as np
from . import __version__
from .contracts import AuditTrail, Ledger, Query, Measurement, digest, canonical
from .design import get_design, policies_for
from .models import GaussianProcess, LinearObservationModel, baseline_predictions, model_hash
from .committee import MechanismCommittee
from .assumptions import register
from .acquisition import propose
from .evaluation import FinalEvaluator, metrics, diagnostic_gate
from .simulator import SyntheticOracle

@dataclass(frozen=True)
class RunConfig:
    scenario: str = "confounded"
    policy: str = "guarded"
    seed: int = 0
    training_budget: float = 24.0
    observation_model: str = "aware"
    max_steps: int = 120

    def __post_init__(self) -> None:
        get_design(self.scenario)
        if self.policy not in policies_for(self.scenario):
            raise ValueError(f"policy {self.policy} is not supported for {self.scenario}")
        if type(self.seed) is not int or not 0 <= self.seed < 2 ** 32:
            raise ValueError("seed must be an integer in [0, 2^32)")
        if not np.isfinite(self.training_budget) or not 4 <= self.training_budget <= 64:
            raise ValueError("training budget must be finite and between 4 and 64")
        if type(self.max_steps) is not int or not 1 <= self.max_steps <= 240:
            raise ValueError("max_steps must be between 1 and 240")
        if self.observation_model not in ("aware", "identity"):
            raise ValueError("observation model must be aware or identity")
        if get_design(self.scenario).family != "linear" and self.observation_model != "aware":
            raise ValueError("identity operator ablation only applies to linear scenarios")


def runtime_fingerprint() -> dict:
    source = sorted(Path(__file__).parent.glob("*.py"))
    return {"python": platform.python_version(), "numpy": importlib.metadata.version("numpy"),
            "scipy": importlib.metadata.version("scipy"), "platform": platform.system(),
            "source_sha256": digest({p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in source})}


def _choose_model(train, validation, design, config, fallback):
    comparisons = {}
    if design.family == "committee":
        model = MechanismCommittee(train, design)
    elif design.family == "linear":
        model = LinearObservationModel(train, design, config.observation_model)
    elif design.family == "gp":
        model = GaussianProcess(train)
        if config.policy == "guarded" and len(train) >= 6:
            shorter = GaussianProcess(train, length=0.06)
            long_score, short_score = metrics(model, validation), metrics(shorter, validation)
            comparisons = {"long_rmse": long_score["rmse_observed"], "short_rmse": short_score["rmse_observed"]}
            if short_score["rmse_observed"] < 0.85 * long_score["rmse_observed"]:
                model = shorter
    else:
        high = GaussianProcess(train, mode="high_only")
        if config.policy == "hf_only" or fallback:
            model = high
        elif config.policy == "naive_pool":
            model = GaussianProcess(train, mode="pooled")
        else:
            multi = GaussianProcess(train, mode="multifidelity")
            model = multi
            if config.policy == "guarded" and sum(r.query.fidelity == "high" for r in train) >= 4:
                high_score, multi_score = metrics(high, validation), metrics(multi, validation)
                comparisons = {"high_only_rmse": high_score["rmse_observed"], "multifidelity_rmse": multi_score["rmse_observed"]}
                if multi_score["rmse_observed"] > 1.15 * high_score["rmse_observed"] + 0.01:
                    fallback = True
                    model = high
    diagnosis = metrics(model, validation)
    rank = model.rank if design.family == "linear" else None
    gate = diagnostic_gate(diagnosis, rank)
    return model, diagnosis, gate, fallback, comparisons


def run_experiment(config: RunConfig, *, detailed: bool = True) -> dict:
    started = time.perf_counter()
    design = get_design(config.scenario)
    oracle = SyntheticOracle(config.scenario, config.seed)
    policy_rng = np.random.default_rng(np.random.SeedSequence([config.seed, 1789]))
    ledger, trail = Ledger(), AuditTrail()
    trail.add("protocol", {"config": asdict(config), "config_hash": digest(asdict(config)),
                           "mode": "synthetic-only", "version": __version__,
                           "final_test_access": "after-model-freeze-only"})
    for q in design.initial():
        if config.policy == "hf_only" and q.fidelity == "low":
            continue
        ledger.append(oracle.observe(q, "train"))
    trail.add("initial_observations", {"record_ids": [r.record_id for r in ledger.view("train")]})
    for q in design.evaluation_queries("validation"):
        ledger.append(oracle.observe(q, "validation"))
    validation = ledger.view("validation")
    trail.add("diagnostic_partition", {"record_ids": [r.record_id for r in validation],
                                        "reused_for_model_selection": True,
                                        "cost": sum(r.cost for r in validation)})
    snapshots = []
    fallback = False
    stop_reason = "max-steps"
    next_reason = "initial-space-spread-observations"
    plot_queries = tuple(Query(float(x)) for x in np.linspace(0, 1, 81))
    plot_variants = {"sum/none": plot_queries}
    if design.family in ("linear", "committee"):
        plot_variants.update({"first/none": tuple(Query(q.condition, readout="first") for q in plot_queries),
                              "sum/attenuate_b": tuple(Query(q.condition, intervention="attenuate_b") for q in plot_queries)})
    for step in range(config.max_steps + 1):
        train = ledger.view("train", for_fit=True)
        model, diagnosis, gate, fallback, comparisons = _choose_model(train, validation, design, config, fallback)
        budget = ledger.budget()
        trail.add("fit_and_diagnose", {"step": step, "model_hash": model_hash(model),
                                       "fit_record_ids": model.card()["fit_record_ids"],
                                       "diagnostic_record_ids": [r.record_id for r in validation],
                                       "diagnosis": diagnosis, "gate": gate, "fallback": fallback,
                                       "comparisons": comparisons})
        assumptions = register(design, model, gate, tuple(r.record_id for r in validation))
        trail.add("assumptions_reviewed", {"step": step, "register": assumptions})
        snapshot = {"assumptions": assumptions, "step": step, "n_train": len(train), "cost": budget["train_cost"],
                    "model": model.name, "rank": getattr(model, "rank", None),
                    "diagnostic": diagnosis, "gate": gate, "fallback": fallback,
                    "last_reason": next_reason, "comparisons": comparisons}
        if hasattr(model, "probabilities"):
            snapshot["candidate_probabilities"] = model.probabilities.tolist()
        if detailed:
            predictions = {}
            for label, queries in plot_variants.items():
                mean, var = model.predict(queries)
                lo, hi = mean - 1.96 * np.sqrt(var), mean + 1.96 * np.sqrt(var)
                if hasattr(model, "predictive_intervals"):
                    _, _, lo, hi = model.predictive_intervals(queries, np.array([design.noise(q) for q in queries]))
                predictions[label] = {"x": [q.condition for q in queries], "mean": mean.tolist(),
                                      "lower": lo.tolist(), "upper": hi.tolist(),
                                      "latent_sd": np.sqrt(var).tolist(), "interval": "conditional-latent-95"}
            snapshot["predictions"] = predictions
        snapshots.append(snapshot)
        # Model misspecification is not solved by spending the remaining budget.
        # This gate is developmental, noisy and calibrated only by this pilot.
        if (config.policy == "guarded" and design.family in ("linear", "committee") and len(train) >= 8
                and (design.family == "committee" or getattr(model, "rank", 0) == 2) and diagnosis["standardized_squared_residual"] > 4.0):
            stop_reason = "assumption-challenged-revise-observation-or-mechanism"
            break
        remaining = config.training_budget - budget["train_cost"]
        if remaining < 0.25 - 1e-9:
            stop_reason = "training-budget-exhausted"
            break
        if step >= config.max_steps:
            break
        proposal = propose(model, train, design, config.policy, remaining, policy_rng, step + 1, fallback=fallback)
        if proposal is None:
            stop_reason = "no-affordable-eligible-query"
            break
        q = proposal.query
        trail.add("query_proposed", {"step": step + 1, "query": asdict(q), "query_id": q.key,
                                     "model_hash": model_hash(model), "score": proposal.score,
                                     "reason": proposal.reason, "cost": design.cost(q),
                                     "alternatives": list(proposal.alternatives)})
        trail.add("simulator_approval", {"query_id": q.key, "scope": "synthetic-oracle-only",
                                        "authority": "pre-authorized-finite-synthetic-design"})
        measured = oracle.observe(q, "train")
        ledger.append(measured)
        trail.add("observation_committed", {"record_id": measured.record_id, "query_id": q.key,
                                            "split": measured.split, "record_hash": digest(asdict(measured))})
        next_reason = proposal.reason
    # Nothing downstream of this boundary may influence model or query choice.
    card = model.card()
    frozen_hash = model_hash(model)
    trail.add("model_frozen", {"model_hash": frozen_hash, "model_card": card, "stop_reason": stop_reason})
    test_queries = design.evaluation_queries("test")
    frozen_train = ledger.view("train", for_fit=True)
    baselines = baseline_predictions(frozen_train, test_queries, design)
    operator_comparison = None
    if design.family == "linear":
        operator_comparison = {name: LinearObservationModel(frozen_train, design, name).predict(test_queries)[0]
                               for name in ("aware", "identity")}
    for q in test_queries:
        ledger.append(oracle.observe(q, "test"))
    test = ledger.view("test")
    reference = oracle.reference(test_queries)
    final = FinalEvaluator().evaluate(model, test, reference)
    if design.family == "linear":
        final["parameter_rmse_under_synthetic_truth"] = float(np.sqrt(np.mean((model.mean - oracle.theta) ** 2)))
        final["data_design_rank"] = model.rank
    final["baselines_same_training_measurements"] = {
        name: {"rmse_latent": float(np.sqrt(np.mean((value - reference) ** 2))),
               "rmse_observed": float(np.sqrt(np.mean((value - np.array([r.value for r in test])) ** 2)))}
        for name, value in baselines.items()}
    if operator_comparison is not None:
        final["same_queries_operator_ablation"] = {name: {"rmse_latent": float(np.sqrt(np.mean((pred - reference) ** 2)))} for name, pred in operator_comparison.items()}
    if design.family == "committee":
        final["candidate_posterior"] = model.probabilities.tolist()
        final["argmax_candidate"] = model.candidate_names[int(np.argmax(model.probabilities))]
        final["selected_candidate"] = final["argmax_candidate"] if float(np.max(model.probabilities)) >= 0.95 else None
        final["candidate_resolved_at_95_percent"] = final["selected_candidate"] is not None
        final["candidate_claim_passes_synthetic_diagnostic"] = final["selected_candidate"] is not None and gate["status"] != "challenged"
        final["true_candidate_in_library"] = config.scenario == "mechanism_pair"
        final["candidate_choice_correct_in_synthetic_oracle"] = config.scenario == "mechanism_pair" and final["selected_candidate"] == "A"
    # Readout-specific errors prevent a good scalar sum from concealing a bad operator.
    by_readout = {}
    for label in sorted({f"{r.query.readout}/{r.query.intervention}" for r in test}):
        indexes = [i for i, r in enumerate(test) if f"{r.query.readout}/{r.query.intervention}" == label]
        by_readout[label] = metrics(model, tuple(test[i] for i in indexes), reference[indexes])
    final["by_readout"] = by_readout
    trail.add("final_test_evaluated", {"model_hash": frozen_hash, "n_test": len(test),
                                        "record_ids": [r.record_id for r in test], "metrics": final})
    limitations = ["synthetic-only; no biological or clinical validation",
                   "conditional model intervals, not OOD or sequential coverage guarantees",
                   "validation reused adaptively; final test used once per run but suite is developmental",
                   "noise, intervention efficacy and candidate design treated as known by the model",
                   "same fixed synthetic truth across seeds; seeds are Monte Carlo repeats, not donors"]
    result = {"schema_version": "1.1.0", "config": asdict(config),
              "run_id": f"{config.scenario}--{config.policy}--{config.observation_model}--s{config.seed}",
              "evidence_status": "synthetic-pilot-only", "real_data_validation": False,
              "config_hash": digest(asdict(config)), "stop_reason": stop_reason,
              "budget": ledger.budget(), "model_card": card, "assumption_register": assumptions, "model_hash": frozen_hash,
              "snapshots": snapshots, "observations": ledger.records(), "events": trail.events,
              "final": final, "limitations": limitations}
    if detailed:
        result["synthetic_reference_after_freeze"] = {label: {"x": [q.condition for q in queries],
                                                               "y": oracle.reference(queries).tolist()}
                                                      for label, queries in plot_variants.items()}
    result["budget"]["n_simulator_measurement_calls"] = oracle.measurement_calls
    result["budget"]["n_evaluator_truth_queries"] = oracle.reference_calls
    result["deterministic_payload_sha256"] = digest(result)
    result["execution"] = {**runtime_fingerprint(), "elapsed_seconds": time.perf_counter() - started}
    return result


def audit_run(result: dict) -> dict:
    errors = []
    try:
        config = RunConfig(**result["config"])
        if digest(asdict(config)) != result["config_hash"]:
            errors.append("config hash mismatch")
        core = {k: v for k, v in result.items() if k not in ("execution", "deterministic_payload_sha256")}
        if digest(core) != result["deterministic_payload_sha256"]:
            errors.append("payload hash mismatch")
        if not AuditTrail.verify(result["events"]):
            errors.append("event hash chain mismatch")
        ledger = Ledger()
        for raw in result["observations"]:
            row = dict(raw)
            row["query"] = Query(**row["query"])
            row["parent_ids"] = tuple(row["parent_ids"])
            ledger.append(Measurement(**row))
        budget = ledger.budget()
        for name, value in budget.items():
            if isinstance(value, (float, int)) and abs(value - result["budget"][name]) > 1e-8:
                errors.append(f"budget mismatch: {name}")
        if budget["train_cost"] > config.training_budget + 1e-8:
            errors.append("training budget exceeded")
        event_types = [e["type"] for e in result["events"]]
        if event_types.count("model_frozen") != 1 or event_types.count("final_test_evaluated") != 1:
            errors.append("missing or repeated freeze/final test")
        else:
            freeze_i = event_types.index("model_frozen")
            test_i = event_types.index("final_test_evaluated")
            if test_i <= freeze_i or test_i != len(event_types) - 1:
                errors.append("final-test boundary violated")
            if any(x in ("fit_and_diagnose", "query_proposed") for x in event_types[freeze_i + 1:]):
                errors.append("adaptive operation after freeze")
        fit_ids = {r.record_id for r in ledger.view("train", for_fit=True)}
        for e in result["events"]:
            if e["type"] == "fit_and_diagnose" and not set(e["payload"]["fit_record_ids"]) <= fit_ids:
                errors.append("non-training IDs in fit view")
        if digest(result["model_card"]) != result["model_hash"]:
            errors.append("model card hash mismatch")
        frozen = [e for e in result["events"] if e["type"] == "model_frozen"]
        if frozen and frozen[0]["payload"]["model_hash"] != result["model_hash"]:
            errors.append("frozen model mismatch")
        if result["real_data_validation"] or result["evidence_status"] != "synthetic-pilot-only":
            errors.append("unsupported evidence promotion")
        if not np.isfinite(result["final"]["rmse_latent"]):
            errors.append("non-finite final result")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return {"status": "pass" if not errors else "fail", "errors": errors,
            "scope": "structural/runtime evidence isolation; not scientific validity or signed authenticity"}


def load_run(path: Path) -> dict:
    data = path.read_bytes()
    return json.loads(gzip.decompress(data) if path.suffix == ".gz" else data)


def save_run(result: dict, path: Path, *, compact: bool = False) -> None:
    report = audit_run(result)
    if report["errors"]:
        raise ValueError("run audit failed: " + "; ".join(report["errors"]))
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    text = (canonical(result) if compact else json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)) + "\n"
    data = text.encode("utf-8")
    if path.suffix == ".gz":
        data = gzip.compress(data, compresslevel=9, mtime=0)
    temp.write_bytes(data)
    temp.replace(path)
