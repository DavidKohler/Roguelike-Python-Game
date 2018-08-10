import libtcodpy as libtcod

from game_states import GameStates

def handle_keys(key, game_state):
    '''
    Determines key handler from game state
    '''
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)
    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)
    elif game_state == GameStates.LEVEL_UP:
        return handle_level_up_menu(key)
    elif game_state == GameStates.CHARACTER_SCREEN:
        return handle_character_screen(key)
    elif game_state == GameStates.ENTER_SHOP:
        return handle_enter_shop(key)
    elif game_state == GameStates.SELLING:
        return handle_selling(key)
    elif game_state == GameStates.BUYING:
        return handle_buying(key)
    elif game_state == GameStates.RULES:
        return handle_rules_menu(key)
    return {}

def handle_player_turn_keys(key):
    '''
    Basic keys for player turn
    '''
    key_char = chr(key.c)
    # movement keys
    if key.vk == libtcod.KEY_UP or key_char == 'k':
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key_char == 'j':
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key_char == 'h':
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'l':
        return {'move': (1, 0)}
    elif key_char == 'y':
        return {'move': (-1, -1)}
    elif key_char == 'u':
        return {'move': (1, -1)}
    elif key_char == 'b':
        return {'move': (-1, 1)}
    elif key_char == 'n':
        return {'move': (1, 1)}
    elif key_char == 'z':
        return {'wait': True}

    if key_char == 'g':
        return {'pickup': True}
    elif key_char == 'i':
        return {'show_inventory': True}
    elif key_char == 'd':
        return {'drop_inventory': True}
    elif key.vk == libtcod.KEY_ENTER:
        return {'take_stairs': True}
    elif key_char == 'c':
        return {'show_character_screen': True}
    elif key_char == 's':
        return {'shop': True}
    elif key_char == 'r':
        return {'show_rules_screen': True}

    if key.vk == libtcod.KEY_TAB:
        return {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # exit the game
        return {'exit': True}

    # no key was pressed
    return {}

def handle_player_dead_keys(key):
    '''
    Keys for dead player
    '''
    key_char = chr(key.c)

    if key_char == 'i':
        return {'show_inventory': True}

    if key.vk == libtcod.KEY_TAB:
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # exit the menu
        return {'exit': True}

    return {}

def handle_inventory_keys(key):
    '''
    Keys while in inventory
    '''
    index = key.c - ord('a')

    if index >= 0:
        return {'inventory_index': index}

    if key.vk == libtcod.KEY_TAB:
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}

def handle_targeting_keys(key):
    '''
    Keys while targeting
    '''
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    elif key.vk == libtcod.KEY_TAB:
        return {'fullscreen': True}

    return {}

def handle_level_up_menu(key):
    '''
    Keys while in level up menu
    '''
    if key:
        key_char = chr(key.c)

        if key_char == 'a':
            return {'level_up': 'hp'}
        elif key_char == 'b':
            return {'level_up': 'str'}
        elif key_char == 'c':
            return {'level_up': 'def'}
        elif key.vk == libtcod.KEY_TAB:
            return {'fullscreen': True}

    return {}

def handle_character_screen(key):
    '''
    Keys while in character screen
    '''
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    elif key.vk == libtcod.KEY_TAB:
        return {'fullscreen': True}

    return {}

def handle_enter_shop(key):
    '''
    Keys while entering shop
    '''
    key_char = chr(key.c)

    if key_char == 'a':
        return {'shop_sell': True}
    elif key_char == 'b':
        return {'shop_buy': True}
    elif key_char == 'c' or  key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    elif key.vk == libtcod.KEY_TAB:
        return {'fullscreen': True}

    return {}

def handle_selling(key):
    '''
    Keys while selling in shop
    '''
    index = key.c - ord('a')

    if index >= 0:
        return {'sell_index': index}

    if key.vk == libtcod.KEY_TAB:
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # exit the menu
        return {'exit': True}

    return {}

def handle_buying(key):
    '''
    Keys while buying in shop
    '''
    index = key.c - ord('a')

    if index >= 0:
        return {'buy_index': index}

    if key.vk == libtcod.KEY_TAB:
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # exit the menu
        return {'exit': True}

    return {}

def handle_main_menu(key):
    '''
    Keys while on main menu
    '''
    key_char = chr(key.c)

    if key_char == 'a':
        return {'new_game': True}
    elif key_char == 'b':
        return {'load_game': True}
    elif key_char == 'c':
        return {'rules_menu': True}
    elif key_char == 'd' or  key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    elif key.vk == libtcod.KEY_TAB:
        return {'fullscreen': True}

    return {}

def handle_rules_menu(key):
    '''
    Keys while on rules menu
    '''
    key_char = chr(key.c)

    if key_char == 'a' or  key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    elif key.vk == libtcod.KEY_TAB:
        return {'fullscreen': True}

    return {}

def handle_end_menu(key):
    '''
    Keys while on end menu
    '''
    key_char = chr(key.c)

    if key_char == 'a' or  key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    elif key.vk == libtcod.KEY_TAB:
        return {'fullscreen': True}

    return {}

def handle_mouse(mouse):
    '''
    Handles mouse coordinates
    '''
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}

    return {}
