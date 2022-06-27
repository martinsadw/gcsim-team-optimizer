import math

from static import stats_data
from stats import Stats


class Artifact:
    def __init__(self, artifact):
        self.id = artifact['id']
        self.slot = artifact['slotKey']
        self.level = artifact['level']
        self.rarity = artifact['rarity']
        self.set_key = artifact['setKey']
        self.main_stat_key = artifact['mainStatKey']
        self.missing_sub_stats = math.ceil((20 - artifact['level']) / 4)
        self.location = artifact['location']

        sub_stats = {}
        self.empty_sub_stats = 0
        for sub_stat in artifact['substats']:
            if sub_stat['key'] is None:
                self.empty_sub_stats += 1
            elif sub_stat['key'] in stats_data.PERCENT_STATS:
                sub_stats[sub_stat['key']] = sub_stat['value'] / 100
            else:
                sub_stats[sub_stat['key']] = sub_stat['value']
        self.sub_stats = Stats(**sub_stats)

    def upgrade(self, level=20):
        self.level = level

    def calculate_quality(self):
        quality = 0
        for key, sub_stat in self.sub_stats.items():
            quality += float(sub_stat) / Stats.sub_stat(key)

        return quality / 9

    def calculate_score(self, normalized_weights):
        quality = 0

        main_stat_value = Stats.main_stat(self.main_stat_key, self.level)
        main_stat_max_value = Stats.sub_stat(self.main_stat_key)
        quality += (main_stat_value / main_stat_max_value) * normalized_weights[self.main_stat_key]

        for key, sub_stat in self.sub_stats.items():
            max_value = Stats.sub_stat(key)
            quality += (float(sub_stat) / max_value) * normalized_weights[key]

        epsilon = 0.01
        return max(quality, epsilon)

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
