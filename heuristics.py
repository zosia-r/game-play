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
H2 - mobility     : number of legal moves available to the player
H3 – combined     : weighted mix of piece count, advancement and mobility
H4 - capture_potential : number of opponent pieces that can be captured in the next move
H5 - passed_pieces : number of pieces with a clear path to the goal row (no opponent pieces blocking)
"""

import random
from typing import Callable

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
    """H3: Weighted combination of piece count, advancement and mobility.

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

def heuristic_mobility(board: list[list[str]], player: str) -> float:
    """H2: Difference in the number of legal moves available to the player.

    A positive value means *player* has more tactical options than the opponent.
    Encourages positions with greater mobility and flexibility.
    """
    w_mob = len(get_moves(board, PLAYER_W))
    b_mob = len(get_moves(board, PLAYER_B))
    score = w_mob - b_mob
    return score if player == PLAYER_W else -score

def heuristic_capture_potential(board: list[list[str]], player: str) -> float:
    """H4: Number of opponent pieces that can be captured in the next move.

    A positive value means *player* has more immediate capture opportunities than the opponent.
    Encourages aggressive play and tactical awareness.
    """
    opponent = PLAYER_B if player == PLAYER_W else PLAYER_W
    capture_count = 0

    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell == player:
                # Check potential captures in all four diagonal directions
                for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < len(board) and 0 <= nc < len(board[0]):
                        if board[nr][nc] == opponent:
                            capture_count += 1

    return capture_count

def heuristic_passed_pieces(board: list[list[str]], player: str) -> float:
    """H5: Count of pieces with clear path to promotion (no opponent in their column).
    
    A passed piece is guaranteed to promote if it reaches the goal row,
    making them significantly more valuable strategically.
    """
    opponent = PLAYER_B if player == PLAYER_W else PLAYER_W
    rows, cols = len(board), len(board[0])
    w_passed = b_passed = 0
    
    for c in range(cols):
        w_has_opp = b_has_opp = False
        for r in range(rows):
            if board[r][c] == opponent:
                if player == PLAYER_W:
                    b_has_opp = True
                else:
                    w_has_opp = True
            elif board[r][c] == player:
                if player == PLAYER_W and not b_has_opp:
                    w_passed += 1
                elif player == PLAYER_B and not w_has_opp:
                    b_passed += 1
    
    score = w_passed - b_passed
    return score if player == PLAYER_W else -score

# ── Registry ─────────────────────────────────────────────────────────────────

HEURISTICS: dict[int, Callable[[list[list[str]], str], float]] = {
    0: heuristic_piece_count,
    1: heuristic_advancement,
    2: heuristic_mobility,
    3: heuristic_combined,
    4: heuristic_capture_potential,
    5: heuristic_passed_pieces,
}

HEURISTIC_NAMES: dict[int, str] = {
    0: "H0 – piece count",
    1: "H1 – advancement",
    2: "H2 – mobility",
    3: "H3 – combined (piece count + advancement + mobility)",
    4: "H4 – capture potential",
    5: "H5 – passed pieces"
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
