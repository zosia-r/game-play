"""
Board representation, creation and display for Breakthrough.

Board layout (printed)
----------------------
  Row 0 is printed at the top.
  Row (rows-1) is printed at the bottom.

  W starts on the bottom two rows (rows-1, rows-2) and moves upward.
  B starts on the top two rows (0, 1) and moves downward.

Cell symbols
------------
  W  – Player 1 piece
  B  – Player 2 piece
  _  – Empty cell
  o  – Cell vacated by the last move (output marker only)
"""

from constants import PLAYER_W, PLAYER_B, EMPTY, LAST_MARK


def make_initial_board(rows: int = 8, cols: int = 8) -> list[list[str]]:
    """Return the standard Breakthrough starting position for an n×m board.

    W occupies the bottom two rows; B occupies the top two rows.
    W moves first.
    """
    board = [[EMPTY] * cols for _ in range(rows)]

    # B on rows 0 and 1 (top)
    for r in range(2):
        for c in range(cols):
            board[r][c] = PLAYER_B

    # W on rows rows-2 and rows-1 (bottom)
    for r in range(rows - 2, rows):
        for c in range(cols):
            board[r][c] = PLAYER_W

    return board


def board_to_string(
    board: list[list[str]],
    last_from: tuple[int, int] | None = None,
) -> str:
    """Render the board as a multi-line string.

    Parameters
    ----------
    board:      2-D list of cell symbols.
    last_from:  (row, col) of the cell vacated by the last move;
                that cell is displayed as 'o'.
    """
    lines = []
    for r, row in enumerate(board):
        tokens = [
            LAST_MARK if last_from and (r, c) == last_from else cell
            for c, cell in enumerate(row)
        ]
        lines.append(" ".join(tokens))
    return "\n".join(lines)
