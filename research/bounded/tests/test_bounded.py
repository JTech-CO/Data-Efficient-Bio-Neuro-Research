import copy, unittest
import numpy as np
from research.bounded_loop import partial,audit,replicates
from research.bounded_loop.common import digest,group,validate,rng

class PartialTests(unittest.TestCase):
    def exact(self,scenario='bounded_bias'):
        r=partial.run('unit',scenario,19,'triangulated')
        w=r['evaluator_only']['truth'];q=np.array([w['theta0'],w['theta1'],1/w['gain'],-w['offset']/w['gain'],w['recovery']])
        cis=[]
        for g in r['measurement_intervals']:
            x=g['x'];z=w['theta0']+w['theta1']*x
            if g['kind']=='primary':m=w['gain']*(z+w['recovery']*g['delta'])+w['offset']
            elif g['kind']=='reference':m=z+w['ref_bias']
            else:m=w['gain']*w['blank_bias']+w['offset']
            cis.append({**g,'low':m,'high':m})
        return cis,q
    def test_true_parameters_satisfy_linear_constraints(self):
        cis,q=self.exact();self.assertTrue(partial.contains(cis,q,1))
    def test_bias_relaxation_nested(self):
        cis,q=self.exact();small=partial.solve(cis,1);large=partial.solve(cis,2)
        for key,v in small['projections'].items():
            self.assertLessEqual(large['projections'][key]['low'],v['low']+1e-7)
            self.assertGreaterEqual(large['projections'][key]['high'],v['high']-1e-7)
    def test_common_mode_width_does_not_vanish(self):
        cis,q=self.exact('common_in_bounds');s=partial.solve(cis,1)
        self.assertGreater(s['projections']['theta0']['width'],.10)
    def test_common_out_of_bounds_can_be_feasible_and_wrong(self):
        cis,q=self.exact('common_out_of_bounds');s=partial.solve(cis,1)
        self.assertEqual(s['status'],'bounded');self.assertFalse(partial.contains(cis,q,1))
    def test_unanchored_offset_unbounded(self):
        cis,q=self.exact();cis=[c for c in cis if c['kind']=='primary']
        self.assertEqual(partial.solve(cis)['status'],'unbounded')
    def test_conflicting_references_empty(self):
        c=[dict(kind='reference',x=0,delta=0,low=1,high=1),dict(kind='reference',x=0,delta=0,low=3,high=3)]
        self.assertEqual(partial.solve(c)['status'],'empty')
    def test_budget_and_repeats(self):
        for d in partial.DESIGNS:
            gs=partial.design_groups(d);self.assertLessEqual(sum(g['n']*g['unit_cost'] for g in gs),72)
            self.assertTrue(all(g['n']>=4 for g in gs))
    def test_invalid_bias(self):
        with self.assertRaises(ValueError):partial.constraints([], -1)
    def test_reversed_interval(self):
        with self.assertRaises(ValueError):partial.constraints([dict(kind='reference',x=0,low=2,high=1)],1)
    def test_final_excluded_from_confidence_intervals(self):
        g=group('t','fit',0,[1,2,3,4],kind='reference',delta=0)
        f=group('f','final',0,[100,200],kind='reference',delta=0)
        self.assertEqual(partial.intervals([g]),partial.intervals([g,f]))

class AuditTests(unittest.TestCase):
    def test_martingale_conditional_average(self):
        m=audit.SignMonitor()
        for x,d in [(-.7,1),(.8,-1),(.5,1)]:m.update(x,d)
        for x in [-1,-.1,.1,1]:
            a=copy.deepcopy(m);b=copy.deepcopy(m)
            mean=(a.update(x,1)+b.update(x,-1))/2
            zero=copy.deepcopy(m).update(x,0)
            self.assertAlmostEqual(mean,zero,12)
    def test_zero_contrasts_do_not_grow(self):
        m=audit.SignMonitor()
        for _ in range(100):self.assertAlmostEqual(m.update(0,0),1)
        self.assertFalse(m.alarm)
    def test_sign_scale_invariant(self):
        a=audit.SignMonitor();b=audit.SignMonitor()
        for i in range(30):
            d=(-1 if i%3==0 else 1)*(i+.5)
            self.assertAlmostEqual(a.update(.1,d),b.update(.1,d*100),12)
    def test_t_scale_invariant(self):
        x=np.array([1,2,3,4,2,3.]);self.assertAlmostEqual(audit.batch_t_p(x),audit.batch_t_p(100*x),12)
    def test_t_matches_scipy(self):
        from scipy import stats
        x=np.array([1,-2,3,-1,.2,4.]);self.assertAlmostEqual(audit.batch_t_p(x),stats.ttest_1samp(x,0).pvalue,12)
    def test_sign_null_not_equal_to_mean_null(self):
        # mean = 0 but P(positive)=.9, so this violates the sign monitor's null.
        self.assertAlmostEqual(.9*1+.1*(-9),0)
        self.assertNotEqual(.9,.5)
    def test_cost_and_holdout(self):
        r=audit.run('unit','gaussian_null',5,'adaptive_cover');validate(r)
        self.assertLessEqual(r['acquisition_spend'],r['budget'])
        self.assertEqual(r['costs']['final'],81)
        self.assertTrue(all(g['role']!='audit' for g in r['groups'] if g['key'].startswith('fit:')))
    def test_no_audit_is_not_zero_alarm(self):
        r=audit.run('unit','gaussian_null',5,'max_gap',0)
        self.assertTrue(all(m['alarm'] is None for m in r['methods'].values()))
    def test_common_mode_contrast_cancels(self):
        w=audit.make_world('unit','common_mode',5);a,b=audit.truth_functions(w,np.linspace(-1,1,20))
        np.testing.assert_array_equal(a,b)
    def test_invalid_fraction(self):
        with self.assertRaises(ValueError):audit.run('unit','gaussian_null',1,'max_gap',.9)

