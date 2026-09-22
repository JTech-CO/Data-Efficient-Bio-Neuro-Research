from __future__ import annotations
import copy
from dataclasses import replace, asdict
import inspect
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import numpy as np
from jsonschema import Draft202012Validator

from research.closed_loop.contracts import Query, Measurement, Ledger, AuditTrail, ensure_fit_records
from research.closed_loop.design import get_design, SCENARIOS, policies_for
from research.closed_loop.simulator import SyntheticOracle
from research.closed_loop.models import GaussianProcess, LinearObservationModel, rbf
from research.closed_loop.committee import MechanismCommittee
from research.closed_loop.acquisition import propose
from research.closed_loop.evaluation import FinalEvaluator, metrics
from research.closed_loop.runner import RunConfig, run_experiment, audit_run, save_run, load_run
from research.closed_loop.server import LabServer

ROOT = Path(__file__).resolve().parents[2]

def samples(scenario='confounded'):
    oracle = SyntheticOracle(scenario, 0)
    return tuple(oracle.observe(q, 'train') for q in oracle.design.initial())

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.record = samples()[0]

    def test_query_range(self):
        for x in [float('nan'), float('inf'), -0.1, 1.1]:
            with self.assertRaises(ValueError): Query(x)

    def test_unsupported_time(self):
        with self.assertRaises(ValueError): Query(.5, time=2)

    def test_unknown_readout(self):
        with self.assertRaises(ValueError): Query(.5, readout='new-sensor')

    def test_replicate_range(self):
        with self.assertRaises(ValueError): Query(.5, replicate=2)

    def test_measurement_frozen(self):
        with self.assertRaises(Exception): self.record.value = 3

    def test_finite_observation(self):
        with self.assertRaises(ValueError): replace(self.record, value=float('nan'))

    def test_positive_noise(self):
        with self.assertRaises(ValueError): replace(self.record, noise_sd=0)

    def test_no_real_data_ingest(self):
        with self.assertRaises(ValueError): replace(self.record, origin='real')

    def test_no_biological_promotion(self):
        with self.assertRaises(ValueError): replace(self.record, counts_as_new_biological_unit=True)

    def test_fitted_test_producer(self):
        with self.assertRaises(ValueError): replace(self.record, producer_fit_split='test')

    def test_derived_parent_required(self):
        with self.assertRaises(ValueError): replace(self.record, origin='generated')

    def test_duplicate_identity(self):
        ledger = Ledger(); ledger.append(self.record)
        with self.assertRaises(ValueError): ledger.append(self.record)

    def test_duplicate_query_with_new_record_id(self):
        ledger = Ledger(); ledger.append(self.record)
        with self.assertRaises(ValueError): ledger.append(replace(self.record, record_id='new'))

    def test_cross_group_split(self):
        ledger = Ledger(); ledger.append(self.record)
        with self.assertRaises(ValueError): ledger.append(replace(self.record, record_id='test-new', split='test'))

    def test_unresolved_parent(self):
        ledger=Ledger()
        with self.assertRaises(ValueError): ledger.append(replace(self.record, origin='generated', parent_ids=('missing',)))

    def test_parent_cross_split(self):
        ledger=Ledger(); ledger.append(self.record)
        child=replace(self.record, record_id='child', query=Query(.51), split='test', group_id='different', origin='derived', parent_ids=(self.record.record_id,))
        with self.assertRaises(ValueError): ledger.append(child)

    def test_generated_not_fit_evidence(self):
        ledger=Ledger();ledger.append(self.record)
        child=replace(self.record, record_id='child', query=Query(.52), origin='generated', parent_ids=(self.record.record_id,))
        ledger.append(child)
        with self.assertRaises(ValueError): ledger.view('train', for_fit=True)

    def test_test_cannot_be_fit(self):
        with self.assertRaises(ValueError): ensure_fit_records((replace(self.record, split='test'),))

    def test_budget_no_biology(self):
        ledger=Ledger();ledger.append(self.record)
        self.assertEqual(ledger.budget()['n_independent_biological_groups'],0)
        self.assertEqual(ledger.budget()['n_real_measurements'],0)

    def test_legacy_schema_compatibility(self):
        schema=json.loads((ROOT/'schemas/observation.schema.json').read_text())
        Draft202012Validator(schema).validate(self.record.legacy_record())

    def test_hash_chain_tamper(self):
        trail=AuditTrail();trail.add('start',{'a':1});trail.add('finish',{'b':2})
        self.assertTrue(AuditTrail.verify(trail.events))
        trail.events[0]['payload']['a']=9
        self.assertFalse(AuditTrail.verify(trail.events))

