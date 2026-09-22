from __future__ import annotations
import ast, copy, json, math, threading, urllib.request, urllib.error
from pathlib import Path
import numpy as np
import pytest
from scipy.integrate import solve_ivp
from jsonschema import Draft202012Validator
from research_lab.contracts import Query,RunConfig,ObservationAssumptions,SCENARIOS,POLICIES
from research_lab.ledger import EvidenceLedger,TrainingDatum
from research_lab.models import MechanisticEnsemble,PredictiveGP,features,mixture_interval
from research_lab.design import candidate_queries,initial_queries,evaluation_queries
from research_lab.diagnostics import AuditGate
from research_lab.simulator import SyntheticOracle
from research_lab.engine import execute
from research_lab.runner import run_experiment,save_json
from research_lab.server import make_server
ROOT=Path(__file__).resolve().parents[2]

@pytest.mark.parametrize('kwargs',[{'condition':float('nan')},{'condition':4},{'time':-1},{'readout':'RNA'},
                                   {'fidelity':'low'},{'replicate':-1},{'intervention':.2}])
def test_invalid_query(kwargs):
    d=dict(condition=1.,time=1.,readout='aggregate');d.update(kwargs)
    with pytest.raises(ValueError):Query(**d)

@pytest.mark.parametrize('kwargs',[{'budget':float('nan')},{'budget':4},{'budget':100},{'scenario':'clinical'},
                                   {'seed':-1},{'seed':True},{'observer':'oracle'},{'audit_hits':4},
                                   {'quadrature_nodes':1000},{'policy':'GPT'},{'audit_z':float('inf')}])
def test_invalid_config(kwargs):
    with pytest.raises(ValueError):RunConfig(**kwargs)

def test_legacy_schema_compatibility():
    validator=Draft202012Validator(json.loads((ROOT/'schemas/observation.schema.json').read_text()))
    o=SyntheticOracle('identifiable',0)
    for i,role in enumerate(('train','audit','test')):
        validator.validate(o.measure(Query(.4,.4,'aggregate'),role,i))

def test_ledger_append_hash_immutable_exports():
    l=EvidenceLedger();o=SyntheticOracle('identifiable',0);q=Query(.4,.4,'aggregate')
    r=o.measure(q,'train',0);l.append(r,q,'train');r['value']=999
    assert l.training()[0].value!=999
    exported=l.export();assert l.verify(exported)
    exported[0]['observation']['value']=42
    assert not l.verify(exported)
    assert l.verify(l.export())
    with pytest.raises(ValueError):l.append(o.measure(q,'train',0),q,'train')

@pytest.mark.parametrize('mutation',[{'kind':'real'},{'kind':'generated'},{'counts_as_new_biological_unit':True},
                                    {'split':'test'},{'parent_ids':['train-0000']},{'value':float('nan')}])
def test_provenance_rejection(mutation):
    q=Query(.4,.4,'aggregate');r=SyntheticOracle('identifiable',0).measure(q,'train',0);r.update(mutation)
    with pytest.raises(ValueError):EvidenceLedger().append(r,q,'train')

def test_audit_and_test_do_not_enter_fit():
    l=EvidenceLedger();o=SyntheticOracle('identifiable',0);q=Query(.4,.4,'aggregate')
    for i,role in enumerate(('train','audit','test')):l.append(o.measure(q,role,i),q,role)
    assert len(l.training())==1
    assert l.cost==3

def test_analytic_ode_matches_numerical_solution():
    o=SyntheticOracle('identifiable',0);a,b=o.theta;x=1.1;u=1.
    def f(t,z):return [-z[0],-.45*z[1]+.45*.8*a*u*x]
    ts=np.array([.4,1.2,2.4]);sol=solve_ivp(f,(0,2.4),[a*x*(1-u),b*x],t_eval=ts,rtol=1e-10,atol=1e-11)
    actual=o.latent([Query(x,float(t),'aggregate',u) for t in ts])
    np.testing.assert_allclose(actual,sol.y.T,atol=1e-9)

def test_model_features_match_clean_simulation():
    for seed in (0,1):
        o=SyntheticOracle('identifiable',seed);qs=candidate_queries()
        X,b=features(qs,o.true_model,ObservationAssumptions())
        np.testing.assert_allclose(X@o.theta+b,o.clean(qs),atol=1e-12)

def test_no_intervention_mechanisms_equivalent():
    o=SyntheticOracle('observational_equivalence',0);data=[]
    for i,q in enumerate(candidate_queries(True)):
        r=o.measure(q,'train',i);data.append(TrainingDatum(q,r['value'],q.nominal_sigma,r['record_id']))
    m=MechanisticEnsemble(ObservationAssumptions(),data)
    np.testing.assert_allclose(m.weights,[.5,.5],atol=1e-10)
    mi,_=m.information(candidate_queries(True))
    assert np.max(mi)<1e-10

def test_bayesian_update_covariance_psd():
    q=Query(.9,1.2,'aggregate');m=MechanisticEnsemble(ObservationAssumptions(),[TrainingDatum(q,.8,q.nominal_sigma,'r')])
    for cov in m.covariances:
        assert np.linalg.eigvalsh(cov).min()>0
        assert np.trace(cov)<.72
    assert abs(sum(m.weights)-1)<1e-10

def test_information_nonnegative_bounded_and_quadrature_stable():
    m=MechanisticEnsemble(ObservationAssumptions());qs=candidate_queries()
    mi,pi=m.information(qs,20);mi2,_=m.information(qs,80)
    assert np.min(mi)>=0 and np.max(mi)<=math.log(2)+1e-10
    assert np.min(pi)>=0
    assert np.max(np.abs(mi-mi2))<.015

