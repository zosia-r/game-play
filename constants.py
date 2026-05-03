"""
Shared constants for the Breakthrough game.

Board orientation
-----------------
  row 0            – W's winning edge  (top of the printed board)
  row (rows-1)     – W's starting rows (bottom of the printed board)

Players
-------
  W  – Player 1, starts on the bottom two rows, moves upward (row index decreases),
       wins by reaching row 0.
  B  – Player 2, starts on the top two rows, moves downward (row index increases),
       wins by reaching row (rows-1).
"""

PLAYER_W   = 'W'   # Player 1 – moves upward   (row index decreases)
PLAYER_B   = 'B'   # Player 2 – moves downward (row index increases)
EMPTY      = '_'   # Empty cell
LAST_MARK  = 'o'   # Cell vacated by the last move (display only)

WIN_SCORE  =  1_000_000
LOSS_SCORE = -1_000_000

# Search algorithm identifiers
ALGO_MINIMAX   = 'minimax'
ALGO_ALPHABETA = 'alphabeta'
