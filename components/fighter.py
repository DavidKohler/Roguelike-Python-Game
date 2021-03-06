import libtcodpy as libtcod

from game_messages import Message

class Fighter:
    '''
    Basic component of any combative entity (including player)
    '''
    def __init__(self, hp, defense, power, xp=0, coin=0):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.xp = xp
        self.coin = coin

    def add_coin(self, coin):
        '''
        Adds coins
        '''
        self.coin += coin

    @property
    def defense(self):
        '''
        Computes defense after bonuses
        '''
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus

    @property
    def max_hp(self):
        '''
        Computes HP after bonuses
        '''
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def power(self):
        '''
        Computes power after bonuses
        '''
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0

        return self.base_power + bonus

    def attack(self, target):
        '''
        Attacks a target
        '''
        results = []

        damage = self.power - target.fighter.defense

        if damage > 0:
            results.append({'message': Message(
                '{0} attacks {1} for {2} hit points.'.format(self.owner.name.capitalize(),
                target.name, str(damage)), libtcod.white)})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message(
                '{0} attacks {1} but does no damage.'.format(self.owner.name.capitalize(),
                target.name), libtcod.white)})

        return results

    def heal(self, amount):
        '''
        Heals self, some amount
        '''
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def take_damage(self, amount):
        '''
        Takes damage, checks for death, xp, and coins
        '''
        results = []
        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp, 'coin': self.coin})

        return results