class ModelTests(unittest.TestCase):
    def test_kernel_psd(self):
        x=np.linspace(0,1,10);k=rbf(x,x,.2)
        self.assertGreater(np.linalg.eigvalsh(k).min(),0)

    def test_gp_noise_reduces_confidence(self):
        data=samples('smooth');q=(Query(.12),)
        _,low=GaussianProcess(data).predict(q)
        _,high=GaussianProcess(tuple(replace(r,noise_sd=1.) for r in data)).predict(q)
        self.assertGreater(high[0],low[0])

    def test_gp_rejects_validation_fit(self):
        data=samples('smooth')
        with self.assertRaises(ValueError): GaussianProcess((replace(data[0],split='validation'),))

    def test_gp_variance_bounds(self):
        q=tuple(Query(float(x)) for x in np.linspace(0,1,31))
        _,var=GaussianProcess(samples('smooth')).predict(q)
        self.assertTrue(np.all((var>=0)&(var<=1)))

    def test_rank_not_prior_precision(self):
        model=LinearObservationModel(samples(),get_design('confounded'))
        self.assertEqual(model.rank,1)
        self.assertGreater(np.linalg.det(model.covariance),0)

    def test_readout_changes_identifiability(self):
        oracle=SyntheticOracle('confounded',0)
        train=samples()+(oracle.observe(Query(.8,readout='first'),'train'),)
        model=LinearObservationModel(train,oracle.design)
        self.assertEqual(model.rank,2)

    def test_identity_ablation_stays_confounded(self):
        oracle=SyntheticOracle('confounded',0)
        train=samples()+(oracle.observe(Query(.8,readout='first'),'train'),)
        self.assertEqual(LinearObservationModel(train,oracle.design,'identity').rank,1)

    def test_joint_multifidelity_kernel_psd(self):
        model=GaussianProcess(samples('fidelity_helpful'),mode='multifidelity')
        k=model.kernel(model.queries,model.queries)
        self.assertGreater(np.linalg.eigvalsh(k).min(),0)

    def test_high_only_does_not_fit_low(self):
        model=GaussianProcess(samples('fidelity_helpful'),mode='high_only')
        self.assertTrue(all(r.query.fidelity=='high' for r in model.records))

    def test_common_query_noise_is_paired(self):
        a,b=SyntheticOracle('smooth',4),SyntheticOracle('smooth',4)
        a.observe(Query(.9),'train')
        self.assertEqual(a.observe(Query(.4),'train').value,b.observe(Query(.4),'train').value)

    def test_test_noise_separate(self):
        o=SyntheticOracle('smooth',4)
        self.assertNotEqual(o.observe(Query(.4),'train').value,o.observe(Query(.4),'test').value)

    def test_committee_sum_unchanged(self):
        m=MechanismCommittee(samples('mechanism_pair'),get_design('mechanism_pair'))
        np.testing.assert_allclose(m.probabilities,[.5,.5],atol=1e-12)

    def test_projected_information_zero_for_sum(self):
        design=get_design('mechanism_pair');m=MechanismCommittee(samples('mechanism_pair'),design)
        information=m.acquisition_information((Query(.5),Query(.5,readout='first')),design)
        self.assertLess(abs(information[0]),1e-10)
        self.assertGreater(information[1],0.1)
        self.assertLessEqual(information[1],np.log(2))

    def test_mixture_quantiles_ordered(self):
        m=MechanismCommittee(samples('mechanism_pair'),get_design('mechanism_pair'))
        lo,hi,llo,lhi=m.predictive_intervals((Query(.5,readout='first'),),np.array([.1]))
        self.assertLess(lo[0],hi[0]);self.assertLessEqual(llo[0],lhi[0])

    def test_policy_affordability(self):
        design=get_design('confounded');train=samples();m=LinearObservationModel(train,design)
        self.assertIsNone(propose(m,train,design,'information_gain',.1,np.random.default_rng(1),1))

    def test_policy_reads_observable_difference(self):
        design=get_design('mechanism_pair');train=samples('mechanism_pair');m=MechanismCommittee(train,design)
        p=propose(m,train,design,'information_gain',10,np.random.default_rng(1),1)
        self.assertTrue(p.query.readout=='first' or p.query.intervention!='none')

class LoopTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample_run=run_experiment(RunConfig('confounded','guarded',0,8))

    def test_full_run_audit(self): self.assertEqual(audit_run(self.sample_run)['errors'],[])

    def test_run_schema(self):
        schema=json.loads((ROOT/'research/schemas/run.schema.json').read_text())
        Draft202012Validator(schema).validate(self.sample_run)

    def test_seed_determinism(self):
        second=run_experiment(RunConfig('confounded','guarded',0,8))
        self.assertEqual(self.sample_run['deterministic_payload_sha256'],second['deterministic_payload_sha256'])

    def test_json_roundtrip(self):
        self.assertEqual(audit_run(json.loads(json.dumps(self.sample_run)))['status'],'pass')

    def test_payload_tamper(self):
        r=copy.deepcopy(self.sample_run);r['snapshots'][0]['cost']+=1
        self.assertEqual(audit_run(r)['status'],'fail')

    def test_gzip_output_roundtrip(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'run.json.gz'
            save_run(self.sample_run,p,compact=True)
            loaded=load_run(p)
            self.assertEqual(audit_run(loaded)['status'],'pass')
            self.assertEqual(loaded['deterministic_payload_sha256'],self.sample_run['deterministic_payload_sha256'])

    def test_atomic_output_roundtrip(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'run.json';save_run(self.sample_run,p)
            self.assertTrue(p.exists());self.assertFalse(p.with_suffix('.json.tmp').exists())
            self.assertEqual(audit_run(json.loads(p.read_text()))['status'],'pass')

    def test_final_only_after_freeze(self):
        types=[e['type'] for e in self.sample_run['events']]
        self.assertLess(types.index('model_frozen'),types.index('final_test_evaluated'))
        self.assertEqual(types[-1],'final_test_evaluated')

    def test_no_cost_to_target_invention(self):
        self.assertIsNone(self.sample_run['final']['cost_to_target'])

    def test_all_measured_costs_counted(self):
        b=self.sample_run['budget']
        self.assertAlmostEqual(b['train_cost']+b['validation_cost']+b['test_cost'],b['total_measurement_cost'])
        self.assertGreater(b['test_cost'],0)

    def test_single_use_evaluator(self):
        oracle=SyntheticOracle('confounded',0);q=(Query(.5,group='test-only'),)
        records=tuple(oracle.observe(x,'test') for x in q)
        m=LinearObservationModel(samples(),oracle.design);e=FinalEvaluator()
        e.evaluate(m,records,oracle.reference(q))
        with self.assertRaises(RuntimeError):e.evaluate(m,records,oracle.reference(q))

    def test_final_test_cannot_change_acquisition(self):
        original=SyntheticOracle.observe
        def changed(self,q,split):
            record=original(self,q,split)
            return replace(record,value=record.value+20) if split=='test' else record
        with patch.object(SyntheticOracle,'observe',changed):
            altered=run_experiment(RunConfig('confounded','guarded',0,8))
        queries=lambda run:[e['payload']['query_id'] for e in run['events'] if e['type']=='query_proposed']
        self.assertEqual(queries(self.sample_run),queries(altered))
        self.assertNotEqual(self.sample_run['final']['rmse_observed'],altered['final']['rmse_observed'])

    def test_missing_candidate_stops_without_bio_claim(self):
        r=run_experiment(RunConfig('mechanism_outside','guarded',0,16))
        self.assertTrue(r['stop_reason'].startswith('assumption-challenged'))
        self.assertFalse(r['real_data_validation'])
        self.assertFalse(r['final']['true_candidate_in_library'])

    def test_sum_only_cannot_choose_candidate(self):
        r=run_experiment(RunConfig('mechanism_pair','fixed_readout',0,8))
        np.testing.assert_allclose(r['final']['candidate_posterior'],[.5,.5],atol=1e-10)
        self.assertIsNone(r['final']['selected_candidate'])
        self.assertFalse(r['final']['candidate_resolved_at_95_percent'])

    def test_information_resolves_observable_pair(self):
        r=run_experiment(RunConfig('mechanism_pair','information_gain',0,16))
        self.assertGreater(r['final']['candidate_posterior'][0],0.99)

    def test_hf_only_does_not_query_low(self):
        r=run_experiment(RunConfig('fidelity_helpful','hf_only',0,8))
        self.assertTrue(all(o['query']['fidelity']=='high' for o in r['observations']))

    def test_budget_validation(self):
        for budget in [float('nan'),3,65]:
            with self.assertRaises(ValueError):RunConfig(training_budget=budget)

    def test_policy_validation(self):
        with self.assertRaises(ValueError):RunConfig('smooth','unknown')

    def test_seed_validation(self):
        with self.assertRaises(ValueError):RunConfig(seed=True)

    def test_no_oracle_import_in_policy_or_model(self):
        from research.closed_loop import acquisition, models, committee
        for module in [acquisition,models,committee]:
            text=inspect.getsource(module)
            self.assertNotIn('from .simulator',text)
            self.assertNotIn('import SyntheticOracle',text)

class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=LabServer(0)
        cls.port=cls.server.server_address[1]
        cls.url=f'http://127.0.0.1:{cls.port}'
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join(timeout=2)

    def test_health_token(self):
        with urlopen(self.url+'/api/health') as response:
            data=json.load(response)
        self.assertEqual(data['mode'],'synthetic-local-runner');self.assertTrue(data['csrf_token'])

    def test_csrf_reject(self):
        request=Request(self.url+'/api/run',data=b'{}',headers={'Content-Type':'application/json'},method='POST')
        with self.assertRaises(HTTPError) as c:urlopen(request)
        self.assertEqual(c.exception.code,403)

    def test_invalid_host(self):
        request=Request(self.url+'/api/health',headers={'Host':'attacker.example'})
        with self.assertRaises(HTTPError) as c:urlopen(request)
        self.assertEqual(c.exception.code,403)

    def test_input_reject(self):
        headers={'Content-Type':'application/json','Origin':self.url,'X-Lab-Token':self.server.token}
        request=Request(self.url+'/api/run',data=json.dumps({'training_budget':999}).encode(),headers=headers,method='POST')
        with self.assertRaises(HTTPError) as c:urlopen(request)
        self.assertEqual(c.exception.code,400)

    def test_private_path_not_served(self):
        with self.assertRaises(HTTPError) as c:urlopen(self.url+'/.git/config')
        self.assertEqual(c.exception.code,404)

    def test_actual_local_execution(self):
        headers={'Content-Type':'application/json','Origin':self.url,'X-Lab-Token':self.server.token}
        request=Request(self.url+'/api/run',data=json.dumps({'scenario':'smooth','policy':'random','seed':997,'training_budget':4}).encode(),headers=headers,method='POST')
        with urlopen(request) as response:data=json.load(response)
        self.assertEqual(data['audit']['status'],'pass')
        self.assertEqual(data['run']['budget']['train_cost'],4)
        (ROOT/'research/results/local'/f"{data['run']['run_id']}.json").unlink(missing_ok=True)

if __name__=='__main__':unittest.main()
