def upgrade_characters(characters_data):
    for character in characters_data:
        character['level'] = 90
        character['max_level'] = 90
        character['ascension'] = 6
        character['talent_1'] = 9
        character['talent_2'] = 9
        character['talent_3'] = 9


def add_character(characters_data, character_name, constellation=0):
    characters_data.append({
        'id': 0,
        'level': 90,
        'max_level': 90,
        'ascension': 6,
        'constellation': constellation,
        'talent_1': 9,
        'talent_2': 9,
        'talent_3': 9,
        'key': character_name
    })