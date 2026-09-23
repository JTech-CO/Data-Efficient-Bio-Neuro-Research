from __future__ import annotations
import unittest, copy, inspect, math
import numpy as np
from scipy.integrate import quad
from scipy.stats import t, norm
from research.triad_loop import transfer as D, spatial as E, noise as F
from research.triad_loop.common import Observation,Collector,rng_for,wls,validate_run,wilson,digest


class Contracts(unittest.TestCase):
    def record(self,**kw):return Observation(**({'record_id':'x','kind':'sample','x':0.,'value':1.,'cost':1.,'replicate':0}|kw))
    def test_real_rejected(self):
        with self.assertRaises(ValueError):self.record(origin='real')
    def test_generated_rejected(self):
        with self.assertRaises(ValueError):self.record(origin='generated')
    def test_biology_rejected(self):
        with self.assertRaises(ValueError):self.record(counts_as_biological_unit=True)
    def test_authorization_rejected(self):
        with self.assertRaises(ValueError):self.record(real_world_authorized=True)
    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError):self.record(value=float('nan'))
    def test_negative_cost(self):
        with self.assertRaises(ValueError):self.record(cost=-1)
    def test_bad_split(self):
        with self.assertRaises(ValueError):self.record(split='whatever')
    def test_test_before_freeze(self):
        c=Collector('x',lambda *a:0.)
        with self.assertRaises(RuntimeError):c.take('sample',0,split='test')
    def test_acquisition_after_freeze(self):
        c=Collector('x',lambda *a:0.);c.freeze({})
        with self.assertRaises(RuntimeError):c.take('sample',0)
    def test_final_test_once(self):
        c=Collector('x',lambda *a:0.);c.freeze({});c.finish()
        with self.assertRaises(RuntimeError):c.finish()
    def test_lineage(self):
        c=Collector('x',lambda *a:0.);a=c.take('sample',0);b=c.take('sample',0)
        self.assertEqual(b.parent_id,a.record_id);self.assertEqual(b.replicate,1)
    def test_canonical_coordinate_parent(self):
        c=Collector('x',lambda *a:0.)
        a=c.take('sample',.1+.2);b=c.take('sample',.3)
        self.assertEqual(a.x,b.x);self.assertEqual(b.parent_id,a.record_id)
    def test_stream_separation(self):
        self.assertNotEqual(rng_for('dev',0).normal(),rng_for('eval',0).normal())
    def test_stream_determinism(self):self.assertEqual(rng_for('q',0).normal(),rng_for('q',0).normal())
    def test_wilson_limits(self):
        self.assertGreater(wilson(0,10)[1],0);self.assertLess(wilson(10,10)[0],1)


class Transfer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runs={p:D.run('test','both_shift',3,p) for p in D.PROTOCOLS}
    def test_external_rank(self):self.assertEqual(self.runs['external_only']['model']['expanded_physical_rank'],4)
    def test_addition_rank(self):self.assertEqual(self.runs['addition_only']['model']['expanded_physical_rank'],5)
    def test_anchored_rank(self):
        for p in ('addition_blank','orthogonal_only','triangulated'):
            self.assertEqual(self.runs[p]['model']['expanded_physical_rank'],6)
    def test_unresolved_no_unique_theta(self):
        for p in ('external_only','addition_only'):
            self.assertIsNone(self.runs[p]['model']['physical']);self.assertIsNone(self.runs[p]['metrics']['latent_rmse'])
    def test_gain_only_scope(self):self.assertEqual(self.runs['addition_only']['model']['transfer_scope'],'gain_only_offset_unresolved')
    def test_equal_budgets(self):
        for r in self.runs.values():self.assertEqual(r['costs']['fit'],48)
    def test_known_anchor_recovery(self):
        self.assertLess(self.runs['orthogonal_only']['metrics']['latent_rmse'],.2)
    def test_no_causal_claim(self):
        for r in self.runs.values():self.assertFalse(r['model']['causal_source_identified'])
    def test_ledger_validation(self):
        for r in self.runs.values():self.assertGreater(validate_run(r),0)
    def test_tampering_detected(self):
        r=copy.deepcopy(self.runs['triangulated']);r['observations'][0]['value']+=1
        with self.assertRaises(AssertionError):validate_run(r)
    def test_event_tampering(self):
        r=copy.deepcopy(self.runs['triangulated']);r['events'][1]['payload']['x']=.8
        with self.assertRaises(AssertionError):validate_run(r)
    def test_constant_offset_equivalence(self):
        obs=[Observation(**o) for o in self.runs['addition_only']['observations'] if o['split']=='fit']
        p=np.array([1.,.8,1.3,.2,1.,0.]);q=p.copy();q[0]+=.4;q[3]-=p[2]*.4
        np.testing.assert_allclose(D.physical_map(p,obs),D.physical_map(q,obs),atol=1e-12)
    def test_blank_breaks_offset_equivalence(self):
        obs=[Observation(**o) for o in self.runs['addition_blank']['observations'] if o['split']=='fit']
        p=np.array([1.,.8,1.3,.2,1.,0.]);q=p.copy();q[0]+=.4;q[3]-=p[2]*.4
        self.assertGreater(np.linalg.norm(D.physical_map(p,obs)-D.physical_map(q,obs)),.2)
    def test_fit_refuses_test(self):
        obs=[Observation(**o) for o in self.runs['external_only']['observations']]
        with self.assertRaises(ValueError):D.fit_transfer(obs)
    def test_common_anchor_counterexample(self):
        w=D.make_world('test','common_anchor_failure',3)
        self.assertNotEqual(w.gain,1.)
        # Noiseless apparent coordinate is g*z+b; standard addition appears unit slope.
        z=w.latent(.3);self.assertAlmostEqual(w.main(z+.7/w.gain)-w.main(z),.7)


