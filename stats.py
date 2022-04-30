import artifact_data
from gcsim_names import good_to_gcsim_stats


class Stats:
    __slots__ = artifact_data.ATTRIBUTE_LIST

    def __init__(self, **kwargs):
        for attribute in artifact_data.ATTRIBUTE_LIST:
            setattr(self, attribute, kwargs.get(attribute, 0))

    @classmethod
    def by_stats_count(cls, quality=1, rarity_reference=5, **kwargs):
        stats = {key: Stats.sub_stat(key, value, quality, rarity_reference) for key, value in kwargs.items()}
        return cls(**stats)

    @classmethod
    def by_artifact_main_stat(cls, stat_key, level):
        stats = cls()
        stats[stat_key] += Stats.main_stat(stat_key, level)
        return stats

    @classmethod
    def by_artifact_sub_stat(cls, stat_key, quant=1, quality=1, rarity_reference=5):
        stats = cls()
        stats[stat_key] += Stats.sub_stat(stat_key, quant, quality, rarity_reference)
        return stats

    @staticmethod
    def main_stat(stat_key, level):
        return artifact_data.MAIN_STAT[stat_key][level]

    @staticmethod
    def sub_stat(stat_key, quant=1, quality=1, rarity_reference=5):
        return quant * quality * artifact_data.MAX_SUB_STAT[stat_key][rarity_reference]

    def to_gcsim_text(self):
        text = ' '.join(['{key}={value:.2f}'.format(key=good_to_gcsim_stats[attribute], value=value)
                         for attribute, value in self.items()])

        return text

    def calculate_power(self, rarity_reference=5):
        power = 0
        for key, sub_stat in self.items():
            power += sub_stat / artifact_data.MAX_SUB_STAT[key][rarity_reference]

        return power

    def to_json(self):
        return {slot: self[slot] for slot in self.__slots__ if self[slot] > 0}

    def __str__(self):
        return self.to_gcsim_text()

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __add__(self, other):
        new_stats = {attribute: self[attribute] + other[attribute] for attribute in artifact_data.ATTRIBUTE_LIST}
        return Stats(**new_stats)

    def __sub__(self, other):
        new_stats = {attribute: self[attribute] - other[attribute] for attribute in artifact_data.ATTRIBUTE_LIST}
        return Stats(**new_stats)

    def __iter__(self):
        yield from self.keys()

    def keys(self):
        return iter([attribute for attribute in artifact_data.ATTRIBUTE_LIST if self[attribute] > 0])

    def values(self):
        return iter([self[attribute] for attribute in artifact_data.ATTRIBUTE_LIST if self[attribute] > 0])

    def items(self):
        return iter([(attribute, self[attribute]) for attribute in artifact_data.ATTRIBUTE_LIST if self[attribute] > 0])