class ReplicateTests(unittest.TestCase):
    def setUp(self):
        self.x=np.linspace(-.9,.9,12);self.y=replicates.basis(self.x)@np.array([.4,.7,-.1])
        self.Y=self.y[:,None]+rng('test').normal(0,.1,(12,4))
    def test_pure_error_partition(self):
        p=replicates.pure_error(self.x,self.Y);self.assertLess(p['identity_error'],1e-12)
        self.assertEqual(p['df_pure'],36);self.assertEqual(p['df_lack_of_fit'],9)
    def test_difference_noise_ignores_shared_mean(self):
        a=replicates.fit(self.x,self.Y,'difference_logvar_base')
        b=replicates.fit(self.x,self.Y+5*np.sin(3*self.x)[:,None],'difference_logvar_base')
        np.testing.assert_allclose(a['gamma'],b['gamma'],rtol=1e-12,atol=1e-12)
    def test_shared_batch_not_measured_by_differences(self):
        shift=rng('batch').normal(0,2,(12,1));a=self.Y[:,::2]-self.Y[:,1::2]
        b=(self.Y+shift)[:,::2]-(self.Y+shift)[:,1::2]
        np.testing.assert_allclose(a,b,atol=1e-14)
    def test_plus_is_real_basis_not_stub(self):
        y=self.Y+.5*np.sin(np.pi*self.x)[:,None]
        a=replicates.fit(self.x,y,'difference_logvar_base');b=replicates.fit(self.x,y,'difference_logvar_plus')
        self.assertEqual(len(a['beta']),3);self.assertEqual(len(b['beta']),4)
    def test_bootstrap_reproducible_and_finite(self):
        r=replicates.run('unit','combined',17,4,bootstrap=20)
        fresh=replicates.run('unit','combined',17,4,bootstrap=20)
        self.assertEqual(digest(r),digest(fresh));validate(r)
        self.assertEqual(len(r['bootstrap_models']),20)
    def test_single_component_mixture(self):
        from research.bounded_loop.common import normal_metrics
        mean=np.array([0.,1.]);noise=np.array([1.,2.]);truth=np.array([0.,1.]);obs=np.array([.1,.9])
        m=replicates.mixture_metrics(mean[None,:],noise[None,:],truth,obs)
        n=normal_metrics(mean,np.full(2,1e-12),noise,truth,obs)
        self.assertAlmostEqual(m['nll'],n['nll'],10)
        self.assertAlmostEqual(m['observed_width'],n['observed_width'],7)
    def test_repeat_budget(self):
        for k in replicates.REPLICATION:
            r=replicates.run('unit','normal',3,k,bootstrap=20)
            self.assertEqual(r['costs']['fit'],48);self.assertEqual(r['costs']['final'],81)
    def test_reject_bad_repeat_count(self):
        with self.assertRaises(ValueError):replicates.run('unit','normal',1,3)

class RecordTests(unittest.TestCase):
    def test_hash_detects_value_tampering(self):
        r=audit.run('unit','gaussian_null',3,'max_gap');r['groups'][0]['values'][0]+=1
        with self.assertRaises(AssertionError):validate(r)
    def test_seed_streams_differ(self):self.assertNotEqual(float(rng('fit').normal()),float(rng('final').normal()))
    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError):group('x','fit',0,[np.nan])
    def test_no_implicit_json_overwrite(self):
        import tempfile
        from pathlib import Path
        from research.bounded_loop.common import write_json
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.json';write_json(p,{'a':1})
            with self.assertRaises(FileExistsError):write_json(p,{'a':2})
if __name__=='__main__':unittest.main()
