# =====================================================================
# PROJECT: Web-Based Tic-Tac-Toe using Minimax Algorithm
# TECH STACK: Python (Flask Backend) + HTML/CSS/JS (Frontend)
# FEATURES: First-Player Selection (Human / AI Bot), Optimal Minimax
# =====================================================================

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Representing players
HUMAN = 'O'
AI = 'X'
EMPTY = ''


def check_winner(board):
    """
    Checks if there is a winner on the 3x3 board.
    Returns 'X', 'O', 'Draw', or None (if game is ongoing).
    """
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]

    for condition in win_conditions:
        a, b, c = condition
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]

    if EMPTY not in board:
        return 'Draw'

    return None


def minimax(board, depth, is_maximizing):
    """
    Minimax Algorithm: Recursively evaluates all possible board positions.
    - AI ('X') tries to maximize score (+10).
    - Human ('O') tries to minimize score (-10).
    """
    result = check_winner(board)

    # Base Cases (Terminal States)
    if result == AI:
        return 10 - depth  # Prefer faster wins
    if result == HUMAN:
        return depth - 10  # Delay inevitable losses
    if result == 'Draw':
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = AI
                score = minimax(board, depth + 1, False)
                board[i] = EMPTY
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = HUMAN
                score = minimax(board, depth + 1, True)
                board[i] = EMPTY
                best_score = min(score, best_score)
        return best_score


def find_best_move(board):
    """
    Evaluates minimax scores for all empty cells and returns
    the best move index (0-8) for AI ('X').
    """
    best_score = -float('inf')
    best_move = -1

    for i in range(9):
        if board[i] == EMPTY:
            board[i] = AI
            score = minimax(board, 0, False)
            board[i] = EMPTY
            if score > best_score:
                best_score = score
                best_move = i

    return best_move


# ---------------------------------------------------------------------
# Web Server Routes
# ---------------------------------------------------------------------

@app.route('/')
def home():
    """Renders the main web page."""
    return render_template('index.html')


@app.route('/move', methods=['POST'])
def make_move():
    """
    Executes AI move using Minimax and returns updated state.
    Handles both AI opening moves and mid-game turns.
    """
    data = request.get_json()
    board = data.get('board', [EMPTY] * 9)

    # Check if game is already terminal
    status = check_winner(board)
    if status is not None:
        return jsonify({'board': board, 'status': status, 'ai_move': None})

    # Find optimal AI move
    ai_index = find_best_move(board)
    if ai_index != -1:
        board[ai_index] = AI

    # Re-evaluate status after AI move
    status = check_winner(board)

    return jsonify({
        'board': board,
        'status': status if status else 'Ongoing',
        'ai_move': ai_index
    })


if __name__ == '__main__':
    app.run(debug=True)