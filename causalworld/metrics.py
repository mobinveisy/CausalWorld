import numpy as np
from scipy.stats import spearmanr
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

def trajectory_metrics(pred,y):
    d = np.linalg.norm(pred[...,:2]-y[...,:2],axis=-1)
    return {
        "mse": float(np.mean((pred-y)**2)),
        "ade": float(d.mean()),
        "fde": float(d[:,-1].mean()),
        "pcve": float(np.abs(pred[:,-1,3]-y[:,-1,3]).mean()),
    }

def cee(pred,y,cf_pred,ycf):
    real = ycf[:,-1,3]-y[:,-1,3]
    est = cf_pred[:,-1,3]-pred[:,-1,3]
    return float(np.abs(real-est).mean())

def latent_probe(z,mass):
    if z is None or len(np.unique(mass)) < 2:
        return {"mass_probe_r2": float("nan"), "pc1_mass_spearman": float("nan")}
    reg = LinearRegression().fit(z,mass)
    r2 = float(r2_score(mass,reg.predict(z)))
    zc = z-z.mean(0,keepdims=True)
    _,_,vt = np.linalg.svd(zc,full_matrices=False)
    rho = spearmanr(zc@vt[0],mass).statistic
    return {"mass_probe_r2": r2, "pc1_mass_spearman": float(abs(rho))}
