import libtcodpy as libtcod

def menu(con, header, options, width, screen_width, screen_height, special=0):
    '''
    Abstract menu creator
    '''
    if len(options) > 26: raise ValueError('Cannot have a menu with more \
        than 26 options.')

    # calculate total height for the header after auto-wrap and one line per option
    header_height = libtcod.console_get_height_rect(con, 0, 0, width,
        screen_height, header)
    height = (2 * len(options)) + header_height

    # create off-screen console that represents menu window
    window = libtcod.console_new(width, height)

    # print header with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE,
        libtcod.LEFT, header)

    # print all options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 2
        letter_index += 1

    y_end = y
    # blit contents of window to root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    if special == 1:
        libtcod.console_blit(window, 0, 0, width, height, 0, x + 10, y, 1.0, 0.7)
    elif special == 2:
        libtcod.console_blit(window, 0, 0, width, height, 0, x + 26, y, 1.0, 0.7)
    else:
        libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

    # special sell menu
    if special == 1:
        window2 = libtcod.console_new(20, 11)
        libtcod.console_set_default_foreground(window2, libtcod.white)
        libtcod.console_print_rect_ex(window2, 0, 0, width, height, libtcod.BKGND_NONE,
            libtcod.LEFT, header)
        libtcod.console_print_ex(window2, 0, 1, libtcod.BKGND_NONE, libtcod.LEFT, '  SELL SELL SELL!')
        libtcod.console_print_ex(window2, 0, 3, libtcod.BKGND_NONE, libtcod.LEFT, '  CHOOSE WHAT YOU')
        libtcod.console_print_ex(window2, 0, 5, libtcod.BKGND_NONE, libtcod.LEFT, '  WANT TO SELL!')
        libtcod.console_print_ex(window2, 0, 8, libtcod.BKGND_NONE, libtcod.LEFT, '  OR HIT \'ESC\'')
        libtcod.console_print_ex(window2, 0, 10, libtcod.BKGND_NONE, libtcod.LEFT, '  TO EXIT MENU')


        libtcod.console_blit(window2, 0, 0, 20, 20, 0, x - 15, y, 1.0, 0.7)

    # special buy menu
    if special == 2:
        window2 = libtcod.console_new(20, 11)
        libtcod.console_set_default_foreground(window2, libtcod.white)
        libtcod.console_print_rect_ex(window2, 0, 0, width, height, libtcod.BKGND_NONE,
            libtcod.LEFT, header)
        libtcod.console_print_ex(window2, 0, 1, libtcod.BKGND_NONE, libtcod.LEFT, '  BUY BUY BUY!')
        libtcod.console_print_ex(window2, 0, 3, libtcod.BKGND_NONE, libtcod.LEFT, '  CHOOSE WHAT YOU')
        libtcod.console_print_ex(window2, 0, 5, libtcod.BKGND_NONE, libtcod.LEFT, '  WANT TO BUY!')
        libtcod.console_print_ex(window2, 0, 8, libtcod.BKGND_NONE, libtcod.LEFT, '  OR HIT \'ESC\'')
        libtcod.console_print_ex(window2, 0, 10, libtcod.BKGND_NONE, libtcod.LEFT, '  TO EXIT MENU')

        libtcod.console_blit(window2, 0, 0, 20, 20, 0, x, y, 1.0, 0.7)

def inventory_menu(con, header, player, inventory_width, screen_width, screen_height):
    '''
    Creates menu for inventory
    '''
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = []

        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append('{0} (on main hand)'.format(item.name))
            elif player.equipment.off_hand == item:
                options.append('{0} (on off hand)'.format(item.name))
            elif player.equipment.chestplate == item:
                options.append('{0} (on chest)'.format(item.name))
            elif player.equipment.leggings == item:
                options.append('{0} (on legs)'.format(item.name))
            elif player.equipment.helmet == item:
                options.append('{0} (on head)'.format(item.name))
            elif player.equipment.boots == item:
                options.append('{0} (on feet)'.format(item.name))
            elif player.equipment.belt == item:
                options.append('{0} (on waist)'.format(item.name))
            elif player.equipment.ring_1 == item:
                options.append('{0} (first finger)'.format(item.name))
            elif player.equipment.ring_2 == item:
                options.append('{0} (second finger)'.format(item.name))
            elif player.equipment.ring_3 == item:
                options.append('{0} (third finger)'.format(item.name))
            elif player.equipment.ring_4 == item:
                options.append('{0} (fourth finger)'.format(item.name))
            elif player.equipment.ring_5 == item:
                options.append('{0} (fifth finger)'.format(item.name))
            elif player.equipment.ring_6 == item:
                options.append('{0} (in hand)'.format(item.name))
            else:
                options.append(item.name)

    menu(con, header, options, inventory_width, screen_width, screen_height)

