import libtcodpy as libtcod

from components.ai import BasicMonster
from components.cashable import Cashable
from components.equipment import EquipmentSlots
from components.equippable import Equippable
from components.fighter import Fighter
from components.item import Item
from components.inventory import Inventory
from components.shopkeep import Shopkeep
from components.stairs import Stairs

from entity import Entity

from game_messages import Message

from item_functions import cast_confuse, cast_fireball, cast_lightning, cast_mistletoe, cast_ragnarok, heal

from map_objects.rectangle import Rect
from map_objects.tile import Tile

from random import randint

from random_utils import from_dungeon_level, random_choice_from_dict

from render_functions import RenderOrder

class GameMap:
    '''
    Controls game map object and entity placement
    '''
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

        self.dungeon_level = dungeon_level

    def initialize_tiles(self):
        '''
        Initialize a 2D array of tiles
        '''
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def create_room(self, room):
        '''
        Digs out room, making tiles passible
        '''
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width,
            map_height, player, entities):
        '''
        Creates map of current dungeon floor
        '''
        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

        for r in range(max_rooms):
            # random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # random pos in map boundaries
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # use rectangle room class
            new_room = Rect(x, y, w, h)

            # check for intersecting rooms
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break

            else:
                self.create_room(new_room)

                # center coordinates of new room
                (new_x, new_y) = new_room.center()

                center_of_last_room_x = new_x
                center_of_last_room_y = new_y

                if num_rooms == 0:
                    # starting room
                    player.x = new_x
                    player.y = new_y

                    shopkeep_component = Shopkeep(True)
                    inventory_component = Inventory(50)
                    shopkeeper = Entity(new_x+1, new_y+1, '$', libtcod.Color(5, 5, 5),
                        'Shopkeeper', blocks=True,render_order=RenderOrder.ACTOR,
                        shopkeep=shopkeep_component, inventory=inventory_component)

                    equippable_component = Equippable(EquipmentSlots.BOOTS,
                        power_bonus=-10, defense_bonus=-10, max_hp_bonus=50)
                    cashable_component = Cashable(5)
                    item = Entity(x, y, 'b', libtcod.Color(149, 104, 26),
                        'Fresh Timbs (-10P -10D +50HP)', equippable=equippable_component,
                        cashable=cashable_component)

                    shopkeeper.inventory.add_item(item)
                    entities.append(shopkeeper)
                    self.tiles[new_x+1][new_y+1].blocked = True
                else:
                    # all rooms after the first
                    # connect to previous room with tunnels
                    '''
                    if num_rooms == 1:
                        #33% chance of generating a shop on second room
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()
                        if randint(0, 1) == 1:
                            # first move horizontally, then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                            # first move vertically, then horizontally
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)

                        shopkeeper = Entity(new_x, new_y, '$', libtcod.Color(5, 5, 5),
                            'Shopkeeper', blocks=True,render_order=RenderOrder.ACTOR)

                        entities.append(shopkeeper)
                        rooms.append(new_room)
                        num_rooms += 1

                        continue
                    '''
                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # random choice of tunnel
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room, entities)
                # append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

        # create stairs entity in center of last room
        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>',
            libtcod.white, 'Stairs', render_order=RenderOrder.STAIRS,
            stairs=stairs_component)
        entities.append(down_stairs)

    def create_h_tunnel(self, x1, x2, y):
        '''
        Digs out horizontal tunnel
        '''
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        '''
        Digs out vertical tunnel
        '''
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities):
        '''
        Places items or monsters in room
        '''
        max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [5, 6]],
            self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1, 1], [2, 4]], self.dungeon_level)
        number_of_items = randint(0, max_items_per_room)
        number_of_monsters = randint(0, max_monsters_per_room)

        monster_chances = {
            'orc': 80,
            'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]],
                self.dungeon_level)
        }

        item_chances = {
            #HELMET
            'light_helm': from_dungeon_level([[5, 2], [0, 9]], self.dungeon_level),
            'medium_helm': from_dungeon_level([[5, 8], [0, 16]], self.dungeon_level),
            'dwarven_helm': from_dungeon_level([[5, 15], [0, 22]], self.dungeon_level),
            'valkyrie_helm': from_dungeon_level([[5, 21], [0, 31]], self.dungeon_level),
            'helm_of_awe': from_dungeon_level([[5, 30]], self.dungeon_level),
            'hulidshjalmr': from_dungeon_level([[5, 40]], self.dungeon_level),
            #CHESTPLATE
            'leather_chestplate': from_dungeon_level([[5, 2], [0, 9]], self.dungeon_level),
            'chainmail': from_dungeon_level([[5, 8], [0, 16]], self.dungeon_level),
            'dwarven_chestplate': from_dungeon_level([[5, 15], [0, 22]], self.dungeon_level),
            'falcon_cloak': from_dungeon_level([[5, 21], [0, 31]], self.dungeon_level),
            'tarnkappe': from_dungeon_level([[5, 30]], self.dungeon_level),
            'golden_coat': from_dungeon_level([[5, 37]], self.dungeon_level),
            #LEGGINGS
            'light_leggings': from_dungeon_level([[5, 2], [0, 10]], self.dungeon_level),
            'chain_leggings': from_dungeon_level([[5, 9], [0, 18]], self.dungeon_level),
            'dwarven_leggings': from_dungeon_level([[5, 17], [0, 28]], self.dungeon_level),
            'leggings_of_baldur': from_dungeon_level([[5, 27]], self.dungeon_level),
            'leggings_of_odin': from_dungeon_level([[5, 35]], self.dungeon_level),
            #BOOTS
            'light_boots': from_dungeon_level([[5, 2], [0, 11]], self.dungeon_level),
            'timbs': from_dungeon_level([[1, 5]], self.dungeon_level),
            'steel_boots': from_dungeon_level([[5, 10], [0, 19]], self.dungeon_level),
            'dwarven_boots': from_dungeon_level([[5, 18], [0, 27]], self.dungeon_level),
            'helskor': from_dungeon_level([[5, 26]], self.dungeon_level),
            'shoes_of_vidarr': from_dungeon_level([[5, 30]], self.dungeon_level),
            #BELT
            'leather_belt': from_dungeon_level([[5, 2], [0, 16]], self.dungeon_level),
            'girdle_of_brynhilder': from_dungeon_level([[5, 15], [0, 31]], self.dungeon_level),
            'megingjord': from_dungeon_level([[5, 30]], self.dungeon_level),
            #RINGS
            'space_stone': from_dungeon_level([[2, 2], [0, 10]], self.dungeon_level),
            'mind_stone': from_dungeon_level([[2, 8], [0, 18]], self.dungeon_level),
            'reality_stone': from_dungeon_level([[2, 16], [0, 26]], self.dungeon_level),
            'power_stone': from_dungeon_level([[2, 24], [0, 32]], self.dungeon_level),
            'time_stone': from_dungeon_level([[2, 30], [0, 40]], self.dungeon_level),
            'soul_stone': from_dungeon_level([[2, 36]], self.dungeon_level),
            #OFF_HAND
            'wooden_shield': from_dungeon_level([[15, 4], [0, 11]], self.dungeon_level),
            'sturdy_shield': from_dungeon_level([[15, 10], [0, 18]], self.dungeon_level),
            'dwarven_shield': from_dungeon_level([[10, 17], [0, 26]], self.dungeon_level),
            'jotun_shield': from_dungeon_level([[10, 25], [0, 31]], self.dungeon_level),
            'shield_of_hel': from_dungeon_level([[7, 30], [0, 36]], self.dungeon_level),
            'ullrs_shield': from_dungeon_level([[5, 35]], self.dungeon_level),
            'svallin': from_dungeon_level([[5, 38]], self.dungeon_level),
            #MAIN_HAND
            'iron_sword': from_dungeon_level([[10, 4], [0, 8]], self.dungeon_level),
            'berserker_sword': from_dungeon_level([[10, 7], [0, 13]], self.dungeon_level),
            'dwarven_axe': from_dungeon_level([[7, 12], [0, 16]], self.dungeon_level),
            'viking_halberd': from_dungeon_level([[5, 15], [0, 21]], self.dungeon_level),
            'laevateinn': from_dungeon_level([[5, 10], [0, 16]], self.dungeon_level),
            'dainsleif': from_dungeon_level([[5, 15], [0, 21]], self.dungeon_level),
            'skofnung': from_dungeon_level([[5, 20], [0, 26]], self.dungeon_level),
            'hrotti': from_dungeon_level([[5, 25], [0, 32]], self.dungeon_level),
            'ridill': from_dungeon_level([[5, 25], [0, 32]], self.dungeon_level),
            'gram': from_dungeon_level([[5, 30], [0, 40]], self.dungeon_level),
            'mistilteinn': from_dungeon_level([[5, 30], [0, 42]], self.dungeon_level),
            'gungnir': from_dungeon_level([[4, 38]], self.dungeon_level),
            'tyrfing': from_dungeon_level([[4, 38]], self.dungeon_level),
            'mjolnir': from_dungeon_level([[4, 42]], self.dungeon_level),
            #POTION
            's_healing_potion': from_dungeon_level([[40, 1], [0, 15]], self.dungeon_level),
            'm_healing_potion': from_dungeon_level([[40, 15], [0, 30]], self.dungeon_level),
            'l_healing_potion': from_dungeon_level([[35, 30]], self.dungeon_level),
            'full_healing_salve': from_dungeon_level([[25, 40]], self.dungeon_level),
            #SCROLL
            'confusion_scroll': from_dungeon_level([[20, 2], [10, 9]], self.dungeon_level),
            'lightning_scroll': from_dungeon_level([[20, 8], [10, 17]], self.dungeon_level),
            'fireball_scroll': from_dungeon_level([[15, 16], [10, 23]], self.dungeon_level),
            'mistletoe': from_dungeon_level([[12, 22]], self.dungeon_level),
            'ragnarok': from_dungeon_level([[5, 30]], self.dungeon_level)
        }

        for i in range(number_of_monsters):
            # choose random location in room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and \
                    entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)
                '''
                All monsters available
                '''
                if monster_choice == 'orc':
                    fighter_component = Fighter(hp=20, defense=0, power=3, xp=35, coin=10)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'o', libtcod.Color(14, 27, 112), 'Orc',
                        blocks=True,render_order=RenderOrder.ACTOR,
                        fighter=fighter_component, ai=ai_component)
                else:
                    fighter_component = Fighter(hp=30, defense=2, power=8, xp=100, coin=30)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'T', libtcod.darker_green, 'Troll',
                        blocks=True, fighter=fighter_component,
                        render_order=RenderOrder.ACTOR, ai=ai_component)

                entities.append(monster)

        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and \
                    entity.y == y]):
                item_choice = random_choice_from_dict(item_chances)
                '''
                All items available
                '''
                #POTION
                if item_choice == 's_healing_potion':
                    item_component = Item(use_function=heal, amount=35)
                    item = Entity(x, y, '+', libtcod.Color(208, 15, 15),
                        'Small Healing Potion (+35HP)', render_order=RenderOrder.ITEM,
                        item=item_component)
                elif item_choice == 'm_healing_potion':
                    item_component = Item(use_function=heal, amount=70)
                    item = Entity(x, y, '+', libtcod.Color(220, 15, 15),
                        'Medium Healing Potion (+70HP)', render_order=RenderOrder.ITEM,
                        item=item_component)
                elif item_choice == 'l_healing_potion':
                    item_component = Item(use_function=heal, amount=100)
                    item = Entity(x, y, '+', libtcod.Color(240, 10, 10),
                        'Large Healing Potion (+100HP)', render_order=RenderOrder.ITEM,
                        item=item_component)
                elif item_choice == 'full_healing_salve':
                    item_component = Item(use_function=heal, amount=800)
                    item = Entity(x, y, '+', libtcod.Color(255, 0, 0),
                        'Full Healing Salve', render_order=RenderOrder.ITEM,
                        item=item_component)
                #HELMET
                elif item_choice == 'light_helm':
                    equippable_component = Equippable(EquipmentSlots.HELMET,
                        defense_bonus=1)
                    item = Entity(x, y, 'n', libtcod.Color(96, 98, 114),
                        'Light Helm (+1D)', equippable=equippable_component)
                elif item_choice == 'medium_helm':
                    equippable_component = Equippable(EquipmentSlots.HELMET,
                        defense_bonus=2)
                    item = Entity(x, y, 'n', libtcod.Color(100, 100, 110),
                        'Medium Helm (+2D)', equippable=equippable_component)
                elif item_choice == 'dwarven_helm':
                    equippable_component = Equippable(EquipmentSlots.HELMET,
                        defense_bonus=4, max_hp_bonus=10)
                    item = Entity(x, y, 'n', libtcod.Color(27, 35, 107),
                        'Dwarven Helm (+4D +10HP)', equippable=equippable_component)
                elif item_choice == 'valkyrie_helm':
                    equippable_component = Equippable(EquipmentSlots.HELMET,
                        defense_bonus=6, power_bonus=6)
                    item = Entity(x, y, 'n', libtcod.Color(114, 80, 13),
                        'Valkyrie Helm (+6D +6P)', equippable=equippable_component)
                elif item_choice == 'helm_of_awe':
                    equippable_component = Equippable(EquipmentSlots.HELMET,
                        defense_bonus=8, max_hp_bonus=30)
                    item = Entity(x, y, 'n', libtcod.Color(20, 77, 18),
                        'Helm of Awe (+8D +30HP)', equippable=equippable_component)
                elif item_choice == 'hulidshjalmr':
                    equippable_component = Equippable(EquipmentSlots.HELMET,
                        defense_bonus=12, power_bonus=5, max_hp_bonus=20)
                    item = Entity(x, y, 'n', libtcod.Color(164, 154, 20),
                        'Hulidshjalmr (+12D +5P +20HP)', equippable=equippable_component)
                #CHESTPLATE
                elif item_choice == 'leather_chestplate':
                    equippable_component = Equippable(EquipmentSlots.CHESTPLATE,
                        defense_bonus=1)
                    item = Entity(x, y, 'W', libtcod.Color(104, 69, 7),
                        'Leather Chestplate (+1D)', equippable=equippable_component)
                elif item_choice == 'chainmail':
                        equippable_component = Equippable(EquipmentSlots.CHESTPLATE,
                            defense_bonus=2)
                        item = Entity(x, y, 'W', libtcod.Color(164, 164, 164),
                            'Chainmail Chestplate (+2D)', equippable=equippable_component)
                elif item_choice == 'dwarven_chestplate':
                        equippable_component = Equippable(EquipmentSlots.CHESTPLATE,
                            defense_bonus=4, max_hp_bonus=10)
                        item = Entity(x, y, 'W', libtcod.Color(41, 62, 146),
                            'Dwarven Chestplate (+4D +10HP)', equippable=equippable_component)
                elif item_choice == 'falcon_cloak':
                        equippable_component = Equippable(EquipmentSlots.CHESTPLATE,
                            defense_bonus=6)
                        item = Entity(x, y, 'W', libtcod.Color(183, 151, 94),
                            'Falcon Cloak (+6D)', equippable=equippable_component)
                elif item_choice == 'tarnkappe':
                        equippable_component = Equippable(EquipmentSlots.CHESTPLATE,
                            defense_bonus=8, power_bonus=6, max_hp_bonus=10)
                        item = Entity(x, y, 'W', libtcod.Color(54, 45, 30),
                            'Tarnkappe (+8D +6P +10HP)', equippable=equippable_component)
                elif item_choice == 'golden_coat':
                        equippable_component = Equippable(EquipmentSlots.CHESTPLATE,
                            defense_bonus=12, power_bonus=5, max_hp_bonus=20)
                        item = Entity(x, y, 'W', libtcod.Color(175, 144, 18),
                            'Golden Coat of Chainmail (+12D +5P +20HP)',
                            equippable=equippable_component)
                #LEGGINGS
                elif item_choice == 'light_leggings':
                    equippable_component = Equippable(EquipmentSlots.LEGGINGS,
                        defense_bonus=1)
                    item = Entity(x, y, 'U', libtcod.Color(220, 187, 50),
                        'Light Leggings (+1D)', equippable=equippable_component)
                elif item_choice == 'chain_leggings':
                    equippable_component = Equippable(EquipmentSlots.LEGGINGS,
                        defense_bonus=2)
                    item = Entity(x, y, 'U', libtcod.Color(154, 154, 154),
                        'Chain Leggings (+2D)', equippable=equippable_component)
                elif item_choice == 'dwarven_leggings':
                    equippable_component = Equippable(EquipmentSlots.LEGGINGS,
                        defense_bonus=4, max_hp_bonus=10)
                    item = Entity(x, y, 'U', libtcod.Color(38, 51, 117),
                        'Dwarven Leggings (+4D +10HP)',
                        equippable=equippable_component)
                elif item_choice == 'leggings_of_baldur':
                    equippable_component = Equippable(EquipmentSlots.LEGGINGS,
                        defense_bonus=6, max_hp_bonus=10)
                    item = Entity(x, y, 'U', libtcod.Color(23, 98, 53),
                        'Leggings of Baldur (+6D +10HP)',
                        equippable=equippable_component)
                elif item_choice == 'leggings_of_odin':
                    equippable_component = Equippable(EquipmentSlots.LEGGINGS,
                        defense_bonus=10, power_bonus=6, max_hp_bonus=10)
                    item = Entity(x, y, 'U', libtcod.Color(152, 169, 2),
                        'Leggings of Odin (+10D +6P +10HP)',
                        equippable=equippable_component)
                #BOOTS
                elif item_choice == 'light_boots':
                    equippable_component = Equippable(EquipmentSlots.BOOTS,
                        defense_bonus=1)
                    item = Entity(x, y, 'b', libtcod.Color(149, 149, 26),
                        'Light Boots (+1D)', equippable=equippable_component)
                elif item_choice == 'timbs':
                    equippable_component = Equippable(EquipmentSlots.BOOTS,
                        power_bonus=-10, defense_bonus=-10, max_hp_bonus=50)
                    item = Entity(x, y, 'b', libtcod.Color(149, 104, 26),
                        'Fresh Timbs (-10P -10D +50HP)', equippable=equippable_component)
                elif item_choice == 'steel_boots':
                    equippable_component = Equippable(EquipmentSlots.BOOTS,
                        defense_bonus=2)
                    item = Entity(x, y, 'b', libtcod.Color(100, 100, 100),
                        'Steel Boots (+2D)', equippable=equippable_component)
                elif item_choice == 'dwarven_boots':
                    equippable_component = Equippable(EquipmentSlots.BOOTS,
                        defense_bonus=4, max_hp_bonus=10)
                    item = Entity(x, y, 'b', libtcod.Color(32, 32, 112),
                        'Dwarven Boots (+4D +10HP)', equippable=equippable_component)
                elif item_choice == 'helskor':
                    equippable_component = Equippable(EquipmentSlots.BOOTS,
                        defense_bonus=6, max_hp_bonus=15)
                    item = Entity(x, y, 'b', libtcod.Color(137, 29, 8),
                        'Helskor (+6D +15HP)', equippable=equippable_component)
                elif item_choice == 'shoes_of_vidarr':
                    equippable_component = Equippable(EquipmentSlots.BOOTS,
                        defense_bonus=10, max_hp_bonus=10)
                    item = Entity(x, y, 'b', libtcod.Color(137, 8, 137),
                        'Shoes of Vidarr (+10D +10HP)',
                        equippable=equippable_component)
                #BELT
                elif item_choice == 'leather_belt':
                    equippable_component = Equippable(EquipmentSlots.BELT,
                        defense_bonus=1)
                    item = Entity(x, y, '-', libtcod.Color(135, 94, 23),
                        'Leather Belt (+1D)', equippable=equippable_component)
                elif item_choice == 'girdle_of_brynhilder':
                    equippable_component = Equippable(EquipmentSlots.BELT,
                        defense_bonus=2, max_hp_bonus=30)
                    item = Entity(x, y, '-', libtcod.Color(20, 18, 14),
                        'Girdle of Brynhilder (+2D +30HP)',
                        equippable=equippable_component)
                elif item_choice == 'megingjord':
                    equippable_component = Equippable(EquipmentSlots.BELT,
                        defense_bonus=5, power_bonus=10, max_hp_bonus=10)
                    item = Entity(x, y, '-', libtcod.Color(90, 90, 90),
                        'Megingjord (+5D +10P +10HP)',
                        equippable=equippable_component)
                #RINGS
                elif item_choice == 'space_stone':
                    equippable_component = Equippable(EquipmentSlots.RING_1,
                        defense_bonus=1, power_bonus=1, max_hp_bonus=5)
                    item = Entity(x, y, '*', libtcod.Color(35, 188, 212),
                        'Space Stone (+1D +1P +5HP)',
                        equippable=equippable_component)
                elif item_choice == 'mind_stone':
                    equippable_component = Equippable(EquipmentSlots.RING_2,
                        defense_bonus=2, power_bonus=2, max_hp_bonus=5)
                    item = Entity(x, y, '*', libtcod.Color(238, 224, 30),
                        'Mind Stone (+2D +2P +8HP)', equippable=equippable_component)
                elif item_choice == 'reality_stone':
                    equippable_component = Equippable(EquipmentSlots.RING_3,
                        defense_bonus=4, power_bonus=4, max_hp_bonus=10)
                    item = Entity(x, y, '*', libtcod.Color(223, 22, 22),
                        'Reality Stone (+4D +4P +10HP)',
                        equippable=equippable_component)
                elif item_choice == 'power_stone':
                    equippable_component = Equippable(EquipmentSlots.RING_4,
                        defense_bonus=6, power_bonus=6, max_hp_bonus=12)
                    item = Entity(x, y, '*', libtcod.Color(118, 19, 168),
                        'Power Stone (+6D +6P +12HP)',
                        equippable=equippable_component)
                elif item_choice == 'time_stone':
                    equippable_component = Equippable(EquipmentSlots.RING_5,
                        defense_bonus=7, power_bonus=7, max_hp_bonus=14)
                    item = Entity(x, y, '*', libtcod.Color(19, 168, 39),
                        'Time Stone (+7D +7P +14HP)',
                        equippable=equippable_component)
                elif item_choice == 'soul_stone':
                    equippable_component = Equippable(EquipmentSlots.RING_6,
                        defense_bonus=8, power_bonus=8, max_hp_bonus=16)
                    item = Entity(x, y, '*', libtcod.Color(218, 149, 46),
                        'Soul Stone (+8D +8P +16HP)',
                        equippable=equippable_component)
                #OFF_HAND
                elif item_choice == 'wooden_shield':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND,
                        defense_bonus=1)
                    item = Entity(x, y, ']', libtcod.Color(65, 43, 9),
                        'Wooden Shield (+1D)', equippable=equippable_component)
                elif item_choice == 'sturdy_shield':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND,
                        defense_bonus=2)
                    item = Entity(x, y, ']', libtcod.Color(50, 40, 50),
                        'Sturdy Shield (+2D)', equippable=equippable_component)
                elif item_choice == 'dwarven_shield':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND,
                        defense_bonus=4, max_hp_bonus=6)
                    item = Entity(x, y, ']', libtcod.Color(35, 49, 119),
                        'Dwarven Shield (+4D +6HP)', equippable=equippable_component)
                elif item_choice == 'jotun_shield':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND,
                        defense_bonus=5, power_bonus=8)
                    item = Entity(x, y, ']', libtcod.Color(88, 115, 214),
                        'Jotun Shield (+5D +8P)', equippable=equippable_component)
                elif item_choice == 'shield_of_hel':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND,
                        defense_bonus=8, power_bonus=2, max_hp_bonus=10)
                    item = Entity(x, y, ']', libtcod.Color(165, 25, 40),
                        'Shield of Hel (+8D +2P +10HP)',
                        equippable=equippable_component)
                elif item_choice == 'ullrs_shield':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND,
                        defense_bonus=10)
                    item = Entity(x, y, ']', libtcod.Color(65, 155, 77),
                        'Ullr\'s Shield (+10D)', equippable=equippable_component)
                elif item_choice == 'svallin':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND,
                        defense_bonus=14, power_bonus=10, max_hp_bonus=15)
                    item = Entity(x, y, ']', libtcod.Color(123, 148, 39),
                        'Svallin (+14D +10P +15HP)', equippable=equippable_component)
                #MAIN_HAND
                elif item_choice == 'iron_sword':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
                        power_bonus=3)
                    item = Entity(x, y, '/', libtcod.Color(97, 101, 82),
                        'Iron Sword (+3P)', equippable=equippable_component)
                elif item_choice == 'berserker_sword':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
                        power_bonus=4)
                    item = Entity(x, y, '/', libtcod.Color(50, 50, 50),
                        'Berserker Sword (+4P)', equippable=equippable_component)
                elif item_choice == 'dwarven_axe':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
                        power_bonus=5, max_hp_bonus=5)
                    item = Entity(x, y, '/', libtcod.Color(54, 61, 119),
                        'Dwarven Axe (+5P +5HP)', equippable=equippable_component)
                elif item_choice == 'viking_halberd':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
                        power_bonus=6)
                    item = Entity(x, y, '/', libtcod.Color(155, 85, 111),
                        'Viking Halberd (+6P)', equippable=equippable_component)
                elif item_choice == 'laevateinn':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
                        power_bonus=7, defense_bonus=2)
                    item = Entity(x, y, '/', libtcod.Color(38, 218, 233),
                        'Laevateinn (+7P +2D)', equippable=equippable_component)
                elif item_choice == 'dainsleif':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
                        power_bonus=8, max_hp_bonus=10)
                    item = Entity(x, y, '/', libtcod.Color(25, 144, 25),
                        'Dainsleif (+8P +10HP)', equippable=equippable_component)
                elif item_choice == 'skofnung':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
                        power_bonus=10)
                    item = Entity(x, y, '/', libtcod.Color(32, 24, 38),
                        'Skofnung (+10P)', equippable=equippable_component)
                elif item_choice == 'hrotti':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
                        power_bonus=12)
                    item = Entity(x, y, '/', libtcod.Color(176, 192, 110),
                        'Hrotti (+12P)', equippable=equippable_component)
                elif item_choice == 'ridill':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
                        power_bonus=4, defense_bonus=6, max_hp_bonus=30)
                    item = Entity(x, y, '/', libtcod.Color(206, 206, 206),
                        'Ridill (+4P +6D +30HP)', equippable=equippable_component)
                elif item_choice == 'gram':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
                        power_bonus=15, max_hp_bonus=15)
                    item = Entity(x, y, '/', libtcod.Color(109, 72, 125),
                        'Gram (+15P +15HP)', equippable=equippable_component)
                elif item_choice == 'mistilteinn':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
                        power_bonus=14, defense_bonus=10, max_hp_bonus=30)
                    item = Entity(x, y, '/', libtcod.Color(40, 172, 35),
                        'Mistilteinn (+14P +10D +30HP)', equippable=equippable_component)
                elif item_choice == 'gungnir':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
                        power_bonus=20, defense_bonus=10)
                    item = Entity(x, y, '/', libtcod.Color(5, 5, 5),
                        'Gungnir (+20P +10D)', equippable=equippable_component)
                elif item_choice == 'tyrfing':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
                        power_bonus=20, max_hp_bonus=50)
                    item = Entity(x, y, '/', libtcod.Color(139, 152, 25),
                        'Tyrfing (+20P +50HP)', equippable=equippable_component)
                elif item_choice == 'mjolnir':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
                        power_bonus=35)
                    item = Entity(x, y, '/', libtcod.Color(235, 245, 0),
                        'Mjolnir (+35P)', equippable=equippable_component)
                #Scrolls
                elif item_choice == 'confusion_scroll':
                    item_component = Item(use_function=cast_confuse, targeting=True,
                        targeting_message=Message(
                        'Left-click an enemy to confuse it, or right-click to cancel.',
                        libtcod.light_cyan))
                    item = Entity(x, y, '#', libtcod.light_pink, 'Confusion Scroll',
                        render_order=RenderOrder.ITEM, item=item_component)
                elif item_choice == 'lightning_scroll':
                    item_component = Item(use_function=cast_lightning, damage=40,
                        maximum_range=5)
                    item = Entity(x, y, '#', libtcod.yellow, 'Lightning Scroll',
                        render_order=RenderOrder.ITEM, item=item_component)
                elif item_choice == 'fireball_scroll':
                    item_component = Item(use_function=cast_fireball, targeting=True,
                        targeting_message=Message(
                        'Left-click a target tile for the fireball, or right-click to cancel.',
                        libtcod.light_cyan), damage=25, radius=3)
                    item = Entity(x, y, '#', libtcod.red, 'Fireball Scroll',
                        render_order=RenderOrder.ITEM, item=item_component)
                elif item_choice == 'mistletoe':
                    item_component = Item(use_function=cast_mistletoe, damage=100,
                        maximum_range=15)
                    item = Entity(x, y, '#', libtcod.Color(40, 172, 35),
                        'Mistletoe Scroll', render_order=RenderOrder.ITEM,
                        item=item_component)
                else:
                    item_component = Item(use_function=cast_ragnarok, targeting=True,
                        targeting_message=Message(
                        'Left-click a target tile for Ragnarok, or right-click to cancel.',
                        libtcod.light_cyan), damage=500, radius=20)
                    item = Entity(x, y, '#', libtcod.Color(5, 5, 5), 'Scroll of Ragnarok',
                        render_order=RenderOrder.ITEM, item=item_component)

                entities.append(item)

    def is_blocked(self, x, y):
        '''
        Checks if (x,y) is blocked
        '''
        if self.tiles[x][y].blocked:
            return True

        return False

    def next_floor(self, player, message_log, constants):
        '''
        Creates and goes to next floor in dungeon
        '''
        self.dungeon_level += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'],
                    constants['room_max_size'], constants['map_width'],
                    constants['map_height'], player, entities)

        # heals player by half their max health
        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message(
            'You take a moment to rest, and recover your strength.',
            libtcod.light_violet))

        return entities
