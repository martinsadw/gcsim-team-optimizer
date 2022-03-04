import math

from artifact_data import percent_stats
from character_data import character_weapon_type_map
from weapon_data import weapon_type_map


def read_artifacts(good_data):
    artifact_data = {
        'flower': [],
        'plume': [],
        'sands': [],
        'goblet': [],
        'circlet': []
    }

    for artifact in good_data['artifacts']:
        new_artifact = {
            'id': artifact['Id'],
            'level': artifact['level'],
            'set_key': artifact['setKey'],
            'main_stat_key': artifact['mainStatKey'],
            'sub_stats': {},
            'empty_sub_stats': 0,
            'missing_sub_stats': math.ceil((20 - artifact['level']) / 4),
            'location': artifact['location']
        }
        for sub_stat in artifact['substats']:
            if sub_stat['key'] is None:
                new_artifact['empty_sub_stats'] += 1
            elif sub_stat['key'] in percent_stats:
                new_artifact['sub_stats'][sub_stat['key']] = sub_stat['value'] / 100
            else:
                new_artifact['sub_stats'][sub_stat['key']] = sub_stat['value']

        artifact_data[artifact['slotKey']].append(new_artifact)

    return artifact_data


def read_weapons(good_data):
    weapon_data = {
        'bow': [],
        'catalyst': [],
        'polearm': [],
        'claymore': [],
        'sword': []
    }

    for weapon_id, weapon in enumerate(good_data['weapons']):
        ascension = weapon['ascension']
        max_level = (20 + ascension * 20) if ascension <= 1 else (40 + (ascension - 1) * 10)
        new_weapon = {
            'id': weapon_id,
            'level': weapon['level'],
            'max_level': max_level,
            'ascension': ascension,
            'refinement': weapon['refinement'],
            'key': weapon['key'],
            'type': weapon_type_map[weapon['key']],
            'location': weapon['location']
        }

        weapon_data[new_weapon['type']].append(new_weapon)

    return weapon_data


def read_characters(good_data):
    characters_data = []

    for character_id, character in enumerate(good_data['characters']):
        ascension = character['ascension']
        max_level = (20 + ascension * 20) if ascension <= 1 else (40 + (ascension - 1) * 10)
        new_character = {
            'id': character_id,
            'level': character['level'],
            'max_level': max_level,
            'ascension': ascension,
            'constellation': character['constellation'],
            'talent_1': character['talent']['auto'],
            'talent_2': character['talent']['skill'],
            'talent_3': character['talent']['burst'],
            'key': character['key']
        }

        characters_data.append(new_character)

    return characters_data


def get_artifact_piece_by_character(artifacts_data, artifact_type, character_name):
    # artifact_type = character_weapon_type_map[character_name]

    for artifact in artifacts_data[artifact_type]:
        if artifact['location'] == character_name:
            return artifact

    return None


def get_weapons_by_name(weapons_data, weapon_name):
    if weapon_name not in weapon_type_map:
        return []

    weapon_type = weapon_type_map[weapon_name]
    weapons = list((x for x in weapons_data[weapon_type] if x['key'] == weapon_name))

    return weapons


def get_weapon_by_character(weapons_data, character_name):
    weapon_type = character_weapon_type_map[character_name]

    for weapon in weapons_data[weapon_type]:
        if weapon['location'] == character_name:
            return weapon

    return None


def get_character_by_name(characters_data, character_name):
    character = next((x for x in characters_data if x['key'] == character_name))

    return character
