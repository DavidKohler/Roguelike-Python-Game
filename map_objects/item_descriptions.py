import libtcodpy as libtcod

from components.cashable import Cashable
from components.equipment import EquipmentSlots
from components.equippable import Equippable
from components.item import Item

from entity import Entity

from game_messages import Message

from item_functions import cast_confuse, cast_fireball, cast_lightning, cast_mistletoe, cast_ragnarok, heal

from render_functions import RenderOrder

def get_item(item_choice, x, y):
    if item_choice == 's_healing_potion':
        item_component = Item(use_function=heal, amount=35)
        cashable_component = Cashable(200)
        item = Entity(x, y, '+', libtcod.Color(208, 15, 15),
            'Small Healing Potion (+35HP)', render_order=RenderOrder.ITEM,
            item=item_component, cashable=cashable_component)
    elif item_choice == 'm_healing_potion':
        item_component = Item(use_function=heal, amount=70)
        cashable_component = Cashable(600)
        item = Entity(x, y, '+', libtcod.Color(220, 15, 15),
            'Medium Healing Potion (+70HP)', render_order=RenderOrder.ITEM,
            item=item_component, cashable=cashable_component)
    elif item_choice == 'l_healing_potion':
        item_component = Item(use_function=heal, amount=100)
        cashable_component = Cashable(1000)
        item = Entity(x, y, '+', libtcod.Color(240, 10, 10),
            'Large Healing Potion (+100HP)', render_order=RenderOrder.ITEM,
            item=item_component, cashable=cashable_component)
    elif item_choice == 'full_healing_salve':
        item_component = Item(use_function=heal, amount=800)
        cashable_component = Cashable(2000)
        item = Entity(x, y, '+', libtcod.Color(255, 0, 0),
            'Full Healing Salve', render_order=RenderOrder.ITEM,
            item=item_component, cashable=cashable_component)
    #HELMET
    elif item_choice == 'light_helm':
        equippable_component = Equippable(EquipmentSlots.HELMET,
            defense_bonus=1)
        cashable_component = Cashable(100)
        item = Entity(x, y, 'n', libtcod.Color(96, 98, 114),
            'Light Helm (+1D)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'medium_helm':
        equippable_component = Equippable(EquipmentSlots.HELMET,
            defense_bonus=2)
        cashable_component = Cashable(500)
        item = Entity(x, y, 'n', libtcod.Color(100, 100, 110),
            'Medium Helm (+2D)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'dwarven_helm':
        equippable_component = Equippable(EquipmentSlots.HELMET,
            defense_bonus=4, max_hp_bonus=10)
        cashable_component = Cashable(1000)
        item = Entity(x, y, 'n', libtcod.Color(27, 35, 107),
            'Dwarven Helm (+4D +10HP)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'valkyrie_helm':
        equippable_component = Equippable(EquipmentSlots.HELMET,
            defense_bonus=6, power_bonus=6)
        cashable_component = Cashable(2000)
        item = Entity(x, y, 'n', libtcod.Color(114, 80, 13),
            'Valkyrie Helm (+6D +6P)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'helm_of_awe':
        equippable_component = Equippable(EquipmentSlots.HELMET,
            defense_bonus=8, max_hp_bonus=30)
        cashable_component = Cashable(4000)
        item = Entity(x, y, 'n', libtcod.Color(20, 77, 18),
            'Helm of Awe (+8D +30HP)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'hulidshjalmr':
        equippable_component = Equippable(EquipmentSlots.HELMET,
            defense_bonus=12, power_bonus=5, max_hp_bonus=20)
        cashable_component = Cashable(6000)
        item = Entity(x, y, 'n', libtcod.Color(164, 154, 20),
            'Hulidshjalmr (+12D +5P +20HP)', equippable=equippable_component,
            cashable=cashable_component)
    #CHESTPLATE
    elif item_choice == 'leather_chestplate':
        equippable_component = Equippable(EquipmentSlots.CHESTPLATE,
            defense_bonus=1)
        cashable_component = Cashable(100)
        item = Entity(x, y, 'W', libtcod.Color(104, 69, 7),
            'Leather Chestplate (+1D)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'chainmail':
            equippable_component = Equippable(EquipmentSlots.CHESTPLATE,
                defense_bonus=2)
            cashable_component = Cashable(500)
            item = Entity(x, y, 'W', libtcod.Color(164, 164, 164),
                'Chainmail Chestplate (+2D)', equippable=equippable_component,
                cashable=cashable_component)
    elif item_choice == 'dwarven_chestplate':
            equippable_component = Equippable(EquipmentSlots.CHESTPLATE,
                defense_bonus=4, max_hp_bonus=10)
            cashable_component = Cashable(1000)
            item = Entity(x, y, 'W', libtcod.Color(41, 62, 146),
                'Dwarven Chestplate (+4D +10HP)', equippable=equippable_component,
                cashable=cashable_component)
    elif item_choice == 'falcon_cloak':
            equippable_component = Equippable(EquipmentSlots.CHESTPLATE,
                defense_bonus=6)
            cashable_component = Cashable(2000)
            item = Entity(x, y, 'W', libtcod.Color(183, 151, 94),
                'Falcon Cloak (+6D)', equippable=equippable_component,
                cashable=cashable_component)
    elif item_choice == 'tarnkappe':
            equippable_component = Equippable(EquipmentSlots.CHESTPLATE,
                defense_bonus=8, power_bonus=6, max_hp_bonus=10)
            cashable_component = Cashable(4000)
            item = Entity(x, y, 'W', libtcod.Color(54, 45, 30),
                'Tarnkappe (+8D +6P +10HP)', equippable=equippable_component,
                cashable=cashable_component)
    elif item_choice == 'golden_coat':
            equippable_component = Equippable(EquipmentSlots.CHESTPLATE,
                defense_bonus=12, power_bonus=5, max_hp_bonus=20)
            cashable_component = Cashable(6000)
            item = Entity(x, y, 'W', libtcod.Color(175, 144, 18),
                'Golden Coat of Chainmail (+12D +5P +20HP)',
                equippable=equippable_component, cashable=cashable_component)
    #LEGGINGS
    elif item_choice == 'light_leggings':
        equippable_component = Equippable(EquipmentSlots.LEGGINGS,
            defense_bonus=1)
        cashable_component = Cashable(100)
        item = Entity(x, y, 'U', libtcod.Color(220, 187, 50),
            'Light Leggings (+1D)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'chain_leggings':
        equippable_component = Equippable(EquipmentSlots.LEGGINGS,
            defense_bonus=2)
        cashable_component = Cashable(500)
        item = Entity(x, y, 'U', libtcod.Color(154, 154, 154),
            'Chain Leggings (+2D)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'dwarven_leggings':
        equippable_component = Equippable(EquipmentSlots.LEGGINGS,
            defense_bonus=4, max_hp_bonus=10)
        cashable_component = Cashable(1000)
        item = Entity(x, y, 'U', libtcod.Color(38, 51, 117),
            'Dwarven Leggings (+4D +10HP)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'leggings_of_baldur':
        equippable_component = Equippable(EquipmentSlots.LEGGINGS,
            defense_bonus=6, max_hp_bonus=10)
        cashable_component = Cashable(2000)
        item = Entity(x, y, 'U', libtcod.Color(23, 98, 53),
            'Leggings of Baldur (+6D +10HP)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'leggings_of_odin':
        equippable_component = Equippable(EquipmentSlots.LEGGINGS,
            defense_bonus=10, power_bonus=6, max_hp_bonus=10)
        cashable_component = Cashable(5000)
        item = Entity(x, y, 'U', libtcod.Color(152, 169, 2),
            'Leggings of Odin (+10D +6P +10HP)', equippable=equippable_component,
            cashable=cashable_component)
    #BOOTS
    elif item_choice == 'light_boots':
        equippable_component = Equippable(EquipmentSlots.BOOTS,
            defense_bonus=1)
        cashable_component = Cashable(100)
        item = Entity(x, y, 'b', libtcod.Color(149, 149, 26),
            'Light Boots (+1D)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'timbs':
        equippable_component = Equippable(EquipmentSlots.BOOTS,
            power_bonus=-10, defense_bonus=-10, max_hp_bonus=50)
        cashable_component = Cashable(50)
        item = Entity(x, y, 'b', libtcod.Color(149, 104, 26),
            'Fresh Timbs (-10P -10D +50HP)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'steel_boots':
        equippable_component = Equippable(EquipmentSlots.BOOTS,
            defense_bonus=2)
        cashable_component = Cashable(500)
        item = Entity(x, y, 'b', libtcod.Color(100, 100, 100),
            'Steel Boots (+2D)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'dwarven_boots':
        equippable_component = Equippable(EquipmentSlots.BOOTS,
            defense_bonus=4, max_hp_bonus=10)
        cashable_component = Cashable(1000)
        item = Entity(x, y, 'b', libtcod.Color(32, 32, 112),
            'Dwarven Boots (+4D +10HP)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'helskor':
        equippable_component = Equippable(EquipmentSlots.BOOTS,
            defense_bonus=6, max_hp_bonus=15)
        cashable_component = Cashable(2000)
        item = Entity(x, y, 'b', libtcod.Color(137, 29, 8),
            'Helskor (+6D +15HP)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'shoes_of_vidarr':
        equippable_component = Equippable(EquipmentSlots.BOOTS,
            defense_bonus=10, max_hp_bonus=10)
        cashable_component = Cashable(5000)
        item = Entity(x, y, 'b', libtcod.Color(137, 8, 137),
            'Shoes of Vidarr (+10D +10HP)', equippable=equippable_component,
            cashable=cashable_component)
    #BELT
    elif item_choice == 'leather_belt':
        equippable_component = Equippable(EquipmentSlots.BELT,
            defense_bonus=1)
        cashable_component = Cashable(100)
        item = Entity(x, y, '-', libtcod.Color(135, 94, 23),
            'Leather Belt (+1D)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'girdle_of_brynhilder':
        equippable_component = Equippable(EquipmentSlots.BELT,
            defense_bonus=2, max_hp_bonus=30)
        cashable_component = Cashable(500)
        item = Entity(x, y, '-', libtcod.Color(20, 18, 14),
            'Girdle of Brynhilder (+2D +30HP)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'megingjord':
        equippable_component = Equippable(EquipmentSlots.BELT,
            defense_bonus=5, power_bonus=10, max_hp_bonus=10)
        cashable_component = Cashable(2000)
        item = Entity(x, y, '-', libtcod.Color(90, 90, 90),
            'Megingjord (+5D +10P +10HP)', equippable=equippable_component,
            cashable=cashable_component)
    #RINGS
    elif item_choice == 'space_stone':
        equippable_component = Equippable(EquipmentSlots.RING_1,
            defense_bonus=1, power_bonus=1, max_hp_bonus=5)
        cashable_component = Cashable(1000)
        item = Entity(x, y, '*', libtcod.Color(35, 188, 212),
            'Space Stone (+1D +1P +5HP)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'mind_stone':
        equippable_component = Equippable(EquipmentSlots.RING_2,
            defense_bonus=2, power_bonus=2, max_hp_bonus=5)
        cashable_component = Cashable(2000)
        item = Entity(x, y, '*', libtcod.Color(238, 224, 30),
            'Mind Stone (+2D +2P +8HP)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'reality_stone':
        equippable_component = Equippable(EquipmentSlots.RING_3,
            defense_bonus=4, power_bonus=4, max_hp_bonus=10)
        cashable_component = Cashable(3000)
        item = Entity(x, y, '*', libtcod.Color(223, 22, 22),
            'Reality Stone (+4D +4P +10HP)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'power_stone':
        equippable_component = Equippable(EquipmentSlots.RING_4,
            defense_bonus=6, power_bonus=6, max_hp_bonus=12)
        cashable_component = Cashable(4000)
        item = Entity(x, y, '*', libtcod.Color(118, 19, 168),
            'Power Stone (+6D +6P +12HP)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'time_stone':
        equippable_component = Equippable(EquipmentSlots.RING_5,
            defense_bonus=7, power_bonus=7, max_hp_bonus=14)
        cashable_component = Cashable(5000)
        item = Entity(x, y, '*', libtcod.Color(19, 168, 39),
            'Time Stone (+7D +7P +14HP)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'soul_stone':
        equippable_component = Equippable(EquipmentSlots.RING_6,
            defense_bonus=8, power_bonus=8, max_hp_bonus=16)
        cashable_component = Cashable(6000)
        item = Entity(x, y, '*', libtcod.Color(218, 149, 46),
            'Soul Stone (+8D +8P +16HP)', equippable=equippable_component,
            cashable=cashable_component)
    #OFF_HAND
    elif item_choice == 'wooden_shield':
        equippable_component = Equippable(EquipmentSlots.OFF_HAND,
            defense_bonus=1)
        cashable_component = Cashable(100)
        item = Entity(x, y, ']', libtcod.Color(65, 43, 9),
            'Wooden Shield (+1D)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'sturdy_shield':
        equippable_component = Equippable(EquipmentSlots.OFF_HAND,
            defense_bonus=2)
        cashable_component = Cashable(500)
        item = Entity(x, y, ']', libtcod.Color(50, 40, 50),
            'Sturdy Shield (+2D)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'dwarven_shield':
        equippable_component = Equippable(EquipmentSlots.OFF_HAND,
            defense_bonus=4, max_hp_bonus=6)
        cashable_component = Cashable(1000)
        item = Entity(x, y, ']', libtcod.Color(35, 49, 119),
            'Dwarven Shield (+4D +6HP)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'jotun_shield':
        equippable_component = Equippable(EquipmentSlots.OFF_HAND,
            defense_bonus=5, power_bonus=8)
        cashable_component = Cashable(2000)
        item = Entity(x, y, ']', libtcod.Color(88, 115, 214),
            'Jotun Shield (+5D +8P)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'shield_of_hel':
        equippable_component = Equippable(EquipmentSlots.OFF_HAND,
            defense_bonus=8, power_bonus=2, max_hp_bonus=10)
        cashable_component = Cashable(3000)
        item = Entity(x, y, ']', libtcod.Color(165, 25, 40),
            'Shield of Hel (+8D +2P +10HP)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'ullrs_shield':
        equippable_component = Equippable(EquipmentSlots.OFF_HAND,
            defense_bonus=10)
        cashable_component = Cashable(4000)
        item = Entity(x, y, ']', libtcod.Color(65, 155, 77),
            'Ullr\'s Shield (+10D)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'svallin':
        equippable_component = Equippable(EquipmentSlots.OFF_HAND,
            defense_bonus=14, power_bonus=10, max_hp_bonus=15)
        cashable_component = Cashable(5500)
        item = Entity(x, y, ']', libtcod.Color(123, 148, 39),
            'Svallin (+14D +10P +15HP)', equippable=equippable_component,
            cashable=cashable_component)
    #MAIN_HAND
    elif item_choice == 'iron_sword':
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
            power_bonus=3)
        cashable_component = Cashable(100)
        item = Entity(x, y, '/', libtcod.Color(97, 101, 82),
            'Iron Sword (+3P)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'berserker_sword':
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
            power_bonus=4)
        cashable_component = Cashable(400)
        item = Entity(x, y, '/', libtcod.Color(50, 50, 50),
            'Berserker Sword (+4P)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'dwarven_axe':
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
            power_bonus=5, max_hp_bonus=5)
        cashable_component = Cashable(800)
        item = Entity(x, y, '/', libtcod.Color(54, 61, 119),
            'Dwarven Axe (+5P +5HP)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'viking_halberd':
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
            power_bonus=6)
        cashable_component = Cashable(1200)
        item = Entity(x, y, '/', libtcod.Color(155, 85, 111),
            'Viking Halberd (+6P)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'laevateinn':
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
            power_bonus=7, defense_bonus=2)
        cashable_component = Cashable(1700)
        item = Entity(x, y, '/', libtcod.Color(38, 218, 233),
            'Laevateinn (+7P +2D)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'dainsleif':
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
            power_bonus=8, max_hp_bonus=10)
        cashable_component = Cashable(2200)
        item = Entity(x, y, '/', libtcod.Color(25, 144, 25),
            'Dainsleif (+8P +10HP)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'skofnung':
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
            power_bonus=10)
        cashable_component = Cashable(2600)
        item = Entity(x, y, '/', libtcod.Color(32, 24, 38),
            'Skofnung (+10P)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'hrotti':
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
            power_bonus=12)
        cashable_component = Cashable(3200)
        item = Entity(x, y, '/', libtcod.Color(176, 192, 110),
            'Hrotti (+12P)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'ridill':
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
            power_bonus=4, defense_bonus=6, max_hp_bonus=30)
        cashable_component = Cashable(3800)
        item = Entity(x, y, '/', libtcod.Color(206, 206, 206),
            'Ridill (+4P +6D +30HP)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'gram':
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
            power_bonus=15, max_hp_bonus=15)
        cashable_component = Cashable(4500)
        item = Entity(x, y, '/', libtcod.Color(109, 72, 125),
            'Gram (+15P +15HP)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'mistilteinn':
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
            power_bonus=14, defense_bonus=10, max_hp_bonus=30)
        cashable_component = Cashable(5000)
        item = Entity(x, y, '/', libtcod.Color(40, 172, 35),
            'Mistilteinn (+14P +10D +30HP)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'gungnir':
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
            power_bonus=20, defense_bonus=10)
        cashable_component = Cashable(6000)
        item = Entity(x, y, '/', libtcod.Color(5, 5, 5),
            'Gungnir (+20P +10D)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'tyrfing':
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
            power_bonus=20, max_hp_bonus=50)
        cashable_component = Cashable(6000)
        item = Entity(x, y, '/', libtcod.Color(139, 152, 25),
            'Tyrfing (+20P +50HP)', equippable=equippable_component,
            cashable=cashable_component)
    elif item_choice == 'mjolnir':
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND,
            power_bonus=35)
        cashable_component = Cashable(7000)
        item = Entity(x, y, '/', libtcod.Color(235, 245, 0),
            'Mjolnir (+35P)', equippable=equippable_component,
            cashable=cashable_component)
    #Scrolls
    elif item_choice == 'confusion_scroll':
        item_component = Item(use_function=cast_confuse, targeting=True,
            targeting_message=Message(
            'Left-click an enemy to confuse it, or right-click to cancel.',
            libtcod.light_cyan))
        cashable_component = Cashable(200)
        item = Entity(x, y, '#', libtcod.light_pink, 'Confusion Scroll',
            render_order=RenderOrder.ITEM, item=item_component,
            cashable=cashable_component)
    elif item_choice == 'lightning_scroll':
        item_component = Item(use_function=cast_lightning, damage=40,
            maximum_range=5)
        cashable_component = Cashable(500)
        item = Entity(x, y, '#', libtcod.yellow, 'Lightning Scroll',
            render_order=RenderOrder.ITEM, item=item_component,
            cashable=cashable_component)
    elif item_choice == 'fireball_scroll':
        item_component = Item(use_function=cast_fireball, targeting=True,
            targeting_message=Message(
            'Left-click a target tile for the fireball, or right-click to cancel.',
            libtcod.light_cyan), damage=25, radius=3)
        cashable_component = Cashable(1000)
        item = Entity(x, y, '#', libtcod.red, 'Fireball Scroll',
            render_order=RenderOrder.ITEM, item=item_component,
            cashable=cashable_component)
    elif item_choice == 'mistletoe':
        item_component = Item(use_function=cast_mistletoe, damage=100,
            maximum_range=15)
        cashable_component = Cashable(1500)
        item = Entity(x, y, '#', libtcod.Color(40, 172, 35),
            'Mistletoe Scroll', render_order=RenderOrder.ITEM,
            item=item_component, cashable=cashable_component)
    else:
        item_component = Item(use_function=cast_ragnarok, targeting=True,
            targeting_message=Message(
            'Left-click a target tile for Ragnarok, or right-click to cancel.',
            libtcod.light_cyan), damage=500, radius=20)
        cashable_component = Cashable(2500)
        item = Entity(x, y, '#', libtcod.Color(5, 5, 5), 'Scroll of Ragnarok',
            render_order=RenderOrder.ITEM, item=item_component,
            cashable=cashable_component)

    return item
