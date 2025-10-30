import numpy as np
import math


P = 5000      
L = 2          
E = 2e11       
rho = 7850     
stress_limit = 100e6  
deflection_limit = 0.0027  


def objective_function(x):
    b, h = x  
    weight = rho * b * h * L  

    
    stress = (6 * P * L) / (b * h ** 2)

    
    deflection = (4 * P * L ** 3) / (E * b * h ** 3)

    
    penalty = 0
    if stress > stress_limit:
        penalty += (stress - stress_limit) ** 2
    if deflection > deflection_limit:
        penalty += (deflection - deflection_limit) ** 2

    return weight + 1e10 * penalty  


def levy_flight(Lambda):
    sigma = (math.gamma(1 + Lambda) * math.sin(math.pi * Lambda / 2) /
            (math.gamma((1 + Lambda) / 2) * Lambda * 2 ** ((Lambda - 1) / 2))) ** (1 / Lambda)
    u = np.random.randn(2) * sigma
    v = np.random.randn(2)
    step = u / np.abs(v) ** (1 / Lambda)
    return step


def cuckoo_search(n=15, max_iter=50, pa=0.25):
    nests = np.random.uniform([0.01, 0.01], [0.1, 0.3], (n, 2))  
    fitness = np.array([objective_function(x) for x in nests])
    best = nests[np.argmin(fitness)]

    for t in range(max_iter):
        for i in range(n):
            step_size = 0.01 * levy_flight(1.5)
            new_solution = nests[i] + step_size * (nests[i] - best)
            new_solution = np.clip(new_solution, [0.01, 0.01], [0.1, 0.3])
            new_fitness = objective_function(new_solution)

            if new_fitness < fitness[i]:
                nests[i] = new_solution
                fitness[i] = new_fitness

        rand = np.random.rand(n)
        for i in range(n):
            if rand[i] < pa:
                nests[i] = np.random.uniform([0.01, 0.01], [0.1, 0.3])
                fitness[i] = objective_function(nests[i])

        best = nests[np.argmin(fitness)]
        if (t + 1) % 10 == 0:
            print(f"Iteration {t+1}: Best = {best}, Weight = {objective_function(best):.5f}")

    return best


best_solution = cuckoo_search()
print("\nOptimal Beam Dimensions (b, h):", best_solution)
b, h = best_solution
print(f"Final Weight = {objective_function(best_solution):.4f} kg")