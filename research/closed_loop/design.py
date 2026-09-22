"""Public design metadata. No simulator truth is exposed to fitting or acquisition."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from .contracts import Query

SCENARIOS = ("smooth", "narrow_peak", "confounded", "biased_sensor", "missing_term",
             "fidelity_helpful", "fidelity_deceptive", "mechanism_pair", "mechanism_outside")

@dataclass(frozen=True)
class Design:
    family: str
    measurement_noise: float = 0.08

    def cost(self, q: Query) -> float:
        if self.family == "fidelity":
            return 0.25 if q.fidelity == "low" else 1.0
        if self.family in ("linear", "committee"):
            return 1.0 + (0.8 if q.readout == "first" else 0) + (1.2 if q.intervention != "none" else 0)
        return 1.0

    def noise(self, q: Query) -> float:
        if self.family == "fidelity" and q.fidelity == "low":
            return 0.10
        return 0.10 if q.readout == "first" else self.measurement_noise

    def feature(self, q: Query, observation_model: str = "aware") -> np.ndarray:
        """H(q) acts on theta=(a,b). Ignoring H is an explicit ablation."""
        if observation_model == "identity":
            return np.array([q.condition, q.condition])
        if observation_model != "aware":
            raise ValueError("unknown observation model")
        b_factor = 0.2 if q.intervention == "attenuate_b" else 1.0
        return q.condition * np.array([1.0, 0.0 if q.readout == "first" else b_factor])

    def candidates(self) -> tuple[Query, ...]:
        xs = np.linspace(0.025, 0.975, 33)
        readouts = ("sum", "first") if self.family in ("linear", "committee") else ("sum",)
        interventions = ("none", "attenuate_b") if self.family in ("linear", "committee") else ("none",)
        fidelities = ("high", "low") if self.family == "fidelity" else ("high",)
        return tuple(Query(float(x), readout=r, intervention=i, fidelity=f, replicate=rep)
                     for x in xs for r in readouts for i in interventions for f in fidelities for rep in (0, 1)
                     if not (r == "first" and i != "none"))

    def initial(self) -> tuple[Query, ...]:
        xs = (0.12, 0.38, 0.71, 0.9)
        if self.family == "fidelity":
            return tuple(Query(x, fidelity=f) for x in (0.12, 0.5, 0.9) for f in ("high", "low"))
        return tuple(Query(x) for x in xs)

    def evaluation_queries(self, split: str) -> tuple[Query, ...]:
        xs = np.linspace(0.035, 0.965, 9) if split == "validation" else np.linspace(0.01, 0.99, 61)
        if self.family in ("linear", "committee"):
            return tuple(Query(float(x), readout=r, intervention=i, group=f"{split}-condition")
                         for x in xs for r, i in (("sum", "none"), ("first", "none"), ("sum", "attenuate_b")))
        return tuple(Query(float(x), group=f"{split}-condition") for x in xs)

    def allowed(self, q: Query) -> bool:
        if self.family not in ("linear", "committee") and (q.readout != "sum" or q.intervention != "none"):
            return False
        if self.family != "fidelity" and q.fidelity != "high":
            return False
        return not (q.readout == "first" and q.intervention != "none")


def get_design(scenario: str) -> Design:
    if scenario not in SCENARIOS:
        raise ValueError(f"unknown scenario: {scenario}")
    family = "fidelity" if scenario.startswith("fidelity_") else "committee" if scenario.startswith("mechanism_") else "linear" if scenario in ("confounded", "biased_sensor", "missing_term") else "gp"
    return Design(family)

def policies_for(scenario: str) -> tuple[str, ...]:
    family = get_design(scenario).family
    if family == "gp":
        return ("random", "space_filling", "max_variance", "guarded")
    if family in ("linear", "committee"):
        return ("random", "fixed_readout", "observation_variance", "information_gain", "guarded")
    return ("hf_only", "naive_pool", "multifidelity", "guarded")
