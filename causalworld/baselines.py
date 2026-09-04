import numpy as np
from .simulator import CollisionConfig, simulate_collision

def constant_velocity(initial,steps,dt):
    initial=np.asarray(initial,np.float32)
    n=len(initial); out=np.zeros((n,steps,4),np.float32)
    for t in range(steps):
        tt=t*dt
        out[:,t,0]=initial[:,0]+initial[:,2]*tt
        out[:,t,1]=initial[:,1]+initial[:,3]*tt
        out[:,t,2:]=initial[:,2:]
    return out

def analytic_oracle(initial,masses,steps,physics):
    rows=[]
    for s,m in zip(initial,masses):
        rows.append(simulate_collision(CollisionConfig(
            m_a=physics.m_a,m_b=float(m),x_a0=float(s[0]),x_b0=float(s[1]),
            v_a0=float(s[2]),v_b0=float(s[3]),radius_a=physics.radius_a,
            radius_b=physics.radius_b,restitution=physics.restitution,
            dt=physics.dt,steps=steps
        ))["states"])
    return np.stack(rows)
