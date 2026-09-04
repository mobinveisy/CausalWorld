import torch
import torch.nn.functional as F

def consistency_loss(z_each):
    return ((z_each-z_each.mean(1,keepdim=True))**2).mean()

def variance_loss(z, floor=0.20):
    std = torch.sqrt(z.var(0,unbiased=False)+1e-4)
    return torch.relu(floor-std).mean()

def causal_loss(pred,y,cf_pred,ycf,z,ze,zcf,zecf,
                w_cf=1.0,w_effect=1.0,w_cons=0.1,w_var=0.03):
    factual = F.mse_loss(pred,y)
    counterfactual = F.mse_loss(cf_pred,ycf)

    # Strong causal objective: predicted intervention effect should match the
    # true matched counterfactual effect, not merely each trajectory separately.
    true_effect = ycf - y
    pred_effect = cf_pred - pred
    effect = F.mse_loss(pred_effect,true_effect)

    cons = 0.5*(consistency_loss(ze)+consistency_loss(zecf))
    var = 0.5*(variance_loss(z)+variance_loss(zcf))
    total = factual + w_cf*counterfactual + w_effect*effect + w_cons*cons + w_var*var
    return total, {
        "loss": float(total.detach()), "factual": float(factual.detach()),
        "counterfactual": float(counterfactual.detach()), "effect": float(effect.detach()),
        "consistency": float(cons.detach()), "variance": float(var.detach())
    }
