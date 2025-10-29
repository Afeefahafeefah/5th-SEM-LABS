from queue import PriorityQueue

# Manhattan distance heuristic
def manhattan(current, goal):
    dist = 0
    for i in range(9):
        if current[i] != 0:
            goal_index = goal.index(current[i])
            x1, y1 = divmod(i, 3)
            x2, y2 = divmod(goal_index, 3)
            dist += abs(x1 - x2) + abs(y1 - y2)
    return dist

# Generate neighboring states
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

# A* search using Manhattan distance
def solve_8_puzzle_manhattan(start, goal):
    pq = PriorityQueue()
    pq.put((manhattan(start, goal), 0, [start]))  # (f, g, path)
    visited = set()

    while not pq.empty():
        f, g, path = pq.get()
        state = path[-1]
        h = manhattan(state, goal)

        print("Current state:")
        print_board(state)
        print(f"g(n) = {g}, h(n) = {h}, f(n) = {g + h}")
        print("-" * 25)

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
                new_h = manhattan(neighbor, goal)
                new_f = new_g + new_h
                pq.put((new_f, new_g, path + [neighbor]))

    print("No solution found.")

def print_board(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])

# Example usage
start = (1, 0, 3,
         4, 2, 6,
         7, 5, 8)

goal = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)

solve_8_puzzle_manhattan(start, goal)
