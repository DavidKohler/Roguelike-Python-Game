import libtcodpy as libtcod

from components.ai import BasicMonster
from components.fighter import Fighter

from entity import Entity

from game_messages import Message

from render_functions import RenderOrder

def get_monster(monster_choice, x, y):
    # normal orc
    if monster_choice == 'draugr':
        fighter_component = Fighter(hp=20, defense=0, power=4, xp=30, coin=10)
        ai_component = BasicMonster()

        monster = Entity(x, y, 'o', libtcod.Color(14, 27, 112), 'Draugr',
            blocks=True,render_order=RenderOrder.ACTOR,
            fighter=fighter_component, ai=ai_component)
    elif monster_choice == 'draugrV2':
        fighter_component = Fighter(hp=25, defense=1, power=9, xp=45, coin=15)
        ai_component = BasicMonster()

        monster = Entity(x, y, 'o', libtcod.Color(14, 27, 112), 'Draugr',
            blocks=True, fighter=fighter_component,
            render_order=RenderOrder.ACTOR, ai=ai_component)
    elif monster_choice == 'draugrV3':
        fighter_component = Fighter(hp=35, defense=4, power=23, xp=75, coin=20)
        ai_component = BasicMonster()

        monster = Entity(x, y, 'o', libtcod.Color(14, 27, 112), 'Draugr',
            blocks=True, fighter=fighter_component,
            render_order=RenderOrder.ACTOR, ai=ai_component)
    elif monster_choice == 'draugrV4':
        fighter_component = Fighter(hp=40, defense=10, power=58, xp=100, coin=25)
        ai_component = BasicMonster()

        monster = Entity(x, y, 'o', libtcod.Color(14, 27, 112), 'Draugr',
            blocks=True, fighter=fighter_component,
            render_order=RenderOrder.ACTOR, ai=ai_component)
    # fire orc
    elif monster_choice == 'fire_draugr':
        fighter_component = Fighter(hp=25, defense=2, power=17, xp=40, coin=15)
        ai_component = BasicMonster()

        monster = Entity(x, y, 'o', libtcod.Color(210, 26, 30), 'Fire Draugr',
            blocks=True,render_order=RenderOrder.ACTOR,
            fighter=fighter_component, ai=ai_component)
    elif monster_choice == 'fire_draugrV2':
        fighter_component = Fighter(hp=30, defense=5, power=36, xp=60, coin=20)
        ai_component = BasicMonster()

        monster = Entity(x, y, 'o', libtcod.Color(210, 26, 30), 'Fire Draugr',
            blocks=True, fighter=fighter_component,
            render_order=RenderOrder.ACTOR, ai=ai_component)
    elif monster_choice == 'fire_draugrV3':
        fighter_component = Fighter(hp=40, defense=10, power=79, xp=100, coin=25)
        ai_component = BasicMonster()

        monster = Entity(x, y, 'o', libtcod.Color(210, 26, 30), 'Fire Draugr',
            blocks=True, fighter=fighter_component,
            render_order=RenderOrder.ACTOR, ai=ai_component)
    elif monster_choice == 'fire_draugrV4':
        fighter_component = Fighter(hp=50, defense=15, power=88, xp=125, coin=30)
        ai_component = BasicMonster()

        monster = Entity(x, y, 'o', libtcod.Color(210, 26, 30), 'Fire Draugr',
            blocks=True, fighter=fighter_component,
            render_order=RenderOrder.ACTOR, ai=ai_component)
    # frost orc
    elif monster_choice == 'frost_draugr':
        fighter_component = Fighter(hp=30, defense=2, power=24, xp=50, coin=20)
        ai_component = BasicMonster()

        monster = Entity(x, y, 'o', libtcod.Color(0, 180, 255), 'Frost Draugr',
            blocks=True,render_order=RenderOrder.ACTOR,
            fighter=fighter_component, ai=ai_component)
    elif monster_choice == 'frost_draugrV2':
        fighter_component = Fighter(hp=40, defense=10, power=63, xp=80, coin=25)
        ai_component = BasicMonster()

        monster = Entity(x, y, 'o', libtcod.Color(0, 180, 255), 'Frost Draugr',
            blocks=True, fighter=fighter_component,
            render_order=RenderOrder.ACTOR, ai=ai_component)
    elif monster_choice == 'frost_draugrV3':
        fighter_component = Fighter(hp=50, defense=17, power=88, xp=110, coin=30)
        ai_component = BasicMonster()

        monster = Entity(x, y, 'o', libtcod.Color(0, 180, 255), 'Frost Draugr',
            blocks=True, fighter=fighter_component,
            render_order=RenderOrder.ACTOR, ai=ai_component)
    elif monster_choice == 'frost_draugrV4':
        fighter_component = Fighter(hp=55, defense=25, power=95, xp=140, coin=35)
        ai_component = BasicMonster()

        monster = Entity(x, y, 'o', libtcod.Color(0, 180, 255), 'Frost Draugr',
            blocks=True, fighter=fighter_component,
            render_order=RenderOrder.ACTOR, ai=ai_component)
    # normal troll
    elif monster_choice == 'troll':
        fighter_component = Fighter(hp=50, defense=0, power=13, xp=70, coin=20)
        ai_component = BasicMonster()

        monster = Entity(x, y, 'T', libtcod.darker_green, 'Troll',
            blocks=True, fighter=fighter_component,
            render_order=RenderOrder.ACTOR, ai=ai_component)
    elif monster_choice == 'trollV2':
        fighter_component = Fighter(hp=75, defense=1, power=28, xp=120, coin=35)
        ai_component = BasicMonster()

        monster = Entity(x, y, 'T', libtcod.darker_green, 'Troll',
            blocks=True, fighter=fighter_component,
            render_order=RenderOrder.ACTOR, ai=ai_component)
    # fire troll
    elif monster_choice == 'fire_troll':
        fighter_component = Fighter(hp=50, defense=1, power=23, xp=150, coin=40)
        ai_component = BasicMonster()

        monster = Entity(x, y, 'T', libtcod.Color(210, 26, 30), 'Fire Troll',
            blocks=True, fighter=fighter_component,
            render_order=RenderOrder.ACTOR, ai=ai_component)
    elif monster_choice == 'fire_trollV2':
        fighter_component = Fighter(hp=80, defense=6, power=65, xp=200, coin=60)
        ai_component = BasicMonster()

        monster = Entity(x, y, 'T', libtcod.Color(210, 26, 30), 'Fire Troll',
            blocks=True, fighter=fighter_component,
            render_order=RenderOrder.ACTOR, ai=ai_component)
    # frost troll
    elif monster_choice == 'frost_troll':
        fighter_component = Fighter(hp=100, defense=5, power=69, xp=200, coin=70)
        ai_component = BasicMonster()

        monster = Entity(x, y, 'T', libtcod.Color(0, 180, 255), 'Frost Troll',
            blocks=True, fighter=fighter_component,
            render_order=RenderOrder.ACTOR, ai=ai_component)
    elif monster_choice == 'frost_trollV2':
        fighter_component = Fighter(hp=150, defense=12, power=97, xp=300, coin=90)
        ai_component = BasicMonster()

        monster = Entity(x, y, 'T', libtcod.Color(0, 180, 255), 'Frost Troll',
            blocks=True, fighter=fighter_component,
            render_order=RenderOrder.ACTOR, ai=ai_component)
    # brunnmigi
    elif monster_choice == 'brunnmigi':
        fighter_component = Fighter(hp=50, defense=2, power=26, xp=170, coin=40)
        ai_component = BasicMonster()

        monster = Entity(x, y, chr(135), libtcod.Color(210, 148, 22), 'Brunnmigi',
            blocks=True,render_order=RenderOrder.ACTOR,
            fighter=fighter_component, ai=ai_component)
    # fylgja
    elif monster_choice == 'fylgja':
        fighter_component = Fighter(hp=65, defense=5, power=37, xp=200, coin=70)
        ai_component = BasicMonster()

        monster = Entity(x, y, chr(133), libtcod.Color(255, 255, 255), 'Fylgja',
            blocks=True,render_order=RenderOrder.ACTOR,
            fighter=fighter_component, ai=ai_component)
    # valkyrie
    elif monster_choice == 'valkyrie':
        fighter_component = Fighter(hp=100, defense=10, power=76, xp=300, coin=90)
        ai_component = BasicMonster()

        monster = Entity(x, y, chr(237), libtcod.Color(80, 60, 30), 'Valkyrie',
            blocks=True,render_order=RenderOrder.ACTOR,
            fighter=fighter_component, ai=ai_component)
    # lindworm
    elif monster_choice == 'lindworm':
        fighter_component = Fighter(hp=160, defense=8, power=57, xp=340, coin=100)
        ai_component = BasicMonster()

        monster = Entity(x, y, '~', libtcod.Color(0, 0, 0), 'Lindworm',
            blocks=True,render_order=RenderOrder.ACTOR,
            fighter=fighter_component, ai=ai_component)
    elif monster_choice == 'fire_lindworm':
        fighter_component = Fighter(hp=200, defense=10, power=86, xp=600, coin=200)
        ai_component = BasicMonster()

        monster = Entity(x, y, '~', libtcod.Color(210, 26, 30), 'Fire Lindworm',
            blocks=True,render_order=RenderOrder.ACTOR,
            fighter=fighter_component, ai=ai_component)
    elif monster_choice == 'frost_lindworm':
        fighter_component = Fighter(hp=200, defense=10, power=108, xp=800, coin=250)
        ai_component = BasicMonster()

        monster = Entity(x, y, '~', libtcod.Color(0, 180, 255), 'Frost Lindworm',
            blocks=True,render_order=RenderOrder.ACTOR,
            fighter=fighter_component, ai=ai_component)
    # vatnaevattir
    elif monster_choice == 'vatnaevattir':
        fighter_component = Fighter(hp=200, defense=0, power=78, xp=300, coin=250)
        ai_component = BasicMonster()

        monster = Entity(x, y, chr(131), libtcod.Color(0, 34, 144), 'Vatnaevattir',
            blocks=True,render_order=RenderOrder.ACTOR,
            fighter=fighter_component, ai=ai_component)
    #jotunn
    elif monster_choice == 'jotunn':
        fighter_component = Fighter(hp=200, defense=8, power=130, xp=1000, coin=400)
        ai_component = BasicMonster()

        monster = Entity(x, y, chr(215), libtcod.Color(0, 180, 255), 'Jotunn',
            blocks=True,render_order=RenderOrder.ACTOR,
            fighter=fighter_component, ai=ai_component)

    return monster
