from weapon_data import weapon_type_map


class Weapon:
    def __init__(self, weapon, weapon_id):
        self.id = weapon_id
        self.level = weapon['level']
        self.ascension = weapon['ascension']
        self.max_level = (20 + self.ascension * 20) if self.ascension <= 1 else (40 + (self.ascension - 1) * 10)
        self.refinement = weapon['refinement']
        self.key = weapon['key']
        self.type = weapon_type_map[weapon['key']]
        self.location = weapon['location']

    def upgrade(self):
        self.level = 90
        self.max_level = 90
        self.ascension = 6

    @staticmethod
    def upgrade_weapons(weapons_data):
        for weapons_type in weapons_data.values():
            for weapon in weapons_type:
                weapon.upgrade()
