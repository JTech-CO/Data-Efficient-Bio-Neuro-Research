#!/usr/bin/env python3
"""Synthetic-only GP acquisition stress test, not biological validation.

No downloads, pretrained models, or test-driven acquisition. The target functions,
hyperparameters, budgets and seeds are fixed in source. A stationary fixed GP's
variance acquisition depends on locations, not observed target values.
"""
from __future__ import annotations
import argparse
import json
import platform
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import cho_factor, cho_solve, solve_triangular
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LENGTH_SCALE = 0.18
NOISE_SD = 0.06
BUDGETS = (6, 10, 18, 30)


def kernel(x: np.ndarray, z: np.ndarray, length_scale: float = LENGTH_SCALE) -> np.ndarray:
    if length_scale <= 0:
        raise ValueError("length_scale must be positive")
    return np.exp(-0.5 * ((np.asarray(x)[:, None] - np.asarray(z)[None, :]) / length_scale) ** 2)


def target(x: np.ndarray, scenario: str) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    base = np.sin(2 * np.pi * x) + 0.15 * np.cos(4 * np.pi * x)
    if scenario == "smooth":
        return base
    if scenario == "narrow_peak":
        return base + 1.3 * np.exp(-((x - 0.613) / 0.019) ** 2)
    raise ValueError(f"Unknown scenario: {scenario}")


