# 4-Queens Hill Climbing
#x0=3,x1=1,x2=2,x3=0
import copy

N = 4

# Cost function: counts number of attacking queen pairs
def cost(state):
    attacks = 0
    for i in range(N):
        for j in range(i+1, N):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                attacks += 1
    return attacks

# Generate all neighbours by moving each queen to every other row
def get_neighbours(state):
    neighbours = []
    for col in range(N):
        for row in range(N):
            if row != state[col]:                 # move queen in the same column
                new_state = state.copy()
                new_state[col] = row
                neighbours.append(new_state)
    return neighbours

# Hill Climbing algorithm
def hill_climbing(initial_state):
    current = initial_state
    steps = 1
    print(f"Step {steps}: State = {current}, Cost = {cost(current)}")

    while True:
        neighbours = get_neighbours(current)
        
        # Calculate cost for all neighbours
        neighbour_costs = [(cost(n), n) for n in neighbours]
        
        # Find neighbour with minimum cost
        neighbour_costs.sort(key=lambda x: (x[0], x[1]))  # tie-breaker: lexicographically smallest
        best_cost, best_neighbour = neighbour_costs[0]

        # Show all neighbours
        print("\nNeighbours and costs:")
        for c, n in neighbour_costs:
            print(f"State = {n}, Cost = {c}")

        # If no improvement, stop
        if best_cost >= cost(current):
            print("\nNo better neighbour found. Algorithm terminates.")
            break

        # Move to the best neighbour
        current = best_neighbour
        steps += 1
        print(f"\nStep {steps}: Move to {current}, Cost = {cost(current)}")

        # If goal reached
        if cost(current) == 0:
            print("\nGoal state reached!")
            break

    print(f"\nFinal State: {current}, Final Cost: {cost(current)}")
    return current


# Initial state from your example
initial_state = [3, 1, 2, 0]
final_state = hill_climbing(initial_state)
