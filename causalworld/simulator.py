from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class CollisionConfig:
    m_a: float = 1.0
    m_b: float = 1.0
    x_a0: float = 0.0
    x_b0: float = 1.0
    v_a0: float = 1.0
    v_b0: float = 0.0
    radius_a: float = 0.05
    radius_b: float = 0.05
    restitution: float = 0.90
    dt: float = 0.02
    steps: int = 60

def impact_velocities(m1, m2, u1, u2, e=1.0):
    denom = m1 + m2
    v1 = (m1*u1 + m2*u2 - m2*e*(u1-u2)) / denom
    v2 = (m1*u1 + m2*u2 + m1*e*(u1-u2)) / denom
    return float(v1), float(v2)

def simulate_collision(cfg: CollisionConfig):
    x1, x2, v1, v2 = map(float, (cfg.x_a0, cfg.x_b0, cfg.v_a0, cfg.v_b0))
    collided = False
    collision_index = -1
    states = np.zeros((cfg.steps, 4), dtype=np.float32)
    for t in range(cfg.steps):
        states[t] = (x1, x2, v1, v2)
        nx1, nx2 = x1 + v1*cfg.dt, x2 + v2*cfg.dt
        if (not collided) and (nx1 + cfg.radius_a >= nx2 - cfg.radius_b):
            v1, v2 = impact_velocities(cfg.m_a, cfg.m_b, v1, v2, cfg.restitution)
            collided = True
            collision_index = t
            contact = 0.5 * ((nx1 + cfg.radius_a) + (nx2 - cfg.radius_b))
            nx1, nx2 = contact - cfg.radius_a, contact + cfg.radius_b
        x1, x2 = nx1, nx2
    return {
        "states": states,
        "initial": np.asarray([cfg.x_a0, cfg.x_b0, cfg.v_a0, cfg.v_b0], np.float32),
        "collision_index": collision_index,
        "mass_b": float(cfg.m_b),
    }
