# TODO: add more heuristics, make it a class
"""
Heuristic evaluation functions for Breakthrough.

Every heuristic has the signature::

    heuristic(board, player) -> float

and returns a value from *player*'s perspective:
  positive  – position favours *player*
  negative  – position favours the opponent
  0         – balanced

Each player randomly picks one heuristic per move (see engine.py),
so all three functions must remain self-contained and consistent.

Available heuristics
--------------------
H0 – piece_count  : difference in total piece counts
H1 – advancement  : sum of forward progress of all pieces
H2 – combined     : weighted mix of piece count, advancement and mobility
"""

import random

from config import PLAYER_W, PLAYER_B, WIN_SCORE, LOSS_SCORE
from game import get_moves, check_winner


# ── Individual heuristics ────────────────────────────────────────────────────

def heuristic_piece_count(board: list[list[str]], player: str) -> float:
    """H0: Difference in the number of pieces remaining on the board.

    A positive value means *player* has more pieces than the opponent.
    Simple and fast; ignores piece positions entirely.
    """
    w = b = 0
    for row in board:
        for cell in row:
            if cell == PLAYER_W:
                w += 1
            elif cell == PLAYER_B:
                b += 1
    score = w - b   # raw score from W's perspective
    return score if player == PLAYER_W else -score


def heuristic_advancement(board: list[list[str]], player: str) -> float:
    """H1: Sum of forward progress of all friendly pieces toward the goal row.

    W's progress for a piece at row r  = (rows - 1 - r)  (closer to row 0 → higher)
    B's progress for a piece at row r  = r                (closer to row rows-1 → higher)

    Encourages aggressive forward movement.
    """
    rows  = len(board)
    w_adv = b_adv = 0
    for r, row in enumerate(board):
        for cell in row:
            if cell == PLAYER_W:
                w_adv += (rows - 1 - r)   # W moves toward row 0
            elif cell == PLAYER_B:
                b_adv += r                # B moves toward row rows-1
    score = w_adv - b_adv
    return score if player == PLAYER_W else -score


def heuristic_combined(board: list[list[str]], player: str) -> float:
    """H2: Weighted combination of piece count, advancement and mobility.

    Weights:
      2.0 × piece-count difference
      1.0 × advancement difference
      0.5 × mobility difference (number of legal moves available)

    Balances material advantage, positional progress and tactical options.
    """
    rows  = len(board)
    w_cnt = w_adv = b_cnt = b_adv = 0

    for r, row in enumerate(board):
        for cell in row:
            if cell == PLAYER_W:
                w_cnt += 1
                w_adv += (rows - 1 - r)
            elif cell == PLAYER_B:
                b_cnt += 1
                b_adv += r

    w_mob = len(get_moves(board, PLAYER_W))
    b_mob = len(get_moves(board, PLAYER_B))

    score = (
        2.0 * (w_cnt - b_cnt)
        + 1.0 * (w_adv - b_adv)
        + 0.5 * (w_mob - b_mob)
    )
    return score if player == PLAYER_W else -score


# ── Registry ─────────────────────────────────────────────────────────────────

HEURISTICS: dict[int, callable] = {
    0: heuristic_piece_count,
    1: heuristic_advancement,
    2: heuristic_combined,
}

HEURISTIC_NAMES: dict[int, str] = {
    0: "H0 – piece count",
    1: "H1 – advancement",
    2: "H2 – combined (piece count + advancement + mobility)",
}

ALL_HEURISTIC_IDS: list[int] = list(HEURISTICS.keys())


def pick_random_heuristic() -> int:
    """Return a randomly chosen heuristic id from ALL_HEURISTIC_IDS."""
    return random.choice(ALL_HEURISTIC_IDS)


def evaluate(board: list[list[str]], player: str, heuristic_id: int) -> float:
    """Return a terminal score or a heuristic estimate for *player*.

    Terminal states always return ±WIN_SCORE so they are clearly
    distinguishable from any heuristic estimate.
    """
    winner = check_winner(board)
    if winner == player:
        return WIN_SCORE
    if winner is not None:
        return LOSS_SCORE
    return HEURISTICS[heuristic_id](board, player)
