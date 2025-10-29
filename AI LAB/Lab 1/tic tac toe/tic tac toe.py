import math

# Initialize empty board
board = [" " for _ in range(9)]

def print_board(board):
    """Display the Tic Tac Toe board"""
    for i in range(3):
        row = board[i*3:(i+1)*3]
        print("| " + " | ".join(row) + " |")
    print()

def available_moves(board):
    """Return list of available move indices"""
    return [i for i, cell in enumerate(board) if cell == " "]

def winner(board):
    """Check if there is a winner or tie"""
    win_cond = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]

    for combo in win_cond:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != " ":
            return board[combo[0]]

    if " " not in board:
        return "Tie"

    return None

def minimax(board, depth, is_maximizing):
    """Minimax algorithm to find the optimal move"""
    result = winner(board)
    if result == "X":
        return -1
    elif result == "O":
        return 1
    elif result == "Tie":
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in available_moves(board):
            board[move] = "O"
            score = minimax(board, depth + 1, False)
            board[move] = " "
            best_score = max(score, best_score)
        return best_score

    else:
        best_score = math.inf
        for move in available_moves(board):
            board[move] = "X"
            score = minimax(board, depth + 1, True)
            board[move] = " "
            best_score = min(score, best_score)
        return best_score

def best_move(board):
    """Find the best move for AI using minimax"""
    best_score = -math.inf
    move = None
    for i in available_moves(board):
        board[i] = "O"
        score = minimax(board, 0, False)
        board[i] = " "
        if score > best_score:
            best_score = score
            move = i
    return move

def play():
    """Main game loop"""
    print("Tic Tac Toe (You = X, AI = O)")
    print_board(board)

    while True:
        # Human move
        try:
            human_move = int(input("Enter your move (0-8): "))
            if human_move < 0 or human_move > 8 or board[human_move] != " ":
                print("Invalid move, try again.\n")
                continue
        except ValueError:
            print("Please enter a valid number (0-8).\n")
            continue

        board[human_move] = "X"
        print_board(board)

        if winner(board):
            print("Winner:", winner(board))
            break

        # AI move
        ai_move = best_move(board)
        board[ai_move] = "O"
        print(f"AI chose: {ai_move}\n")
        print_board(board)

        if winner(board):
            print("Winner:", winner(board))
            break

# Start game
play()
