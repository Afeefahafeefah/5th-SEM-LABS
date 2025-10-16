import random
import math

# Coordinates: depot at (0,0), 6 customers
customers = [(0, 0), (2, 5), (5, 2), (6, 6), (8, 3), (1, 7), (7, 8)]
num_customers = len(customers)

population_size = 20
generations = 100
crossover_rate = 0.8
mutation_rate = 0.2

def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def route_distance(route):
    dist = distance(customers[0], customers[route[0]])
    for i in range(len(route)-1):
        dist += distance(customers[route[i]], customers[route[i+1]])
    dist += distance(customers[route[-1]], customers[0])
    return dist

def fitness(route):
    return 1 / (route_distance(route) + 1e-6)

def create_individual():
    route = list(range(1, num_customers))
    random.shuffle(route)
    return route

def crossover(parent1, parent2):
    if random.random() > crossover_rate:
        return parent1[:]
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child = [None]*len(parent1)
    child[start:end+1] = parent1[start:end+1]
    pos = (end+1) % len(parent1)
    for city in parent2:
        if city not in child:
            child[pos] = city
            pos = (pos+1) % len(parent1)
    return child

def mutate(route):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]

def select(population, fitnesses):
    total_fit = sum(fitnesses)
    pick = random.uniform(0, total_fit)
    current = 0
    for ind, fit in zip(population, fitnesses):
        current += fit
        if current > pick:
            return ind
    return population[-1]

# Main GA loop
population = [create_individual() for _ in range(population_size)]
best_route = None
best_distance = float("inf")

for gen in range(generations):
    fitnesses = [fitness(ind) for ind in population]
    new_population = []

    # Elitism
    best_idx = fitnesses.index(max(fitnesses))
    if route_distance(population[best_idx]) < best_distance:
        best_route = population[best_idx][:]
        best_distance = route_distance(best_route)
    new_population.append(best_route)

    while len(new_population) < population_size:
        parent1 = select(population, fitnesses)
        parent2 = select(population, fitnesses)
        child = crossover(parent1, parent2)
        mutate(child)
        new_population.append(child)

    population = new_population

    if gen % 10 == 0:
        print(f"Gen {gen}: Best Distance = {best_distance:.2f}")

# Results
print("\nBest route found:", best_route)
print("Best distance:", round(best_distance, 2))
