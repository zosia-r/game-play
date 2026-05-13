"""
Configuration for the game.
"""

PLAYER_W   = 'W'
PLAYER_B   = 'B'
EMPTY      = '_'
LAST_MARK  = 'o'

WIN_SCORE  =  1_000_000
LOSS_SCORE = -1_000_000

# Search algorithm identifiers
ALGO_MINIMAX   = 'minimax'
ALGO_ALPHABETA = 'alphabeta'

def opponent(player: str) -> str:
    return PLAYER_B if player == PLAYER_W else PLAYER_W
