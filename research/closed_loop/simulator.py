"""Isolated synthetic oracle. Only the runner/evaluator imports this module.

This is an abstract stress test, not a biological simulator or a digital brain.
Per-query seeded noise makes common queries paired across acquisition policies.
"""
from __future__ import annotations
import hashlib
import numpy as np
from .contracts import Query, Measurement
from .design import get_design

class SyntheticOracle:
    def __init__(self, scenario: str, seed: int) -> None:
        self.scenario = scenario
        self.seed = seed
        self.design = get_design(scenario)
        self.theta = np.array([1.2, 0.8])
        self.measurement_calls = 0
        self.reference_calls = 0

    def _mean(self, q: Query) -> float:
        x = q.condition
        if self.design.family == "committee":
            z = np.array([x, x * x])
            if self.scenario == "mechanism_outside":
                z += np.array([0.8 * np.sin(3 * np.pi * x), 0.15])
            h = np.array([1.0, 0.0 if q.readout == "first" else 0.2 if q.intervention == "attenuate_b" else 1.0])
            return float(h @ z)
        if self.design.family == "linear":
            phi = self.design.feature(q)
            value = float(phi @ self.theta)
            if self.scenario == "biased_sensor" and q.readout == "first":
                value *= 0.55
            if self.scenario == "missing_term":
                value += 0.75 * np.sin(3 * np.pi * x)
            return value
        base = 0.8 * np.sin(2 * np.pi * x) + 0.22 * np.cos(4 * np.pi * x)
        if self.scenario == "narrow_peak":
            base += 1.3 * np.exp(-0.5 * ((x - 0.635) / 0.018) ** 2)
        if q.fidelity == "low":
            if self.scenario == "fidelity_helpful":
                base = 0.8 * base + 0.15
            else:
                # Smooth but input-dependent wrong relation. No policy can see this rule.
                base = (1 - 1.8 / (1 + np.exp(-35 * (x - 0.5)))) * base + 0.5 * np.sin(7 * np.pi * x)
        return float(base)

    def observe(self, q: Query, split: str) -> Measurement:
        if not self.design.allowed(q):
            raise ValueError("query is outside the declared design")
        key = f"{self.scenario}|{self.seed}|{split}|{q.key}"
        words = np.frombuffer(hashlib.sha256(key.encode()).digest(), dtype="<u4").tolist()
        rng = np.random.default_rng(np.random.SeedSequence(words))
        sd = self.design.noise(q)
        self.measurement_calls += 1
        return Measurement(record_id=f"{split}-{q.key}", query=q,
                           value=self._mean(q) + float(rng.normal(0, sd)), noise_sd=sd,
                           cost=self.design.cost(q), split=split,
                           group_id=f"sim-{self.seed}-{split}-{q.condition_key}")

    def reference(self, queries: tuple[Query, ...]) -> np.ndarray:
        self.reference_calls += len(queries)
        return np.array([self._mean(q) for q in queries])
