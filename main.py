"""
Breakthrough – entry point.

Usage
-----
  python main.py [options]

Options
-------
  --size N              Board size N×N          (default: 8)
  --depth D, -d D       Search depth            (default: 3)
  --heuristic {0,1,2}   Evaluation heuristic    (default: 2)
                          0 – piece count
                          1 – advancement
                          2 – combined (piece count + advancement + mobility)
  --input FILE, -i FILE Read starting board from FILE
  --max-rounds R        Round limit             (default: 200)
  --quiet, -q           Print only the final result

Performance note
----------------
On an 8×8 board a search depth of 2-3 is recommended.
Depth 4+ leads to very long computation times.

Standard output
---------------
  Final board position followed by the winner and round count.

Standard error
--------------
  Number of decision-tree nodes visited and wall-clock time.

Examples
--------
  python main.py
  python main.py --size 6 --depth 3 --heuristic 1
  python main.py --depth 2 --quiet
  cat board.txt | python main.py --depth 3
"""

import sys
import time
import argparse

import search
from board import make_initial_board, board_from_string, board_to_string
from constants import PLAYER_B
from engine import play_game


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="breakthrough",
        description="Breakthrough – Minimax with alpha-beta pruning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python main.py\n"
            "  python main.py --size 6 --depth 3 --heuristic 1\n"
            "  cat board.txt | python main.py --depth 2 --quiet"
        ),
    )
    parser.add_argument(
        "--size", type=int, default=8,
        help="Board size N×N (default: 8)",
    )
    parser.add_argument(
        "--depth", "-d", type=int, default=3,
        help="Maximum search depth (default: 3)",
    )
    parser.add_argument(
        "--heuristic", "-H", type=int, default=2, choices=[0, 1, 2],
        help="Evaluation heuristic: 0=piece count, 1=advancement, 2=combined (default: 2)",
    )
    parser.add_argument(
        "--input", "-i", type=str, default=None,
        help="File containing the starting board position",
    )
    parser.add_argument(
        "--max-rounds", type=int, default=200,
        help="Maximum number of rounds before the game is stopped (default: 200)",
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true",
        help="Suppress move-by-move output; print final result only",
    )
    return parser


def load_board(args) -> list[list[str]]:
    """Load the starting board from a file, stdin, or use the default position."""
    N = args.size
    if args.input:
        with open(args.input) as f:
            return board_from_string(f.read(), N, N)
    if not sys.stdin.isatty():
        text = sys.stdin.read()
        if text.strip():
            return board_from_string(text, N, N)
    return make_initial_board(N, N)


def main() -> None:
    parser = build_parser()
    args   = parser.parse_args()

    board = load_board(args)

    start = time.time()
    winner, rounds, final_board, last_from = play_game(
        board,
        depth        = args.depth,
        heuristic_id = args.heuristic,
        max_rounds   = args.max_rounds,
        verbose      = not args.quiet,
    )
    elapsed = time.time() - start

    # ── Standard output: final board + result ────────────────────────────────
    print()
    print(board_to_string(final_board, last_from=last_from))
    print()
    winner_label = "Player 1 (B)" if winner == PLAYER_B else "Player 2 (W)"
    print(f"Rounds played: {rounds}.  Winner: {winner_label}.")

    # ── Standard error: algorithm statistics ─────────────────────────────────
    print(f"Decision-tree nodes visited: {search.nodes_visited}", file=sys.stderr)
    print(f"Algorithm runtime:           {elapsed:.3f} s",         file=sys.stderr)


if __name__ == "__main__":
    main()
