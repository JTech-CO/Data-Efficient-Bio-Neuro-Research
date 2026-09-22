from __future__ import annotations
import ast, dataclasses, json, math, unittest
from pathlib import Path
import numpy as np
from research.diagnostic_loop.contracts import Action, Observation, PublicDesign, Ledger, pure_error, AuditTrail
from research.diagnostic_loop.worlds import make_world, SCENARIOS
from research.diagnostic_loop.inference import fit_model
from research.diagnostic_loop.design import choose, gains, POLICIES
from research.diagnostic_loop.diagnostics import audit_panel, diagnose, alarm_summary, empirical_threshold, CHANNELS, PANEL_COST
from research.diagnostic_loop.runner import run_world, FinalEvaluator
from research.diagnostic_loop.study import diagnostic_trajectory, wilson

class ContractsTests(unittest.TestCase):
    def test_invalid_actions(self):
        for kwargs in ({'kind':'real','x':0},{'kind':'sample','x':2},{'kind':'sample','x':float('nan')},{'kind':'sample','x':0,'n':3}):
            with self.assertRaises(ValueError): Action(**kwargs)
    def test_same_condition_ignores_batch_size(self):
        self.assertEqual(Action('sample',.5,1).key,Action('sample',.5,4).key)
    def test_real_rejected(self):
        with self.assertRaises(ValueError): Observation('x',Action('sample',0),1,'fit',0,origin='real')
        with self.assertRaises(ValueError): Observation('x',Action('sample',0),1,'fit',0,real_world_authorized=True)
    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError): Observation('x',Action('sample',0),math.inf,'fit',0)
    def test_duplicate_rejected(self):
        l=Ledger();o=Observation('a',Action('sample',0),1,'fit',0);l.append(o)
        with self.assertRaises(ValueError):l.append(o)
    def test_parent_boundary(self):
        l=Ledger();l.append(Observation('a',Action('sample',0),1,'fit',0))
        with self.assertRaises(ValueError):l.append(Observation('b',Action('sample',0),1,'audit',1,'a'))
    def test_technical_replicate_accounting(self):
        w=make_world('development','normal',0);l=Ledger();w.observe(Action('reference',0,4),'fit',l)
        self.assertEqual(l.counts()['fit_cost'],6);self.assertEqual(l.counts()['n_biological_units'],0)
        self.assertEqual(len({r.parent_id for r in l.view('fit')[1:]}),1)
    def test_split_noise_independent(self):
        w=make_world('development','normal',0);l=Ledger()
        a=w.observe(Action('sample',0,2),'fit',l);b=w.observe(Action('sample',0,2),'audit',l)
        self.assertNotEqual(a[0].value,b[0].value)
    def test_order_independent_measurements(self):
        w=make_world('development','normal',0);a=Ledger();b=Ledger()
        x=Action('sample',-.5);y=Action('reference',1.)
        w.observe(x,'fit',a);w.observe(y,'fit',a);w.observe(y,'fit',b);w.observe(x,'fit',b)
        self.assertEqual({r.record_id:r.value for r in a.view('fit')},{r.record_id:r.value for r in b.view('fit')})
    def test_raw_records_roundtrip(self):
        w=make_world('development','normal',0);l=Ledger();w.observe(Action('sample',0),'fit',l)
        d=json.loads(json.dumps(l.export(),allow_nan=False));self.assertEqual(d[0]['origin'],'simulated')

