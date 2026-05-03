"""
Board representation, creation, parsing and display for Breakthrough.

Board layout
------------
- Rows are indexed 0 (bottom) to N-1 (top).
- Player B starts on rows 0-1 and wins by reaching row N-1.
- Player W starts on rows N-2, N-1 and wins by reaching row 0.

Cell symbols
------------
  B        – Player 1 piece
  W        – Player 2 piece
  _        – Empty cell
  o        – Cell from which the last move was made (output only)
"""

from constants import PLAYER_B, PLAYER_W, EMPTY, LAST_MARK


def make_initial_board(rows: int = 8, cols: int = 8) -> list[list[str]]:
    """Return a standard Breakthrough starting position."""
    board = [[EMPTY] * cols for _ in range(rows)]
    for r in range(2):
        for c in range(cols):
            board[r][c] = PLAYER_B
    for r in range(rows - 2, rows):
        for c in range(cols):
            board[r][c] = PLAYER_W
    return board


def board_from_string(text: str, rows: int, cols: int) -> list[list[str]]:
    """Parse a board from a text string (m lines × n space-separated tokens).

    The 'o' marker is treated as an empty cell on input.
    Missing cells are filled with EMPTY.
    """
    board: list[list[str]] = []
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]

    for line in lines[:rows]:
        tokens = line.split()[:cols]
        row = [
            EMPTY if t == LAST_MARK else (t if t in (PLAYER_B, PLAYER_W, EMPTY) else EMPTY)
            for t in tokens
        ]
        while len(row) < cols:
            row.append(EMPTY)
        board.append(row)

    while len(board) < rows:
        board.append([EMPTY] * cols)

    return board


def board_to_string(
    board: list[list[str]],
    last_from: tuple[int, int] | None = None,
) -> str:
    """Render the board as a string.

    Parameters
    ----------
    board:      2-D list of cell symbols.
    last_from:  (row, col) of the cell that was vacated by the last move;
                it will be shown as 'o'.
    """
    lines = []
    for r, row in enumerate(board):
        tokens = [
            LAST_MARK if last_from and (r, c) == last_from else cell
            for c, cell in enumerate(row)
        ]
        lines.append(" ".join(tokens))
    return "\n".join(lines)
