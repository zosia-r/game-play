"""
Breakthrough – command-line entry point.

Usage
-----
  python main.py [options]

Options
-------
  --rows N, -r N        Number of board rows                 (default: 8)
  --cols M, -c M        Number of board columns              (default: 8)
  --depth D, -d D       Search depth limit                   (default: 3)
  --algorithm {minimax,alphabeta}, -a {minimax,alphabeta}
                        Search algorithm to use              (default: alphabeta)
  --max-rounds R        Round limit before forced stop       (default: 200)
  --quiet, -q           Print only the final board and result

Heuristics
----------
  On every move each player independently picks one of three heuristics at random:
    H0 – piece count
    H1 – advancement (forward progress)
    H2 – combined (piece count + advancement + mobility)

Board orientation
-----------------
  Row 0 is printed at the top.
  W (Player 1) starts on the bottom two rows and moves upward; moves first.
  B (Player 2) starts on the top two rows and moves downward.

Performance note
----------------
  Plain Minimax explores the full tree: O(b^d).
  Alpha-beta reduces this to O(b^(d/2)) in the best case.
  On an 8×8 board a depth of 2-3 is practical for alpha-beta;
  plain Minimax at depth > 2 is very slow.

Standard output
---------------
  Move-by-move log (unless --quiet), final board and result.

Standard error
--------------
  Total decision-tree nodes visited and wall-clock runtime.

Examples
--------
  python main.py
  python main.py --rows 6 --cols 8 --depth 3 --algorithm alphabeta
  python main.py --algorithm minimax --depth 2 --quiet
"""

import sys
import time
import argparse

import algorithms as search_module
from board import make_initial_board, board_to_string
from config import PLAYER_W, ALGO_MINIMAX, ALGO_ALPHABETA
from engine import play_game


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="breakthrough",
        description="Breakthrough – Minimax / alpha-beta with randomised per-move heuristics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python main.py\n"
            "  python main.py --rows 6 --cols 8 --depth 3 --algorithm alphabeta\n"
            "  python main.py --algorithm minimax --depth 2 --quiet\n"
        ),
    )
    parser.add_argument(
        "--rows", "-r", type=int, default=8,
        help="Number of board rows (default: 8)",
    )
    parser.add_argument(
        "--cols", "-c", type=int, default=8,
        help="Number of board columns (default: 8)",
    )
    parser.add_argument(
        "--depth", "-d", type=int, default=3,
        help="Search depth limit (default: 3; for plain minimax keep ≤ 2 on 8×8)",
    )
    parser.add_argument(
        "--algorithm", "-a",
        choices=[ALGO_MINIMAX, ALGO_ALPHABETA],
        default=ALGO_ALPHABETA,
        help=(
            f"Search algorithm: '{ALGO_MINIMAX}' = plain Minimax, "
            f"'{ALGO_ALPHABETA}' = Minimax with alpha-beta pruning (default)"
        ),
    )
    parser.add_argument(
        "--max-rounds", type=int, default=200,
        help="Maximum number of half-moves before the game is stopped (default: 200)",
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true",
        help="Suppress move-by-move output; print only the final board and result",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args   = parser.parse_args()

    board = make_initial_board(args.rows, args.cols)

    start = time.time()
    winner, rounds, final_board = play_game(
        board,
        depth      = args.depth,
        algorithm  = args.algorithm,
        max_rounds = args.max_rounds,
        verbose    = not args.quiet,
    )
    elapsed = time.time() - start

    # ── Standard output ───────────────────────────────────────────────────────
    print()
    print(board_to_string(final_board))
    print()
    winner_label = "Player 1 (W)" if winner == PLAYER_W else "Player 2 (B)"
    print(f"Rounds played: {rounds}.  Winner: {winner_label}.")

    # ── Standard error ────────────────────────────────────────────────────────
    print(f"Decision-tree nodes visited: {search_module.nodes_visited}", file=sys.stderr)
    print(f"Algorithm runtime:           {elapsed:.3f} s",               file=sys.stderr)


if __name__ == "__main__":
    main()
