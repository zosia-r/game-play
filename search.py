"""
Minimax search with alpha-beta pruning for Breakthrough.

Algorithm overview
------------------
The standard Minimax algorithm searches the game tree by alternating between
MAX nodes (the root player maximises the score) and MIN nodes (the opponent
minimises the score).

Alpha-beta pruning eliminates subtrees that cannot influence the final
decision:
  alpha – best score the MAX player is already guaranteed
  beta  – best score the MIN player is already guaranteed

When alpha >= beta we can prune the remaining children of the current node
because the opponent would never allow the position to be reached.

In the best case (moves explored in optimal order) alpha-beta reduces the
effective branching factor from b to sqrt(b), allowing twice the search depth
in the same time compared to plain Minimax.

References
----------
Russell, S. & Norvig, P. (2003). Artificial Intelligence: A Modern Approach,
2nd ed., pp. 162-170.
"""

from constants import PLAYER_B, PLAYER_W, WIN_SCORE, LOSS_SCORE
from game import get_moves, apply_move, check_winner
from heuristics import evaluate

# Global counter – reset before each full search in play_game
nodes_visited: int = 0


def minimax(
    board: list[list[str]],
    depth: int,
    maximizing: bool,
    current_player: str,
    root_player: str,
    heuristic_id: int,
    alpha: float,
    beta: float,
) -> tuple[float, tuple | None]:
    """Recursive Minimax with alpha-beta pruning.

    Parameters
    ----------
    board:          Current board state.
    depth:          Remaining search depth.
    maximizing:     True when it is the root player's turn to move.
    current_player: The player whose moves are generated at this node.
    root_player:    The player from whose perspective the score is computed
                    (always maximised at the root).
    heuristic_id:   Index of the evaluation heuristic to use at leaf nodes.
    alpha:          Best score MAX is already guaranteed (lower bound).
    beta:           Best score MIN is already guaranteed (upper bound).

    Returns
    -------
    (score, move)
        score – minimax value of this node.
        move  – best move found, or None at terminal/leaf nodes.
    """
    global nodes_visited
    nodes_visited += 1

    # ── Terminal state ───────────────────────────────────────────────────────
    winner = check_winner(board)
    if winner is not None:
        # Add remaining depth so the algorithm prefers faster victories
        if winner == root_player:
            return WIN_SCORE + depth, None
        else:
            return LOSS_SCORE - depth, None

    # ── Depth limit reached ──────────────────────────────────────────────────
    if depth == 0:
        return evaluate(board, root_player, heuristic_id), None

    # ── Generate moves ───────────────────────────────────────────────────────
    moves = get_moves(board, current_player)
    if not moves:
        # No legal moves – current player loses
        val = LOSS_SCORE if current_player == root_player else WIN_SCORE
        return val, None

    opponent  = PLAYER_W if current_player == PLAYER_B else PLAYER_B
    best_move = moves[0]

    # ── MAX node (root player's turn) ────────────────────────────────────────
    if maximizing:
        best_val = float("-inf")
        for move in moves:
            val, _ = minimax(
                apply_move(board, move),
                depth - 1,
                False,
                opponent,
                root_player,
                heuristic_id,
                alpha,
                beta,
            )
            if val > best_val:
                best_val, best_move = val, move
            alpha = max(alpha, best_val)
            if alpha >= beta:
                break  # beta cut-off
        return best_val, best_move

    # ── MIN node (opponent's turn) ───────────────────────────────────────────
    else:
        best_val = float("inf")
        for move in moves:
            val, _ = minimax(
                apply_move(board, move),
                depth - 1,
                True,
                opponent,
                root_player,
                heuristic_id,
                alpha,
                beta,
            )
            if val < best_val:
                best_val, best_move = val, move
            beta = min(beta, best_val)
            if alpha >= beta:
                break  # alpha cut-off
        return best_val, best_move


def choose_move(
    board: list[list[str]],
    player: str,
    depth: int,
    heuristic_id: int,
) -> tuple | None:
    """Return the best move for *player* using Minimax with alpha-beta.

    This is the public entry point for the search.
    """
    _, move = minimax(
        board, depth, True, player, player, heuristic_id,
        float("-inf"), float("inf"),
    )
    return move