def main_menu(con, background_image, screen_width, screen_height):
    '''
    Creates Main Menu
    '''
    libtcod.image_blit_2x(background_image, 0, 0, 0)

    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4,
        libtcod.BKGND_NONE, libtcod.CENTER, 'DESCENT INTO JOTUNHEIM')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2) - 1,
        libtcod.BKGND_NONE, libtcod.CENTER, 'BY DAVID KOHLER')

    menu(con, '', ['NEW GAME', 'CONTINUE', 'RULES', 'QUIT'], 24,
        screen_width, screen_height + 5)

def rules_menu(con, background_image, screen_width, screen_height):
    '''
    Creates Rules Menu
    '''
    libtcod.image_blit_2x(background_image, 0, 0, 0)

    libtcod.console_set_default_foreground(0, libtcod.black)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 20,
        libtcod.BKGND_NONE, libtcod.CENTER, 'RULES')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 16,
        libtcod.BKGND_NONE, libtcod.CENTER,
        'WELCOME TO DESCENT INTO JOTUNHEIM, A ROGUELIKE CREATED BY DAVID KOHLER')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 14,
        libtcod.BKGND_NONE, libtcod.CENTER,
        'YOU ARE A TREASURE HUNTER EXPLORING JOTUNHEIM FOR A SECRET TREASURE TROVE')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 12,
        libtcod.BKGND_NONE, libtcod.CENTER,
        'ACCORDING TO LEGEND, THE TREASURE IS HIDDEN 50 STORIES UNDERNEATH THE REALM')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 10,
        libtcod.BKGND_NONE, libtcod.CENTER,
        'MAKE YOUR WAY THRU 50 FLOORS OF RANDOM DUNGEONS TO REACH YOUR REWARD ')

    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 6,
        libtcod.BKGND_NONE, libtcod.CENTER,
        'USE THE ARROW KEYS TO MOVE AND ATTACK (OR USE STANDARD VIM CONTROLS)')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4,
        libtcod.BKGND_NONE, libtcod.CENTER,
        'USE THE Y, U, B, N KEYS FOR DIAGONAL MOVEMENT AND ATTACK (VIM STANDARD)')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 2,
        libtcod.BKGND_NONE, libtcod.CENTER,
        'USE I TO ENTER INVENTORY, D TO DROP ITEMS FROM INVENTORY, R TO SEE RULES')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2),
        libtcod.BKGND_NONE, libtcod.CENTER,
        'G TO GRAB ITEMS, C TO SEE CHARACTER INFO, Z TO WAIT AND PASS YOUR TURN')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) + 2,
        libtcod.BKGND_NONE, libtcod.CENTER,
        'TAB FOR FULLSCREEN, HOVER WITH MOUSE TO SEE ITEM OR MONSTER NAMES')

    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) + 6,
        libtcod.BKGND_NONE, libtcod.CENTER,
        'THE < ICON INDICATES STAIRS. PRESS ENTER WHILE ON THE ICON TO GO TO NEXT FLOOR')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) + 8,
        libtcod.BKGND_NONE, libtcod.CENTER,
        'THE $ ICON INDICATES A SHOP. PRESS S WHILE ON THE ICON TO ENTER SHOP MENU')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) + 10,
        libtcod.BKGND_NONE, libtcod.CENTER,
        'THE +, #, n, W, U, b, -, *, ], / ICONS ARE ITEMS. ENTER INVENTORY TO EQUIP')

    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) + 14,
        libtcod.BKGND_NONE, libtcod.CENTER,
        'ANYTHING ELSE IS AN ENEMY THAT WANTS YOU DEAD')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) + 16,
        libtcod.BKGND_NONE, libtcod.CENTER,
        'GOOD LUCK')

    menu(con, '', ['RETURN'], 24,
        screen_width, screen_height + 42)

