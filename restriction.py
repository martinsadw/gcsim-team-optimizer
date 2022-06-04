import numpy as np

import artifact_data
from character_data import character_weapon_type_map


def get_equipments_mask(team, equipment_lock):
    quant_characters = len(team)
    character_length = len(artifact_data.EQUIPMENT_ID.keys())
    equipments_mask = np.zeros((quant_characters * character_length,), dtype=bool)
    for character, slots in equipment_lock.items():
        try:
            char_index = team.index(character)
        except ValueError:
            continue

        for slot in slots:
            slot_index = artifact_data.EQUIPMENT_ID[slot]
            equip_index = character_length * char_index + slot_index
            equipments_mask[equip_index] = True

    return equipments_mask


def get_character_mask(team, character_lock):
    quant_characters = len(team)
    character_mask = np.zeros((quant_characters,), dtype=bool)
    for character in character_lock:
        try:
            char_index = team.index(character)
        except ValueError:
            continue

        character_mask[char_index] = True

    return character_mask


def get_stat_subset(team, character_lock=None, equipment_lock=None):
    stat_subset = []
    goblet_stats = {'physical_dmg_', 'anemo_dmg_', 'geo_dmg_', 'electro_dmg_', 'hydro_dmg_', 'pyro_dmg_', 'cryo_dmg_'}
    circlet_stats = {'heal_'}
    for i, character in enumerate(team):
        if character in character_lock:
            continue

        stats = set(artifact_data.ATTRIBUTE_LIST)
        if character in equipment_lock:
            if 'goblet' in equipment_lock[character]:
                stats -= goblet_stats
            if 'circlet' in equipment_lock[character]:
                stats -= circlet_stats
        stat_subset.extend([(i, stat_key) for stat_key in stats])

    return stat_subset


def validate_equipments(equipment_vector, team):
    penalty = 1
    penalty *= check_repeated_equipment(equipment_vector, team)

    return penalty


def check_repeated_equipment(equipment_vector, team):
    character_length = len(artifact_data.EQUIPMENT_ID.keys())
    used_equipments = set()
    for i, character_name in enumerate(team):
        weapon_type = character_weapon_type_map[character_name]

        weapon_key = (weapon_type, equipment_vector[i * character_length])
        if weapon_key in used_equipments:
            return 0
        used_equipments.add(weapon_key)

        for j in range(1, character_length):
            artifact_key = (j, equipment_vector[i * character_length + j])
            if artifact_key in used_equipments:
                return 0
            used_equipments.add(artifact_key)

    return 1
