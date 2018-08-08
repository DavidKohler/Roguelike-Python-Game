from random import randint

def from_dungeon_level(table, dungeon_level):
    '''
    Allows random selection weights to change based on dungeon level
    '''
    for (value, level) in reversed(table):
        if dungeon_level >= level:
            return value

    return 0

def random_choice_index(chances):
    '''
    Creates index and total of random choices
    '''
    random_chance = randint(1, sum(chances))

    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w

        if random_chance <= running_sum:
            return choice
        choice += 1


def random_choice_from_dict(choice_dict):
    '''
    Chooses random choice from passed in dictionary
    '''
    choices = list(choice_dict.keys())
    chances = list(choice_dict.values())

    return choices[random_choice_index(chances)]
