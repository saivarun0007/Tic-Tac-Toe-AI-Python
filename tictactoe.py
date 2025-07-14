"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on board.
    """
    x_count = 0
    o_count = 0
    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1

    if x_count > o_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Ensure action is valid before proceeding
    if not (0 <= action[0] < 3 and 0 <= action[1] < 3):
        raise ValueError(f"Action {action} is out of bounds.")
    if board[action[0]][action[1]] != EMPTY:
        raise ValueError(f"Action {action} is not a valid empty cell.")

    i, j = action
    new_board = copy.deepcopy(board) # CRITICAL: Use deepcopy to avoid modifying original board state
    new_board[i][j] = player(board) # The current player makes the move
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not EMPTY:
            return row[0]

    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] and board[0][j] is not EMPTY:
            return board[0][j]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    if not actions(board): # No empty cells left, so it's a tie
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    Assumes terminal(board) is True.
    """
    w = winner(board)
    if w == X:
        return 1
    elif w == O:
        return -1
    else: # It's a tie
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current_player = player(board)

    if current_player == X:
        v = -math.inf
        best_action = None
        for action in actions(board):
            # We want to maximize the value for X
            score = value(result(board, action))
            if score > v:
                v = score
                best_action = action
        return best_action

    else: # current_player == O
        v = math.inf
        best_action = None
        for action in actions(board):
            # We want to minimize the value for O
            score = value(result(board, action))
            if score < v:
                v = score
                best_action = action
        return best_action


def value(board):
    """
    Helper function for minimax:
    Returns the optimal value for the current player on the board.
    """
    if terminal(board):
        return utility(board)

    if player(board) == X: # Maximizing player (X)
        v = -math.inf
        for action in actions(board):
            v = max(v, value(result(board, action)))
        return v

    else: # Minimizing player (O)
        v = math.inf
        for action in actions(board):
            v = min(v, value(result(board, action)))
        return v