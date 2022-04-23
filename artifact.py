import math

from artifact_data import artifact_main_stat, artifact_max_sub_stat, percent_stats


class Artifact:
    def __init__(self, artifact):
        self.id = artifact['Id']
        self.slot = artifact['slotKey']
        self.level = artifact['level']
        self.rarity = artifact['rarity']
        self.set_key = artifact['setKey']
        self.main_stat_key = artifact['mainStatKey']
        self.missing_sub_stats = math.ceil((20 - artifact['level']) / 4)
        self.location = artifact['location']

        self.sub_stats = {}
        self.empty_sub_stats = 0
        for sub_stat in artifact['substats']:
            if sub_stat['key'] is None:
                self.empty_sub_stats += 1
            elif sub_stat['key'] in percent_stats:
                self.sub_stats[sub_stat['key']] = sub_stat['value'] / 100
            else:
                self.sub_stats[sub_stat['key']] = sub_stat['value']

    def upgrade(self, level=20):
        self.level = level

    def calculate_quality(self):
        quality = 0
        for key, sub_stat in self.sub_stats.items():
            quality += float(sub_stat) / artifact_max_sub_stat[key][str(self.rarity)]

        return quality / 9

    def calculate_score(self, normalized_weights):
        rarity_str = str(self.rarity)
        quality = 0

        main_stat_value = artifact_main_stat[self.main_stat_key][self.level]
        main_stat_max_value = artifact_max_sub_stat[self.main_stat_key][rarity_str]
        quality += (main_stat_value / main_stat_max_value) * normalized_weights[self.main_stat_key]

        for key, sub_stat in self.sub_stats.items():
            max_value = artifact_max_sub_stat[key][rarity_str]
            quality += (float(sub_stat) / max_value) * normalized_weights[key]

        epsilon = 0.01
        return max(quality, epsilon)

    @staticmethod
    def calculate_artifact_stats(artifacts):
        stats = {
            'artifact_set': {},
            'main_stats': {
                'hp': 0,
                'hp_': 0,
                'atk': 0,
                'atk_': 0,
                'def_': 0,
                'eleMas': 0,
                'enerRech_': 0,
                'heal_': 0,
                'critRate_': 0,
                'critDMG_': 0,
                'physical_dmg_': 0,
                'anemo_dmg_': 0,
                'geo_dmg_': 0,
                'electro_dmg_': 0,
                'hydro_dmg_': 0,
                'pyro_dmg_': 0,
                'cryo_dmg_': 0
            },
            'sub_stats': {
                'hp': 0,
                'hp_': 0,
                'atk': 0,
                'atk_': 0,
                'def': 0,
                'def_': 0,
                'eleMas': 0,
                'enerRech_': 0,
                'heal_': 0,
                'critRate_': 0,
                'critDMG_': 0
            }
        }

        for artifact in artifacts.values():
            if artifact is None:
                continue

            stat_value = artifact_main_stat[artifact.main_stat_key][artifact.level]
            stats['main_stats'][artifact.main_stat_key] += stat_value

            for sub_stat_key, sub_stat_value in artifact.sub_stats.items():
                if sub_stat_key:
                    stat_value = sub_stat_value
                    stats['sub_stats'][sub_stat_key] += stat_value

            if artifact.set_key in stats['artifact_set']:
                stats['artifact_set'][artifact.set_key] += 1
            else:
                stats['artifact_set'][artifact.set_key] = 1

        return stats

    def __repr__(self):
        sub_stat_str = 'sub_stats=('
        sub_stat_str += ', '.join([f'{key}={value:.2f}' for key, value in self.sub_stats.items()])
        sub_stat_str += ')'

        return f'Artifact(id={self.id}, slot={self.slot}, level={self.level}, rarity={self.rarity},' \
               f'set_key={self.set_key}, main_stat_key={self.main_stat_key},' \
               f'missing_sub_stats={self.missing_sub_stats}, empty_sub_stats={self.empty_sub_stats},' \
               f'location={self.location}, {sub_stat_str})'


def artifact_quality(artifact):
    return artifact.calculate_quality()
