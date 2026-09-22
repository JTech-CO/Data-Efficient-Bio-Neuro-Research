"""Two declared mechanistic hypotheses with observation-projected information gain.

Candidate A has z=(x,x^2), B has z=(x^2,x). Both give the same summed
readout. Readout or intervention changes can distinguish them. These are fixed
abstract hypotheses, not discovered biological laws or fitted neural networks.
"""
from __future__ import annotations
import numpy as np
from scipy.special import logsumexp, ndtr
from numpy.polynomial.hermite import hermgauss
from .contracts import Query, Measurement, ensure_fit_records
from .design import Design

class MechanismCommittee:
    candidate_names = ("A", "B")

    def __init__(self, records: tuple[Measurement, ...], design: Design):
        ensure_fit_records(records)
        self.records = records
        self.design = design
        means = self.candidate_means(tuple(r.query for r in records))
        y = np.array([r.value for r in records])
        sd = np.array([r.noise_sd for r in records])
        logp = np.log(np.array([0.5, 0.5])) - np.sum(0.5 * ((means - y[None, :]) / sd) ** 2, axis=1)
        self.log_probabilities = logp - logsumexp(logp)
        self.probabilities = np.exp(self.log_probabilities)
        self.name = "finite-observation-committee"

    @staticmethod
    def candidate_means(queries: tuple[Query, ...]) -> np.ndarray:
        x = np.array([q.condition for q in queries])
        b = np.array([0.0 if q.readout == "first" else 0.2 if q.intervention == "attenuate_b" else 1.0 for q in queries])
        return np.vstack((x + b * x ** 2, x ** 2 + b * x))

    def predict(self, queries: tuple[Query, ...]) -> tuple[np.ndarray, np.ndarray]:
        means = self.candidate_means(queries)
        mean = self.probabilities @ means
        variance = np.sum(self.probabilities[:, None] * (means - mean) ** 2, axis=0)
        return mean, np.maximum(variance, 1e-12)

    def acquisition_information(self, queries: tuple[Query, ...], design: Design) -> np.ndarray:
        means = self.candidate_means(queries)
        sd = np.array([design.noise(q) for q in queries])
        nodes, weights = hermgauss(12)
        values = np.zeros(len(queries))
        for k in range(2):
            y = means[k, :, None] + np.sqrt(2) * sd[:, None] * nodes[None, :]
            z = (y[None, :, :] - means[:, :, None]) / sd[None, :, None]
            conditional = -0.5 * z ** 2 - np.log(sd)[None, :, None] - 0.5 * np.log(2 * np.pi)
            mixture = logsumexp(self.log_probabilities[:, None, None] + conditional, axis=0)
            expected = ((conditional[k] - mixture) * weights[None, :]).sum(axis=1) / np.sqrt(np.pi)
            values += self.probabilities[k] * expected
        entropy = -float(np.sum(self.probabilities * self.log_probabilities))
        return np.clip(values, 0, max(0.0, entropy))

    def predictive_intervals(self, queries, noise):
        means = self.candidate_means(queries)
        noise = np.asarray(noise)
        bounds = []
        for probability in (0.025, 0.975):
            lo, hi = means.min(axis=0) - 10 * noise, means.max(axis=0) + 10 * noise
            for _ in range(50):
                mid = 0.5 * (lo + hi)
                cdf = np.sum(self.probabilities[:, None] * ndtr((mid[None, :] - means) / noise[None, :]), axis=0)
                lo = np.where(cdf < probability, mid, lo)
                hi = np.where(cdf >= probability, mid, hi)
            bounds.append(0.5 * (lo + hi))
        order = np.argsort(means, axis=0)
        sorted_means = np.take_along_axis(means, order, axis=0)
        weights = np.take_along_axis(np.broadcast_to(self.probabilities[:, None], means.shape), order, axis=0)
        cumulative = np.cumsum(weights, axis=0)
        latent = [np.take_along_axis(sorted_means, np.argmax(cumulative >= p, axis=0)[None, :], axis=0)[0] for p in (0.025, 0.975)]
        return bounds[0], bounds[1], latent[0], latent[1]

    def predictive_nll(self, queries, y, noise):
        means = self.candidate_means(queries)
        logp = -0.5 * ((y[None, :] - means) / noise[None, :]) ** 2 - np.log(noise)[None, :] - 0.5 * np.log(2 * np.pi)
        return float(np.mean(-logsumexp(self.log_probabilities[:, None] + logp, axis=0)))

    def card(self) -> dict:
        return {"model": self.name, "fit_record_ids": [r.record_id for r in self.records],
                "candidate_names": list(self.candidate_names), "posterior_probabilities": self.probabilities.tolist(),
                "candidate_equations": {"A": "z1=x; z2=x^2", "B": "z1=x^2; z2=x"},
                "observation_operator": "H(q)=[1, 1] or [1, 0] or [1, 0.2]",
                "uncertainty": "finite Gaussian-mixture observation quantiles and discrete latent quantiles",
                "interval_caveat": "quantiles remain conditional on candidate completeness and known noise",
                "parameter_identifiability": "finite-candidate discrimination only; no continuous parameters",
                "real_data_validation": False}
