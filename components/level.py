class Level:
    '''
    Component that tracks level and xp
    '''
    def __init__(self, current_level=1, current_xp=0, level_up_base=200, level_up_factor=150):
        self.current_level = current_level
        self.current_xp = current_xp
        self.level_up_base = level_up_base
        self.level_up_factor = level_up_factor

    def add_xp(self, xp):
        '''
        Adds xp
        '''
        self.current_xp += xp

        if self.current_xp > self.experience_to_next_level:
            self.current_xp -= self.experience_to_next_level
            self.current_level += 1

            return True
        else:
            return False

    @property
    def experience_to_next_level(self):
        '''
        Computes experience needed to next level up
        '''
        return self.level_up_base + self.current_level * self.level_up_factor
