"""Policies receive public design, training observations and fitted predictions only."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from .contracts import Query, Measurement
from .design import Design
from .models import GaussianProcess, LinearObservationModel

@dataclass(frozen=True)
class Proposal:
    query: Query
    score: float
    reason: str
    alternatives: tuple[dict, ...]


def propose(model: GaussianProcess | LinearObservationModel, records: tuple[Measurement, ...],
            design: Design, policy: str, remaining: float, rng: np.random.Generator,
            step: int, *, fallback: bool = False) -> Proposal | None:
    seen = {r.query.key for r in records}
    candidate_list = []
    for q in design.candidates():
        if q.key in seen or design.cost(q) > remaining + 1e-9:
            continue
        # Replicate 1 can only follow replicate 0 of the same declared query.
        if q.replicate == 1:
            first = Query(q.condition, q.time, q.readout, q.intervention, q.fidelity, 0, q.group)
            if first.key not in seen:
                continue
        if policy == "fixed_readout" and (q.readout != "sum" or q.intervention != "none"):
            continue
        if (policy == "hf_only" or fallback) and q.fidelity != "high":
            continue
        if design.family == "fidelity" and policy in ("multifidelity", "guarded") and step % 4 == 0 and q.fidelity != "high":
            continue
        candidate_list.append(q)
    queries = tuple(candidate_list)
    if not queries:
        return None
    costs = np.array([design.cost(q) for q in queries])
    _, variance = model.predict(queries)
    reason = policy
    if policy == "random" or (policy == "guarded" and step % 5 == 0 and design.family == "gp"):
        scores = rng.random(len(queries))
        reason = "random-exploration" if policy == "guarded" else "uniform-random-eligible-query"
    elif policy == "space_filling":
        xs = np.array([r.query.condition for r in records])
        scores = np.min(np.abs(np.array([q.condition for q in queries])[:, None] - xs), axis=1)
        reason = "farthest-observed-condition"
    elif policy in ("max_variance", "observation_variance"):
        scores = variance
        reason = "maximum-projected-latent-variance"
    else:
        scores = model.acquisition_information(queries, design) / costs
        reason = "hf-integrated-variance-reduction-per-cost" if design.family == "fidelity" and model.mode == "multifidelity" else "projected-information-gain-per-cost"
    if not np.isfinite(scores).all():
        raise ValueError("non-finite acquisition scores")
    # Stable tie breaking: low cost first, then declared grid order.
    order = sorted(range(len(queries)), key=lambda i: (-float(scores[i]), float(costs[i]), i))
    best = order[0]
    alternatives = tuple({"query_id": queries[i].key, "condition": queries[i].condition,
                          "readout": queries[i].readout, "intervention": queries[i].intervention,
                          "fidelity": queries[i].fidelity, "replicate": queries[i].replicate,
                          "score": float(scores[i]), "cost": float(costs[i])} for i in order[:5])
    return Proposal(queries[best], float(scores[best]), reason, alternatives)