class Spatial(unittest.TestCase):
    def test_spending_sum(self):
        self.assertLess(sum(E.alpha_at('spending',i,1000) for i in range(1,1001)),.05)
    def test_bonferroni_sum(self):
        self.assertAlmostEqual(sum(E.alpha_at('bonferroni',i,24) for i in range(1,25)),.05)
    def test_zero_look_rejected(self):
        with self.assertRaises(ValueError):E.alpha_at('spending',0,10)
    def test_exact_gaussian_p(self):
        from scipy.special import ndtr
        self.assertAlmostEqual(2*ndtr(-norm.ppf(.975)),.05)
    def test_policy_no_world_argument(self):self.assertNotIn('world',inspect.signature(E.choose).parameters)
    def test_equal_costs(self):
        for p in E.POLICIES:
            r=E.run('test','narrow',1,p,24,1);self.assertEqual(r['costs']['audit'],24);validate_run(r)
    def test_expensive_control_fewer_pairs(self):
        self.assertEqual(E.run('test','normal',1,'uniform',24,3)['n_pairs'],6)
    def test_fixed_panel_three_locations(self):
        r=E.run('test','narrow',1,'fixed_three');self.assertEqual(len({v['x'] for v in r['history']}),3)
    def test_stratified_one_per_bin(self):
        r=E.run('test','normal',1,'stratified');n=r['n_pairs']
        bins={min(n-1,int((v['x']+1)*n/2)) for v in r['history']};self.assertEqual(len(bins),n)
    def test_common_mode_contrast_zero(self):
        w=E.make_world('test','common_mode',1);np.testing.assert_array_equal(w.contrast(np.linspace(-1,1,9)),np.zeros(9))
    def test_tail_outside_claimed_guarantee(self):
        r=E.run('test','t3_null',1,'uniform');self.assertFalse(r['evaluator_truth']['gaussian_null_assumptions_hold'])
    def test_audit_not_training(self):
        r=E.run('test','normal',1,'uniform');self.assertTrue(all(o['split']=='audit' for o in r['observations']))


class Noise(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runs={m:F.run('test','gaussian',8,m,'random') for m in F.ESTIMATORS}
    def test_same_passive_data(self):self.assertEqual(len({r['data_digest'] for r in self.runs.values()}),1)
    def test_three_refits(self):
        for r in self.runs.values():self.assertEqual(set(r['models']),set(F.ESTIMATORS))
    def test_complete_pairs(self):
        for r in self.runs.values():self.assertEqual(r['costs']['fit'],48);self.assertEqual(r['costs']['test'],81)
    def test_noise_pair_cancels_mean(self):
        self.assertAlmostEqual(((.3+1)-(.3+2))/np.sqrt(2),(1-2)/np.sqrt(2))
    def test_no_nonfit_estimation(self):
        obs=[Observation(**o) for o in next(iter(self.runs.values()))['observations']]
        with self.assertRaises(ValueError):F.fit(obs,'hom_gaussian')
    def test_finite_scores(self):
        for r in self.runs.values():
            for e in r['evaluation'].values():self.assertTrue(all(math.isfinite(v) for v in e.values()))
    def test_crps_nonnegative(self):
        for r in self.runs.values():
            for e in r['evaluation'].values():self.assertGreaterEqual(e['crps'],0)
    def test_crps_student_quadrature(self):
        m={'estimator':'student_t','beta':[0,0,0],'covariance':np.zeros((3,3)).tolist(),'noise_coef':[0,0],'scale':1.,'converged':True}
        got=F.scores(m,np.array([0.]),np.array([.7]),np.array([0.]))['crps']
        a=quad(lambda z:t.cdf(z,4)**2,-np.inf,.7)[0]
        b=quad(lambda z:(1-t.cdf(z,4))**2,.7,np.inf)[0]
        self.assertAlmostEqual(got,a+b,places=6)
    def test_crps_normal_quadrature(self):
        m={'estimator':'hom_gaussian','beta':[0,0,0],'covariance':np.zeros((3,3)).tolist(),'noise_coef':[0,0],'scale':1.,'converged':True}
        got=F.scores(m,np.array([0.]),np.array([.7]),np.array([0.]))['crps']
        want=quad(lambda z:norm.cdf(z)**2,-np.inf,.7)[0]+quad(lambda z:(1-norm.cdf(z))**2,.7,np.inf)[0]
        self.assertAlmostEqual(got,want,places=6)
    def test_approximation_flag(self):
        for m in self.runs['hom_gaussian']['models'].values():self.assertFalse(m['noise_uncertainty_integrated'])
    def test_bad_budget_rejected(self):
        with self.assertRaises(ValueError):F.run('test','gaussian',1,'hom_gaussian','ivr',47)
    def test_covariance_psd(self):
        for m in self.runs['hom_gaussian']['models'].values():self.assertGreaterEqual(np.linalg.eigvalsh(m['covariance']).min(),-1e-9)
    def test_replay_determinism(self):
        r=F.run('test','gaussian',8,'hom_gaussian','random')
        self.assertEqual(digest(r),digest(self.runs['hom_gaussian']))
    def test_validated_records(self):
        for r in self.runs.values():validate_run(r)

if __name__=='__main__':unittest.main()
