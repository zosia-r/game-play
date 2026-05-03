"""
Core game logic for Breakthrough: move generation, application and win detection.

Move rules
----------
- A piece may move one step straight forward onto an empty cell.
- A piece may move one step diagonally forward onto an empty cell (no capture).
- A piece may capture an adjacent diagonal opponent piece by moving onto its cell.
- Straight-forward captures are NOT allowed.

A player wins when:
- One of their pieces reaches the opponent's home edge, OR
- The opponent has no legal moves.
"""

from constants import PLAYER_B, PLAYER_W, EMPTY

Move = tuple[tuple[int, int], tuple[int, int]]   # ((fr, fc), (tr, tc))


def get_moves(board: list[list[str]], player: str) -> list[Move]:
    """Return all legal moves for *player* in the current board position."""
    rows      = len(board)
    cols      = len(board[0])
    direction = 1 if player == PLAYER_B else -1   # B moves up, W moves down
    opponent  = PLAYER_W if player == PLAYER_B else PLAYER_B
    moves: list[Move] = []

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != player:
                continue
            nr = r + direction
            if not (0 <= nr < rows):
                continue

            # Straight forward – empty cells only
            if board[nr][c] == EMPTY:
                moves.append(((r, c), (nr, c)))

            # Diagonal forward – empty cell or capture
            for dc in (-1, 1):
                nc = c + dc
                if 0 <= nc < cols and board[nr][nc] in (EMPTY, opponent):
                    moves.append(((r, c), (nr, nc)))

    return moves


def apply_move(board: list[list[str]], move: Move) -> list[list[str]]:
    """Return a new board with *move* applied (original board is not mutated)."""
    new_board = [row[:] for row in board]
    (fr, fc), (tr, tc) = move
    new_board[tr][tc] = new_board[fr][fc]
    new_board[fr][fc] = EMPTY
    return new_board


def check_winner(board: list[list[str]]) -> str | None:
    """Return the winner ('B' or 'W') or None if the game is still ongoing."""
    rows = len(board)
    cols = len(board[0])

    # Check whether any piece has reached the opposite edge
    for c in range(cols):
        if board[rows - 1][c] == PLAYER_B:
            return PLAYER_B
        if board[0][c] == PLAYER_W:
            return PLAYER_W

    # A player with no legal moves loses
    if not get_moves(board, PLAYER_B):
        return PLAYER_W
    if not get_moves(board, PLAYER_W):
        return PLAYER_B

    return None
