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

    def __repr__(self):
        return f'Character(id={self.id}, level={self.level}, ascension={self.ascension},' \
               f'constellation={self.constellation}, talent_1={self.talent_1}, talent_2={self.talent_2},' \
               f'talent_3={self.talent_3}, key={self.key})'
