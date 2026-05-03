"""
Heuristic evaluation functions for Breakthrough.

Every heuristic has the signature::

    heuristic(board, player) -> float

and returns a value from the perspective of *player*:
  positive  – position favours *player*
  negative  – position favours the opponent
  0         – balanced position

Available heuristics
--------------------
H0 – piece_count   : raw difference in piece counts
H1 – advancement   : sum of forward progress of all pieces
H2 – combined      : weighted mix of piece count, advancement, and mobility
"""

from constants import PLAYER_B, PLAYER_W, WIN_SCORE, LOSS_SCORE
from game import get_moves, check_winner


# ── Individual heuristics ────────────────────────────────────────────────────

def heuristic_piece_count(board: list[list[str]], player: str) -> float:
    """H0: Difference in the number of pieces on the board.

    Rewards having more pieces than the opponent.
    Simple but ignores positional factors entirely.
    """
    b = w = 0
    for row in board:
        for cell in row:
            if cell == PLAYER_B:
                b += 1
            elif cell == PLAYER_W:
                w += 1
    score = b - w
    return score if player == PLAYER_B else -score


def heuristic_advancement(board: list[list[str]], player: str) -> float:
    """H1: Sum of forward progress of all pieces towards the winning edge.

    Each piece contributes its row distance from the starting edge.
    Encourages pushing pieces forward aggressively.
    """
    rows  = len(board)
    b_adv = w_adv = 0
    for r, row in enumerate(board):
        for cell in row:
            if cell == PLAYER_B:
                b_adv += r                # B wants high row indices
            elif cell == PLAYER_W:
                w_adv += (rows - 1 - r)  # W wants low row indices
    score = b_adv - w_adv
    return score if player == PLAYER_B else -score


def heuristic_combined(board: list[list[str]], player: str) -> float:
    """H2: Weighted combination of piece count, advancement, and mobility.

    Weights:
      2.0 × piece count difference
      1.0 × advancement difference
      0.5 × mobility difference (number of legal moves)

    Balances material advantage, positional progress and tactical flexibility.
    """
    rows  = len(board)
    b_cnt = b_adv = w_cnt = w_adv = 0

    for r, row in enumerate(board):
        for cell in row:
            if cell == PLAYER_B:
                b_cnt += 1
                b_adv += r
            elif cell == PLAYER_W:
                w_cnt += 1
                w_adv += (rows - 1 - r)

    b_mob = len(get_moves(board, PLAYER_B))
    w_mob = len(get_moves(board, PLAYER_W))

    score = (
        2.0 * (b_cnt - w_cnt)
        + 1.0 * (b_adv - w_adv)
        + 0.5 * (b_mob - w_mob)
    )
    return score if player == PLAYER_B else -score


# ── Registry ─────────────────────────────────────────────────────────────────

HEURISTICS: dict[int, callable] = {
    0: heuristic_piece_count,
    1: heuristic_advancement,
    2: heuristic_combined,
}

HEURISTIC_NAMES: dict[int, str] = {
    0: "Piece count (H0)",
    1: "Advancement (H1)",
    2: "Combined: piece count + advancement + mobility (H2)",
}


def evaluate(board: list[list[str]], player: str, heuristic_id: int) -> float:
    """Return a terminal score or the heuristic estimate for *player*.

    Terminal states always return WIN_SCORE or LOSS_SCORE so the search
    can distinguish forced wins/losses from heuristic estimates.
    """
    winner = check_winner(board)
    if winner == player:
        return WIN_SCORE
    if winner is not None:
        return LOSS_SCORE
    return HEURISTICS[heuristic_id](board, player)
