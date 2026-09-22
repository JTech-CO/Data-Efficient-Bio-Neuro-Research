"""Append-only evidence ledger with provenance and split boundaries."""
from __future__ import annotations
import copy, hashlib, json, math
from dataclasses import dataclass
from .contracts import Query

@dataclass(frozen=True)
class TrainingDatum:
    query: Query
    value: float
    sigma: float
    record_id: str

class EvidenceLedger:
    def __init__(self):
        self._events: list[dict] = []
        self._ids: set[str] = set()
        self._last_hash = "0"*64

    def append(self, record: dict, query: Query, role: str) -> None:
        if role not in ("train", "audit", "test", "derived"):
            raise ValueError("Unknown evidence role")
        if record.get("record_id") in self._ids:
            raise ValueError("Duplicate evidence id")
        if not record.get("record_id"):
            raise ValueError("Missing evidence id")
        if record.get("kind") != "simulated":
            raise ValueError("Research runner accepts simulator evidence only, never real/generated data")
        if record.get("counts_as_new_biological_unit") is not False:
            raise ValueError("Synthetic evidence cannot count as a biological unit")
        expected={"train":"train","audit":"validation","test":"test","derived":"train"}[role]
        if record.get("split") != expected:
            raise ValueError("Role/split mismatch")
        if not isinstance(record.get("value"),(int,float)) or not math.isfinite(record['value']):
            raise ValueError("Observation must be finite")
        if record.get("parent_ids"):
            raise ValueError("Fresh simulator observations must not masquerade as derivatives")
        if record.get("producer",{}).get("fit_split") != "not_fitted":
            raise ValueError("Simulator provenance is not independently generated")
        body={"observation":copy.deepcopy(record),"query":query.to_dict(),"role":role,
              "cost":query.cost,"nominal_sigma":query.nominal_sigma,"previous_hash":self._last_hash}
        digest=hashlib.sha256(json.dumps(body,sort_keys=True,allow_nan=False).encode()).hexdigest()
        body["hash"]=digest
        self._events.append(body); self._ids.add(record['record_id']); self._last_hash=digest

    def training(self) -> tuple[TrainingDatum,...]:
        return tuple(TrainingDatum(Query(**e['query']),e['observation']['value'],e['nominal_sigma'],e['observation']['record_id'])
                     for e in self._events if e['role']=='train')

    def export(self) -> list[dict]:
        return copy.deepcopy(self._events)

    @property
    def cost(self) -> float:
        return round(sum(e['cost'] for e in self._events),8)

    @staticmethod
    def verify(events: list[dict]) -> bool:
        prev="0"*64; ids=set()
        for e in events:
            payload={k:v for k,v in e.items() if k!='hash'}
            if payload.get('previous_hash')!=prev:
                return False
            rid=payload.get('observation',{}).get('record_id')
            if not rid or rid in ids:
                return False
            ids.add(rid)
            digest=hashlib.sha256(json.dumps(payload,sort_keys=True,allow_nan=False).encode()).hexdigest()
            if digest!=e.get('hash'):
                return False
            prev=digest
        return True
