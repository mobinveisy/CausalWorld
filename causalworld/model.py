import torch
from torch import nn

class PhysicsEncoder(nn.Module):
    def __init__(self, state_dim=4, hidden=48, latent=8):
        super().__init__()
        self.frame = nn.Sequential(nn.Linear(state_dim, hidden), nn.SiLU(),
                                   nn.Linear(hidden, hidden), nn.SiLU())
        self.gru = nn.GRU(hidden, hidden, batch_first=True, bidirectional=True)
        self.head = nn.Sequential(nn.Linear(hidden*2, hidden), nn.SiLU(),
                                  nn.Linear(hidden, latent))
    def forward(self, context):
        b,k,t,d = context.shape
        x = self.frame(context.reshape(b*k,t,d))
        _, h = self.gru(x)
        h = torch.cat([h[-2], h[-1]], dim=-1)
        z_each = self.head(h).reshape(b,k,-1)
        return z_each.mean(1), z_each

class TimeDecoder(nn.Module):
    def __init__(self, cond_dim, state_dim=4, hidden=96):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim+cond_dim+1, hidden), nn.SiLU(),
            nn.Linear(hidden, hidden), nn.SiLU(),
            nn.Linear(hidden, hidden), nn.SiLU(),
            nn.Linear(hidden, state_dim)
        )
    def forward(self, initial, cond, steps):
        b = initial.shape[0]
        tau = torch.linspace(0,1,steps,device=initial.device,dtype=initial.dtype)[None,:,None].expand(b,-1,-1)
        init = initial[:,None,:].expand(-1,steps,-1)
        c = cond[:,None,:].expand(-1,steps,-1)
        return init + tau*self.net(torch.cat([init,c,tau],dim=-1))

class CausalWorld(nn.Module):
    def __init__(self, latent_dim=8, encoder_hidden=48, decoder_hidden=96):
        super().__init__()
        self.encoder = PhysicsEncoder(hidden=encoder_hidden, latent=latent_dim)
        self.decoder = TimeDecoder(latent_dim, hidden=decoder_hidden)
    def encode(self, context):
        return self.encoder(context)
    def predict(self, initial, z, steps):
        return self.decoder(initial,z,steps)
    def forward(self, context, initial, steps):
        z, ze = self.encode(context)
        return self.predict(initial,z,steps), z, ze

class NoContextDynamics(nn.Module):
    def __init__(self, hidden=96):
        super().__init__()
        self.decoder = TimeDecoder(0, hidden=hidden)
    def forward(self, initial, steps):
        return self.decoder(initial, initial.new_zeros((initial.shape[0],0)), steps)

class OracleMassDynamics(nn.Module):
    def __init__(self, hidden=96):
        super().__init__()
        self.decoder = TimeDecoder(1, hidden=hidden)
    def forward(self, initial, mass, steps):
        return self.decoder(initial, mass[:,None], steps)
