#finding the optimal Time Multiplier Setting and Plug Settings of overcurrent relays in a power system.

import numpy as np

# --- Problem Parameters ---
n_relays = 3
CTI = 0.2
I_fault = np.array([5.5, 4.8, 4.2])  # fault currents (example)
w_i = np.ones(n_relays)              # all equal importance

# Bounds
TMS_min, TMS_max = 0.1, 1.0
PS_min, PS_max = 0.5, 2.0

# --- PSO Parameters ---
num_particles = 20
max_iter = 100
w = 0.7      # inertia weight
c1 = 1.5     # cognitive coefficient
c2 = 1.5     # social coefficient

# --- Objective Function ---
def relay_time(TMS, PS, I):
    return 0.14 * TMS / ((I / PS)**0.02 - 1)

def objective(X):
    TMS = X[0::2]
    PS = X[1::2]
    t = relay_time(TMS, PS, I_fault)
    penalty = 0
   
    # Constraint: primary-backup coordination
    for i in range(n_relays-1):
        if t[i+1] - t[i] < CTI:
            penalty += 1000 * abs(CTI - (t[i+1] - t[i]))
   
    return np.sum(w_i * t) + penalty

# --- Initialize Swarm ---
dim = 2 * n_relays
pos = np.random.uniform(low=[TMS_min, PS_min]*n_relays,
                        high=[TMS_max, PS_max]*n_relays,
                        size=(num_particles, dim))
vel = np.zeros((num_particles, dim))
pbest = pos.copy()
pbest_val = np.array([objective(p) for p in pbest])
gbest = pbest[np.argmin(pbest_val)]
gbest_val = np.min(pbest_val)

# --- PSO Loop ---
for _ in range(max_iter):
    for i in range(num_particles):
        r1, r2 = np.random.rand(dim), np.random.rand(dim)
        vel[i] = (w * vel[i] +
                  c1 * r1 * (pbest[i] - pos[i]) +
                  c2 * r2 * (gbest - pos[i]))
        pos[i] += vel[i]
       
        # enforce bounds
        pos[i][0::2] = np.clip(pos[i][0::2], TMS_min, TMS_max)
        pos[i][1::2] = np.clip(pos[i][1::2], PS_min, PS_max)
       
        val = objective(pos[i])
        if val < pbest_val[i]:
            pbest[i] = pos[i].copy()
            pbest_val[i] = val
   
    # update global best
    if np.min(pbest_val) < gbest_val:
        gbest = pbest[np.argmin(pbest_val)]
        gbest_val = np.min(pbest_val)

# --- Result ---
print("Optimal settings (TMS, PS):")
for i in range(n_relays):
    print(f"Relay {i+1}: TMS={gbest[2*i]:.3f}, PS={gbest[2*i+1]:.3f}")
print(f"\nMinimum total operation time = {gbest_val:.4f}")