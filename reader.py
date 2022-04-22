import math
from collections import defaultdict

from artifact import Artifact

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
        slot_key = artifact['slotKey']
        artifact_data[slot_key].append(Artifact(artifact))

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
    for artifact in artifacts_data[artifact_type]:
        if artifact.location == character_name:
            return artifact

    return None


def get_artifact_set_by_character(artifacts_data, character_name):
    artifacts = {
        'flower': get_artifact_piece_by_character(artifacts_data, 'flower', character_name),
        'plume': get_artifact_piece_by_character(artifacts_data, 'plume', character_name),
        'sands': get_artifact_piece_by_character(artifacts_data, 'sands', character_name),
        'goblet': get_artifact_piece_by_character(artifacts_data, 'goblet', character_name),
        'circlet': get_artifact_piece_by_character(artifacts_data, 'circlet', character_name)
    }

    return artifacts


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


def get_character_build_by_name(characters_data, weapons_data, artifacts_data, character_name):
    character_build = {
        'character': get_character_by_name(characters_data, character_name),
        'weapon': get_weapon_by_character(weapons_data, character_name),
        'artifacts': get_artifact_set_by_character(artifacts_data, character_name)
    }

    return character_build


def get_team_build(characters_data, weapons_data, artifacts_data, team_list):
    team_info = [get_character_build_by_name(characters_data, weapons_data, artifacts_data, name)
                 for name in team_list]

    return team_info


def get_team_vector(characters_data, weapons_data, artifacts_data, team_list):
    character_length = 6
    quant_character = len(team_list)
    team_vector = [0] * (character_length * quant_character)

    for i, character_name in enumerate(team_list):
        weapon_type = character_weapon_type_map[character_name]
        for j, weapon in enumerate(weapons_data[weapon_type]):
            if weapon['location'] == character_name:
                team_vector[i * character_length] = j
                break

        for j, artifact_type in enumerate(['flower', 'plume', 'sands', 'goblet', 'circlet']):
            for k, artifact in enumerate(artifacts_data[artifact_type]):
                if artifact.location == character_name:
                    team_vector[i * character_length + j + 1] = k
                    break

    return team_vector


def get_team_build_by_vector(characters_data, weapons_data, artifacts_data, team_list, equipment_vector):
    weapons_types = [character_weapon_type_map[name] for name in team_list]
    weapons_options = [weapons_data[weapon_type] for weapon_type in weapons_types]

    team_info = []
    for i, name in enumerate(team_list):
        team_info.append({
            'character': get_character_by_name(characters_data, name),
            'weapon': weapons_options[i][equipment_vector[i*6 + 0]],
            'artifacts': {
                'flower': artifacts_data['flower'][equipment_vector[i*6 + 1]],
                'plume': artifacts_data['plume'][equipment_vector[i*6 + 2]],
                'sands': artifacts_data['sands'][equipment_vector[i*6 + 3]],
                'goblet': artifacts_data['goblet'][equipment_vector[i*6 + 4]],
                'circlet': artifacts_data['circlet'][equipment_vector[i*6 + 5]]
            }
        })
    return team_info


def get_equipment_vector_quant_options(weapons_data, artifacts_data, team_list):
    weapons_types = [character_weapon_type_map[name] for name in team_list]
    artifacts_quant_options = [
        len(artifacts_data['flower']),
        len(artifacts_data['plume']),
        len(artifacts_data['sands']),
        len(artifacts_data['goblet']),
        len(artifacts_data['circlet']),
    ]

    quant_options = []
    for i, weapon_type in enumerate(weapons_types):
        quant_options.append(len(weapons_data[weapon_type]))
        quant_options.extend(artifacts_quant_options)

    return quant_options


def get_equipment_vector_weighted_options(data, actions, team_gradient):
    characters_data, weapons_data, artifacts_data = data

    equipments_score = []

    for i, weights in enumerate(team_gradient):
        normalized_weights = defaultdict(int)
        weights_max = max(weights.values())
        for key, value in weights.items():
            normalized_weights[key] = value / weights_max

        weapon_type = character_weapon_type_map[actions['team'][i]]
        equipments_score.append([1 for _ in weapons_data[weapon_type]])

        for artifacts in artifacts_data.values():
            scores = [artifact.calculate_score(normalized_weights) for artifact in artifacts]
            equipments_score.append(scores)

    return equipments_score


def validate_team(team_list, equipment_vector):
    character_length = 6

    used_equipments = set()
    for i, character_name in enumerate(team_list):
        weapon_type = character_weapon_type_map[character_name]

        weapon_key = (weapon_type, equipment_vector[i * character_length])
        if weapon_key in used_equipments:
            return False
        used_equipments.add(weapon_key)

        for j in range(1, character_length):
            artifact_key = (j, equipment_vector[i * character_length + j])
            if artifact_key in used_equipments:
                return False
            used_equipments.add(artifact_key)

    return True
