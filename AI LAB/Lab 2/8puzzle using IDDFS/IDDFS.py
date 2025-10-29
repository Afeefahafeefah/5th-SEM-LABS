from collections import deque


def get_neighbors(state):
    neighbors = []
    i = state.index(0)
    row, col = divmod(i, 3)
    moves = [(-1,0),(1,0),(0,-1),(0,1)]  # up, down, left, right

    for dr, dc in moves:
        r, c = row + dr, col + dc
        if 0 <= r < 3 and 0 <= c < 3:
            new_i = r * 3 + c
            new_state = list(state)
            new_state[i], new_state[new_i] = new_state[new_i], new_state[i]
            neighbors.append(tuple(new_state))
    return neighbors

# Depth-Limited DFS
def DLS(state, goal, depth, visited, path, node_labels, node_counter, level_nodes):
    if depth not in level_nodes:
        level_nodes[depth] = []

    label = node_labels[state]
    level_nodes[depth].append(label)

    if state == goal:
        return path, True

    if depth == 0:
        return None, False

    visited.add(state)

    for neighbor in get_neighbors(list(state)):
        if neighbor not in visited:
            node_counter[0] += 1
            node_labels[neighbor] = chr(65 + (node_counter[0] % 26))  # A-Z cycle
            result, found = DLS(neighbor, goal, depth - 1, visited.copy(),
                                path + [neighbor], node_labels, node_counter, level_nodes)
            if found:
                return result, True
    return None, False

# Iterative Deepening DFS
def IDDFS(start, goal, max_depth=10):
    for depth in range(max_depth + 1):
        node_labels = {start: 'A'}
        node_counter = [0]
        level_nodes = {}
        print(f"\nDepth limit = {depth}")
        path, found = DLS(start, goal, depth, set(), [start], node_labels, node_counter, level_nodes)

        # Print nodes encountered at each depth
        for lvl in sorted(level_nodes.keys()):
            print(f"Depth {depth - lvl}: {', '.join(level_nodes[lvl])}")

        if found:
            print("\nSolution found at depth", depth, "in", len(path) - 1, "moves!\n")
            print("Final Path (Node Labels):")
            for i, step in enumerate(path):
                print(f"Node {node_labels[step]}:")
                print_board(step)
                print()
            return

    print("\nNo solution found within depth limit.")

def print_board(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])

# Example usage
start = (1, 2, 3,
         4, 0, 6,
         7, 5, 8)

goal = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)

IDDFS(start, goal, max_depth=5)