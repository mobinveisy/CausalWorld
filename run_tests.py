import numpy as np, torch
from causalworld.simulator import impact_velocities,CollisionConfig,simulate_collision
from causalworld.dataset import DatasetSpec,CollisionDataset
from causalworld.model import CausalWorld
def check():
    v1,v2=impact_velocities(1,1,1,0,1); assert abs(v1)<1e-6 and abs(v2-1)<1e-6
    light=simulate_collision(CollisionConfig(m_b=.5,v_a0=1.3))["states"]
    heavy=simulate_collision(CollisionConfig(m_b=2.0,v_a0=1.3))["states"]
    assert light[-1,3]>heavy[-1,3]
    ds=CollisionDataset(DatasetSpec((.5,1.5),(.5,1.5),4,3,1)); x=ds[0]
    assert x["context"].shape==(3,60,4)
    m=CausalWorld(); p,z,ze=m(torch.randn(2,3,60,4),torch.randn(2,4),60)
    assert p.shape==(2,60,4) and z.shape==(2,8) and ze.shape==(2,3,8)
    print("ALL TESTS PASSED")
if __name__=="__main__":check()
