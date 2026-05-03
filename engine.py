"""
Game loop for the basic version of Breakthrough.

Both players are controlled by the Minimax agent using the same heuristic,
so the first player's predictions about the opponent's responses are always
accurate (symmetric play).
"""

from constants import PLAYER_B, PLAYER_W
from board import board_to_string
from game import apply_move, check_winner
from heuristics import evaluate, HEURISTIC_NAMES
from search import choose_move, nodes_visited
import search  # needed to reset the global counter


def play_game(
    board: list[list[str]],
    depth: int,
    heuristic_id: int,
    max_rounds: int = 200,
    verbose: bool = True,
) -> tuple[str, int, list[list[str]], tuple | None]:
    """Run a full game between two Minimax agents.

    Parameters
    ----------
    board:        Starting board position.
    depth:        Minimax search depth (applies to both players).
    heuristic_id: Evaluation heuristic used by both agents.
    max_rounds:   Safety limit on the number of half-moves (plies).
    verbose:      Print move-by-move log to stdout.

    Returns
    -------
    (winner, rounds, final_board, last_from)
        winner      – 'B' or 'W'
        rounds      – total number of half-moves played
        final_board – board state at the end of the game
        last_from   – (row, col) vacated by the last move, for 'o' display
    """
    # Reset the global node counter before the game starts
    search.nodes_visited = 0

    current   = PLAYER_B   # Player B always moves first
    rounds    = 0
    last_from = None
    winner    = None

    if verbose:
        print("=" * 54)
        print("BREAKTHROUGH  –  basic version  (Minimax + α-β)")
        print(f"  Board      : {len(board)} × {len(board[0])}")
        print(f"  Depth      : {depth}")
        print(f"  Heuristic  : {HEURISTIC_NAMES[heuristic_id]}")
        print("=" * 54)
        print("\nInitial position:")
        print(board_to_string(board))
        print()

    while rounds < max_rounds:
        winner = check_winner(board)
        if winner:
            break

        move = choose_move(board, current, depth, heuristic_id)
        if move is None:
            # No legal moves – current player loses immediately
            winner = PLAYER_W if current == PLAYER_B else PLAYER_B
            if verbose:
                label = "1 (B)" if current == PLAYER_B else "2 (W)"
                print(f"Player {label} has no legal moves – loses.")
            break

        (fr, fc), (tr, tc) = move
        board     = apply_move(board, move)
        last_from = (fr, fc)
        rounds   += 1

        if verbose:
            label = "1 (B)" if current == PLAYER_B else "2 (W)"
            print(f"Round {rounds:3d}  |  Player {label}  |  ({fr},{fc}) -> ({tr},{tc})")

        current = PLAYER_W if current == PLAYER_B else PLAYER_B

    else:
        # Round limit reached – declare winner by heuristic score
        score  = evaluate(board, PLAYER_B, heuristic_id)
        winner = PLAYER_B if score >= 0 else PLAYER_W
        if verbose:
            print(f"\nRound limit ({max_rounds}) reached.")

    # Refresh winner in case check_winner now detects a terminal state
    winner = check_winner(board) or winner
    return winner, rounds, board, last_from