class InferenceTests(unittest.TestCase):
    def setUp(self):
        self.w=make_world('development','gain_offset',10);self.l=Ledger()
        for a in audit_panel(): self.w.observe(a,'fit',self.l)
        self.rr=self.l.view('fit');self.m=fit_model(self.rr,self.w.public)
    def test_fit_no_audit_or_test(self):
        for split in ('audit','test'):
            with self.assertRaises(ValueError):fit_model(tuple(dataclasses.replace(r,split=split) for r in self.rr),self.w.public)
    def test_full_rank_with_references(self):
        self.assertEqual(self.m.observation_rank,5)
    def test_missing_reference_rank_not_repaired_by_prior(self):
        m=fit_model(tuple(r for r in self.rr if r.action.kind!='reference'),self.w.public)
        self.assertEqual(m.observation_rank,3);self.assertFalse(m.rank_status()['identified_in_declared_linear_likelihood'])
    def test_covariance_positive(self):
        self.assertGreater(np.linalg.eigvalsh(self.m.covariance).min(),0)
    def test_conjugate_linear_equation(self):
        h=np.array([self.w.public.row(r.action) for r in self.rr]);y=np.array([r.value for r in self.rr])
        sd=np.array([1.5,1,.8,.4,.5]);p0=np.diag(1/sd**2)
        self.assertTrue(np.allclose((p0+h.T@h/self.m.noise_variance)@self.m.mean,p0@np.array([0,1,0,1,0])+h.T@y/self.m.noise_variance))
    def test_pure_error_cancels_group_mean(self):
        pe,df,g=pure_error(self.rr)
        shifted=tuple(dataclasses.replace(r,value=r.value+10*self.w.public.row(r.action).sum()) for r in self.rr)
        self.assertAlmostEqual(pe,pure_error(shifted)[0],10);self.assertEqual(df,len(self.rr)-g)
    def test_noise_estimation_not_truth(self):
        m=fit_model(self.rr,self.w.public,estimate_noise=False)
        self.assertAlmostEqual(m.noise_variance,.12**2)
    def test_calibration_propagation_not_narrower(self):
        x=np.linspace(-1,1,21);u=np.ones(21)
        mu,v=self.m.predict_latent(self.w.public,x,u)
        mp,vp=self.m.predict_latent(self.w.public,x,u,propagate_calibration=False)
        self.assertTrue(np.allclose(mu,mp));self.assertTrue(np.all(v>=vp-1e-12))
    def test_information_nonnegative(self):
        for a in audit_panel():
            g=gains(self.m,self.w.public,a)
            for k in ('theta_local_information','sensor_information','joint_information'):self.assertGreaterEqual(g[k],0)
    def test_all_policy_budgets(self):
        for p in POLICIES:
            r=choose(p,self.m,self.w.public,self.rr,3,np.random.default_rng(0))
            if r: self.assertLessEqual(r[0].cost,3)
    def test_no_reference_ablation(self):
        r=choose('no_reference',self.m,self.w.public,self.rr,9,np.random.default_rng(0))
        self.assertNotEqual(r[0].kind,'reference')
    def test_inference_and_design_do_not_import_oracle(self):
        root=Path(__file__).resolve().parents[2]/'diagnostic_loop'
        for name in ('inference.py','design.py','diagnostics.py'):
            tree=ast.parse((root/name).read_text())
            for node in ast.walk(tree):
                if isinstance(node,ast.ImportFrom):self.assertNotEqual(node.module,'worlds')

