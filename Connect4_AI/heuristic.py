from State import State
from constant import *


def heuristic(state: State):
    # Implements the heuristic here
    score = 0
    board = state.state_board
    score += 1000 * eval_score_four_consecutive(board, PLAYER)
    score -= 1000 * eval_score_four_consecutive(board, AI)
    score += 10 * eval_score_three_consecutive(board, PLAYER)
    score -= 10 * eval_score_three_consecutive(board, AI)
    score += 5 * eval_center_score(board, PLAYER)
    score -= 5 * eval_center_score(board, AI)

    return score


def eval_score_four_consecutive(board, player):
    count = 0
    # Horizontal score
    for row in range(6):
        for col in range(4):
            if all(board[row][col + i] == player for i in range(4)):
                count += 1
    # Vertical Score
    for row in range(3):
        for col in range(7):
            if all(board[row + i][col] == player for i in range(4)):
                count += 1
    # Diagonal score
    for row in range(3):
        for col in range(4):
            if all(board[row + i][col + i] == player for i in range(4)):
                count += 1
    for row in range(3):
        for col in range(3, 7):
            if all(board[row + i][col - i] == player for i in range(4)):
                count += 1
    return count


def eval_score_three_consecutive(board, player):
    count = 0
    # Horizontal
    for row in range(6):
        for col in range(5):
            if col == 4:
                if (
                    board[row][col] == player
                    and board[row][col + 1] == player
                    and board[row][col + 2] == "-"
                ) or (
                    board[row][col] == player
                    and board[row][col + 1] == player
                    and board[row][col + 2] == player
                ):
                    count += 1
            else:
                if (
                    board[row][col] == player
                    and board[row][col + 1] == player
                    and board[row][col + 2] == "-"
                    and board[row][col + 3] == player
                ):
                    count += 1
    # Vertical
    for row in range(4):
        for col in range(7):
            if row == 3:
                if (
                    board[row][col] == player
                    and board[row + 1][col] == player
                    and board[row + 2][col] == "-"
                ) or (
                    board[row][col] == player
                    and board[row + 1][col] == player
                    and board[row + 2][col] == player
                ):
                    count += 1
            else:
                if (
                    board[row][col] == player
                    and board[row + 1][col] == player
                    and board[row + 2][col] == "-"
                    and board[row + 3][col] == player
                ):
                    count += 1
    # Diagonal
    for row in range(4):
        for col in range(5):
            if col == 4 or row == 3:
                if (
                    board[row][col] == player
                    and board[row + 1][col + 1] == player
                    and board[row + 2][col + 2] == "-"
                ):
                    count += 1
            else:
                if (
                    board[row][col] == player
                    and board[row + 1][col + 1] == player
                    and board[row + 2][col + 2] == "-"
                    and board[row + 3][col + 3] == player
                ):
                    count += 1
    for row in range(4):
        for col in range(2, 7):
            if row == 3:
                if (
                    board[row][col] == player
                    and board[row + 1][col - 1] == player
                    and board[row + 2][col - 2] == "-"
                ) or (
                    board[row][col] == player
                    and board[row + 1][col - 1] == player
                    and board[row + 2][col - 2] == player
                ):
                    count += 1
            else:
                if (
                    board[row][col] == player
                    and board[row + 1][col - 1] == player
                    and board[row + 2][col - 2] == "-"
                    and board[row + 3][col - 3] == player
                ):
                    count += 1
    return count


def eval_center_score(board, player):
    count = sum(board[row][col] == player for row in range(6) for col in range(3, 5))
    return count
