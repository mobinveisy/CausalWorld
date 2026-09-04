from pathlib import Path
import matplotlib.pyplot as plt
from causalworld.simulator import CollisionConfig,simulate_collision
out=Path('paper_assets_demo'); out.mkdir(exist_ok=True)
plt.figure(figsize=(8,4))
for mass in [0.5,1.0,1.5,2.5]:
    s=simulate_collision(CollisionConfig(m_b=mass,v_a0=1.4))['states']
    plt.plot(s[:,1],label=f'm_B={mass}')
plt.xlabel('frame'); plt.ylabel('object B position'); plt.legend(); plt.tight_layout(); plt.savefig(out/'hidden_mass_effect.png',dpi=180)
print(out/'hidden_mass_effect.png')
