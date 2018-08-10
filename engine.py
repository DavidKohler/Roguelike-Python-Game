import libtcodpy as libtcod

from death_functions import kill_monster, kill_player

from entity import get_blocking_entities_at_location

from fov_functions import initialize_fov, recompute_fov

from game_messages import Message

from game_states import GameStates

from input_handlers import handle_keys, handle_main_menu, handle_mouse, handle_rules_menu, handle_end_menu

from loader_functions.initialize_new_game import get_constants, get_game_variables
from loader_functions.data_loaders import load_game, save_game

from menus import main_menu, message_box, rules_menu, end_menu

from render_functions import clear_all, render_all

def play_game(player, entities, game_map, message_log, game_state, con,
            panel, constants):
    '''
    Main engine and executor of code
    '''
    fov_recompute = True

    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state

    targeting_item = None

    while not libtcod.console_is_window_closed():

        if game_map.dungeon_level == 51:
            end_game(player)

        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS |
            libtcod.EVENT_MOUSE, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, constants['fov_radius'],
                        constants['fov_light_walls'], constants['fov_algorithm'])

        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute,
                message_log, constants['screen_width'], constants['screen_height'],
                constants['bar_width'], constants['panel_height'],
                constants['panel_y'], mouse, constants['colors'], game_state)

        fov_recompute = False

        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key, game_state)
        mouse_action = handle_mouse(mouse)

        # checks for actions
        move = action.get('move')
        wait = action.get('wait')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        take_stairs = action.get('take_stairs')
        level_up = action.get('level_up')
        show_character_screen = action.get('show_character_screen')
        show_rules_screen = action.get('show_rules_screen')
        shop = action.get('shop')
        shop_sell = action.get('shop_sell')
        shop_buy = action.get('shop_buy')
        sell_index = action.get('sell_index')
        buy_index = action.get('buy_index')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

        player_turn_results = []

        # player moving
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x,
                        destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)

                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        # player waiting
        elif wait:
            game_state = GameStates.ENEMY_TURN

        # player tries to pick up item
        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)

                    break
            else:
                message_log.add_message(Message('There is nothing here to pick up.',
                        libtcod.yellow))

        # player shows inventory menu
        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        # player shows inventory menu
        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        # player selects object from inventory
        if inventory_index is not None and \
                previous_game_state != GameStates.PLAYER_DEAD and \
                inventory_index < len(player.inventory.items):
            item = player.inventory.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item,
                    entities=entities, fov_map=fov_map))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))

        # player tries to take stairs
        if take_stairs and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.stairs and entity.x == player.x and entity.y == player.y:
                    entities = game_map.next_floor(player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    libtcod.console_clear(con)

                    break
            else:
                message_log.add_message(Message('There are no stairs here.',
                    libtcod.yellow))
        # player levels up
        if level_up:
            if level_up == 'hp':
                player.fighter.base_max_hp += 20
                player.fighter.hp += 20
            elif level_up == 'str':
                player.fighter.base_power += 1
            elif level_up == 'def':
                player.fighter.base_defense += 1

            game_state = previous_game_state

        # player opens character screen
        if show_character_screen:
            previous_game_state = game_state
            game_state = GameStates.CHARACTER_SCREEN

        # player opens rules screen
        if show_rules_screen:
            previous_game_state = game_state
            game_state = GameStates.RULES

        # player tries to target
        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click

                item_use_results = player.inventory.use(targeting_item,
                    entities=entities, fov_map=fov_map, target_x=target_x,
                    target_y=target_y)
                player_turn_results.extend(item_use_results)
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})

        # player tries to enter shop
        if shop and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.shopkeep and entity.x == player.x and entity.y == player.y:
                    previous_game_state = game_state
                    game_state = GameStates.ENTER_SHOP

                    break
            else:
                message_log.add_message(Message('There is no shopkeeper here.',
                    libtcod.yellow))

        # player tries to sell
        if shop_sell:
            game_state = GameStates.SELLING

        # player tries to sell item at shop
        if sell_index is not None and previous_game_state != GameStates.PLAYER_DEAD and\
                game_state == GameStates.SELLING and sell_index < len(player.inventory.items):

            for entity in entities:
                if entity.shopkeep:
                    item_cost = player.inventory.items[sell_index].cashable.coin
                    player.fighter.coin += (item_cost // 10)
                    message_log.add_message(Message('You sell {0}for {1} coins.'\
                        .format(player.inventory.items[sell_index].name.split('(')[0],
                        (item_cost // 10)), libtcod.blue))
                    player.inventory.remove_item(player.inventory.items[sell_index])

                    break

        # player tries to buy
        if shop_buy:
            game_state = GameStates.BUYING

        # player tries to buy item at shop
        if buy_index is not None and previous_game_state != GameStates.PLAYER_DEAD and\
                game_state == GameStates.BUYING and buy_index < 25:

            for entity in entities:
                if entity.shopkeep:
                    player_coin = player.fighter.coin
                    item_cost = entity.inventory.items[buy_index].cashable.coin
                    if player_coin >= item_cost:
                        player.inventory.add_item(entity.inventory.items[buy_index])
                        player.fighter.coin -= item_cost
                        message_log.add_message(Message('You buy {0}for {1} coins.'\
                            .format(entity.inventory.items[buy_index].name.split('(')[0],
                            item_cost), libtcod.blue))
                    else:
                        message_log.add_message(Message('Not enough coins!',
                            libtcod.yellow))

                    break

        # exit menu or game
        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY,
                    GameStates.CHARACTER_SCREEN, GameStates.RULES):
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            elif game_state == GameStates.ENTER_SHOP:
                game_state = GameStates.PLAYERS_TURN
            elif game_state in (GameStates.SELLING, GameStates.BUYING):
                game_state = GameStates.ENTER_SHOP
            else:
                save_game(player, entities, game_map, message_log, game_state)

                return True

        # toggle fullscreen
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        # player turn results
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')
            equip = player_turn_result.get('equip')
            targeting = player_turn_result.get('targeting')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')
            xp = player_turn_result.get('xp')
            coin = player_turn_result.get('coin')

            # adds message to log
            if message:
                message_log.add_message(message)

            # deals with dead entity
            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

            # item picked up
            if item_added:
                entities.remove(item_added)

                game_state = GameStates.ENEMY_TURN

            # item used
            if item_consumed:
                game_state = GameStates.ENEMY_TURN

            # item dropped
            if item_dropped:
                entities.append(item_dropped)

                game_state = GameStates.ENEMY_TURN

            # item equip toggled
            if equip:
                equip_results = player.equipment.toggle_equip(equip)

                for equip_result in equip_results:
                    equipped = equip_result.get('equipped')
                    dequipped = equip_result.get('dequipped')

                    if equipped:
                        message_log.add_message(Message('You equipped the {0}'\
                            .format(equipped.name.split('(')[0])))

                    if dequipped:
                        message_log.add_message(Message('You dequipped the {0}'\
                            .format(dequipped.name.split('(')[0])))

                game_state = GameStates.ENEMY_TURN

            # something targeted
            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING

                targeting_item = targeting

                message_log.add_message(targeting_item.item.targeting_message)

            # targeting cancelled
            if targeting_cancelled:
                game_state = previous_game_state

                message_log.add_message(Message('Targeting cancelled'))

            # gained xp
            if xp:
                leveled_up = player.level.add_xp(xp)
                message_log.add_message(Message('You gain {0} experience points.'\
                    .format(xp), libtcod.orange))

                if leveled_up:
                    message_log.add_message(Message(
                        'Your battle skills grow stronger! You reached level {0}'\
                            .format(player.level.current_level) + '!',
                            libtcod.yellow))
                    previous_game_state = game_state
                    game_state = GameStates.LEVEL_UP

            # gained coins
            if coin:
                player.fighter.add_coin(coin)
                message_log.add_message(Message('You gain {0} coins.'\
                    .format(coin), libtcod.orange))
        # enemy takes turn
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map,
                        game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        # adds message to log
                        if message:
                            message_log.add_message(message)

                        # checks for dead entity
                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            message_log.add_message(message)

                            # if player is dead, we're done
                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    # if player is dead, we're done
                    if game_state == GameStates.PLAYER_DEAD:
                        break
            # player's turn again
            else:
                game_state = GameStates.PLAYERS_TURN

def main():
    '''
    Loads and initializes all it needs. Starts game
    '''
    constants = get_constants()

    # uses custom font image
    libtcod.console_set_custom_font("./art/terminal8x8_gs_ro.png",
        libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(constants['screen_width'], constants['screen_height'],
        constants['window_title'], False)

    con = libtcod.console_new(constants['screen_width'], constants['screen_height'])
    panel = libtcod.console_new(constants['screen_width'], constants['panel_height'])

    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None

    show_main_menu = True
    show_load_error_message = False

    # uses custom background image
    main_menu_background_image = libtcod.image_load('./art/background.png')

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE,
            key, mouse)

        if show_main_menu:
            main_menu(con, main_menu_background_image, constants['screen_width'],
                constants['screen_height'])

            if show_load_error_message:
                message_box(con, 'No save game to load', 50, constants['screen_width'],
                    constants['screen_height'])

            libtcod.console_flush()

            action = handle_main_menu(key)

            new_game = action.get('new_game')
            load_saved_game = action.get('load_game')
            rules_menu = action.get('rules_menu')
            exit_game = action.get('exit')
            fullscreen = action.get('fullscreen')

            # toggle fullscreen
            if fullscreen:
                libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

            if show_load_error_message and (new_game or load_saved_game or exit_game):
                show_load_error_message = False
            elif new_game:
                player, entities, game_map, message_log, game_state = \
                    get_game_variables(constants)
                game_state = GameStates.PLAYERS_TURN

                show_main_menu = False
            elif load_saved_game:
                try:
                    player, entities, game_map, message_log, game_state = load_game()
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif rules_menu:
                show_rules()
            elif exit_game:
                break

        else:
            libtcod.console_clear(con)
            play_game(player, entities, game_map, message_log, game_state, con,
                panel, constants)

            show_main_menu = True

def show_rules():
    '''
    Shows Rules
    '''
    constants = get_constants()

    con = libtcod.console_new(constants['screen_width'], constants['screen_height'])
    panel = libtcod.console_new(constants['screen_width'], constants['panel_height'])

    show_rules_menu = True

    # uses custom background image
    rules_menu_background_image = libtcod.image_load('./art/rules_background.png')

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE,
            key, mouse)

        if show_rules_menu:
            rules_menu(con, rules_menu_background_image, constants['screen_width'],
                      constants['screen_height'])

            libtcod.console_flush()

            action = handle_rules_menu(key)

            exit_game = action.get('exit')
            fullscreen = action.get('fullscreen')

            # toggle fullscreen
            if fullscreen:
                libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

            if exit_game:
                show_rules_menu = False

        else:
            return True

def end_game(player):
    '''
    Shows End Game screen
    '''
    constants = get_constants()

    con = libtcod.console_new(constants['screen_width'], constants['screen_height'])
    panel = libtcod.console_new(constants['screen_width'], constants['panel_height'])

    show_end_menu = True

    # uses custom background image
    end_menu_background_image = libtcod.image_load('./art/end_screen2.png')

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE,
            key, mouse)

        if show_end_menu:
            end_menu(con, end_menu_background_image, player, constants['screen_width'],
                      constants['screen_height'])

            libtcod.console_flush()

            action = handle_end_menu(key)

            exit_game = action.get('exit')
            fullscreen = action.get('fullscreen')

            # toggle fullscreen
            if fullscreen:
                libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

            if exit_game:
                show_end_menu = False

        else:
            exit()

if __name__ == '__main__':
    main()
