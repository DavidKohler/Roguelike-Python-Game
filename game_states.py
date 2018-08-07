from enum import Enum

class GameStates(Enum):
    '''
    Enumerates game states
    '''
    PLAYERS_TURN = 1
    ENEMY_TURN = 2
    PLAYER_DEAD = 3
    SHOW_INVENTORY = 4
    DROP_INVENTORY = 5
    TARGETING = 6
    LEVEL_UP = 7
    CHARACTER_SCREEN = 8
    ENTER_SHOP = 9
    SELLING = 10
    BUYING = 11