def predict(x: np.ndarray, y: np.ndarray, query: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    x, y, query = (np.asarray(v, dtype=float) for v in (x, y, query))
    if x.ndim != 1 or y.shape != x.shape or query.ndim != 1:
        raise ValueError("Expected matching one-dimensional x/y and one-dimensional query")
    if not all(np.isfinite(v).all() for v in (x, y, query)):
        raise ValueError("Nonfinite input")
    c = cho_factor(kernel(x, x) + (NOISE_SD**2 + 1e-10) * np.eye(len(x)), lower=True)
    cross = kernel(x, query)
    mean = cross.T @ cho_solve(c, y)
    projected = solve_triangular(c[0], cross, lower=True)
    variance = np.maximum(1.0 - np.einsum("ij,ij->j", projected, projected), 0.0)
    return mean, variance


def one_run(seed: int, scenario: str, policy: str) -> list[dict]:
    if policy not in ("random", "max_variance"):
        raise ValueError("Unknown policy")
    pool = np.linspace(0.0, 1.0, 401)
    # Strictly between pool points; these targets never enter acquisition.
    test = (np.arange(400, dtype=float) + 0.5) / 400
    noise_rng = np.random.default_rng(seed + 1000)
    pool_y = target(pool, scenario) + noise_rng.normal(0, NOISE_SD, pool.size)
    init_rng = np.random.default_rng(seed)
    selected = [0, len(pool) - 1] + init_rng.choice(np.arange(1, len(pool) - 1), 4, replace=False).tolist()
    acquisition_rng = np.random.default_rng(seed + 2000)
    scores = []
    for n in range(BUDGETS[0], BUDGETS[-1] + 1):
        if n in BUDGETS:
            mean, var = predict(pool[selected], pool_y[selected], test)
            truth = target(test, scenario)
            half = 1.959963984540054 * np.sqrt(var)
            scores.append({
                "seed": seed, "scenario": scenario, "policy": policy, "n_queries": n,
                "rmse": float(np.sqrt(np.mean((mean - truth)**2))),
                "latent_pointwise_95_coverage": float(np.mean(np.abs(mean - truth) <= half)),
                "mean_interval_width": float(np.mean(2 * half)),
                "selected_indices": selected.copy()
            })
        if n == BUDGETS[-1]:
            break
        available = np.ones(pool.size, dtype=bool)
        available[selected] = False
        if policy == "random":
            index = int(acquisition_rng.choice(np.flatnonzero(available)))
        else:
            _, variance = predict(pool[selected], pool_y[selected], pool)
            variance[~available] = -np.inf
            index = int(np.argmax(variance))
        selected.append(index)
    return scores


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, default=20)
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "results")
    args = parser.parse_args()
    if not 2 <= args.seeds <= 200:
        parser.error("--seeds must be between 2 and 200")
    args.output.mkdir(parents=True, exist_ok=True)
    runs = [r for scenario in ("smooth", "narrow_peak") for seed in range(args.seeds)
            for policy in ("random", "max_variance") for r in one_run(seed, scenario, policy)]
    summary = []
    for scenario in ("smooth", "narrow_peak"):
        for policy in ("random", "max_variance"):
            for budget in BUDGETS:
                rr = [r for r in runs if r["scenario"] == scenario and r["policy"] == policy and r["n_queries"] == budget]
                row = {"scenario": scenario, "policy": policy, "n_queries": budget, "n_seeds": args.seeds}
                for metric in ("rmse", "latent_pointwise_95_coverage", "mean_interval_width"):
                    values = [r[metric] for r in rr]
                    row[metric + "_mean"] = float(np.mean(values))
                    row[metric + "_sd"] = float(np.std(values, ddof=1))
                summary.append(row)
    for name, data in (("runs.json", runs), ("summary.json", summary)):
        (args.output / name).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    environment = {"python": platform.python_version(), "numpy": np.__version__,
                   "scipy": scipy.__version__, "matplotlib": matplotlib.__version__,
                   "platform": platform.platform(), "seeds": args.seeds,
                   "length_scale": LENGTH_SCALE, "noise_sd": NOISE_SD, "budgets": BUDGETS,
                   "source": "fully synthetic fixed functions; zero biological observations",
                   "interval": "latent-function pointwise nominal 95%; empirical diagnostic, not a coverage theorem"}
    (args.output / "environment.json").write_text(json.dumps(environment, indent=2) + "\n", encoding="utf-8")
    for scenario in ("smooth", "narrow_peak"):
        for metric, label, filelabel in (("rmse", "RMSE on locked synthetic grid", "rmse"),
              ("latent_pointwise_95_coverage", "Empirical latent-function interval coverage", "coverage")):
            fig, ax = plt.subplots(figsize=(7.4, 4.7))
            for policy in ("random", "max_variance"):
                rr = [r for r in summary if r["scenario"] == scenario and r["policy"] == policy]
                ax.plot([r["n_queries"] for r in rr], [r[metric + "_mean"] for r in rr], marker="o", label=policy)
            if filelabel == "coverage":
                ax.axhline(0.95, linestyle=":", label="nominal 0.95")
                ax.set_ylim(0, 1.02)
            ax.set_title(f"Synthetic-only stress test: {scenario}")
            ax.set_xlabel("Queried synthetic observations")
            ax.set_ylabel(label)
            ax.legend()
            fig.tight_layout()
            fig.savefig(args.output / f"{scenario}_{filelabel}.png", dpi=170)
            plt.close(fig)
    # Algebraic counterexample: duplicated design columns identify a+b, not a and b.
    x = np.linspace(-1, 1, 31)
    design = np.column_stack((x, x))
    example = {"equation": "y=(a+b)*x", "design_rank": int(np.linalg.matrix_rank(design)),
               "n_parameters": 2, "pairs": [[1, 2], [2, 1], [0, 3]],
               "max_prediction_difference": float(np.max(np.abs(design @ np.array([1, 2]) - design @ np.array([2, 1])))),
               "interpretation": "Only a+b is identified by these observations; more of the same does not separate a,b."}
    (args.output / "identifiability.json").write_text(json.dumps(example, indent=2) + "\n", encoding="utf-8")
    for row in summary:
        if row["n_queries"] == BUDGETS[-1]:
            print(row["scenario"], row["policy"], "RMSE", round(row["rmse_mean"], 5),
                  "coverage", round(row["latent_pointwise_95_coverage_mean"], 4))


if __name__ == "__main__":
    main()
