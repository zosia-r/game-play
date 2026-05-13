"""
Core game logic: move generation, application and win detection.

Move rules:
- A piece may step straight forward onto an empty cell (no capture)
- A piece may step diagonally forward onto an empty cell (no capture)
- A piece may capture an opponent piece by stepping diagonally forward
  onto its cell.

Move direction:
- W moves upward: row index decreases (direction = -1)
- B moves downward: row index increases (direction = +1)

Victory conditions
- White wins by placing any piece on row 0
- Black wins by placing any piece on row (rows-1)
- player with no legal moves loses
"""

from config import PLAYER_W, PLAYER_B, EMPTY, LAST_MARK

Move = tuple[tuple[int, int], tuple[int, int]]   # ((from_row, from_col), (to_row, to_col))


def get_moves(board: list[list[str]], player: str) -> list[Move]:
    rows = len(board)
    cols = len(board[0])
    direction = -1 if player == PLAYER_W else 1
    opponent = PLAYER_B if player == PLAYER_W else PLAYER_W
    moves: list[Move] = []

    for row in range(rows):
        for col in range(cols):
            if board[row][col] != player:
                continue
            next_row = row + direction
            if not (0 <= next_row < rows):
                continue

            # step straight forward onto an empty cell (no capture)
            if board[next_row][col] == EMPTY:
                moves.append(((row, col), (next_row, col)))

            # step diagonally forward onto an empty cell (capture or no capture)
            for dir_col in (-1, 1):
                next_col = col + dir_col
                if 0 <= next_col < cols and board[next_row][next_col] in (EMPTY, opponent):
                    moves.append(((row, col), (next_row, next_col)))

    return moves


def apply_move(board: list[list[str]], move: Move) -> list[list[str]]:
    new_board = [row[:] for row in board]
    (fr, fc), (tr, tc) = move
    new_board[tr][tc] = new_board[fr][fc]
    new_board[fr][fc] = EMPTY
    return new_board


def check_winner(board: list[list[str]]) -> str | None:
    rows = len(board)
    cols = len(board[0])

    # check winning rows
    for col in range(cols):
        if board[0][col] == PLAYER_W:
            return PLAYER_W
        if board[rows - 1][col] == PLAYER_B:
            return PLAYER_B

    # check if any moves left
    if not get_moves(board, PLAYER_W):
        return PLAYER_B
    if not get_moves(board, PLAYER_B):
        return PLAYER_W

    return None
