"""New action/observation types; the v1.1 contracts remain unchanged.

The runner owns the synthetic oracle. Inference and policies receive only a
PublicDesign and immutable measurements, never World truth or final outcomes.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from collections import defaultdict
import math
import numpy as np
from research.closed_loop.contracts import digest, AuditTrail

KINDS = ("sample", "reference", "intervention")
SPLITS = ("fit", "audit", "test")
COSTS = {"sample": 1.0, "reference": 1.5, "intervention": 1.8}

@dataclass(frozen=True)
class Action:
    kind: str
    x: float
    n: int = 2

    def __post_init__(self):
        if self.kind not in KINDS or not math.isfinite(self.x) or not -1 <= self.x <= 1:
            raise ValueError("synthetic action requires known kind and x in [-1,1]")
        if type(self.n) is not int or self.n not in (1, 2, 4):
            raise ValueError("technical batch size must be 1, 2 or 4")

    @property
    def key(self):
        # Batch size does not define a new experimental condition.
        return f"{self.kind}:{self.x:.8f}"

    @property
    def cost(self):
        return COSTS[self.kind] * self.n

    @property
    def u(self):
        return int(self.kind == "intervention")

@dataclass(frozen=True)
class PublicDesign:
    basis: str
    nominal_sd: float = 0.12

    def __post_init__(self):
        if self.basis not in ("linear", "tanh", "cubic"):
            raise ValueError("unknown public basis")
        if not math.isfinite(self.nominal_sd) or self.nominal_sd <= 0:
            raise ValueError("positive nominal noise required")

    def phi(self, x):
        x = np.asarray(x, dtype=float)
        if self.basis == "linear": return x
        if self.basis == "tanh": return np.tanh(1.5*x) / np.tanh(1.5)
        return 0.65*x + 0.35*x**3

    def psi(self, x):
        return 1 + 0.5*self.phi(x)**2

    def row(self, a: Action):
        if a.kind == "reference":
            return np.array([0., 0., 0., a.x, 1.])
        return np.array([1., float(self.phi(a.x)), a.u*float(self.psi(a.x)), 0., 0.])

@dataclass(frozen=True)
class Observation:
    record_id: str
    action: Action
    value: float
    split: str
    replicate_index: int
    parent_id: str | None = None
    origin: str = "simulated"
    real_world_authorized: bool = False

    def __post_init__(self):
        if self.split not in SPLITS or self.origin != "simulated" or self.real_world_authorized:
            raise ValueError("this module accepts simulated observations only")
        if not self.record_id or not math.isfinite(self.value) or self.replicate_index < 0:
            raise ValueError("invalid observation")

    @property
    def cost(self):
        return COSTS[self.action.kind]

    def to_dict(self):
        d = asdict(self)
        d.update(cost=self.cost, counts_as_new_biological_unit=False,
                 measured_quantity="dimensionless_sensor_response")
        return d

class Ledger:
    def __init__(self):
        self._records: list[Observation] = []
        self._ids: set[str] = set()
        self._keys: set[tuple] = set()

    def append(self, obs: Observation):
        key = (obs.split, obs.action.key, obs.replicate_index)
        if obs.record_id in self._ids or key in self._keys:
            raise ValueError("duplicate observation; replicates need a new index")
        if obs.parent_id is not None:
            parent = next((r for r in self._records if r.record_id == obs.parent_id), None)
            if parent is None or parent.split != obs.split or parent.action.key != obs.action.key:
                raise ValueError("unresolved or cross-split replicate parent")
        self._records.append(obs); self._ids.add(obs.record_id); self._keys.add(key)

    def view(self, split):
        if split not in SPLITS: raise ValueError("unknown split")
        return tuple(r for r in self._records if r.split == split)

    def counts(self):
        out = {f"{s}_cost": sum(r.cost for r in self.view(s)) for s in SPLITS}
        out.update(n_simulated=len(self._records), n_biological_units=0,
                   cost_unit="synthetic_measurement_unit")
        out["acquisition_cost"] = out["fit_cost"] + out["audit_cost"]
        out["all_measurement_cost"] = out["acquisition_cost"] + out["test_cost"]
        return out

    def export(self):
        return [r.to_dict() for r in self._records]

def pure_error(records):
    """Within-condition residual SSE and df; technical repeats are not subjects."""
    groups = defaultdict(list)
    for r in records: groups[r.action.key].append(r.value)
    sse, df = 0., 0
    for values in groups.values():
        a = np.asarray(values)
        sse += float(np.sum((a-a.mean())**2)); df += len(a)-1
    return sse, df, len(groups)

def require_fit(records):
    if not records: raise ValueError("no fit records")
    if any(r.split != "fit" or r.origin != "simulated" for r in records):
        raise ValueError("audit/test/derived records must not enter parameter fitting")
