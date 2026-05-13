"""
Game loop for Breakthrough.

Both players use the same search algorithm, but on
every move each player independently randomly picks one of the defined
heuristics.
"""

import algorithms
from config import PLAYER_W, PLAYER_B, ALGO_ALPHABETA, LAST_MARK, opponent
from board import board_to_string
from game import apply_move, check_winner
from heuristics import evaluate, HEURISTIC_NAMES, pick_random_heuristic


def play_game(
    board: list[list[str]],
    depth: int,
    algorithm: str = ALGO_ALPHABETA,
    max_rounds: int = 200,
    verbose: bool = True,
) -> tuple[str, int, list[list[str]]]:
    """Run a complete game between two agents.
    """
    # Init
    algorithms.nodes_visited = 0

    current   = PLAYER_W
    rounds    = 0
    winner    = None

    # Basic info
    print("=" * 100)
    print("BREAKTHROUGH GAME")
    print(f"  Board      : {len(board)} rows x {len(board[0])} cols")
    print(f"  Depth      : {depth}")
    print(f"  Algorithm  : {"Minimax" if algorithm == "minimax" else "Alpha-Beta"}")
    print(f"  Heuristics :") 
    print("\n".join(f"\t- {HEURISTIC_NAMES[i]}" for i in range(len(HEURISTIC_NAMES))))
    print(f"  First move : Player W")
    print("=" * 100)
    print("\nInitial board:")
    print(board_to_string(board))
    print()

    while rounds < max_rounds:
        winner = check_winner(board)
        if winner:
            break

        # Each player picks a heuristic at random for each move
        heuristic_id = pick_random_heuristic()

        move = algorithms.choose_move(board, current, depth, heuristic_id, algorithm)

        if move is None:
            winner = opponent(current)
            print(f"Player {current} has no legal moves – loses.")
            break

        (fr, fc), (tr, tc) = move
        board = apply_move(board, move)
        rounds += 1

        if verbose:
            h_name = HEURISTIC_NAMES[heuristic_id].split()[0]
            print(
                f"Round {rounds:3d}  |  Player {current}  "
                f"|  ({fr},{fc}) -> ({tr},{tc})  "
                f"|  heuristic: {h_name}"
            )

        current = opponent(current)

    else:
        # Round limit – tie
        winner = None
        print(f"\nRound limit ({max_rounds}) reached.")

    
    board[fr][fc] = LAST_MARK
    return winner, rounds, board
