import numpy as np
import random

# Objective function: smaller = better (less energy)
def energy_function(x):
    orientation, east, west, shading = x
    return (orientation - 90)**2 + (east - 3)**2 + (west - 2)**2 + (shading - 0.5)**2

# Grey Wolf Optimizer 
def GWO(num_wolves=6, max_iter=20):
    dim = 4
    bounds = [(0, 180), (1, 5), (1, 5), (0.2, 0.8)]  # limits for each parameter
    
    # initialize wolves randomly
    wolves = [np.array([random.uniform(lb, ub) for lb, ub in bounds]) for _ in range(num_wolves)]
    scores = [energy_function(w) for w in wolves]
    
    # identify alpha, beta, delta
    idx = np.argsort(scores)
    alpha, beta, delta = wolves[idx[0]], wolves[idx[1]], wolves[idx[2]]
    
    for t in range(max_iter):
        a = 2 - 2*(t/max_iter)  # linearly decreasing from 2 to 0
        
        for i in range(num_wolves):
            X = wolves[i]
            A1, C1 = 2*a*random.random() - a, 2*random.random()
            A2, C2 = 2*a*random.random() - a, 2*random.random()
            A3, C3 = 2*a*random.random() - a, 2*random.random()

            D_alpha = abs(C1*alpha - X)
            D_beta = abs(C2*beta - X)
            D_delta = abs(C3*delta - X)

            X1 = alpha - A1*D_alpha
            X2 = beta  - A2*D_beta
            X3 = delta - A3*D_delta

            new_pos = (X1 + X2 + X3)/3

            # clip to bounds
            for j in range(dim):
                lb, ub = bounds[j]
                new_pos[j] = np.clip(new_pos[j], lb, ub)
            
            wolves[i] = new_pos
        
        # update best wolves
        scores = [energy_function(w) for w in wolves]
        idx = np.argsort(scores)
        alpha, beta, delta = wolves[idx[0]], wolves[idx[1]], wolves[idx[2]]

        if t % 5 == 0 or t == max_iter-1:
            print(f"Iteration {t+1}: Best Energy = {scores[idx[0]]:.4f}, Best Design = {alpha}")

    print("\n🏁 Final Best Design Found:")
    print(f"Orientation: {alpha[0]:.2f}°")
    print(f"East window width: {alpha[1]:.2f} m")
    print(f"West window width: {alpha[2]:.2f} m")
    print(f"Shading transmittance: {alpha[3]:.2f}")
    print(f"Minimum estimated energy: {energy_function(alpha):.4f}")

# Run
GWO()
