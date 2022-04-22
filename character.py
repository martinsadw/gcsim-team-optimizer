class Character:
    def __init__(self, character, character_id):
        self.id = character_id
        self.level = character['level']
        self.ascension = character['ascension']
        self.max_level = (20 + self.ascension * 20) if self.ascension <= 1 else (40 + (self.ascension - 1) * 10)
        self.constellation = character['constellation']
        self.talent_1 = character['talent']['auto']
        self.talent_2 = character['talent']['skill']
        self.talent_3 = character['talent']['burst']
        self.key = character['key']

    def upgrade(self):
        self.level = 90
        self.max_level = 90
        self.ascension = 6
        self.talent_1 = 9
        self.talent_2 = 9
        self.talent_3 = 9

    @staticmethod
    def upgrade_characters(characters_data):
        for character in characters_data:
            character.upgrade()

    @staticmethod
    def add_character(characters_data, character_name, constellation=0):
        characters_data.append(Character({
            'level': 90,
            'ascension': 6,
            'constellation': constellation,
            'talent': {
                'auto': 9,
                'skill': 9,
                'burst': 9,
            },
            'key': character_name
        }, len(characters_data)))
