"""Small conjugate regression, transformed into biological/sensor coordinates.

beta=(g*theta0+b, g*theta1, g*theta2, g, b) makes the observation
likelihood linear. Independent Gaussian beta priors imply a particular,
non-independent prior in theta coordinates. We do not hide this assumption.
Noise is a shrinkage plug-in estimate from within-condition technical repeats,
not full Bayesian integration. Transformed intervals use the delta method.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from .contracts import PublicDesign, Action, require_fit, pure_error

@dataclass
class Fit:
    mean: np.ndarray
    covariance: np.ndarray
    noise_variance: float
    pure_error_df: int
    observation_rank: int
    sample_rank: int
    reference_rank: int
    n_fit: int

    def theta(self):
        g = float(self.mean[3])
        if abs(g) < 0.05: raise ArithmeticError("gain too close to zero for delta approximation")
        t = np.array([(self.mean[0]-self.mean[4])/g, self.mean[1]/g, self.mean[2]/g])
        j = np.zeros((3,5)); j[0,0]=1/g; j[0,4]=-1/g
        j[1,1]=1/g; j[2,2]=1/g; j[:,3] = -t/g
        return t, j, j @ self.covariance @ j.T

    def rank_status(self):
        return {"rank":self.observation_rank,"sample_rank":self.sample_rank,
                "reference_rank":self.reference_rank,
                "identified_in_declared_linear_likelihood":bool(self.observation_rank==5),
                "mechanism_truth_certified":False,
                "reason":"full-rank-conditional-on-model" if self.observation_rank==5 else "prior-does-not-repair-data-rank"}

    def summary(self):
        t,_,v=self.theta()
        return {"beta":self.mean.tolist(),"theta_delta":t.tolist(),
                "theta_sd_delta":np.sqrt(np.maximum(np.diag(v),0)).tolist(),
                "sigma_plugin":float(np.sqrt(self.noise_variance)),"pure_error_df":self.pure_error_df,
                "n_fit":self.n_fit, **self.rank_status()}

    def predict_latent(self, public, x, u, *, propagate_calibration=True):
        t,j,_=self.theta()
        x,u = np.asarray(x,float),np.asarray(u,float)
        h=np.column_stack([np.ones_like(x),public.phi(x),u*public.psi(x)])
        if not propagate_calibration: j[:,3:]=0
        v=h@j
        return h@t, np.maximum(np.einsum('ij,jk,ik->i',v,self.covariance,v),0)

    def predict_sensor(self, public, x, u):
        x,u = np.asarray(x,float),np.asarray(u,float)
        h=np.column_stack([np.ones_like(x),public.phi(x),u*public.psi(x),np.zeros_like(x),np.zeros_like(x)])
        return h@self.mean, np.maximum(np.einsum('ij,jk,ik->i',h,self.covariance,h),0)

def fit_model(records, public: PublicDesign, *, estimate_noise=True):
    require_fit(records)
    h=np.array([public.row(r.action) for r in records]); y=np.array([r.value for r in records])
    pe,df,_=pure_error(records)
    nominal=public.nominal_sd**2
    # Inverse-gamma a0=2,b0=nominal: prior mean nominal.
    sigma=(nominal+0.5*pe)/(1+0.5*df) if estimate_noise else nominal
    sigma=max(float(sigma),1e-10)
    m0=np.array([0.,1.,0.,1.,0.]); sd=np.array([1.5,1.0,0.8,0.4,0.5])
    p0=np.diag(1/sd**2)
    precision=p0+h.T@h/sigma
    cov=np.linalg.solve(precision,np.eye(5)); cov=(cov+cov.T)/2
    mean=cov@(p0@m0+h.T@y/sigma)
    sr=[i for i,r in enumerate(records) if r.action.kind!="reference"]
    rr=[i for i,r in enumerate(records) if r.action.kind=="reference"]
    rank=lambda a: int(np.linalg.matrix_rank(a)) if a.size else 0
    return Fit(mean,cov,sigma,df,rank(h),rank(h[sr,:3]),rank(h[rr,3:]),len(records))

def identity_baseline(records, public):
    """Same-data baseline that incorrectly treats sensor output as latent units."""
    require_fit(records)
    rr=[r for r in records if r.action.kind!="reference"]
    h=np.array([public.row(r.action)[:3] for r in rr]); y=np.array([r.value for r in rr])
    return np.linalg.solve(h.T@h+1e-6*np.eye(3),h.T@y)
