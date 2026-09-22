"""Diagnostics may guide development; the final held-out evaluator is single use."""
from __future__ import annotations
import numpy as np
from .contracts import Measurement
from .models import GaussianProcess, LinearObservationModel


def metrics(model: GaussianProcess | LinearObservationModel,
            records: tuple[Measurement, ...], reference: np.ndarray | None = None) -> dict:
    if not records:
        raise ValueError("evaluation records cannot be empty")
    mean, variance = model.predict(tuple(r.query for r in records))
    y = np.array([r.value for r in records])
    variance_y = variance + np.square([r.noise_sd for r in records])
    error = y - mean
    obs_lo, obs_hi = mean - 1.96 * np.sqrt(variance_y), mean + 1.96 * np.sqrt(variance_y)
    latent_lo, latent_hi = mean - 1.96 * np.sqrt(variance), mean + 1.96 * np.sqrt(variance)
    nll = float(np.mean(0.5 * (np.log(2 * np.pi * variance_y) + error ** 2 / variance_y)))
    if hasattr(model, "predictive_intervals"):
        noise = np.array([r.noise_sd for r in records])
        queries = tuple(r.query for r in records)
        obs_lo, obs_hi, latent_lo, latent_hi = model.predictive_intervals(queries, noise)
        nll = model.predictive_nll(queries, y, noise)
    result = {"n": len(records), "rmse_observed": float(np.sqrt(np.mean(error ** 2))),
              "mae_observed": float(np.mean(abs(error))),
              "observation_95_coverage": float(np.mean((y >= obs_lo) & (y <= obs_hi))),
              "observation_95_mean_width": float(np.mean(obs_hi - obs_lo)),
              "predictive_nll": nll,
              "standardized_squared_residual": float(np.mean(error ** 2 / variance_y))}
    if reference is not None:
        result.update({"rmse_latent": float(np.sqrt(np.mean((reference - mean) ** 2))),
                       "latent_95_coverage": float(np.mean((reference >= latent_lo - 1e-12) & (reference <= latent_hi + 1e-12))),
                       "latent_95_mean_width": float(np.mean(latent_hi - latent_lo))})
    return result


def diagnostic_gate(result: dict, rank: int | None = None) -> dict:
    reasons = []
    if result["standardized_squared_residual"] > 4.0:
        reasons.append("residual-model-mismatch")
    if result["observation_95_coverage"] < 0.75:
        reasons.append("undercoverage-on-reused-diagnostic")
    if rank is not None and rank < 2:
        reasons.append("data-design-rank-deficient")
    return {"status": "challenged" if reasons else "within-diagnostic-thresholds",
            "reasons": reasons, "evidence_scope": "synthetic-adaptively-reused-validation",
            "formal_sequential_coverage_guarantee": False}

class FinalEvaluator:
    def __init__(self) -> None:
        self.used = False

    def evaluate(self, model, records: tuple[Measurement, ...], reference: np.ndarray) -> dict:
        if self.used:
            raise RuntimeError("final test is single-use after model freeze")
        if any(r.split != "test" for r in records):
            raise ValueError("final evaluator requires test records")
        self.used = True
        result = metrics(model, records, reference)
        result["final_target_passed"] = bool(result["rmse_latent"] <= 0.12 and
                                               result["observation_95_coverage"] >= 0.80 and
                                               result["observation_95_mean_width"] <= 0.80)
        result["cost_to_target"] = None
        result["cost_to_target_reason"] = "No repeated locked-test evaluation; first-passage cost not estimated"
        return result
