import libtcodpy as libtcod

from components.ai import BasicMonster
from components.equipment import EquipmentSlots
from components.equippable import Equippable
from components.fighter import Fighter
from components.item import Item
from components.stairs import Stairs

from entity import Entity

from game_messages import Message

from item_functions import cast_confuse, cast_fireball, cast_lightning, heal

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
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def create_room(self, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width,
            map_height, player, entities):
        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

        for r in range(max_rooms):
            # random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # "Rect" class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break

            else:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                self.create_room(new_room)

                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                center_of_last_room_x = new_x
                center_of_last_room_y = new_y

                if num_rooms == 0:
                    # this is the first room, where the player starts at
                    player.x = new_x
                    player.y = new_y
                else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin (random number that is either 0 or 1)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room, entities)
                # finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>',
            libtcod.white, 'Stairs', render_order=RenderOrder.STAIRS,
            stairs=stairs_component)
        entities.append(down_stairs)

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities):
        max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [5, 6]],
            self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1, 1], [2, 4]], self.dungeon_level)
        number_of_items = randint(0, max_items_per_room)
        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)

        monster_chances = {
            'orc': 80,
            'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]],
                self.dungeon_level)
        }

        item_chances = {
            #HELMET
            'light_helm': from_dungeon_level([[5, 2], [0, 6]], self.dungeon_level),
            'medium_helm': from_dungeon_level([[5, 6], [0, 10]], self.dungeon_level),
            'dwarven_helm': from_dungeon_level([[5, 10], [0, 15]], self.dungeon_level),
            'valkyrie_helm': from_dungeon_level([[5, 15], [0, 20]], self.dungeon_level),
            'helm_of_awe': from_dungeon_level([[5, 25]], self.dungeon_level),
            'hulidshjalmr': from_dungeon_level([[4, 30]], self.dungeon_level),
            #CHESTPLATE
            'leather_chestplate': from_dungeon_level([[5, 2], [0, 6]], self.dungeon_level),
            'chainmail': from_dungeon_level([[5, 5], [0, 10]], self.dungeon_level),
            'dwarven_chestplate': from_dungeon_level([[5, 9], [0, 15]], self.dungeon_level),
            'falcon_cloak': from_dungeon_level([[5, 12], [0, 20]], self.dungeon_level),
            'tarnkappe': from_dungeon_level([[5, 20]], self.dungeon_level),
            'golden_coat': from_dungeon_level([[4, 25]], self.dungeon_level),
            #LEGGINGS
            'light_leggings': from_dungeon_level([[5, 2], [0, 5]], self.dungeon_level),
            'chain_leggings': from_dungeon_level([[5, 6], [0, 12]], self.dungeon_level),
            'dwarven_leggings': from_dungeon_level([[5, 12], [0, 18]], self.dungeon_level),
            'leggings_of_baldur': from_dungeon_level([[5, 20]], self.dungeon_level),
            'leggings_of_odin': from_dungeon_level([[4, 30]], self.dungeon_level),
            #BOOTS
            'light_boots': from_dungeon_level([[5, 2], [0, 5]], self.dungeon_level),
            'timbs': from_dungeon_level([[5, 5]], self.dungeon_level),
            'steel_boots': from_dungeon_level([[5, 6], [0, 12]], self.dungeon_level),
            'dwarven_boots': from_dungeon_level([[5, 11], [0, 17]], self.dungeon_level),
            'helskor': from_dungeon_level([[5, 20]], self.dungeon_level),
            'shoes_of_vidarr': from_dungeon_level([[4, 25]], self.dungeon_level),
            #BELT
            'leather_belt': from_dungeon_level([[5, 2], [0, 7]], self.dungeon_level),
            'girdle_of_brynhilder': from_dungeon_level([[5, 7], [0, 20]], self.dungeon_level),
            'megingjord': from_dungeon_level([[5, 20]], self.dungeon_level),
            #RINGS
            'space_stone': from_dungeon_level([[3, 2]], self.dungeon_level),
            'mind_stone': from_dungeon_level([[3, 6]], self.dungeon_level),
            'reality_stone': from_dungeon_level([[3, 12]], self.dungeon_level),
            'power_stone': from_dungeon_level([[3, 20]], self.dungeon_level),
            'time_stone': from_dungeon_level([[3, 25]], self.dungeon_level),
            'soul_stone': from_dungeon_level([[3, 30]], self.dungeon_level),
            #OFF_HAND
            'wooden_shield': from_dungeon_level([[15, 4], [0, 10]], self.dungeon_level),
            'sturdy_shield': from_dungeon_level([[15, 10], [0, 14]], self.dungeon_level),
            'dwarven_shield': from_dungeon_level([[10, 14], [0, 18]], self.dungeon_level),
            'jotun_shield': from_dungeon_level([[10, 18], [0, 20]], self.dungeon_level),
            'shield_of_hel': from_dungeon_level([[7, 20], [0, 25]], self.dungeon_level),
            'ullrs_shield': from_dungeon_level([[5, 25]], self.dungeon_level),
            'svallin': from_dungeon_level([[3, 30]], self.dungeon_level),
            #MAIN_HAND
            'iron_sword': from_dungeon_level([[10, 4], [0, 8]], self.dungeon_level),
            'berserker_sword': from_dungeon_level([[10, 7], [0, 11]], self.dungeon_level),
            'dwarven_axe': from_dungeon_level([[7, 10], [0, 14]], self.dungeon_level),
            'viking_halberd': from_dungeon_level([[5, 12], [0, 15]], self.dungeon_level),
            'laevateinn': from_dungeon_level([[5, 8], [0, 12]], self.dungeon_level),
            'dainsleif': from_dungeon_level([[4, 12], [0, 18]], self.dungeon_level),
            'skofnung': from_dungeon_level([[4, 15], [0, 20]], self.dungeon_level),
            'hrotti': from_dungeon_level([[3, 20], [0, 27]], self.dungeon_level),
            'ridill': from_dungeon_level([[3, 20], [0, 27]], self.dungeon_level),
            'gram': from_dungeon_level([[3, 25], [0, 32]], self.dungeon_level),
            'mistilteinn': from_dungeon_level([[3, 25], [0, 35]], self.dungeon_level),
            'gungnir': from_dungeon_level([[3, 30]], self.dungeon_level),
            'tyrfing': from_dungeon_level([[3, 30]], self.dungeon_level),
            'mjolnir': from_dungeon_level([[1, 30]], self.dungeon_level),
            #POTION
            's_healing_potion': from_dungeon_level([[40, 1], [0, 20]], self.dungeon_level),
            'm_healing_potion': from_dungeon_level([[25, 15], [0, 30]], self.dungeon_level),
            'l_healing_potion': from_dungeon_level([[20, 25]], self.dungeon_level),
            'full_healing_salve': from_dungeon_level([[10, 30]], self.dungeon_level),
            #SCROLL
            'confusion_scroll': from_dungeon_level([[10, 2]], self.dungeon_level),
            'lightning_scroll': from_dungeon_level([[20, 5]], self.dungeon_level),
            'fireball_scroll': from_dungeon_level([[20, 9]], self.dungeon_level),
            'mistletoe': from_dungeon_level([[10, 14]], self.dungeon_level),
            'ragnarok': from_dungeon_level([[8, 20]], self.dungeon_level)
        }

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and \
                    entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)
                if monster_choice == 'orc':
                    fighter_component = Fighter(hp=20, defense=0, power=3, xp=35)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'o', libtcod.Color(14, 27, 112), 'Orc',
                        blocks=True,render_order=RenderOrder.ACTOR,
                        fighter=fighter_component, ai=ai_component)
                else:
                    fighter_component = Fighter(hp=30, defense=2, power=8, xp=100)
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

                #POTION
                if item_choice == 's_healing_potion':
                    item_component = Item(use_function=heal, amount=35)
                    item = Entity(x, y, '+', libtcod.Color(208, 15, 15),
                        'Small Healing Potion', render_order=RenderOrder.ITEM,
                        item=item_component)
                elif item_choice == 'm_healing_potion':
                    item_component = Item(use_function=heal, amount=70)
                    item = Entity(x, y, '+', libtcod.Color(220, 15, 15),
                        'Medium Healing Potion', render_order=RenderOrder.ITEM,
                        item=item_component)
                elif item_choice == 'l_healing_potion':
                    item_component = Item(use_function=heal, amount=100)
                    item = Entity(x, y, '+', libtcod.Color(240, 10, 10),
                        'Large Healing Potion', render_order=RenderOrder.ITEM,
                        item=item_component)
                elif item_choice == 'full_healing_salve':
                    item_component = Item(use_function=heal, amount=800)
                    item = Entity(x, y, '+', libtcod.Color(255, 0, 0),
                        'Full Healing Salve', render_order=RenderOrder.ITEM,
                        item=item_component)
                #HELMET
                elif item_choice == 'light_helm':
                    equippable_component = Equippable(EquipmentSlots.HELMET,
                        defense_bonus=2)
                    item = Entity(x, y, 'n', libtcod.Color(96, 98, 114),
                        'Light Helm (+2D)', equippable=equippable_component)
                elif item_choice == 'medium_helm':
                    equippable_component = Equippable(EquipmentSlots.HELMET,
                        defense_bonus=4)
                    item = Entity(x, y, 'n', libtcod.Color(100, 100, 110),
                        'Medium Helm (+4D)', equippable=equippable_component)
                elif item_choice == 'dwarven_helm':
                    equippable_component = Equippable(EquipmentSlots.HELMET,
                        defense_bonus=6, max_hp_bonus=10)
                    item = Entity(x, y, 'n', libtcod.Color(27, 35, 107),
                        'Dwarven Helm (+6D +10HP)', equippable=equippable_component)
                elif item_choice == 'valkyrie_helm':
                    equippable_component = Equippable(EquipmentSlots.HELMET,
                        defense_bonus=8, power_bonus=8)
                    item = Entity(x, y, 'n', libtcod.Color(114, 80, 13),
                        'Valkyrie Helm (+8D +8P)', equippable=equippable_component)
                elif item_choice == 'helm_of_awe':
                    equippable_component = Equippable(EquipmentSlots.HELMET,
                        defense_bonus=12, max_hp_bonus=30)
                    item = Entity(x, y, 'n', libtcod.Color(20, 77, 18),
                        'Helm of Awe (+12D +30HP)', equippable=equippable_component)
                elif item_choice == 'hulidshjalmr':
                    equippable_component = Equippable(EquipmentSlots.HELMET,
                        defense_bonus=15, power_bonus=5, max_hp_bonus=20)
                    item = Entity(x, y, 'n', libtcod.Color(164, 154, 20),
                        'Hulidshjalmr (+15D +5P +20HP)', equippable=equippable_component)
                #CHESTPLATE
                elif item_choice == 'leather_chestplate':
                    equippable_component = Equippable(EquipmentSlots.CHESTPLATE,
                        defense_bonus=2)
                    item = Entity(x, y, '#', libtcod.Color(104, 69, 7),
                        'Leather Chestplate (+2D)', equippable=equippable_component)
                elif item_choice == 'chainmail':
                        equippable_component = Equippable(EquipmentSlots.CHESTPLATE,
                            defense_bonus=4)
                        item = Entity(x, y, '#', libtcod.Color(164, 164, 164),
                            'Chainmail Chestplate (+4D)', equippable=equippable_component)
                elif item_choice == 'dwarven_chestplate':
                        equippable_component = Equippable(EquipmentSlots.CHESTPLATE,
                            defense_bonus=6, max_hp_bonus=10)
                        item = Entity(x, y, '#', libtcod.Color(41, 62, 146),
                            'Dwarven Chestplate (+6D +10HP)', equippable=equippable_component)
                elif item_choice == 'falcon_cloak':
                        equippable_component = Equippable(EquipmentSlots.CHESTPLATE,
                            defense_bonus=8)
                        item = Entity(x, y, '#', libtcod.Color(183, 151, 94),
                            'Falcon Cloak (+8D)', equippable=equippable_component)
                elif item_choice == 'tarnkappe':
                        equippable_component = Equippable(EquipmentSlots.CHESTPLATE,
                            defense_bonus=12, power_bonus=8, max_hp_bonus=10)
                        item = Entity(x, y, '#', libtcod.Color(54, 45, 30),
                            'Tarnkappe (+12D +8P +10HP)', equippable=equippable_component)
                elif item_choice == 'golden_coat':
                        equippable_component = Equippable(EquipmentSlots.CHESTPLATE,
                            defense_bonus=15, power_bonus=5, max_hp_bonus=20)
                        item = Entity(x, y, '#', libtcod.Color(175, 144, 18),
                            'Golden Coat of Chainmail (+15D +5P +20HP)',
                            equippable=equippable_component)
                #LEGGINGS
                elif item_choice == 'light_leggings':
                    equippable_component = Equippable(EquipmentSlots.LEGGINGS,
                        defense_bonus=2)
                    item = Entity(x, y, 'U', libtcod.Color(220, 187, 50),
                        'Light Leggings (+2D)', equippable=equippable_component)
                elif item_choice == 'chain_leggings':
                    equippable_component = Equippable(EquipmentSlots.LEGGINGS,
                        defense_bonus=4)
                    item = Entity(x, y, 'U', libtcod.Color(154, 154, 154),
                        'Chain Leggings (+4D)', equippable=equippable_component)
                elif item_choice == 'dwarven_leggings':
                    equippable_component = Equippable(EquipmentSlots.LEGGINGS,
                        defense_bonus=6, max_hp_bonus=10)
                    item = Entity(x, y, 'U', libtcod.Color(38, 51, 117),
                        'Dwarven Leggings (+6D +10HP)',
                        equippable=equippable_component)
                elif item_choice == 'leggings_of_baldur':
                    equippable_component = Equippable(EquipmentSlots.LEGGINGS,
                        defense_bonus=18, max_hp_bonus=10)
                    item = Entity(x, y, 'U', libtcod.Color(23, 98, 53),
                        'Leggings of Baldur (+18D +10HP)',
                        equippable=equippable_component)
                elif item_choice == 'leggings_of_odin':
                    equippable_component = Equippable(EquipmentSlots.LEGGINGS,
                        defense_bonus=12, power_bonus=15, max_hp_bonus=10)
                    item = Entity(x, y, 'U', libtcod.Color(152, 169, 2),
                        'Leggings of Odin (+12D +15P +10HP)',
                        equippable=equippable_component)
                #BOOTS
                elif item_choice == 'light_boots':
                    equippable_component = Equippable(EquipmentSlots.BOOTS,
                        defense_bonus=2)
                    item = Entity(x, y, 'b', libtcod.Color(149, 149, 26),
                        'Light Boots (+2D)', equippable=equippable_component)
                elif item_choice == 'timbs':
                    equippable_component = Equippable(EquipmentSlots.BOOTS,
                        power_bonus=30)
                    item = Entity(x, y, 'b', libtcod.Color(149, 104, 26),
                        'Fresh Timbs (+30P)', equippable=equippable_component)
                elif item_choice == 'steel_boots':
                    equippable_component = Equippable(EquipmentSlots.BOOTS,
                        defense_bonus=5)
                    item = Entity(x, y, 'b', libtcod.Color(100, 100, 100),
                        'Steel Boots (+5D)', equippable=equippable_component)
                elif item_choice == 'dwarven_boots':
                    equippable_component = Equippable(EquipmentSlots.BOOTS,
                        defense_bonus=6, max_hp_bonus=10)
                    item = Entity(x, y, 'b', libtcod.Color(32, 32, 112),
                        'Dwarven Boots (+6D +10HP)', equippable=equippable_component)
                elif item_choice == 'helskor':
                    equippable_component = Equippable(EquipmentSlots.BOOTS,
                        defense_bonus=10, max_hp_bonus=15)
                    item = Entity(x, y, 'b', libtcod.Color(137, 29, 8),
                        'Helskor (+10D +15HP)', equippable=equippable_component)
                elif item_choice == 'shoes_of_vidarr':
                    equippable_component = Equippable(EquipmentSlots.BOOTS,
                        defense_bonus=20, max_hp_bonus=10)
                    item = Entity(x, y, 'b', libtcod.Color(137, 8, 137),
                        'Shoes of Vidarr (+20D +10HP)',
                        equippable=equippable_component)
                #BELT
                elif item_choice == 'leather_belt':
                    equippable_component = Equippable(EquipmentSlots.BELT,
                        defense_bonus=2)
                    item = Entity(x, y, '-', libtcod.Color(135, 94, 23),
                        'Leather Belt (+2D)', equippable=equippable_component)
                elif item_choice == 'girdle_of_brynhilder':
                    equippable_component = Equippable(EquipmentSlots.BELT,
                        defense_bonus=2, max_hp_bonus=30)
                    item = Entity(x, y, '-', libtcod.Color(20, 18, 14),
                        'Girdle of Brynhilder (+2D +30HP)',
                        equippable=equippable_component)
                elif item_choice == 'megingjord':
                    equippable_component = Equippable(EquipmentSlots.BELT,
                        defense_bonus=8, power_bonus=15, max_hp_bonus=8)
                    item = Entity(x, y, '-', libtcod.Color(90, 90, 90),
                        'Megingjord (+8D +15P +8HP)',
                        equippable=equippable_component)
                #RINGS
                elif item_choice == 'space_stone':
                    equippable_component = Equippable(EquipmentSlots.RING_1,
                        defense_bonus=5, power_bonus=5, max_hp_bonus=5)
                    item = Entity(x, y, '*', libtcod.Color(35, 188, 212),
                        'Space Stone (+5D +5P +5HP)',
                        equippable=equippable_component)
                elif item_choice == 'mind_stone':
                    equippable_component = Equippable(EquipmentSlots.RING_2,
                        defense_bonus=5, power_bonus=5, max_hp_bonus=5)
                    item = Entity(x, y, '*', libtcod.Color(238, 224, 30),
                        'Mind Stone (+8D +8P +8HP)', equippable=equippable_component)
                elif item_choice == 'reality_stone':
                    equippable_component = Equippable(EquipmentSlots.RING_3,
                        defense_bonus=10, power_bonus=10, max_hp_bonus=10)
                    item = Entity(x, y, '*', libtcod.Color(223, 22, 22),
                        'Reality Stone (+10D +10P +10HP)',
                        equippable=equippable_component)
                elif item_choice == 'power_stone':
                    equippable_component = Equippable(EquipmentSlots.RING_4,
                        defense_bonus=12, power_bonus=12, max_hp_bonus=12)
                    item = Entity(x, y, '*', libtcod.Color(118, 19, 168),
                        'Power Stone (+12D +12P +12HP)',
                        equippable=equippable_component)
                elif item_choice == 'time_stone':
                    equippable_component = Equippable(EquipmentSlots.RING_5,
                        defense_bonus=14, power_bonus=14, max_hp_bonus=14)
                    item = Entity(x, y, '*', libtcod.Color(19, 168, 39),
                        'Time Stone (+14D +14P +14HP)',
                        equippable=equippable_component)
                elif item_choice == 'soul_stone':
                    equippable_component = Equippable(EquipmentSlots.RING_6,
                        defense_bonus=16, power_bonus=16, max_hp_bonus=16)
                    item = Entity(x, y, '*', libtcod.Color(218, 149, 46),
                        'Soul Stone (+16D +16P +16HP)',
                        equippable=equippable_component)
                #OFF_HAND
                elif item_choice == 'wooden_shield':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND,
                        defense_bonus=2)
                    item = Entity(x, y, ']', libtcod.Color(65, 43, 9),
                        'Wooden Shield (+2D)', equippable=equippable_component)
                elif item_choice == 'sturdy_shield':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND,
                        defense_bonus=4)
                    item = Entity(x, y, ']', libtcod.Color(50, 40, 50),
                        'Sturdy Shield (+4D)', equippable=equippable_component)
                elif item_choice == 'dwarven_shield':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND,
                        defense_bonus=6, max_hp_bonus=6)
                    item = Entity(x, y, ']', libtcod.Color(35, 49, 119),
                        'Dwarven Shield (+6D +6HP)', equippable=equippable_component)
                elif item_choice == 'jotun_shield':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND,
                        defense_bonus=8, power_bonus=8)
                    item = Entity(x, y, ']', libtcod.Color(88, 115, 214),
                        'Jotun Shield (+8D +8P)', equippable=equippable_component)
                elif item_choice == 'shield_of_hel':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND,
                        defense_bonus=10, power_bonus=2, max_hp_bonus=10)
                    item = Entity(x, y, ']', libtcod.Color(165, 25, 40),
                        'Shield of Hel (+10D +2P +10HP)',
                        equippable=equippable_component)
                elif item_choice == 'ullrs_shield':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND,
                        defense_bonus=15)
                    item = Entity(x, y, ']', libtcod.Color(65, 155, 77),
                        'Ullr\'s Shield (+15D)', equippable=equippable_component)
                elif item_choice == 'svallin':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND,
                        defense_bonus=15, power_bonus=10, max_hp_bonus=15)
                    item = Entity(x, y, ']', libtcod.Color(123, 148, 39),
                        'Svallin (+15D +10P +15HP)', equippable=equippable_component)
                #MAIN_HAND
                elif item_choice == 'iron_sword':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
                        power_bonus=4)
                    item = Entity(x, y, '/', libtcod.Color(97, 101, 82),
                        'Iron Sword (+4P)', equippable=equippable_component)
                elif item_choice == 'berserker_sword':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
                        power_bonus=5)
                    item = Entity(x, y, '/', libtcod.Color(50, 50, 50),
                        'Berserker Sword (+5P)', equippable=equippable_component)
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
                        power_bonus=11)
                    item = Entity(x, y, '/', libtcod.Color(32, 24, 38),
                        'Skofnung (+11P)', equippable=equippable_component)
                elif item_choice == 'hrotti':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
                        power_bonus=15)
                    item = Entity(x, y, '/', libtcod.Color(176, 192, 110),
                        'Hrotti (+15P)', equippable=equippable_component)
                elif item_choice == 'ridill':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
                        power_bonus=4, defense_bonus=4, max_hp_bonus=30)
                    item = Entity(x, y, '/', libtcod.Color(206, 206, 206),
                        'Ridill (+4P +4D +30HP)', equippable=equippable_component)
                elif item_choice == 'gram':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
                        power_bonus=15, max_hp_bonus=15)
                    item = Entity(x, y, '/', libtcod.Color(109, 72, 125),
                        'Gram (+15P +15HP)', equippable=equippable_component)
                elif item_choice == 'mistilteinn':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
                        power_bonus=10, defense_bonus=10, max_hp_bonus=30)
                    item = Entity(x, y, '/', libtcod.Color(40, 172, 35),
                        'Mistilteinn (+10P +10D +30HP)', equippable=equippable_component)
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
                        'Left-click an enemy to confuse it, or right-click to \
                        cancel.', libtcod.light_cyan))
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
                        'Left-click a target tile for the fireball, or right-click\
                         to cancel.', libtcod.light_cyan), damage=25, radius=3)
                    item = Entity(x, y, '#', libtcod.red, 'Fireball Scroll',
                        render_order=RenderOrder.ITEM, item=item_component)
                elif item_choice == 'mistletoe':
                    item_component = Item(use_function=cast_lightning, damage=100,
                        maximum_range=15)
                    item = Entity(x, y, '#', libtcod.Color(40, 172, 35),
                        'Mistletoe Scroll', render_order=RenderOrder.ITEM,
                        item=item_component)
                else:
                    item_component = Item(use_function=cast_fireball, targeting=True,
                        targeting_message=Message('Left-click a target tile for \
                        the casting, or right-click to cancel.',
                        libtcod.light_cyan), damage=100, radius=5)
                    item = Entity(x, y, '#', libtcod.Color(5, 5, 5), 'Ragnarok',
                        render_order=RenderOrder.ITEM, item=item_component)

                entities.append(item)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

    def next_floor(self, player, message_log, constants):
        self.dungeon_level += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'],
                    constants['room_max_size'], constants['map_width'],
                    constants['map_height'], player, entities)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover \
            your strength.', libtcod.light_violet))

        return entities
