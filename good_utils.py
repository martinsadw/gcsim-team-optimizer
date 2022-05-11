from collections import defaultdict
import json

from artifact import Artifact
from character import Character
from weapon import Weapon

from character_data import character_weapon_type_map
from weapon_data import weapon_type_map


class GoodData:
    def __init__(self, good_data):
        self.good_data = good_data
        self.artifacts = self.read_artifacts(self.good_data)
        self.weapons = self.read_weapons(self.good_data)
        self.characters = self.read_characters(self.good_data)

    @classmethod
    def from_filename(cls, good_filename):
        with open(good_filename) as good_file:
            good_data = json.load(good_file)

        return cls(good_data)

    @staticmethod
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

    @staticmethod
    def read_characters(good_data):
        characters_data = []

        for character_id, character in enumerate(good_data['characters']):
            characters_data.append(Character(character, character_id))

        return characters_data

    @staticmethod
    def read_weapons(good_data):
        weapon_data = {
            'bow': [],
            'catalyst': [],
            'polearm': [],
            'claymore': [],
            'sword': []
        }

        for weapon_id, weapon in enumerate(good_data['weapons']):
            weapon_type = weapon_type_map[weapon['key']]
            weapon_data[weapon_type].append(Weapon(weapon, weapon_id))

        return weapon_data

    def upgrade_artifacts(self):
        for artifacts_piece in self.artifacts.values():
            for artifact in artifacts_piece:
                artifact.upgrade()

    def upgrade_characters(self):
        for character in self.characters:
            character.upgrade()

    def add_character(self, character_name, constellation=0):
        new_character = {
            'level': 90,
            'ascension': 6,
            'constellation': constellation,
            'talent': {
                'auto': 9,
                'skill': 9,
                'burst': 9,
            },
            'key': character_name
        }
        self.characters.append(Character(new_character, len(self.characters)))

    def upgrade_weapons(self):
        for weapons_type in self.weapons.values():
            for weapon in weapons_type:
                weapon.upgrade()

    def get_artifact_piece_by_character(self, artifact_type, character_name):
        for artifact in self.artifacts[artifact_type]:
            if artifact.location == character_name:
                return artifact

        return None

    def get_artifact_set_by_character(self, character_name):
        artifacts = {
            'flower': self.get_artifact_piece_by_character('flower', character_name),
            'plume': self.get_artifact_piece_by_character('plume', character_name),
            'sands': self.get_artifact_piece_by_character('sands', character_name),
            'goblet': self.get_artifact_piece_by_character('goblet', character_name),
            'circlet': self.get_artifact_piece_by_character('circlet', character_name)
        }

        return artifacts

    def get_weapons_by_name(self, weapon_name):
        if weapon_name not in weapon_type_map:
            return []

        weapon_type = weapon_type_map[weapon_name]
        weapons = list((x for x in self.weapons[weapon_type] if x.key == weapon_name))

        return weapons

    def get_weapon_by_character(self, character_name):
        weapon_type = character_weapon_type_map[character_name]

        for weapon in self.weapons[weapon_type]:
            if weapon.location == character_name:
                return weapon

        return None

    def get_character_by_name(self, character_name):
        character = next((x for x in self.characters if x.key == character_name))

        return character

    def get_character_build_by_name(self, character_name):
        character_build = {
            'character': self.get_character_by_name(character_name),
            'weapon': self.get_weapon_by_character(character_name),
            'artifacts': self.get_artifact_set_by_character(character_name)
        }

        return character_build

    def get_team_build(self, team_list):
        team_info = [self.get_character_build_by_name(name) for name in team_list]

        return team_info

    def get_team_vector(self, team_list):
        character_length = 6
        quant_character = len(team_list)
        team_vector = [0] * (character_length * quant_character)

        for i, character_name in enumerate(team_list):
            weapon_type = character_weapon_type_map[character_name]
            for j, weapon in enumerate(self.weapons[weapon_type]):
                if weapon.location == character_name:
                    team_vector[i * character_length] = j
                    break

            for j, artifact_type in enumerate(['flower', 'plume', 'sands', 'goblet', 'circlet']):
                for k, artifact in enumerate(self.artifacts[artifact_type]):
                    if artifact.location == character_name:
                        team_vector[i * character_length + j + 1] = k
                        break

        return team_vector

    def get_team_build_by_vector(self, team_list, equipment_vector):
        weapons_types = [character_weapon_type_map[name] for name in team_list]
        weapons_options = [self.weapons[weapon_type] for weapon_type in weapons_types]

        team_info = []
        for i, name in enumerate(team_list):
            team_info.append({
                'character': self.get_character_by_name(name),
                'weapon': weapons_options[i][equipment_vector[i*6 + 0]],
                'artifacts': {
                    'flower': self.artifacts['flower'][equipment_vector[i*6 + 1]],
                    'plume': self.artifacts['plume'][equipment_vector[i*6 + 2]],
                    'sands': self.artifacts['sands'][equipment_vector[i*6 + 3]],
                    'goblet': self.artifacts['goblet'][equipment_vector[i*6 + 4]],
                    'circlet': self.artifacts['circlet'][equipment_vector[i*6 + 5]]
                }
            })
        return team_info

    def get_equipment_vector_quant_options(self, team_list):
        weapons_types = [character_weapon_type_map[name] for name in team_list]
        artifacts_quant_options = [
            len(self.artifacts['flower']),
            len(self.artifacts['plume']),
            len(self.artifacts['sands']),
            len(self.artifacts['goblet']),
            len(self.artifacts['circlet']),
        ]

        quant_options = []
        for i, weapon_type in enumerate(weapons_types):
            quant_options.append(len(self.weapons[weapon_type]))
            quant_options.extend(artifacts_quant_options)

        return quant_options

    def get_equipment_vector_weighted_options(self, team_list, team_gradient):
        equipments_score = []

        for i, weights in enumerate(team_gradient):
            normalized_weights = defaultdict(int)
            if len(weights.values()) > 0:
                weights_max = max(weights.values())
                for key, value in weights.items():
                    normalized_weights[key] = value / weights_max

            weapon_type = character_weapon_type_map[team_list[i]]
            equipments_score.append([1 for _ in self.weapons[weapon_type]])

            for artifacts in self.artifacts.values():
                scores = [artifact.calculate_score(normalized_weights) for artifact in artifacts]
                equipments_score.append(scores)

        return equipments_score

    def validate_team(self, team_list, equipment_vector):
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