def end_menu(con, background_image, player, screen_width, screen_height):
    '''
    Creates End Game Menu
    '''
    libtcod.image_blit_2x(background_image, 0, 0, 0)

    # create off-screen console that represents menu window
    window = libtcod.console_new(screen_width - 20, screen_height - 20)

    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_set_default_foreground(window, libtcod.white)

    x = int(screen_width / 2)
    y = int(screen_height / 2)

    libtcod.console_print_ex(window, x - 15, y - 23,
        libtcod.BKGND_NONE, libtcod.CENTER, 'CONGRATULATIONS')
    libtcod.console_print_ex(window, x - 15, y - 18,
        libtcod.BKGND_NONE, libtcod.CENTER, 'AFTER 50 DANGEROUS FLOORS OF MONSTERS AND')
    libtcod.console_print_ex(window, x - 15, y - 16,
        libtcod.BKGND_NONE, libtcod.CENTER, 'DEATH, YOU FINALLY REACH THE CENTER OF')
    libtcod.console_print_ex(window, x - 15, y - 14,
        libtcod.BKGND_NONE, libtcod.CENTER, 'JOTUNHEIM. BEFORE YOU, LIE UNIMAGINABLE')
    libtcod.console_print_ex(window, x - 15, y - 12,
        libtcod.BKGND_NONE, libtcod.CENTER, 'TREASURES AND WEALTH - RICHES THE LIKES')
    libtcod.console_print_ex(window, x - 15, y - 10,
        libtcod.BKGND_NONE, libtcod.CENTER, 'OF WHICH NO ONE IN THE NINE REALMS HAS')
    libtcod.console_print_ex(window, x - 15, y - 8,
        libtcod.BKGND_NONE, libtcod.CENTER, 'EVER SEEN. AND THEY ALL BELONG TO YOU NOW...')

    libtcod.console_print_ex(window, x - 15, y - 4,
        libtcod.BKGND_NONE, libtcod.CENTER, 'THANK YOU FOR PLAYING')

    libtcod.console_print_ex(0, x, int(screen_height - 2) - 2,
        libtcod.BKGND_NONE, libtcod.CENTER, 'DESCENT INTO JOTUNHEIM')
    libtcod.console_print_ex(0, x, int(screen_height - 2),
        libtcod.BKGND_NONE, libtcod.CENTER, 'BY DAVID KOHLER')

    libtcod.console_blit(window, 0, 0, 50, 25, 0, x - 25, y - 20, 1.0, 0.7)

    menu(con, '', ['QUIT'], 24,
        screen_width, screen_height + 20)

def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    '''
    Creates level up menu
    '''
    options = ['VITALITY (+20 HP, from {0})'.format(player.fighter.max_hp),
               'STRENGTH (+1 POWER, from {0})'.format(player.fighter.power),
               'FORTITUDE (+1 DEFENSE, from {0})'.format(player.fighter.defense)]

    menu(con, header, options, menu_width, screen_width, screen_height)

def character_screen(player, character_screen_width, character_screen_height,
        screen_width, screen_height):
    '''
    Creates character screen menu
    '''
    window = libtcod.console_new(character_screen_width, (character_screen_height * 2))

    libtcod.console_set_default_foreground(window, libtcod.white)

    libtcod.console_print_rect_ex(window, 0, 1, character_screen_width,
        character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT,
        'Character Information')
    libtcod.console_print_rect_ex(window, 0, 3, character_screen_width,
        character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT,
        'Level: {0}'.format(player.level.current_level))
    libtcod.console_print_rect_ex(window, 0, 5, character_screen_width,
        character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT,
        'Experience: {0}'.format(player.level.current_xp))
    libtcod.console_print_rect_ex(window, 0, 7, character_screen_width,
        character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT,
        'Experience to Level: {0}'.format(player.level.experience_to_next_level))
    libtcod.console_print_rect_ex(window, 0, 9, character_screen_width,
        character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT,
        'Coin: {0}'.format(player.fighter.coin))
    libtcod.console_print_rect_ex(window, 0, 13, character_screen_width,
        character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT,
        'Maximum HP: {0}'.format(player.fighter.max_hp))
    libtcod.console_print_rect_ex(window, 0, 15, character_screen_width,
        character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT,
        'Attack: {0}'.format(player.fighter.power))
    libtcod.console_print_rect_ex(window, 0, 17, character_screen_width,
        character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT,
        'Defense: {0}'.format(player.fighter.defense))

    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height
    libtcod.console_blit(window, 0, 0, character_screen_width,
        (character_screen_height * 2), 0, x, y, 1.0, 0.7)

def message_box(con, header, width, screen_width, screen_height):
    '''
    Creates message box menu
    '''
    menu(con, header, [], width, screen_width, screen_height)

def enter_shop_menu(con, header, player, menu_width, screen_width, screen_height):
    '''
    Creates menu for entering shop
    '''
    options = ['SELL', 'BUY', 'EXIT']
    menu(con, header, options, menu_width, screen_width, screen_height)

def sell_menu(con, header, player, inventory_width, screen_width, screen_height):
    '''
    Creates menu for selling items at shop
    '''
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = []
        for item in player.inventory.items:
            item_name = item.name.split('(')[0]
            item_name_price = item_name + '(${0})'.format((item.cashable.coin // 10))
            options.append(item_name_price)

    menu(con, header, options, inventory_width, screen_width, screen_height, special=1)

def buy_menu(con, header, shopkeeper, inventory_width, screen_width, screen_height):
    '''
    Creates menu for buying items at shop
    '''
    options = []
    for item in shopkeeper.inventory.items:
        item_name = item.name.split('(')[0]
        item_name_price = item_name + '(${0})'.format(item.cashable.coin)
        options.append(item_name_price)
    menu(con, header, options, inventory_width, screen_width, screen_height, special=2)
