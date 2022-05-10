import numpy as np


EQUIPMENT_ID = {
    'weapon': 0,
    'flower': 1,
    'plume': 2,
    'sands': 3,
    'goblet': 4,
    'circlet': 5,
}


def get_equipments_mask(equipment_lock, team):
    quant_characters = len(team)
    character_length = len(EQUIPMENT_ID.keys())
    equipments_mask = np.zeros((quant_characters * character_length,), dtype=bool)
    for character, slots in equipment_lock.items():
        try:
            char_index = team.index(character)
        except ValueError:
            continue

        for slot in slots:
            slot_index = EQUIPMENT_ID[slot]
            equip_index = character_length * char_index + slot_index
            equipments_mask[equip_index] = True

    return equipments_mask


def get_character_mask(character_lock, team):
    quant_characters = len(team)
    character_mask = np.zeros((quant_characters,), dtype=bool)
    for character in character_lock:
        try:
            char_index = team.index(character)
        except ValueError:
            continue

        character_mask[char_index] = True

    return character_mask
