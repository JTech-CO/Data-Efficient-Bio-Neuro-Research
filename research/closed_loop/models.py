"""Small baselines, exact Gaussian conditioning and an observation-aware linear model.

Hyperparameters are fixed in the preregistered config, not optimized on held-out
labels. All uncertainty is conditional on the stated model and known noise.
"""
from __future__ import annotations
from dataclasses import asdict
import numpy as np
from scipy.linalg import cho_factor, cho_solve
from .contracts import Query, Measurement, ensure_fit_records, digest
from .design import Design


def rbf(a: np.ndarray, b: np.ndarray, length: float, amplitude: float = 1.0) -> np.ndarray:
    if length <= 0 or amplitude <= 0 or not np.isfinite([length, amplitude]).all():
        raise ValueError("invalid kernel scale")
    return amplitude ** 2 * np.exp(-0.5 * ((a[:, None] - b[None, :]) / length) ** 2)

class GaussianProcess:
    def __init__(self, records: tuple[Measurement, ...], *, length: float = 0.20,
                 mode: str = "high_only", discrepancy_length: float = 0.12,
                 discrepancy_amplitude: float = 0.35) -> None:
        ensure_fit_records(records)
        if mode not in ("high_only", "pooled", "multifidelity"):
            raise ValueError("unknown GP mode")
        self.mode = mode
        self.length = length
        self.discrepancy_length = discrepancy_length
        self.discrepancy_amplitude = discrepancy_amplitude
        selected = tuple(r for r in records if mode != "high_only" or r.query.fidelity == "high")
        if not selected:
            raise ValueError("no eligible GP training measurements")
        self.records = selected
        self.queries = tuple(r.query for r in selected)
        self.y = np.array([r.value for r in selected])
        self.noise = np.array([r.noise_sd for r in selected])
        k = self.kernel(self.queries, self.queries) + np.diag(self.noise ** 2)
        self.factor = cho_factor(k + np.eye(len(k)) * 1e-9, lower=True, check_finite=True)
        self.alpha = cho_solve(self.factor, self.y)
        self.name = f"gp-{mode}-l{length:g}"

    def kernel(self, a: tuple[Query, ...], b: tuple[Query, ...]) -> np.ndarray:
        xa, xb = np.array([q.condition for q in a]), np.array([q.condition for q in b])
        k = rbf(xa, xb, self.length)
        if self.mode == "multifidelity":
            ha = np.array([q.fidelity == "high" for q in a], dtype=float)
            hb = np.array([q.fidelity == "high" for q in b], dtype=float)
            # f_H(x)=f_L(x)+delta(x), independent GP priors, rho=1 fixed.
            k += ha[:, None] * hb[None, :] * rbf(xa, xb, self.discrepancy_length, self.discrepancy_amplitude)
        return k

    def predict(self, queries: tuple[Query, ...]) -> tuple[np.ndarray, np.ndarray]:
        cross = self.kernel(self.queries, queries)
        mean = cross.T @ self.alpha
        prior = np.ones(len(queries))
        if self.mode == "multifidelity":
            prior += np.array([q.fidelity == "high" for q in queries]) * self.discrepancy_amplitude ** 2
        variance = prior - np.sum(cross * cho_solve(self.factor, cross), axis=0)
        return mean, np.maximum(variance, 1e-12)

    def posterior_cross(self, a: tuple[Query, ...], b: tuple[Query, ...]) -> np.ndarray:
        return self.kernel(a, b) - self.kernel(a, self.queries) @ cho_solve(self.factor, self.kernel(self.queries, b))

    def acquisition_information(self, queries: tuple[Query, ...], design: Design) -> np.ndarray:
        _, variance = self.predict(queries)
        noise = np.array([design.noise(q) for q in queries])
        if self.mode == "multifidelity":
            target = tuple(Query(float(x)) for x in np.linspace(0, 1, 31))
            cross = self.posterior_cross(target, queries)
            # Integrated reduction of *high-fidelity* posterior variance.
            return np.mean(cross ** 2, axis=0) / (variance + noise ** 2)
        return 0.5 * np.log1p(variance / noise ** 2)

    def card(self) -> dict:
        return {"model": self.name, "mode": self.mode, "length_scale": self.length,
                "discrepancy_length": self.discrepancy_length,
                "discrepancy_amplitude": self.discrepancy_amplitude,
                "rho": 1.0 if self.mode == "multifidelity" else None,
                "fit_record_ids": [r.record_id for r in self.records],
                "uncertainty": "conditional latent Gaussian; known measurement noise added for observation intervals",
                "parameter_identifiability": "not_applicable", "real_data_validation": False}

