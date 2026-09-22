"""The narrow extension seam. Only SyntheticOracle currently implements it.

A future retrospective dataset adapter must retain group partitions and record
provenance. It must not silently impersonate a prospective experiment.
"""
from typing import Protocol
from .contracts import Query, Measurement

class MeasurementAdapter(Protocol):
    def observe(self, q: Query, split: str) -> Measurement:
        ...
