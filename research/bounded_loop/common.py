"""Deterministic records and explicit evidence roles; no external data adapter."""
from __future__ import annotations
import hashlib, json, math
from pathlib import Path
from typing import Any
import numpy as np
from scipy import stats
VERSION = "1.4.0-research.1"

def native(x: Any) -> Any:
    if isinstance(x, dict): return {str(k): native(v) for k,v in x.items()}
    if isinstance(x, (list,tuple)): return [native(v) for v in x]
    if isinstance(x, np.ndarray): return native(x.tolist())
    if isinstance(x, np.generic): return native(x.item())
    if isinstance(x, float) and not math.isfinite(x): raise ValueError("Non-finite number; represent unbounded intervals explicitly")
    return x

def canonical(x: Any) -> bytes:
    return json.dumps(native(x),sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def digest(x: Any) -> str: return hashlib.sha256(canonical(x)).hexdigest()
def rng(*parts: Any) -> np.random.Generator:
    return np.random.default_rng(int.from_bytes(hashlib.sha256(canonical(parts)).digest()[:8],"little"))
def write_json(path: Path, obj: Any, overwrite: bool=False) -> None:
    path=Path(path)
    if path.exists() and not overwrite: raise FileExistsError(f"Refusing to overwrite {path}")
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(native(obj),ensure_ascii=False,indent=2,allow_nan=False)+"\n",encoding="utf-8")
def read_json(path: Path) -> Any: return json.loads(Path(path).read_text(encoding="utf-8"))

def group(key: str, role: str, x: float, values: Any, unit_cost: float=1., **metadata: Any) -> dict:
    if role not in ("fit","audit","final"): raise ValueError("Unknown role")
    vals=np.asarray(values,dtype=float)
    if vals.ndim!=1 or len(vals)<1 or not np.isfinite(vals).all(): raise ValueError("Invalid measurements")
    if not np.isfinite(x) or unit_cost<=0: raise ValueError("Invalid measurement condition")
    return native(dict(key=key,role=role,x=round(float(x),12),source="simulated",replicate_kind="technical",values=vals,
        n=len(vals),unit_cost=unit_cost,cost=len(vals)*unit_cost,**metadata))

def seal(study: str, scenario: str, seed: int, bank: str, groups: list, payload: dict) -> dict:
    keys=[g['key'] for g in groups]
    if len(keys)!=len(set(keys)): raise ValueError("Duplicate group identity")
    train=[g for g in groups if g['role']!='final']
    events=[];previous="0"*64
    for phase in ('acquisition_complete','model_frozen','final_released'):
        e={'phase':phase,'previous':previous,'data_digest':digest(train if phase!='final_released' else groups)}
        e['hash']=digest(e);previous=e['hash'];events.append(e)
    out=native(dict(version=VERSION,study=study,scenario=scenario,seed=seed,bank=bank,
        source="simulated",real_world_authorized=False,causal_source_identified=False,
        groups=groups,evidence_digest=digest(groups),events=events,**payload))
    out['record_digest']=digest(out)
    return out

def validate(record: dict) -> int:
    r=dict(record);d=r.pop('record_digest')
    assert digest(r)==d
    assert r['source']=='simulated' and r['real_world_authorized'] is False
    assert r['causal_source_identified'] is False
    assert digest(r['groups'])==r['evidence_digest']
    assert len({g['key'] for g in r['groups']})==len(r['groups'])
    last='0'*64
    assert [x['phase'] for x in r['events']]==['acquisition_complete','model_frozen','final_released']
    for e in r['events']:
        h=dict(e);dh=h.pop('hash');assert digest(h)==dh and e['previous']==last;last=dh
    train=[g for g in r['groups'] if g['role']!='final']
    assert r['events'][1]['data_digest']==digest(train)
    assert r['events'][2]['data_digest']==digest(r['groups'])
    for g in r['groups']:
        assert g['source']=='simulated' and g['replicate_kind']=='technical'
        assert g['n']==len(g['values']) and g['n']>0
        assert np.isfinite(g['values']).all()
        assert abs(g['cost']-g['n']*g['unit_cost'])<1e-8
    if 'costs' in r:
        for role in ['fit','audit','final']:
            assert abs(sum(g['cost'] for g in r['groups'] if g['role']==role)-r['costs'].get(role,0))<1e-7
    return sum(g['n'] for g in r['groups'])

def costs(groups: list) -> dict:
    c={role:sum(g['cost'] for g in groups if g['role']==role) for role in ('fit','audit','final')}
    c['total']=sum(c.values());return c

def wilson(k: int,n: int,alpha: float=.05) -> list:
    if n==0:return [None,None]
    z=stats.norm.ppf(1-alpha/2);p=k/n;den=1+z*z/n
    centre=(p+z*z/(2*n))/den;half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [float(centre-half),float(centre+half)]

def normal_metrics(mean, var_mean, var_noise, truth, observed) -> dict:
    mean=np.asarray(mean);vv=np.maximum(np.asarray(var_mean),1e-12);vn=np.maximum(np.asarray(var_noise),1e-12)
    vp=vv+vn;truth=np.asarray(truth);observed=np.asarray(observed)
    z=stats.norm.ppf(.975);lo=mean-z*np.sqrt(vp);hi=mean+z*np.sqrt(vp)
    latentlo=mean-z*np.sqrt(vv);latenthi=mean+z*np.sqrt(vv)
    return native({'rmse':np.sqrt(np.mean((mean-truth)**2)),
       'nll':np.mean(.5*np.log(2*np.pi*vp)+.5*(observed-mean)**2/vp),
       'observed_coverage':np.mean((observed>=lo)&(observed<=hi)),
       'observed_width':np.mean(hi-lo),
       'latent_coverage':np.mean((truth>=latentlo)&(truth<=latenthi)),
       'latent_width':np.mean(latenthi-latentlo),
       'interval_score':np.mean(hi-lo+40*np.maximum(lo-observed,0)+40*np.maximum(observed-hi,0))})
