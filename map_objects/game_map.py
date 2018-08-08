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

from map_objects.item_descriptions import get_item
from map_objects.monster_descriptions import get_monster
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

                else:
                    # all rooms after the first
                    # connect to previous room with tunnels

                    if num_rooms == 1 and (randint(0, 2) == 1):
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

                        shopkeep_component = Shopkeep(True)
                        inventory_component = Inventory(25)
                        shopkeeper = Entity(new_x, new_y, '$', libtcod.Color(5, 5, 5),
                            'Shopkeeper', blocks=True,render_order=RenderOrder.SHOPKEEP,
                            shopkeep=shopkeep_component, inventory=inventory_component)

                        shopkeep_inventory = ['s_healing_potion', 'm_healing_potion',
                        'l_healing_potion','full_healing_salve', 'valkyrie_helm',
                        'hulidshjalmr', 'falcon_cloak', 'golden_coat', 'dwarven_leggings',
                        'leggings_of_odin', 'dwarven_boots', 'shoes_of_vidarr',
                        'megingjord', 'shield_of_hel', 'svallin', 'hrotti',
                        'dainsleif', 'tyrfing', 'gungnir', 'mjolnir',
                        'confusion_scroll', 'lightning_scroll', 'fireball_scroll',
                        'mistletoe', 'ragnarok']

                        for item in shopkeep_inventory:
                            item = get_item(item, 0, 0)
                            shopkeeper.inventory.add_item(item)

                        entities.append(shopkeeper)

                    else:
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
        max_monsters_per_room = from_dungeon_level([[2, 1], [3, 12], [4, 25]],
            self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1, 1], [2, 10], [3, 20],
            [4, 30], [5, 40]], self.dungeon_level)
        number_of_items = randint(0, max_items_per_room)
        number_of_monsters = randint(0, max_monsters_per_room)

        monster_chances = {
            'draugr': from_dungeon_level([[7, 1], [0, 10]], self.dungeon_level),
            'draugrV2': from_dungeon_level([[7, 5], [0, 20]], self.dungeon_level),
            'draugrV3': from_dungeon_level([[7, 15], [0, 30]], self.dungeon_level),
            'draugrV4': from_dungeon_level([[7, 25], [0, 40]], self.dungeon_level),
            'fire_draugr': from_dungeon_level([[6, 10], [0, 20]], self.dungeon_level),
            'fire_draugrV2': from_dungeon_level([[6, 20], [0, 30]], self.dungeon_level),
            'fire_draugrV3': from_dungeon_level([[6, 30], [0, 40]], self.dungeon_level),
            'fire_draugrV4': from_dungeon_level([[6, 40]], self.dungeon_level),
            'frost_draugr': from_dungeon_level([[5, 15], [0, 25]], self.dungeon_level),
            'frost_draugrV2': from_dungeon_level([[5, 25], [0, 35]], self.dungeon_level),
            'frost_draugrV3': from_dungeon_level([[5, 35], [0, 40]], self.dungeon_level),
            'frost_draugrV4': from_dungeon_level([[5, 40]], self.dungeon_level),
            'troll': from_dungeon_level([[5, 5], [0, 15]], self.dungeon_level),
            'trollV2': from_dungeon_level([[5, 15], [0, 25]], self.dungeon_level),
            'fire_troll': from_dungeon_level([[4, 14], [0, 25]], self.dungeon_level),
            'fire_trollV2': from_dungeon_level([[4, 25], [0, 35]], self.dungeon_level),
            'frost_troll': from_dungeon_level([[3, 25], [0, 35]], self.dungeon_level),
            'frost_trollV2': from_dungeon_level([[3, 35]], self.dungeon_level),
            'brunnmigi': from_dungeon_level([[4, 15], [0, 25]], self.dungeon_level),
            'fylgja': from_dungeon_level([[5, 22], [0, 32]], self.dungeon_level),
            'valkyrie': from_dungeon_level([[4, 28], [0, 38]], self.dungeon_level),
            'lindworm': from_dungeon_level([[5, 28], [0, 34]], self.dungeon_level),
            'fire_lindworm': from_dungeon_level([[3, 34], [0, 40]], self.dungeon_level),
            'frost_lindworm': from_dungeon_level([[3, 40]], self.dungeon_level),
            'vatnaevattir': from_dungeon_level([[5, 33], [0, 42]], self.dungeon_level),
            'jotunn': from_dungeon_level([[3, 40]], self.dungeon_level)
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
            'space_stone': from_dungeon_level([[3, 2], [0, 10]], self.dungeon_level),
            'mind_stone': from_dungeon_level([[3, 8], [0, 18]], self.dungeon_level),
            'reality_stone': from_dungeon_level([[3, 16], [0, 26]], self.dungeon_level),
            'power_stone': from_dungeon_level([[3, 24], [0, 32]], self.dungeon_level),
            'time_stone': from_dungeon_level([[3, 30], [0, 40]], self.dungeon_level),
            'soul_stone': from_dungeon_level([[3, 36]], self.dungeon_level),
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
            's_healing_potion': from_dungeon_level([[40, 1], [50, 10], [0, 15]], self.dungeon_level),
            'm_healing_potion': from_dungeon_level([[40, 15], [50, 20], [0, 30]], self.dungeon_level),
            'l_healing_potion': from_dungeon_level([[35, 30], [40, 35]], self.dungeon_level),
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
                monster = get_monster(monster_choice, x, y)
                entities.append(monster)

        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and \
                    entity.y == y]):
                item_choice = random_choice_from_dict(item_chances)
                item = get_item(item_choice, x, y)
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
