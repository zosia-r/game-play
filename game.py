"""
Core game logic for Breakthrough: move generation, application and win detection.

Move rules
----------
- A piece may step straight forward onto an empty cell (no capture).
- A piece may step diagonally forward onto an empty cell (no capture).
- A piece may capture an opponent piece by stepping diagonally forward
  onto its cell.
- Straight-forward captures are NOT allowed.

Forward direction
-----------------
  W moves upward   → row index decreases (direction = -1)
  B moves downward → row index increases (direction = +1)

Victory conditions
------------------
  W wins by placing any piece on row 0.
  B wins by placing any piece on row (rows-1).
  A player with no legal moves also loses.
"""

from constants import PLAYER_W, PLAYER_B, EMPTY

Move = tuple[tuple[int, int], tuple[int, int]]   # ((from_row, from_col), (to_row, to_col))


def get_moves(board: list[list[str]], player: str) -> list[Move]:
    """Return all legal moves for *player* in the given board position."""
    rows      = len(board)
    cols      = len(board[0])
    direction = -1 if player == PLAYER_W else 1   # W moves up, B moves down
    opponent  = PLAYER_B if player == PLAYER_W else PLAYER_W
    moves: list[Move] = []

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != player:
                continue
            nr = r + direction
            if not (0 <= nr < rows):
                continue

            # Straight forward – empty cells only (no capture)
            if board[nr][c] == EMPTY:
                moves.append(((r, c), (nr, c)))

            # Diagonal forward – empty cell or opponent capture
            for dc in (-1, 1):
                nc = c + dc
                if 0 <= nc < cols and board[nr][nc] in (EMPTY, opponent):
                    moves.append(((r, c), (nr, nc)))

    return moves


def apply_move(board: list[list[str]], move: Move) -> list[list[str]]:
    """Return a new board with *move* applied. The original board is not modified."""
    new_board = [row[:] for row in board]
    (fr, fc), (tr, tc) = move
    new_board[tr][tc] = new_board[fr][fc]
    new_board[fr][fc] = EMPTY
    return new_board


def check_winner(board: list[list[str]]) -> str | None:
    """Return 'W', 'B', or None if the game is still in progress.

    W wins by reaching row 0; B wins by reaching row (rows-1).
    A player who has no legal moves loses immediately.
    """
    rows = len(board)
    cols = len(board[0])

    # Check winning rows
    for c in range(cols):
        if board[0][c] == PLAYER_W:          # W reached the top edge
            return PLAYER_W
        if board[rows - 1][c] == PLAYER_B:   # B reached the bottom edge
            return PLAYER_B

    # Check whether a player has any moves left
    if not get_moves(board, PLAYER_W):
        return PLAYER_B
    if not get_moves(board, PLAYER_B):
        return PLAYER_W

    return None
