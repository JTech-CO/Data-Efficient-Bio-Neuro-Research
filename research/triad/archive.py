"""Lossless JSON event de-duplication for distributing the synthetic experiment logs.

No observations, model parameters, histories, scores or decisions are removed.
Deterministically reconstructible event hashes and indices are stored once via
whole-record and chain-tip digests. This is integrity checking, not authentication.
"""
from __future__ import annotations
import argparse, copy, gzip, hashlib, json
from pathlib import Path
from research.closed_loop.contracts import digest, AuditTrail

FORMAT='triad-lossless-events-v1'

def pack(record: dict) -> dict:
    if 'archive_format' in record: raise ValueError('Already packed')
    r=copy.deepcopy(record)
    events=r.pop('events')
    if not AuditTrail.verify(events): raise ValueError('Invalid input chain')
    items=[]
    for e in events:
        p=dict(e['payload'])
        if e['type']=='measured': p.pop('record_digest')
        items.append([e['type'],p])
    return {'archive_format':FORMAT,'full_record_digest':digest(record),
            'event_chain_tip':events[-1]['hash'],'event_payloads':items,'record':r}

def unpack(item: dict) -> dict:
    if 'archive_format' not in item: return item
    if item['archive_format']!=FORMAT: raise ValueError('Unknown archive version')
    r=copy.deepcopy(item['record']);byid={o['record_id']:o for o in r['observations']};trail=AuditTrail()
    for typ,payload in item['event_payloads']:
        p=dict(payload)
        if typ=='measured': p['record_digest']=digest(byid[p['record']])
        trail.add(typ,p)
    if trail.events[-1]['hash']!=item['event_chain_tip']: raise ValueError('Chain-tip mismatch')
    r['events']=trail.events
    if digest(r)!=item['full_record_digest']: raise ValueError('Full record digest mismatch')
    return r

def iter_records(path):
    with gzip.open(path,'rt',encoding='utf-8') as f:
        for line in f: yield unpack(json.loads(line))

def convert(src,dst,restore=False):
    src,dst=Path(src),Path(dst)
    if dst.exists(): raise FileExistsError(dst)
    dst.parent.mkdir(parents=True,exist_ok=True);count=0
    with gzip.open(src,'rt',encoding='utf-8') as fi,gzip.open(dst,'wt',encoding='utf-8',compresslevel=9) as fo:
        for line in fi:
            item=json.loads(line);full=unpack(item)
            result=full if restore else pack(full)
            if not restore and unpack(result)!=full: raise AssertionError('Not lossless')
            fo.write(json.dumps(result,ensure_ascii=False,allow_nan=False,separators=(',',':'))+'\n');count+=1
    return {'records':count,'source_bytes':src.stat().st_size,'output_bytes':dst.stat().st_size,
            'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
            'output_sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'all_records_roundtrip_equal':True}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source');p.add_argument('destination');p.add_argument('--restore',action='store_true')
    a=p.parse_args();print(json.dumps(convert(a.source,a.destination,a.restore),indent=2))
if __name__=='__main__': main()
