"""
Search algorithms: Minimax & Alpha-Beta.
"""

from config import PLAYER_W, PLAYER_B, WIN_SCORE, LOSS_SCORE, ALGO_MINIMAX, ALGO_ALPHABETA, opponent
from game import get_moves, apply_move, check_winner
from heuristics import evaluate

# Incremented on every node expansion; reset before each game.
nodes_visited: int = 0


### Plain Minimax

def minimax_plain(
    board: list[list[str]],
    depth: int,
    maximizing: bool,
    current_player: str,
    root_player: str,
    heuristic_id: int,
) -> tuple[float, tuple | None]:
    """Standard Minimax without pruning.

    Searches the full game tree to *depth* plies.  Every reachable node is
    evaluated, making this an exhaustive but slow algorithm.

    Parameters
    ----------
    board:          Current board state.
    depth:          Remaining plies to search.
    maximizing:     True when it is the root player's turn.
    current_player: Player whose moves are generated at this node.
    root_player:    Player from whose perspective the score is computed.
    heuristic_id:   Evaluation heuristic used at leaf/cutoff nodes.

    Returns
    -------
    (score, best_move)
        score      – minimax value of this node.
        best_move  – best move found, or None at terminal/leaf nodes.
    """
    global nodes_visited
    nodes_visited += 1

    # Terminal state
    winner = check_winner(board)
    if winner is not None:
        return (WIN_SCORE + depth if winner == root_player else LOSS_SCORE - depth), None

    # Depth cutoff – apply heuristic evaluation
    if depth == 0:
        return evaluate(board, root_player, heuristic_id), None

    moves = get_moves(board, current_player)
    if not moves:
        val = LOSS_SCORE if current_player == root_player else WIN_SCORE
        return val, None

    opp = opponent(current_player)
    best_move = moves[0]

    if maximizing:
        best_val = float("-inf")
        for move in moves:
            val, _ = minimax_plain(
                apply_move(board, move), depth - 1, False, opp, root_player, heuristic_id
            )
            if val > best_val:
                best_val, best_move = val, move
        return best_val, best_move
    else:
        best_val = float("inf")
        for move in moves:
            val, _ = minimax_plain(
                apply_move(board, move), depth - 1, True, opp, root_player, heuristic_id
            )
            if val < best_val:
                best_val, best_move = val, move
        return best_val, best_move


### Minimax with Alpha-Beta

def minimax_alphabeta(
    board: list[list[str]],
    depth: int,
    maximizing: bool,
    current_player: str,
    root_player: str,
    heuristic_id: int,
    alpha: float,
    beta: float,
) -> tuple[float, tuple | None]:
    """Minimax with alpha-beta pruning.

    Identical in result to minimax_plain but skips branches that cannot
    change the outcome at any ancestor node:

    Alpha cut-off (beta pruning): at a MIN node, if the current value
        already drops to or below *alpha* (the best the MAX player is
        guaranteed elsewhere), the remaining siblings are pruned.

    Beta cut-off (alpha pruning): at a MAX node, if the current value
        already meets or exceeds *beta* (the best the MIN player is
        guaranteed elsewhere), the remaining siblings are pruned.

    Parameters
    ----------
    board:          Current board state.
    depth:          Remaining plies to search.
    maximizing:     True when it is the root player's turn.
    current_player: Player whose moves are generated at this node.
    root_player:    Player from whose perspective the score is computed.
    heuristic_id:   Evaluation heuristic used at leaf/cutoff nodes.
    alpha:          Lower bound: best score MAX is already guaranteed.
    beta:           Upper bound: best score MIN is already guaranteed.

    Returns
    -------
    (score, best_move)
    """
    global nodes_visited
    nodes_visited += 1

    # Terminal state
    winner = check_winner(board)
    if winner is not None:
        return (WIN_SCORE + depth if winner == root_player else LOSS_SCORE - depth), None

    # Depth cutoff
    if depth == 0:
        return evaluate(board, root_player, heuristic_id), None

    moves = get_moves(board, current_player)
    if not moves:
        val = LOSS_SCORE if current_player == root_player else WIN_SCORE
        return val, None

    opp = opponent(current_player)
    best_move = moves[0]

    if maximizing:
        best_val = float("-inf")
        for move in moves:
            val, _ = minimax_alphabeta(
                apply_move(board, move), depth - 1, False,
                opp, root_player, heuristic_id, alpha, beta,
            )
            if val > best_val:
                best_val, best_move = val, move
            alpha = max(alpha, best_val)
            if alpha >= beta:   # beta cut-off
                break
        return best_val, best_move
    else:
        best_val = float("inf")
        for move in moves:
            val, _ = minimax_alphabeta(
                apply_move(board, move), depth - 1, True,
                opp, root_player, heuristic_id, alpha, beta,
            )
            if val < best_val:
                best_val, best_move = val, move
            beta = min(beta, best_val)
            if alpha >= beta:   # alpha cut-off
                break
        return best_val, best_move


### Entry point

def choose_move(
    board: list[list[str]],
    player: str,
    depth: int,
    heuristic_id: int,
    algorithm: str = ALGO_ALPHABETA,
) -> tuple | None:
    """Return the best move for *player* using the selected search algorithm.

    Parameters
    ----------
    board:        Current board state.
    player:       The player to move.
    depth:        Search depth limit.
    heuristic_id: Evaluation heuristic index (0, 1, or 2).
    algorithm:    'minimax' for plain Minimax, 'alphabeta' for alpha-beta
                  pruning (default).

    Returns
    -------
    The best move as ((from_row, from_col), (to_row, to_col)),
    or None if no legal moves exist.
    """
    if algorithm == ALGO_MINIMAX:
        _, move = minimax_plain(
            board, depth, True, player, player, heuristic_id
        )
    else:
        _, move = minimax_alphabeta(
            board, depth, True, player, player, heuristic_id,
            float("-inf"), float("inf"),
        )
    return move
