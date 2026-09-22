"""Typed public contracts. This module has no access to simulator truth."""
from __future__ import annotations
from dataclasses import dataclass, asdict
import math
from typing import Literal

READOUTS = ("aggregate", "pathway_a", "pathway_b")
POLICIES = ("random", "space_filling", "max_variance", "model_information", "guarded_information",
            "guarded_no_gate", "guarded_no_exploration")
SCENARIOS = ("identifiable", "observational_equivalence", "hidden_mechanism", "sensor_shift", "noise_shift")

@dataclass(frozen=True)
class Query:
    condition: float
    time: float
    readout: str
    intervention: float = 0.0
    fidelity: str = "reference"
    replicate: int = 0
    group: str = "synthetic-system"

    def __post_init__(self):
        if not all(math.isfinite(v) for v in (self.condition, self.time, self.intervention)):
            raise ValueError("Query numbers must be finite")
        if not 0.1 <= self.condition <= 2.5 or not 0.1 <= self.time <= 4:
            raise ValueError("Outside research simulator envelope")
        if self.readout not in READOUTS or self.intervention not in (0., 0.5, 1.):
            raise ValueError("Unsupported readout or intervention")
        if self.fidelity != "reference":
            raise ValueError("Multi-fidelity selection is not implemented in this research slice")
        if not isinstance(self.replicate, int) or isinstance(self.replicate, bool) or self.replicate < 0:
            raise ValueError("replicate must be a nonnegative integer")

    @property
    def key(self) -> str:
        return f"x{self.condition:.4f}_t{self.time:.4f}_{self.readout}_u{self.intervention:.1f}_r{self.replicate}"

    @property
    def cost(self) -> float:
        return round({"aggregate":1.0,"pathway_a":1.4,"pathway_b":1.8}[self.readout]
                     + (0.6 if self.intervention else 0.0), 8)

    @property
    def nominal_sigma(self) -> float:
        return {"aggregate":0.12,"pathway_a":0.075,"pathway_b":0.055}[self.readout]

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass(frozen=True)
class ObservationAssumptions:
    """Public *assumed* observation model, never an oracle-calibrated estimate."""
    mode: str = "calibrated"
    version: str = "linear-sensor-v1"

    def __post_init__(self):
        if self.mode not in ("calibrated", "identity"):
            raise ValueError("observer must be calibrated or identity")

    def weights_offset(self, q: Query) -> tuple[float, float, float]:
        if self.mode == "identity":
            return {"aggregate":(1.,1.,0.),"pathway_a":(1.,0.,0.),"pathway_b":(0.,1.,0.)}[q.readout]
        decay = math.exp(-0.18*q.time)
        a,b = {"aggregate":(1.,0.4),"pathway_a":(1.,0.),"pathway_b":(0.,0.8)}[q.readout]
        return a*decay, b*decay, 0.10+0.035*q.time

    def register(self) -> dict:
        return {"version":self.version,"mode":self.mode,
                "status":"assumed_not_empirically_validated",
                "known_metadata":"nominal instrument gains, offset and noise in the toy world",
                "not_estimated":["measurement calibration", "decay rates", "population effects"],
                "mechanism_candidates":["parallel","compensatory"],
                "uncertainty_scope":["Gaussian parameter posterior","finite candidate uncertainty","nominal observation noise"],
                "excluded_uncertainty":["unknown candidate laws","unknown sensor drift","population shift","noise parameter uncertainty"]}

@dataclass(frozen=True)
class RunConfig:
    scenario: str = "identifiable"
    policy: str = "guarded_information"
    seed: int = 0
    budget: float = 24.0
    observer: str = "calibrated"
    audit_every: int = 3
    audit_z: float = 2.5
    audit_hits: int = 2
    audit_window: int = 3
    exploration_every: int = 4
    parameter_weight: float = 0.15
    decision_threshold: float = 0.95
    quadrature_nodes: int = 20

    def __post_init__(self):
        if self.scenario not in SCENARIOS or self.policy not in POLICIES:
            raise ValueError("Unknown scenario or policy")
        if not isinstance(self.seed, int) or isinstance(self.seed, bool) or not 0 <= self.seed <= 2**31-1:
            raise ValueError("seed must be an integer in [0, 2^31-1]")
        if not math.isfinite(self.budget) or not 8 <= self.budget <= 60:
            raise ValueError("budget must be between 8 and 60 synthetic cost units")
        ObservationAssumptions(self.observer)
        if not all(isinstance(v,int) and not isinstance(v,bool) and v>0 for v in
                   (self.audit_every,self.audit_hits,self.audit_window,self.exploration_every,self.quadrature_nodes)):
            raise ValueError("Cadences and quadrature size must be positive integers")
        if self.audit_hits>self.audit_window or self.quadrature_nodes>128:
            raise ValueError("Invalid diagnostic window or quadrature size")
        if not math.isfinite(self.audit_z) or self.audit_z<=0 or not math.isfinite(self.parameter_weight) or self.parameter_weight<0:
            raise ValueError("Invalid diagnostic or utility parameter")
        if not .5 < self.decision_threshold < 1:
            raise ValueError("Invalid decision threshold")

    def to_dict(self):
        return asdict(self)