class DiagnosticTests(unittest.TestCase):
    def test_panel_cost_is_explicit(self):self.assertAlmostEqual(PANEL_COST,25.8)
    def test_invalid_audit_panel(self):
        w=make_world('development','normal',0);l=Ledger();w.observe(Action('sample',0),'audit',l)
        with self.assertRaises(ValueError):diagnose(l.view('audit'),w.public)
    def test_p_values_valid(self):
        for scenario in SCENARIOS:
            t=diagnostic_trajectory(make_world('development',scenario,0),3)
            self.assertEqual(len(t['history']),3)
            for h in t['history']:
                self.assertEqual(set(h['p_values']),set(CHANNELS))
                self.assertTrue(all(0<=p<=1 for p in h['p_values'].values()))
    def test_affine_sensor_does_not_change_mechanism_test(self):
        w=make_world('development','normal',1);l=Ledger()
        for a in audit_panel():w.observe(a,'audit',l)
        records=l.view('audit');p=diagnose(records,w.public)['p_values']['mechanism_lack_of_fit']
        shifted=tuple(dataclasses.replace(r,value=r.value+2+3*float(w.public.phi(r.action.x))) if r.action.kind!='reference' else r for r in records)
        q=diagnose(shifted,w.public)['p_values']['mechanism_lack_of_fit'];self.assertAlmostEqual(p,q,9)
    def test_cumulative_detection_no_certification(self):
        t=diagnostic_trajectory(make_world('development','gain_offset',2),3)
        s=alarm_summary(t['history'],.05/12)
        self.assertFalse(s['causal_source_identified']);self.assertTrue(s['flags']['sensor_affine'])
    def test_nested_threshold_flags(self):
        t=diagnostic_trajectory(make_world('development','noise_scale',2),3)
        loose=alarm_summary(t['history'],.05);tight=alarm_summary(t['history'],.05/12)
        for k in CHANNELS:self.assertLessEqual(tight['flags'][k],loose['flags'][k])
    def test_empirical_order_statistic(self):
        t=empirical_threshold(range(100),.05)
        self.assertEqual(t['order_statistic_index_1based'],96);self.assertEqual(t['score_threshold'],95.)
    def test_wilson_bounds(self):
        a=wilson(0,100);b=wilson(100,100)
        self.assertAlmostEqual(a[0],0);self.assertGreater(a[1],0);self.assertLess(b[0],1);self.assertAlmostEqual(b[1],1)
    def test_reference_transport_counterexample(self):
        w=make_world('development','reference_mismatch',0)
        # Specimen sensor error can be absorbed into unknown latent coefficients.
        wp=dataclasses.replace(w,scenario='normal',theta0=w.gain*w.theta0+w.offset,
                               theta1=w.gain*w.theta1,theta2=w.gain*w.theta2,gain=1.,offset=0.)
        for a in audit_panel():self.assertAlmostEqual(w.sensor_mean(a),wp.sensor_mean(a),12)
    def test_nonidentifiable_gain_transformation(self):
        w=make_world('development','gain_offset',3)
        ww=dataclasses.replace(w,gain=w.gain*2,theta0=w.theta0/2,theta1=w.theta1/2,theta2=w.theta2/2)
        for a in (Action('sample',.4),Action('intervention',-.8)):
            self.assertAlmostEqual(w.sensor_mean(a),ww.sensor_mean(a))
        self.assertNotAlmostEqual(w.sensor_mean(Action('reference',1)),ww.sensor_mean(Action('reference',1)))

class RunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=run_world(make_world('development','combined',11),'block_targeted',.05/12)
    def test_final_single_open(self):self.assertEqual(self.r['evaluation']['test_open_count'],1)
    def test_cost_cap(self):self.assertLessEqual(self.r['costs']['acquisition_cost'],36+3*PANEL_COST+1e-9)
    def test_three_fixed_audits(self):self.assertEqual(len(self.r['audit_history']),3)
    def test_same_data_estimators(self):
        a=self.r['evaluation']['estimators'];self.assertEqual(set(a),{'propagated','plugin_calibration','nominal_noise','identity_baseline','oracle_affine_calibration'})
        self.assertAlmostEqual(a['propagated']['latent']['rmse'],a['plugin_calibration']['latent']['rmse'])
    def test_hash_chain(self):self.assertTrue(AuditTrail.verify(self.r['events']))
    def test_freeze_before_test(self):
        types=[e['type'] for e in self.r['events']]
        self.assertLess(types.index('freeze'),types.index('final_test'))
    def test_json_finite(self):json.dumps(self.r,allow_nan=False)
    def test_no_biological_samples(self):self.assertEqual(self.r['costs']['n_biological_units'],0)
    def test_reproducible_core(self):
        r2=run_world(make_world('development','combined',11),'block_targeted',.05/12)
        self.assertEqual(r2['events'],self.r['events']);self.assertEqual(r2['evaluation'],self.r['evaluation'])
    def test_evaluator_requires_freeze(self):
        with self.assertRaises(RuntimeError):FinalEvaluator().evaluate(None,None,None,{})
    def test_no_audit_equal_budget_reference(self):
        r=run_world(make_world('development','normal',2),'reference_first_no_audit',.05/12)
        self.assertEqual(r['costs']['audit_cost'],0)
        self.assertGreater(r['costs']['fit_cost'],100)
        self.assertLessEqual(r['costs']['acquisition_cost'],113.4+1e-9)
        self.assertIsNone(r['diagnosis']['any_alarm'])

if __name__=='__main__':unittest.main()
