"""Assumptions are revisable claims, not measured observations or executable actions."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from .design import Design

@dataclass(frozen=True)
class Assumption:
    assumption_id: str
    statement: str
    status: str
    basis: str
    checked_record_ids: tuple[str, ...]
    limitation: str


def register(design: Design, model, gate: dict, diagnostic_ids: tuple[str, ...]) -> list[dict]:
    challenged = any(r != "data-design-rank-deficient" for r in gate["reasons"])
    status = "challenged-not-localized" if challenged else "not-rejected-on-reused-diagnostic"
    rows = [Assumption("measurement-noise", "Declared independent Gaussian measurement noise with known scale",
                       "declared-not-estimated", "synthetic design contract", (),
                       "No real instrument calibration or biological-noise validation"),
            Assumption("observation-operator", "The readout/intervention operator maps latent state to measured units",
                       status, "reused held-out diagnostic residuals", diagnostic_ids,
                       "Residual checks do not separate operator error from mechanism error")]
    if design.family == "linear":
        rows.append(Assumption("parameter-separation", "Data distinguish a and b, not merely a+b",
                               "rank-two-under-assumed-operator" if model.rank == 2 else "not-identified",
                               "rank of likelihood design, excluding prior precision", tuple(r.record_id for r in model.records),
                               "Full rank does not establish the correctness of the assumed operator"))
    elif design.family == "committee":
        rows.append(Assumption("candidate-library", "The true response is represented by declared candidate A or B",
                               status, "predictive discrepancy, not posterior concentration alone", diagnostic_ids,
                               "A posterior probability near one can still select a wrong model when truth is outside the library"))
    else:
        rows.append(Assumption("kernel-smoothness", f"Fixed GP kernel family and length {model.length:g} describe the response",
                               status, "conditional predictions and reused diagnostic checks", diagnostic_ids,
                               "Unobserved sharp features may evade both acquisition and diagnostic points"))
    if design.family == "fidelity":
        rows.append(Assumption("fidelity-relation", "LF and HF can be coupled through f_H=f_L+delta with the declared GP discrepancy",
                               "excluded-after-fallback" if model.mode == "high_only" else status,
                               "paired training observations and independent diagnostic selection", diagnostic_ids,
                               "The development gate can miss negative transfer or reject a useful source"))
    return [{**asdict(row), "checked_record_ids": list(row.checked_record_ids)} for row in rows]
