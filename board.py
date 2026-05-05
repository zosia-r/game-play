"""
Board representation, creation and display.


Board orientation:
  - row 0 - top of the board - black's starting row
  - row (rows-1) - bottom of the board - white's starting row

Players:
  - W = white - player 1, starts on the bottom two rows, moves upward (row index decreases),
       wins by reaching row 0.
  - B = black - player 2, starts on the top two rows, moves downward (row index increases),
       wins by reaching row (rows-1).
"""

from config import PLAYER_W, PLAYER_B, EMPTY, LAST_MARK


def make_initial_board(rows: int = 8, cols: int = 8) -> list[list[str]]:
    board = [[EMPTY] * cols for _ in range(rows)]

    # black on top
    for row in range(2):
        for col in range(cols):
            board[row][col] = PLAYER_B

    # white on bottom
    for row in range(rows - 2, rows):
        for col in range(cols):
            board[row][col] = PLAYER_W

    return board


def board_to_string(board: list[list[str]]) -> str:
    lines = []
    for row in board:
        lines.append(" ".join(row))
    return "\n".join(lines)
