"""Model-discrepancy alerts use only prequential audit observations."""
from __future__ import annotations
from collections import deque
import math

class AuditGate:
    def __init__(self,z_threshold=2.5,hits=2,window=3):
        self.threshold=z_threshold; self.hits=hits
        self.recent=deque(maxlen=window);self.suspect=False;self.history=[]

    def observe(self,value,mean,variance,record_id):
        if not all(math.isfinite(v) for v in (value,mean,variance)) or variance<=0:
            raise ValueError('Invalid prequential prediction')
        z=(value-mean)/math.sqrt(variance)
        exceeded=abs(z)>self.threshold
        self.recent.append(exceeded)
        # Sticky within a run: review cannot silently erase an earlier alert.
        self.suspect=self.suspect or sum(self.recent)>=self.hits
        item={'record_id':record_id,'z':z,'threshold':self.threshold,'exceeded':exceeded,'suspect':self.suspect,
              'scope':'screening heuristic; not a sequentially calibrated hypothesis test'}
        self.history.append(item)
        return item