class LinearObservationModel:
    def __init__(self, records: tuple[Measurement, ...], design: Design,
                 observation_model: str = "aware") -> None:
        ensure_fit_records(records)
        if not records:
            raise ValueError("no training records")
        self.records = records
        self.design = design
        self.observation_model = observation_model
        self.features = np.vstack([design.feature(r.query, observation_model) for r in records])
        y = np.array([r.value for r in records])
        weights = 1 / np.square([r.noise_sd for r in records])
        self.data_information = self.features.T @ (weights[:, None] * self.features)
        precision = np.eye(2) / 4.0 + self.data_information
        factor = cho_factor(precision, lower=True)
        self.covariance = cho_solve(factor, np.eye(2))
        self.mean = cho_solve(factor, self.features.T @ (weights * y))
        self.rank = int(np.linalg.matrix_rank(self.features))
        eigen = np.linalg.eigvalsh(self.data_information)
        self.min_data_eigenvalue = max(0.0, float(eigen[0]))
        self.name = f"linear-observation-{observation_model}"

    def predict(self, queries: tuple[Query, ...]) -> tuple[np.ndarray, np.ndarray]:
        phi = np.vstack([self.design.feature(q, self.observation_model) for q in queries])
        return phi @ self.mean, np.maximum(np.einsum("ij,jk,ik->i", phi, self.covariance, phi), 1e-12)

    def acquisition_information(self, queries: tuple[Query, ...], design: Design) -> np.ndarray:
        _, variance = self.predict(queries)
        return 0.5 * np.log1p(variance / np.square([design.noise(q) for q in queries]))

    def card(self) -> dict:
        return {"model": self.name, "fit_record_ids": [r.record_id for r in self.records],
                "observation_operator": self.observation_model,
                "theta_mean": self.mean.tolist(), "theta_covariance": self.covariance.tolist(),
                "data_design_rank": self.rank, "min_data_information_eigenvalue": self.min_data_eigenvalue,
                "parameter_identifiability": "full_rank_under_assumed_operator" if self.rank == 2 else "only_parameter_combination",
                "uncertainty": "conditional Gaussian posterior; prior does not establish data identifiability",
                "real_data_validation": False}


def baseline_predictions(records: tuple[Measurement, ...], queries: tuple[Query, ...],
                         design: Design) -> dict[str, np.ndarray]:
    """All fitting remains train-only, including plain ridge preprocessing."""
    ensure_fit_records(records)
    selected = tuple(r for r in records if r.query.fidelity == "high")
    y = np.array([r.value for r in selected])
    def phi(q: Query) -> list[float]:
        return [1.0, q.condition]
    train = np.array([phi(r.query) for r in selected])
    test = np.array([phi(q) for q in queries])
    ridge = np.linalg.solve(train.T @ train + np.diag([1e-8, 1e-3]), train.T @ y)
    result = {"constant_mean": np.repeat(np.mean(y), len(queries)), "ridge_scalar_condition": test @ ridge}
    if design.family == "linear":
        h = np.vstack([design.feature(r.query) for r in selected])
        h_test = np.vstack([design.feature(q) for q in queries])
        weights = 1 / np.array([r.noise_sd for r in selected])
        coefficients = np.linalg.lstsq(weights[:, None] * h, weights * y, rcond=None)[0]
        result["weighted_linear_known_operator"] = h_test @ coefficients
    return result


def model_hash(model: GaussianProcess | LinearObservationModel) -> str:
    return digest(model.card())
