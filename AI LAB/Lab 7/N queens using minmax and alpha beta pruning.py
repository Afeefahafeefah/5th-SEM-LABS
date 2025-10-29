import math

def is_safe(state, row, col):
    for r, c in enumerate(state):
        if c == col or abs(c - col) == abs(r - row):
            return False
    return True

def actions(state, n):
    row = len(state)
    return [state + [col] for col in range(n) if is_safe(state, row, col)]

def terminal_test(state, n):
    return len(state) == n

def alpha_beta_search(state, alpha, beta, n):
    if terminal_test(state, n):
      
        return 0, state  

    v = -math.inf
    best_state = None
    for child in actions(state, n):
        val, result = alpha_beta_search(child, alpha, beta, n)
   
        if result and len(result) == n:
            return val, result
        
        if val > v:
            v = val
            best_state = child
        alpha = max(alpha, v)
        if beta <= alpha:
            break

    return v, best_state

def solve_n_queens(n):
    score, solution = alpha_beta_search([], -math.inf, math.inf, n)
    if solution and len(solution) == n:
        print("Solution found:")
        print_board(solution)
    else:
        print("No valid solution found.")

def print_board(state):
    n = len(state)
    for r in range(n):
        row = ["Q" if state[r] == c else "." for c in range(n)]
        print(" ".join(row))
    print()


n = int(input("Enter N: "))
solve_n_queens(n)
