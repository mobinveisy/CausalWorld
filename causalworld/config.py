from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class PhysicsConfig:
    m_a: float = 1.0
    restitution: float = 0.90
    radius_a: float = 0.05
    radius_b: float = 0.05
    dt: float = 0.02
    steps: int = 60

@dataclass(frozen=True)
class SplitConfig:
    train_masses: Tuple[float, ...] = (0.50, 0.75, 1.25, 1.50, 2.00)
    iid_masses: Tuple[float, ...] = (0.50, 0.75, 1.25, 1.50, 2.00)
    interpolation_masses: Tuple[float, ...] = (1.00,)
    extrapolation_masses: Tuple[float, ...] = (2.50,)

@dataclass(frozen=True)
class ModelConfig:
    latent_dim: int = 8
    encoder_hidden: int = 48
    decoder_hidden: int = 96
