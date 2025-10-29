import random
import math

# Number of queens
N = 8

# ----- Cost Function -----
# Counts the number of attacking pairs of queens (lower is better)
def cost(state):
    attacks = 0
    for i in range(N):
        for j in range(i+1, N):
            # Same row or diagonal conflict
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                attacks += 1
    return attacks


# ----- Generate a random neighbour -----
# Changes the row of one queen randomly
def random_neighbour(state):
    neighbour = state.copy()
    col = random.randint(0, N-1)                # pick a random column
    neighbour[col] = random.randint(0, N-1)     # move queen to a new row
    return neighbour


# ----- Simulated Annealing Algorithm -----
def simulated_annealing():
    # Step 1: current ← initial state
    current = [random.randint(0, N-1) for _ in range(N)]

    # Step 2: T ← a large positive value
    T = 1000

    while T > 1e-3:   # Step 3: while T > 0 do
        # Step 4: next ← a random neighbour of current
        next_state = random_neighbour(current)

        # Step 5: ΔE ← current.cost - next.cost
        delta_E = cost(current) - cost(next_state)

        # Step 6 & 7: Accept better solution
        if delta_E > 0:
            current = next_state
        else:
            # Step 8 & 9: Accept worse solution with probability e^(ΔE/T)
            p = math.exp(delta_E / T)
            if random.random() < p:
                current = next_state

        # Step 11: decrease T
        T *= 0.95

        # Stop early if we found a perfect solution
        if cost(current) == 0:
            break

    return current


# ----- Run the Algorithm -----
solution = simulated_annealing()

# ----- Display Result -----
print("Final Board State (row positions):", solution)
print("Attacking pairs:", cost(solution))

# Display board visually
def print_board(state):
    for row in range(N):
        line = ""
        for col in range(N):
            if state[col] == row:
                line += " Q "
            else:
                line += " - "
        print(line)
    print()

print_board(solution)
