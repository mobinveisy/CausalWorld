# Method pseudocode for the later paper

```text
Input:
  passive context C = {tau_1, ..., tau_K}
  query initial state s0
  matched counterfactual context C_cf

z      = PhysicsEncoder(C)
z_cf   = PhysicsEncoder(C_cf)

tau_hat    = DynamicsDecoder(s0, z)
tau_cf_hat = DynamicsDecoder(s0, z_cf)

L_factual = MSE(tau_hat, tau)
L_cf      = MSE(tau_cf_hat, tau_cf)
L_effect  = MSE((tau_cf_hat - tau_hat), (tau_cf - tau))
L_cons    = within-world latent consistency
L_var     = anti-collapse regularizer

L = L_factual + lambda_cf L_cf + lambda_effect L_effect
    + lambda_cons L_cons + lambda_var L_var
```

The paper should show equations/pseudocode, not paste long source files into the main body. The repository is the source of truth for exact implementation.
