"""Immutable measurement contracts and semantic provenance checks.

Schema validation describes structure. These checks additionally enforce lineage,
partition isolation and the distinction between simulated evidence and biology.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Literal, Iterable
import hashlib
import json
import math

Split = Literal["train", "validation", "test"]

def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)

def digest(value: object) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()

@dataclass(frozen=True)
class Query:
    condition: float
    time: float = 1.0
    readout: str = "sum"
    intervention: str = "none"
    fidelity: str = "high"
    replicate: int = 0
    group: str = "synthetic-condition"

    def __post_init__(self) -> None:
        if not math.isfinite(self.condition) or not 0 <= self.condition <= 1:
            raise ValueError("condition must be finite and in [0, 1]")
        if not math.isfinite(self.time) or self.time != 1.0:
            raise ValueError("v1.1.0 implements one static time slice only")
        if type(self.replicate) is not int or not 0 <= self.replicate < 2:
            raise ValueError("replicate must be 0 or 1")
        if self.readout not in ("sum", "first") or self.intervention not in ("none", "attenuate_b"):
            raise ValueError("unsupported readout/intervention")
        if self.fidelity not in ("high", "low"):
            raise ValueError("unsupported fidelity")
        if not self.group:
            raise ValueError("group cannot be empty")

    @property
    def key(self) -> str:
        return digest(asdict(self))[:20]

    @property
    def condition_key(self) -> str:
        return f"{self.group}:{self.condition:.8f}"

@dataclass(frozen=True)
class Measurement:
    record_id: str
    query: Query
    value: float
    noise_sd: float
    cost: float
    split: Split
    group_id: str
    origin: str = "simulated"
    parent_ids: tuple[str, ...] = ()
    counts_as_new_biological_unit: bool = False
    producer_fit_split: str = "not_fitted"

    def __post_init__(self) -> None:
        if not self.record_id or not self.group_id:
            raise ValueError("record/group identity is required")
        if not all(math.isfinite(v) for v in (self.value, self.noise_sd, self.cost)):
            raise ValueError("non-finite measurement")
        if self.noise_sd <= 0 or self.cost <= 0:
            raise ValueError("noise and cost must be positive")
        if self.split not in ("train", "validation", "test"):
            raise ValueError("unsupported split")
        if self.origin not in ("simulated", "generated", "imputed", "derived"):
            raise ValueError("This harness does not ingest real biological measurements")
        if self.counts_as_new_biological_unit:
            raise ValueError("synthetic records cannot become biological units")
        if self.producer_fit_split not in ("not_fitted", "train"):
            raise ValueError("producer may not fit validation or test data")
        if self.origin != "simulated" and not self.parent_ids:
            raise ValueError("derived values must retain parents")

    def legacy_record(self) -> dict:
        """Compatible with the unchanged v1.0 observation JSON Schema."""
        return {"record_id": self.record_id, "kind": self.origin,
                "independent_group_id": self.group_id,
                "counts_as_new_biological_unit": False, "split": self.split,
                "unit": "dimensionless", "value": self.value,
                "source_uri": "simulator://closed-loop/v1.1.0/" + self.record_id,
                "license_status": "original-synthetic-output-see-repository-license",
                "parent_ids": list(self.parent_ids),
                "producer": {"artifact_id": "closed-loop-synthetic-oracle", "version": "1.1.0",
                             "fit_split": self.producer_fit_split, "seed": None}}

class Ledger:
    def __init__(self) -> None:
        self._records: dict[str, Measurement] = {}
        self._groups: dict[str, str] = {}
        self._query_keys: set[tuple[str, str]] = set()

    def append(self, record: Measurement) -> None:
        if record.record_id in self._records:
            raise ValueError("duplicate record identity")
        if (record.split, record.query.key) in self._query_keys:
            raise ValueError("duplicate query; increment the declared replicate")
        if record.group_id in self._groups and self._groups[record.group_id] != record.split:
            raise ValueError("group appears in more than one partition")
        for parent in record.parent_ids:
            if parent not in self._records:
                raise ValueError("unresolved parent identity")
            if self._records[parent].split != record.split:
                raise ValueError("lineage crosses a partition boundary")
        self._records[record.record_id] = record
        self._groups[record.group_id] = record.split
        self._query_keys.add((record.split, record.query.key))

    def view(self, split: Split, *, for_fit: bool = False) -> tuple[Measurement, ...]:
        if for_fit and split != "train":
            raise ValueError("only train records may be fitted")
        records = tuple(r for r in self._records.values() if r.split == split)
        if for_fit:
            ensure_fit_records(records)
        return records

    def budget(self) -> dict:
        records = list(self._records.values())
        return {"n_real_measurements": 0, "n_independent_biological_groups": 0,
                "n_simulated_measurements": len(records),
                "n_synthetic_condition_groups": len(self._groups),
                "train_cost": sum(r.cost for r in records if r.split == "train"),
                "validation_cost": sum(r.cost for r in records if r.split == "validation"),
                "test_cost": sum(r.cost for r in records if r.split == "test"),
                "total_measurement_cost": sum(r.cost for r in records),
                "cost_unit": "synthetic_measurement_unit", "annotation_minutes": 0,
                "n_pretraining_examples": 0}

    def records(self) -> list[dict]:
        return [{**asdict(r), "parent_ids": list(r.parent_ids)} for r in self._records.values()]

def ensure_fit_records(records: Iterable[Measurement]) -> None:
    for record in records:
        if record.split != "train":
            raise ValueError("model attempted to fit a non-training record")
        if record.origin != "simulated":
            raise ValueError("pseudo/derived values are not independent fit evidence in this harness")

class AuditTrail:
    """Hash-linked event log: accidental tampering detectable, not a signed attestation."""
    def __init__(self) -> None:
        self.events: list[dict] = []

    def add(self, event_type: str, payload: dict) -> None:
        event = {"index": len(self.events), "type": event_type, "payload": payload,
                 "previous": self.events[-1]["hash"] if self.events else "0" * 64}
        event["hash"] = digest(event)
        self.events.append(event)

    @staticmethod
    def verify(events: list[dict]) -> bool:
        previous = "0" * 64
        for index, event in enumerate(events):
            body = {key: value for key, value in event.items() if key != "hash"}
            if body.get("index") != index or body.get("previous") != previous or digest(body) != event.get("hash"):
                return False
            previous = event["hash"]
        return True
