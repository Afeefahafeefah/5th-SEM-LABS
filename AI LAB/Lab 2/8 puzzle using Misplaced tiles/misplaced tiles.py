from queue import PriorityQueue

# Function to count misplaced tiles
def misplaced(current, goal):
    return sum(1 for i in range(9) if current[i] != 0 and current[i] != goal[i])

# Get all possible next states
def get_neighbors(state):
    neighbors = []
    i = state.index(0)
    row, col = divmod(i, 3)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

    for dr, dc in moves:
        r, c = row + dr, col + dc
        if 0 <= r < 3 and 0 <= c < 3:
            new_i = r * 3 + c
            new_state = list(state)
            new_state[i], new_state[new_i] = new_state[new_i], new_state[i]
            neighbors.append(tuple(new_state))
    return neighbors

# Solve 8 puzzle using Greedy / Best First Search with g,h,f print
def solve_8_puzzle(start, goal):
    pq = PriorityQueue()
    pq.put((misplaced(start, goal), 0, [start]))  # (h, g, path)
    visited = set()

    while not pq.empty():
        h, g, path = pq.get()
        state = path[-1]

        print("Current state:")
        print_board(state)
        print(f"g(n) = {g}, h(n) = {h}, f(n) = {g + h}")
        print("-" * 20)

        if state == goal:
            print("\nSolution found in", g, "moves!\n")
            for step in path:
                print_board(step)
                print()
            return

        visited.add(state)

        for neighbor in get_neighbors(list(state)):
            if neighbor not in visited:
                new_g = g + 1
                new_h = misplaced(neighbor, goal)
                pq.put((new_h, new_g, path + [neighbor]))

    print("No solution found.")

def print_board(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])

# Example usage
start = (1, 2, 3,
         4, 5, 6,
         0, 7, 8)

goal = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)

solve_8_puzzle(start, goal)