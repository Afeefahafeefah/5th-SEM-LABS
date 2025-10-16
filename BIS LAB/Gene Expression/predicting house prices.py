import random

# Toy dataset: features x, y and house price
data = [
    {'x': 1, 'y': 2, 'price': 5},
    {'x': 2, 'y': 1, 'price': 4},
    {'x': 3, 'y': 2, 'price': 8},
]

# Function and terminal sets
functions = ['+', '-', '*', '/']
terminals = ['x', 'y', '1', '2']

POP_SIZE = 6
GENERATIONS = 6
MUTATION_RATE = 0.4

# Generate a random expression
def random_expr(depth=2):
    if depth == 0 or (depth > 0 and random.random() < 0.5):
        return random.choice(terminals)
    else:
        f = random.choice(functions)
        left = random_expr(depth-1)
        right = random_expr(depth-1)
        return f'({left}{f}{right})'

# Evaluate expression safely
def eval_expr(expr, vals):
    try:
        # Add numeric constants to evaluation environment
        safe_vals = vals.copy()
        safe_vals['1'] = 1
        safe_vals['2'] = 2
        result = eval(expr, {}, safe_vals)
        # Prevent extreme values
        if result is None or abs(result) > 1e6:
            return 1e6
        return result
    except (ZeroDivisionError, OverflowError):
        return 1e6

# Fitness = sum of absolute errors
def fitness(expr):
    return sum(abs(eval_expr(expr, d) - d['price']) for d in data)

# Mutation
def mutate(expr):
    if random.random() < MUTATION_RATE:
        expr = list(expr)
        i = random.randint(0, len(expr)-1)
        if expr[i] in terminals:
            expr[i] = random.choice(terminals)
        elif expr[i] in functions:
            expr[i] = random.choice(functions)
        expr = ''.join(expr)
    return expr

# Tournament selection
def select(pop):
    return min(random.sample(pop, 2), key=lambda x: x[1])[0]

# Initialize population
population = [(random_expr(), None) for _ in range(POP_SIZE)]

best_overall = None
best_fit_overall = float('inf')

for gen in range(GENERATIONS):
    # Evaluate fitness
    population = [(expr, fitness(expr)) for expr,_ in population]
    best_expr, best_fit = min(population, key=lambda x: x[1])

    if best_fit < best_fit_overall:
        best_overall = best_expr
        best_fit_overall = best_fit

    print(f"Gen {gen}: best={best_expr}, fitness={best_fit:.2f}")

    # Reproduce new population with elitism
    new_population = [(best_expr, None)]  # keep elite
    while len(new_population) < POP_SIZE:
        parent = select(population)
        child = mutate(parent)
        new_population.append((child, None))
    population = new_population

print(f"\nBest evolved expression={best_overall}")
