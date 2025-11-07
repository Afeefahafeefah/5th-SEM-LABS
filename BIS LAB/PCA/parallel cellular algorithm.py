import random

# Define jobs and machines
jobs = ["J1", "J2", "J3", "J4", "J5"]
num_cells = 5  # number of parallel cells
iterations = 10

# Random initial job orders
population = [random.sample(jobs, len(jobs)) for _ in range(num_cells)]

def fitness(order):
    """Dummy fitness: sum of job indices (pretend processing time). Lower = better."""
    return sum(jobs.index(j) + 1 for j in order)

for it in range(iterations):
    print(f"\nIteration {it+1}")
    fitness_values = [fitness(order) for order in population]

    # Print current population
    for i, order in enumerate(population):
        print(f"Cell {i+1}: {order}, Fitness = {fitness_values[i]}")

    # Each cell interacts with neighbor (if better)
    for i in range(num_cells):
        neighbor = population[(i + 1) % num_cells]
        if fitness(neighbor) < fitness(population[i]):
            # Slightly copy neighbor (simulate improvement)
            swap_idx = random.randint(0, len(jobs)-1)
            population[i][swap_idx] = neighbor[swap_idx]

best = min(population, key=fitness)
print("\n✅ Best schedule found:", best, "with fitness =", fitness(best))
