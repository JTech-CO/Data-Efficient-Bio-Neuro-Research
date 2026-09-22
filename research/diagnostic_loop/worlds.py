"""Evaluator-owned truths. This module is never imported by design or inference.

World identifiers, but not seeds/parameters/labels, are opaque to policies.
New nuisance/effect parameters are drawn per world rather than merely adding
noise to the identical function used in v1.1.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
import hashlib
import numpy as np
from .contracts import Action, Observation, PublicDesign, Ledger

SCENARIOS = ("normal", "gain_offset", "mechanism", "noise_scale", "combined",
             "nonlinear_sensor", "heteroscedastic", "heavy_tail", "local_bump", "reference_mismatch")

def rng_for(*parts):
    key = "|".join(map(str, parts)).encode()
    seed = int.from_bytes(hashlib.sha256(key).digest()[:16], "little")
    return np.random.default_rng(seed)

@dataclass(frozen=True)
class World:
    bank: str
    scenario: str
    index: int
    public: PublicDesign
    theta0: float
    theta1: float
    theta2: float
    gain: float
    offset: float
    noise_multiplier: float
    nonlinear: float
    bump_location: float
    bump_width: float
    bump_height: float

    @property
    def identity(self):
        return f"{self.bank}/{self.scenario}/{self.index}"

    def latent(self, x, u):
        x, u = np.asarray(x, float), np.asarray(u, float)
        z = self.theta0 + self.theta1*self.public.phi(x) + self.theta2*u*self.public.psi(x)
        if self.scenario == "local_bump":
            z = z + self.bump_height*u*np.exp(-0.5*((x-self.bump_location)/self.bump_width)**2)
        return z

    def sensor_mean(self, a: Action):
        if a.kind == "reference":
            if self.scenario == "reference_mismatch": return a.x
            z = a.x
        else: z = float(self.latent(a.x, a.u))
        return float(self.gain*z + self.offset + self.nonlinear*z*z)

    def noise_sd(self, a: Action):
        sd = self.public.nominal_sd*self.noise_multiplier
        if self.scenario == "heteroscedastic":
            sd *= 0.6 + 1.6*abs(a.x)
        return sd

    def observe(self, a: Action, split: str, ledger: Ledger):
        previous = [r for r in ledger.view(split) if r.action.key == a.key]
        start = len(previous)
        parent = previous[0].record_id if previous else None
        out = []
        for j in range(a.n):
            k = start+j
            # Common random numbers by world, split, condition and replicate;
            # action order/policy are not part of the measurement identity.
            rng = rng_for(self.identity, split, a.key, k)
            noise = (rng.standard_t(3)/np.sqrt(3) if self.scenario == "heavy_tail"
                     else rng.normal())
            obs = Observation(f"{self.identity}:{split}:{a.key}:{k}", a,
                              self.sensor_mean(a)+self.noise_sd(a)*float(noise),
                              split, k, parent)
            ledger.append(obs); out.append(obs)
            if parent is None: parent = obs.record_id
        return tuple(out)

    def truth_record(self):
        d = asdict(self)
        d["identity"] = self.identity
        d["fault_tags"] = {
            "sensor": self.scenario in ("gain_offset", "combined", "nonlinear_sensor", "reference_mismatch"),
            "mechanism": self.scenario in ("mechanism", "combined", "local_bump"),
            "noise": self.scenario in ("noise_scale", "combined", "heteroscedastic", "heavy_tail"),
        }
        d["limitations"] = {
            "reference_shared_with_specimen": self.scenario != "reference_mismatch",
            "affine_sensor": self.scenario != "nonlinear_sensor",
            "known_mechanism_basis": self.scenario != "local_bump",
            "gaussian_homoscedastic_noise": self.scenario not in ("heteroscedastic", "heavy_tail"),
        }
        return d

def make_world(bank: str, scenario: str, index: int):
    if bank not in ("development", "calibration", "evaluation", "demo"):
        raise ValueError("unknown bank")
    if scenario not in SCENARIOS or type(index) is not int or index < 0:
        raise ValueError("unknown scenario or negative index")
    # No overlap between developer/calibration and evaluation RNG namespaces.
    rng = rng_for("diagnostic-world-v120", bank, scenario, index)
    basis = "linear" if bank in ("development", "calibration", "demo") else ("tanh" if index%2 == 0 else "cubic")
    t0, t1 = float(rng.uniform(-0.25,0.25)), float(rng.uniform(0.7,1.3))
    sign = float(rng.choice([-1,1]))
    gain, offset, t2, mult, nonlin = 1., 0., 0., 1., 0.
    if scenario in ("gain_offset", "combined", "reference_mismatch"):
        gain = float(rng.uniform(0.55,0.8) if sign < 0 else rng.uniform(1.2,1.45))
        offset = float(rng.choice([-1,1])*rng.uniform(0.10,0.30))
    if scenario in ("mechanism", "combined"):
        t2 = sign*float(rng.uniform(0.18,0.42))
    if scenario in ("noise_scale", "combined"):
        mult = float(rng.uniform(1.6,2.2))
    if scenario == "nonlinear_sensor":
        nonlin = sign*float(rng.uniform(0.20,0.40))
    loc = float(rng.uniform(0.28,0.45)) if bank == "evaluation" else float(rng.uniform(-0.55,-0.3))
    width = float(rng.uniform(0.035,0.065))
    height = sign*float(rng.uniform(0.6,1.0))
    return World(bank,scenario,index,PublicDesign(basis),t0,t1,t2,gain,offset,mult,nonlin,loc,width,height)