def test_identical_mixture_matches_gaussian_quantiles():
    lo,hi=mixture_interval(np.array([[2.],[2.]]),np.array([[.25],[.25]]),np.array([.3,.7]))
    np.testing.assert_allclose([lo[0],hi[0]],[2-.5*1.95996398454,2+.5*1.95996398454],atol=1e-9)

def test_gp_variance_and_noise_scope():
    qs=candidate_queries()[:5];d=[TrainingDatum(q,.5,q.nominal_sigma,str(i)) for i,q in enumerate(qs)]
    gp=PredictiveGP(ObservationAssumptions(),d)
    m,v=gp.predict(qs,False);m2,v2=gp.predict(qs,True)
    assert np.min(v)>0 and np.max(v)<1
    np.testing.assert_allclose(v2-v,[q.nominal_sigma**2 for q in qs],atol=1e-10)
    assert np.isfinite(m).all()

def test_gate_sticky_and_fails_to_claim_formal_test():
    g=AuditGate();g.observe(10,0,1,'a');assert not g.suspect
    g.observe(10,0,1,'b');assert g.suspect
    for i in range(5):g.observe(0,0,1,str(i))
    assert g.suspect and 'not a sequentially' in g.history[-1]['scope']

@pytest.mark.parametrize('policy',POLICIES)
def test_budget_approval_history_and_no_duplicates(policy):
    c=RunConfig(policy=policy,budget=16);o=SyntheticOracle(c.scenario,c.seed);r=execute(c,o.measure)
    assert r['total_cost']<=c.budget
    assert r['information_budget']['real_measurements']==r['information_budget']['biological_units']==0
    assert all(not s['approval']['real_world_authorized'] for s in r['history'])
    keys=[s['approval']['query_key'] for s in r['history']]
    assert len(keys)==len(set(keys))
    assert EvidenceLedger.verify(r['evidence'])
    assert r['history'][-1]['fit_n']==sum(s['phase']=='train' for s in r['history'])
    json.dumps(r,allow_nan=False)

@pytest.mark.parametrize('scenario',SCENARIOS)
def test_scenarios_execute_finite(scenario):
    r=run_experiment(RunConfig(scenario=scenario))
    assert len(r['evaluation']['curves'])==len(r['history'])
    assert r['evaluation']['access'].startswith('post_run')
    assert 0<=r['evaluation']['final']['id']['observation_95_coverage']<=1
    assert r['evaluation']['final']['id']['observation_95_width']>0
    assert not any(s['evidence_status']=='mechanism-supported' for s in r['history'])
    json.dumps(r,allow_nan=False)

def test_observational_equivalence_abstention():
    r=run_experiment(RunConfig(scenario='observational_equivalence'))
    assert r['evaluation']['final']['abstained']
    assert r['stop_reason']=='candidate_pool_exhausted'
    assert r['evaluation']['final']['true_candidate_weight']==pytest.approx(.5)

def test_reproducible_run_and_evaluation_does_not_select():
    c=RunConfig(budget=12);o=SyntheticOracle(c.scenario,c.seed)
    a=execute(c,o.measure);b=run_experiment(c);d=run_experiment(c)
    assert a['acquisition_sha256']==b['acquisition_sha256']==d['acquisition_sha256']
    assert b==d
    assert 'evaluation' not in a

def test_information_boundary_imports():
    for stem in ('models','policies','contracts','diagnostics','ledger'):
        tree=ast.parse((ROOT/f'research_lab/{stem}.py').read_text())
        imports=[n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)]
        assert not any(m and ('simulator' in m or 'evaluation' in m) for m in imports)

def test_query_replay_noise_shared_across_policies():
    o=SyntheticOracle('identifiable',3);q=Query(.4,.4,'aggregate')
    assert o.observed_value(q,'train')==SyntheticOracle('identifiable',3).observed_value(q,'train')
    assert o.observed_value(q,'train')!=o.observed_value(q,'audit')

def test_save_prevents_unintentional_overwrite(tmp_path):
    p=tmp_path/'run.json';save_json(p,{'a':1})
    with pytest.raises(FileExistsError):save_json(p,{'a':2})
    save_json(p,{'a':3},True);assert json.loads(p.read_text())=={'a':3}

@pytest.fixture
def local_server():
    s=make_server(0);t=threading.Thread(target=s.serve_forever,daemon=True);t.start()
    yield f'http://127.0.0.1:{s.server_address[1]}'
    s.shutdown();s.server_close();t.join(timeout=3)

def request_json(url,body=None,headers=None):
    req=urllib.request.Request(url,data=None if body is None else json.dumps(body).encode(),
                               headers=headers or ({'Content-Type':'application/json'} if body is not None else {}))
    with urllib.request.urlopen(req,timeout=15) as res:return json.load(res)

def test_local_server_status_and_run(local_server):
    assert request_json(local_server+'/api/status')['real_data_enabled'] is False
    r=request_json(local_server+'/api/run',{'budget':8,'seed':3})
    assert r['research_only'] and r['total_cost']<=8

@pytest.mark.parametrize('body',[{'scenario':'clinical'},{'seed':-1},{'out':'../../test'},{'budget':100},['upload']])
def test_server_invalid_body(local_server,body):
    with pytest.raises(urllib.error.HTTPError) as e:request_json(local_server+'/api/run',body)
    assert e.value.code==400

def test_server_cross_origin_rejection(local_server):
    with pytest.raises(urllib.error.HTTPError) as e:
        request_json(local_server+'/api/run',{}, {'Content-Type':'application/json','Origin':'https://external.example'})
    assert e.value.code==403
