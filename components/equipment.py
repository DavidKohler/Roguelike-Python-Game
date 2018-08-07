from equipment_slots import EquipmentSlots

class Equipment:
    '''
    Equipment component to apply bonuses from items
    '''
    def __init__(self, main_hand=None, off_hand=None, chestplate=None, leggings=None,
            helmet=None, boots=None, belt=None, ring_1=None, ring_2=None, ring_3=None,
            ring_4=None, ring_5=None, ring_6=None):
        self.main_hand = main_hand
        self.off_hand = off_hand
        self.chestplate = chestplate
        self.leggings = leggings
        self.helmet = helmet
        self.boots = boots
        self.belt = belt
        self.ring_1 = ring_1
        self.ring_2 = ring_2
        self.ring_3 = ring_3
        self.ring_4 = ring_4
        self.ring_5 = ring_5
        self.ring_6 = ring_6

    @property
    def defense_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.defense_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.defense_bonus

        if self.chestplate and self.chestplate.equippable:
            bonus += self.chestplate.equippable.defense_bonus

        if self.leggings and self.leggings.equippable:
            bonus += self.leggings.equippable.defense_bonus

        if self.helmet and self.helmet.equippable:
            bonus += self.helmet.equippable.defense_bonus

        if self.boots and self.boots.equippable:
            bonus += self.boots.equippable.defense_bonus

        if self.belt and self.belt.equippable:
            bonus += self.belt.equippable.defense_bonus

        if self.ring_1 and self.ring_1.equippable:
            bonus += self.ring_1.equippable.defense_bonus

        if self.ring_2 and self.ring_2.equippable:
            bonus += self.ring_2.equippable.defense_bonus

        if self.ring_3 and self.ring_3.equippable:
            bonus += self.ring_3.equippable.defense_bonus

        if self.ring_4 and self.ring_4.equippable:
            bonus += self.ring_4.equippable.defense_bonus

        if self.ring_5 and self.ring_5.equippable:
            bonus += self.ring_5.equippable.defense_bonus

        if self.ring_6 and self.ring_6.equippable:
            bonus += self.ring_6.equippable.defense_bonus

        return bonus

    @property
    def max_hp_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.max_hp_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.max_hp_bonus

        if self.chestplate and self.chestplate.equippable:
            bonus += self.chestplate.equippable.max_hp_bonus

        if self.leggings and self.leggings.equippable:
            bonus += self.leggings.equippable.max_hp_bonus

        if self.helmet and self.helmet.equippable:
            bonus += self.helmet.equippable.max_hp_bonus

        if self.boots and self.boots.equippable:
            bonus += self.boots.equippable.max_hp_bonus

        if self.belt and self.belt.equippable:
            bonus += self.belt.equippable.max_hp_bonus

        if self.ring_1 and self.ring_1.equippable:
            bonus += self.ring_1.equippable.max_hp_bonus

        if self.ring_2 and self.ring_2.equippable:
            bonus += self.ring_2.equippable.max_hp_bonus

        if self.ring_3 and self.ring_3.equippable:
            bonus += self.ring_3.equippable.max_hp_bonus

        if self.ring_4 and self.ring_4.equippable:
            bonus += self.ring_4.equippable.max_hp_bonus

        if self.ring_5 and self.ring_5.equippable:
            bonus += self.ring_5.equippable.max_hp_bonus

        if self.ring_6 and self.ring_6.equippable:
            bonus += self.ring_6.equippable.max_hp_bonus

        return bonus

    @property
    def power_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.power_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.power_bonus

        if self.chestplate and self.chestplate.equippable:
            bonus += self.chestplate.equippable.power_bonus

        if self.leggings and self.leggings.equippable:
            bonus += self.leggings.equippable.power_bonus

        if self.helmet and self.helmet.equippable:
            bonus += self.helmet.equippable.power_bonus

        if self.boots and self.boots.equippable:
            bonus += self.boots.equippable.power_bonus

        if self.belt and self.belt.equippable:
            bonus += self.belt.equippable.power_bonus

        if self.ring_1 and self.ring_1.equippable:
            bonus += self.ring_1.equippable.power_bonus

        if self.ring_2 and self.ring_2.equippable:
            bonus += self.ring_2.equippable.power_bonus

        if self.ring_3 and self.ring_3.equippable:
            bonus += self.ring_3.equippable.power_bonus

        if self.ring_4 and self.ring_4.equippable:
            bonus += self.ring_4.equippable.power_bonus

        if self.ring_5 and self.ring_5.equippable:
            bonus += self.ring_5.equippable.power_bonus

        if self.ring_6 and self.ring_6.equippable:
            bonus += self.ring_6.equippable.power_bonus

        return bonus

    def toggle_equip(self, equippable_entity):
        results = []

        slot = equippable_entity.equippable.slot

        if slot == EquipmentSlots.MAIN_HAND:
            if self.main_hand == equippable_entity:
                self.main_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.main_hand:
                    results.append({'dequipped': self.main_hand})

                self.main_hand = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.OFF_HAND:
            if self.off_hand == equippable_entity:
                self.off_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.off_hand:
                    results.append({'dequipped': self.off_hand})

                self.off_hand = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.CHESTPLATE:
            if self.chestplate == equippable_entity:
                self.chestplate = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.chestplate:
                    results.append({'dequipped': self.chestplate})

                self.chestplate = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.LEGGINGS:
            if self.leggings == equippable_entity:
                self.leggings = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.leggings:
                    results.append({'dequipped': self.leggings})

                self.leggings = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.HELMET:
            if self.helmet == equippable_entity:
                self.helmet = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.helmet:
                    results.append({'dequipped': self.helmet})

                self.helmet = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.BOOTS:
            if self.boots == equippable_entity:
                self.boots = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.boots:
                    results.append({'dequipped': self.boots})

                self.boots = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.BELT:
            if self.belt == equippable_entity:
                self.belt = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.belt:
                    results.append({'dequipped': self.belt})

                self.belt = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.RING_1:
            if self.ring_1 == equippable_entity:
                self.ring_1 = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.ring_1:
                    results.append({'dequipped': self.ring_1})

                self.ring_1 = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.RING_2:
            if self.ring_2 == equippable_entity:
                self.ring_2 = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.ring_2:
                    results.append({'dequipped': self.ring_2})

                self.ring_2 = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.RING_3:
            if self.ring_3 == equippable_entity:
                self.ring_3 = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.ring_3:
                    results.append({'dequipped': self.ring_3})

                self.ring_3 = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.RING_4:
            if self.ring_4 == equippable_entity:
                self.ring_4 = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.ring_4:
                    results.append({'dequipped': self.ring_4})

                self.ring_4 = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.RING_5:
            if self.ring_5 == equippable_entity:
                self.ring_5 = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.ring_5:
                    results.append({'dequipped': self.ring_5})

                self.ring_5 = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.RING_6:
            if self.ring_6 == equippable_entity:
                self.ring_6 = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.ring_6:
                    results.append({'dequipped': self.ring_6})

                self.ring_6 = equippable_entity
                results.append({'equipped': equippable_entity})

        return results
