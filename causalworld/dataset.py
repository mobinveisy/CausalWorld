import random
from dataclasses import dataclass
from typing import Sequence
import numpy as np
import torch
from torch.utils.data import Dataset
from .config import PhysicsConfig
from .simulator import CollisionConfig, simulate_collision

@dataclass(frozen=True)
class DatasetSpec:
    masses: Sequence[float]
    cf_masses: Sequence[float]
    samples: int = 1000
    context_size: int = 3
    seed: int = 42
    v_min: float = 0.75
    v_max: float = 1.75
    x_b_min: float = 0.78
    x_b_max: float = 1.18

class CollisionDataset(Dataset):
    def __init__(self, spec: DatasetSpec, physics=PhysicsConfig()):
        self.spec, self.physics = spec, physics

    def __len__(self):
        return self.spec.samples

    def _sim(self, mass, v, xb):
        p = self.physics
        return simulate_collision(CollisionConfig(
            m_a=p.m_a, m_b=float(mass), x_a0=0.0, x_b0=float(xb),
            v_a0=float(v), v_b0=0.0, radius_a=p.radius_a, radius_b=p.radius_b,
            restitution=p.restitution, dt=p.dt, steps=p.steps
        ))

    def _context(self, mass, rng):
        return np.stack([
            self._sim(mass, rng.uniform(self.spec.v_min, self.spec.v_max),
                      rng.uniform(self.spec.x_b_min, self.spec.x_b_max))["states"]
            for _ in range(self.spec.context_size)
        ]).astype(np.float32)

    def __getitem__(self, idx):
        rng = random.Random(self.spec.seed*1000003 + idx)
        m = rng.choice(tuple(self.spec.masses))
        candidates = [x for x in self.spec.cf_masses if x != m]
        mcf = rng.choice(tuple(candidates))
        context = self._context(m, rng)
        cf_context = self._context(mcf, rng)
        v = rng.uniform(self.spec.v_min, self.spec.v_max)
        xb = rng.uniform(self.spec.x_b_min, self.spec.x_b_max)
        y = self._sim(m, v, xb)
        ycf = self._sim(mcf, v, xb)
        return {
            "context": torch.from_numpy(context),
            "query_initial": torch.from_numpy(y["initial"]),
            "target": torch.from_numpy(y["states"]),
            "mass": torch.tensor(m, dtype=torch.float32),
            "cf_context": torch.from_numpy(cf_context),
            "cf_target": torch.from_numpy(ycf["states"]),
            "cf_mass": torch.tensor(mcf, dtype=torch.float32),
        }
