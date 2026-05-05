"""
Game loop for Breakthrough (basic version).

Agent behaviour
---------------
Both players use the same search algorithm (Minimax or alpha-beta), but on
every individual move each player independently picks one of the three
evaluation heuristics at random.  This means:

  - Neither player is locked into a single strategy throughout the game.
  - The opponent's move cannot be perfectly predicted by the other player,
    making the game less deterministic and more varied across runs.

Turn order
----------
  Player W moves first (as per the task specification).
"""

import random

import algorithms as search_module
from config import PLAYER_W, PLAYER_B, ALGO_ALPHABETA
from board import board_to_string
from game import apply_move, check_winner
from heuristics import evaluate, HEURISTIC_NAMES, pick_random_heuristic, ALL_HEURISTIC_IDS


def play_game(
    board: list[list[str]],
    depth: int,
    algorithm: str = ALGO_ALPHABETA,
    max_rounds: int = 200,
    verbose: bool = True,
) -> tuple[str, int, list[list[str]]]:
    """Run a complete game between two Minimax agents.

    Each agent randomly selects one of the three heuristics before every move.

    Parameters
    ----------
    board:       Starting board position.
    depth:       Search depth limit (same for both players).
    algorithm:   Search algorithm: 'minimax' or 'alphabeta'.
    max_rounds:  Safety limit on the total number of half-moves (plies).
    verbose:     Print a move-by-move log to stdout when True.

    Returns
    -------
    (winner, rounds, final_board)
        winner      – 'W' or 'B'
        rounds      – number of half-moves played
        final_board – board state when the game ended
    """
    search_module.nodes_visited = 0   # reset global counter

    current   = PLAYER_W   # W always moves first
    rounds    = 0
    last_from = None
    winner    = None

    if verbose:
        algo_label = "Minimax (plain)" if algorithm == "minimax" else "Minimax + α-β pruning"
        print("=" * 56)
        print("BREAKTHROUGH  –  basic version")
        print(f"  Board      : {len(board)} rows × {len(board[0])} cols")
        print(f"  Depth      : {depth}")
        print(f"  Algorithm  : {algo_label}")
        print(f"  Heuristics : random per move from "
              f"{[HEURISTIC_NAMES[i] for i in ALL_HEURISTIC_IDS]}")
        print(f"  First move : Player 1 (W)")
        print("=" * 56)
        print("\nInitial position:")
        print(board_to_string(board))
        print()

    while rounds < max_rounds:
        winner = check_winner(board)
        if winner:
            break

        # Each player picks a heuristic at random for this move
        heuristic_id = pick_random_heuristic()

        move = search_module.choose_move(board, current, depth, heuristic_id, algorithm)

        if move is None:
            winner = PLAYER_B if current == PLAYER_W else PLAYER_W
            if verbose:
                label = "1 (W)" if current == PLAYER_W else "2 (B)"
                print(f"Player {label} has no legal moves – loses.")
            break

        (fr, fc), (tr, tc) = move
        board     = apply_move(board, move)
        last_from = (fr, fc)
        rounds   += 1

        if verbose:
            label = "1 (W)" if current == PLAYER_W else "2 (B)"
            h_name = HEURISTIC_NAMES[heuristic_id].split()[0]   # short label
            print(
                f"Round {rounds:3d}  |  Player {label}  "
                f"|  ({fr},{fc}) -> ({tr},{tc})  "
                f"|  heuristic: {h_name}"
            )

        current = PLAYER_B if current == PLAYER_W else PLAYER_W

    else:
        # Round limit – break tie with heuristic score
        score  = evaluate(board, PLAYER_W, pick_random_heuristic())
        winner = PLAYER_W if score >= 0 else PLAYER_B
        if verbose:
            print(f"\nRound limit ({max_rounds}) reached.")

    winner = check_winner(board) or winner
    # TODO: do not return last_from -> edit the board
    return winner, rounds, board
