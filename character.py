def upgrade_characters(characters_data):
    for character in characters_data:
        character['level'] = 90
        character['max_level'] = 90
        character['ascension'] = 6
        character['talent_1'] = 9
        character['talent_2'] = 9
        character['talent_3'] = 9
