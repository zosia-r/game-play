"""
Game loop for Breakthrough.

Both players use the same search algorithm, but on
every move each player independently randomly picks one of the defined
heuristics.
"""

import algorithms
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
    """Run a complete game between two agents.
    """
    algorithms.nodes_visited = 0

    current   = PLAYER_W
    rounds    = 0
    winner    = None

    if verbose:
        algo_label = "Minimax" if algorithm == "minimax" else "Alpha-Beta"
        print("=" * 100)
        print("BREAKTHROUGH GAME")
        print(f"  Board      : {len(board)} rows x {len(board[0])} cols")
        print(f"  Depth      : {depth}")
        print(f"  Algorithm  : {algo_label}")
        print(f"  Heuristics :") 
        print("\n".join(f"\t- {HEURISTIC_NAMES[i]}" for i in ALL_HEURISTIC_IDS))
        print(f"  First move : Player W")
        print("=" * 100)
        print("\nInitial board:")
        print(board_to_string(board))
        print()

    while rounds < max_rounds:
        winner = check_winner(board)
        if winner:
            break

        # Each player picks a heuristic at random for this move
        heuristic_id = pick_random_heuristic()

        move = algorithms.choose_move(board, current, depth, heuristic_id, algorithm)

        if move is None:
            winner = PLAYER_B if current == PLAYER_W else PLAYER_W
            if verbose:
                label = "W" if current == PLAYER_W else "B"
                print(f"Player {label} has no legal moves – loses.")
            break

        (fr, fc), (tr, tc) = move
        board     = apply_move(board, move)
        last_from = (fr, fc)
        rounds   += 1

        if verbose:
            label = "W" if current == PLAYER_W else "B"
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
