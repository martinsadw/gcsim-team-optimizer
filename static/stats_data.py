import copy

EQUIPMENT_NAME = ['weapon', 'flower', 'plume', 'sands', 'goblet', 'circlet']
EQUIPMENT_ID = {key: i for i, key in enumerate(EQUIPMENT_NAME)}

stats = dict()

stats['hp'] = {
    'good_name': 'hp',
    'gcsim_name': 'hp',
    'is_percent': False,
    'main_stat': {
        1: [129, 178, 227, 275, 324],
        2: [258, 331, 404, 478, 551],
        3: [430, 552, 674, 796, 918, 1040, 1162, 1283, 1405, 1527, 1649, 1771, 1893],
        4: [645, 828, 1011, 1194, 1377, 1559, 1742, 1925, 2108, 2291, 2474, 2657, 2839, 3022, 3205, 3388, 3571],
        5: [717, 920, 1123, 1326, 1530, 1733, 1936, 2139, 2342, 2545, 2749, 2952, 3155, 3358, 3561, 3764, 3967, 4171, 4374, 4577, 4780],
    },
    'sub_stat': {
        1: [23.90, 29.88],
        2: [50.19, 60.95, 71.70],
        3: [100.38, 114.72, 129.06, 143.40],
        4: [167.30, 191.20, 215.10, 239.00],
        5: [209.13, 239.00, 268.88, 298.75],
    },
    'main_stat_weight': {
        'flower': 1,
        'plume': 0,
        'sands': 0,
        'goblet': 0,
        'circlet': 0,
    },
    'sub_stat_weight': {
        'flower': 0,
        'plume': 15.0,
        'sands': 15.0,
        'goblet': 15.0,
        'circlet': 15.0,
    }
}

stats['hp_'] = {
    'good_name': 'hp_',
    'gcsim_name': 'hp%',
    'is_percent': True,
    'main_stat': {
        1: [3.1, 4.3, 5.5, 6.7, 7.9],
        2: [4.2, 5.4, 6.6, 7.8, 9],
        3: [5.2, 6.7, 8.2, 9.7, 11.2, 12.7, 14.2, 15.6, 17.1, 18.6, 20.1, 21.6, 23.1],
        4: [6.3, 8.1, 9.9, 11.6, 13.4, 15.2, 17.0, 18.8, 20.6, 22.3, 24.1, 25.9, 27.7, 29.5, 31.3, 33.0, 34.8],
        5: [7.0, 9.0, 11.0, 12.9, 14.9, 16.9, 18.9, 20.9, 22.8, 24.8, 26.8, 28.8, 30.8, 32.8, 34.7, 36.7, 38.7, 40.7, 42.7, 44.6, 46.6],
    },
    'sub_stat': {
        1: [1.17, 1.46],
        2: [1.63, 1.98, 2.33],
        3: [2.45, 2.80, 3.15, 3.50],
        4: [3.26, 3.73, 4.20, 4.66],
        5: [4.08, 4.66, 5.25, 5.83],
    },
    'main_stat_weight': {
        'flower': 0,
        'plume': 0,
        'sands': 0.2668,
        'goblet': 0.2125,
        'circlet': 0.22,
    },
    'sub_stat_weight': {
        'flower': 10.0,
        'plume': 10.0,
        'sands': 10.0,
        'goblet': 10.0,
        'circlet': 10.0,
    }
}

stats['atk'] = {
    'good_name': 'atk',
    'gcsim_name': 'atk',
    'is_percent': False,
    'main_stat': {
        1: [8, 12, 15, 18, 21],
        2: [17, 22, 26, 31, 36],
        3: [28, 36, 44, 52, 60, 68, 76, 84, 91, 99, 107, 115, 123],
        4: [42, 54, 66, 78, 90, 102, 113, 125, 137, 149, 161, 173, 185, 197],
        5: [47, 60, 73, 86, 100, 113, 126, 139, 152, 166, 179, 192, 205, 219, 232, 245, 258, 272, 285, 298, 311],
    },
    'sub_stat': {
        1: [1.56, 1.95],
        2: [3.27, 3.97, 4.67],
        3: [6.54, 7.47, 8.40, 9.34],
        4: [10.89, 12.45, 14.00, 15.56],
        5: [13.62, 15.56, 17.51, 19.45],
    },
    'main_stat_weight': {
        'flower': 0,
        'plume': 1,
        'sands': 0,
        'goblet': 0,
        'circlet': 0,
    },
    'sub_stat_weight': {
        'flower': 15.0,
        'plume': 0,
        'sands': 15.0,
        'goblet': 15.0,
        'circlet': 15.0,
    }
}

stats['atk_'] = {
    'good_name': 'atk_',
    'gcsim_name': 'atk%',
    'is_percent': True,
    'main_stat': {
        1: [3.1, 4.3, 5.5, 6.7, 7.9],
        2: [4.2, 5.4, 6.6, 7.8, 9],
        3: [5.2, 6.7, 8.2, 9.7, 11.2, 12.7, 14.2, 15.6, 17.1, 18.6, 20.1, 21.6, 23.1],
        4: [6.3, 8.1, 9.9, 11.6, 13.4, 15.2, 17.0, 18.8, 20.6, 22.3, 24.1, 25.9, 27.7, 29.5, 31.3, 33.0, 34.8],
        5: [7.0, 9.0, 11.0, 12.9, 14.9, 16.9, 18.9, 20.9, 22.8, 24.8, 26.8, 28.8, 30.8, 32.8, 34.7, 36.7, 38.7, 40.7, 42.7, 44.6, 46.6],
    },
    'sub_stat': {
        1: [1.17, 1.46],
        2: [1.63, 1.98, 2.33],
        3: [2.45, 2.80, 3.15, 3.50],
        4: [3.26, 3.73, 4.20, 4.66],
        5: [4.08, 4.66, 5.25, 5.83],
    },
    'main_stat_weight': {
        'flower': 0,
        'plume': 0,
        'sands': 0.2666,
        'goblet': 0.2125,
        'circlet': 0.22,
    },
    'sub_stat_weight': {
        'flower': 10.0,
        'plume': 10.0,
        'sands': 10.0,
        'goblet': 10.0,
        'circlet': 10.0,
    }
}

stats['def'] = {
    'good_name': 'def',
    'gcsim_name': 'def',
    'is_percent': False,
    'main_stat': {
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
    },
    'sub_stat': {
        1: [1.85, 2.31],
        2: [3.89, 4.72, 5.56],
        3: [7.78, 8.89, 10.00, 11.11],
        4: [12.96, 14.82, 16.67, 18.52],
        5: [16.20, 18.52, 20.83, 23.15],
    },
    'main_stat_weight': {
        'flower': 0,
        'plume': 0,
        'sands': 0,
        'goblet': 0,
        'circlet': 0,
    },
    'sub_stat_weight': {
        'flower': 15.0,
        'plume': 15.0,
        'sands': 15.0,
        'goblet': 15.0,
        'circlet': 15.0,
    }
}

stats['def_'] = {
    'good_name': 'def_',
    'gcsim_name': 'def%',
    'is_percent': True,
    'main_stat': {
        1: [3.9, 5.4, 6.9, 8.4, 9.9],
        2: [5.2, 6.7, 8.2, 9.7, 11.2],
        3: [6.6, 8.4, 10.3, 12.1, 14.0, 15.8, 17.7, 19.6, 21.4, 23.3, 25.1, 27.0, 28.8],
        4: [7.9, 10.1, 12.3, 14.6, 16.8, 19.0, 21.2, 23.5, 25.7, 27.9, 30.2, 32.4, 34.6, 36.8, 39.1, 41.3, 43.5],
        5: [8.7, 11.2, 13.7, 16.2, 18.6, 21.1, 23.6, 26.1, 28.6, 31, 33.5, 36, 38.5, 40.9, 43.4, 45.9, 48.4, 50.8, 53.3, 55.8, 58.3],
    },
    'sub_stat': {
        1: [1.46, 1.82],
        2: [2.04, 2.48, 2.91],
        3: [3.06, 3.50, 3.93, 4.37],
        4: [4.08, 4.66, 5.25, 5.83],
        5: [5.10, 5.83, 6.56, 7.29],
    },
    'main_stat_weight': {
        'flower': 0,
        'plume': 0,
        'sands': 0.2666,
        'goblet': 0.20,
        'circlet': 0.22,
    },
    'sub_stat_weight': {
        'flower': 10.0,
        'plume': 10.0,
        'sands': 10.0,
        'goblet': 10.0,
        'circlet': 10.0,
    }
}

stats['eleMas'] = {
    'good_name': 'eleMas',
    'gcsim_name': 'em',
    'is_percent': False,
    'main_stat': {
        1: [12.6, 17.3, 22.1, 26.9, 31.6],
        2: [16.8, 21.5, 26.3, 31.1, 35.8],
        3: [21.0, 26.9, 32.9, 38.8, 44.8, 50.7, 56.7, 62.6, 68.5, 74.5, 80.4, 86.4, 92.3],
        4: [25.2, 32.3, 39.4, 46.6, 53.7, 60.8, 68.0, 75.1, 82.2, 89.4, 96.5, 103.6, 110.8, 117.9, 125.0, 132.2, 139.3],
        5: [28.0, 35.9, 43.8, 51.8, 59.7, 67.6, 75.5, 83.5, 91.4, 99.3, 107.2, 115.2, 123.1, 131.0, 138.9, 146.9, 154.8, 162.7, 170.6, 178.6, 186.5],
    },
    'sub_stat': {
        1: [4.66, 5.83],
        2: [6.53, 7.93, 9.33],
        3: [9.79, 11.19, 12.59, 13.99],
        4: [13.06, 14.92, 16.79, 18.56],
        5: [16.32, 18.65, 20.98, 23.31],
    },
    'main_stat_weight': {
        'flower': 0,
        'plume': 0,
        'sands': 0.10,
        'goblet': 0.025,
        'circlet': 0.04,
    },
    'sub_stat_weight': {
        'flower': 10.0,
        'plume': 10.0,
        'sands': 10.0,
        'goblet': 10.0,
        'circlet': 10.0,
    }
}

stats['enerRech_'] = {
    'good_name': 'enerRech_',
    'gcsim_name': 'er',
    'is_percent': True,
    'main_stat': {
        1: [3.5, 4.8, 6.1, 7.5, 8.8],
        2: [4.7, 6, 7.3, 8.6, 9.9],
        3: [5.8, 7.5, 9.1, 10.8, 12.4, 14.1, 15.7, 17.4, 19.0, 20.7, 22.3, 24.0, 25.6],
        4: [7.0, 9.0, 11.0, 12.9, 14.9, 16.9, 18.9, 20.9, 22.8, 24.8, 26.8, 28.8, 30.8, 32.8, 34.7, 36.7, 38.7],
        5: [7.8, 10.0, 12.2, 14.4, 16.6, 18.8, 21.0, 23.2, 25.4, 27.6, 29.8, 32.0, 34.2, 36.4, 38.6, 40.8, 43.0, 45.2, 47.4, 49.6, 51.8],
    },
    'sub_stat': {
        1: [1.30, 1.62],
        2: [1.81, 2.20, 2.59],
        3: [2.72, 3.11, 3.50, 3.89],
        4: [3.63, 4.14, 4.66, 5.18],
        5: [4.53, 5.18, 5.83, 6.48],
    },
    'main_stat_weight': {
        'flower': 0,
        'plume': 0,
        'sands': 0.10,
        'goblet': 0,
        'circlet': 0,
    },
    'sub_stat_weight': {
        'flower': 10.0,
        'plume': 10.0,
        'sands': 10.0,
        'goblet': 10.0,
        'circlet': 10.0,
    }
}

stats['physical_dmg_'] = {
    'good_name': 'physical_dmg_',
    'gcsim_name': 'phys%',
    'is_percent': True,
    'main_stat': {
        1: [3.9, 5.4, 6.9, 8.4, 9.9],
        2: [5.2, 6.7, 8.2, 9.7, 11.2],
        3: [6.6, 8.4, 10.3, 12.1, 14.0, 15.8, 17.7, 19.6, 21.4, 23.3, 25.1, 27.0, 28.8],
        4: [7.9, 10.1, 12.3, 14.6, 16.8, 19.0, 21.2, 23.5, 25.7, 27.9, 30.2, 32.4, 34.6, 36.8, 39.1, 41.3, 43.5],
        5: [8.7, 11.2, 13.7, 16.2, 18.6, 21.1, 23.6, 26.1, 28.6, 31, 33.5, 36, 38.5, 40.9, 43.4, 45.9, 48.4, 50.8, 53.3, 55.8, 58.3],
    },
    # NOTE(andre): Not actual substats. These values are based on the def_ attribute
    'sub_stat': {
        1: [1.46, 1.82],
        2: [2.04, 2.48, 2.91],
        3: [3.06, 3.50, 3.93, 4.37],
        4: [4.08, 4.66, 5.25, 5.83],
        5: [5.10, 5.83, 6.56, 7.29],
    },
    'main_stat_weight': {
        'flower': 0,
        'plume': 0,
        'sands': 0,
        'goblet': 0.05,
        'circlet': 0,
    },
    'sub_stat_weight': {
        'flower': 0,
        'plume': 0,
        'sands': 0,
        'goblet': 0,
        'circlet': 0,
    }
}

elemental_stat_base = {
    'good_name': '',
    'gcsim_name': '',
    'is_percent': True,
    'main_stat': {
        1: [3.1, 4.3, 5.5, 6.7, 7.9],
        2: [4.2, 5.4, 6.6, 7.8, 9],
        3: [5.2, 6.7, 8.2, 9.7, 11.2, 12.7, 14.2, 15.6, 17.1, 18.6, 20.1, 21.6, 23.1],
        4: [6.3, 8.1, 9.9, 11.6, 13.4, 15.2, 17.0, 18.8, 20.6, 22.3, 24.1, 25.9, 27.7, 29.5, 31.3, 33.0, 34.8],
        5: [7.0, 9.0, 11.0, 12.9, 14.9, 16.9, 18.9, 20.9, 22.8, 24.8, 26.8, 28.8, 30.8, 32.8, 34.7, 36.7, 38.7, 40.7, 42.7, 44.6, 46.6],
    },
    # NOTE(andre): Not actual substats. These values are based on the hp_ attribute
    'sub_stat': {
        1: [1.17, 1.46],
        2: [1.63, 1.98, 2.33],
        3: [2.45, 2.80, 3.15, 3.50],
        4: [3.26, 3.73, 4.20, 4.66],
        5: [4.08, 4.66, 5.25, 5.83],
    },
    'main_stat_weight': {
        'flower': 0,
        'plume': 0,
        'sands': 0,
        'goblet': 0.05,
        'circlet': 0,
    },
    'sub_stat_weight': {
        'flower': 0,
        'plume': 0,
        'sands': 0,
        'goblet': 0,
        'circlet': 0,
    }
}
_elemental_stats_good = ['anemo_dmg_', 'cryo_dmg_', 'dendro_dmg_', 'electro_dmg_', 'geo_dmg_', 'hydro_dmg_', 'pyro_dmg_']
_elemental_stats_gcsim = ['anemo%', 'cryo%', 'dendro%', 'electro%', 'geo%', 'hydro%', 'pyro%']
for good_name, gcsim_name in zip(_elemental_stats_good, _elemental_stats_gcsim):
    stats[good_name] = copy.deepcopy(elemental_stat_base)
    stats[good_name]['good_name'] = good_name
    stats[good_name]['gcsim_name'] = gcsim_name

stats['critRate_'] = {
    'good_name': 'critRate_',
    'gcsim_name': 'cr',
    'is_percent': True,
    'main_stat': {
        1: [2.1, 2.9, 3.7, 4.5, 5.3],
        2: [2.8, 3.6, 4.4, 5.2, 6.0],
        3: [3.5, 4.5, 5.5, 6.5, 7.5, 8.4, 9.4, 10.4, 11.4, 12.4, 13.4, 14.4, 15.4],
        4: [4.2, 5.4, 6.6, 7.8, 9.0, 10.1, 11.3, 12.5, 13.7, 14.9, 16.1, 17.3, 18.5, 19.7, 20.8, 22.0, 23.2],
        5: [4.7, 6.0, 7.3, 8.6, 9.9, 11.3, 12.6, 13.9, 15.2, 16.6, 17.9, 19.2, 20.5, 21.8, 23.2, 24.5, 25.8, 27.1, 28.4, 29.8, 31.1],
    },
    'sub_stat': {
        1: [0.78, 0.97],
        2: [1.09, 1.32, 1.55],
        3: [1.63, 1.86, 2.10, 2.33],
        4: [2.18, 2.49, 2.80, 3.11],
        5: [2.72, 3.11, 3.50, 3.89],
    },
    'main_stat_weight': {
        'flower': 0,
        'plume': 0,
        'sands': 0,
        'goblet': 0,
        'circlet': 0.10,
    },
    'sub_stat_weight': {
        'flower': 7.5,
        'plume': 7.5,
        'sands': 7.5,
        'goblet': 7.5,
        'circlet': 7.5,
    }
}

stats['critDMG_'] = {
    'good_name': 'critDMG_',
    'gcsim_name': 'cd',
    'is_percent': True,
    'main_stat': {
        1: [4.2, 5.8, 7.4, 9.0, 10.5],
        2: [5.6, 7.2, 8.8, 10.4, 11.9],
        3: [7.0, 9.0, 11.0, 12.9, 14.9, 16.9, 18.9, 20.9, 22.8, 24.8, 26.8, 28.8, 30.8],
        4: [8.4, 10.8, 13.1, 15.5, 17.9, 20.3, 22.7, 25.0, 27.4, 29.8, 32.2, 34.5, 36.9, 39.3, 41.7, 44.1, 46.4],
        5: [9.3, 12.0, 14.6, 17.3, 19.9, 22.5, 25.2, 27.8, 30.5, 33.1, 35.7, 38.4, 41.0, 43.7, 46.3, 49.0, 51.6, 54.2, 56.9, 59.5, 62.2],
    },
    'sub_stat': {
        1: [1.55, 1.94],
        2: [2.18, 2.64, 3.11],
        3: [3.26, 3.73, 4.20, 4.66],
        4: [4.35, 4.97, 5.60, 6.22],
        5: [5.44, 6.22, 6.99, 7.77],
    },
    'main_stat_weight': {
        'flower': 0,
        'plume': 0,
        'sands': 0,
        'goblet': 0,
        'circlet': 0.10,
    },
    'sub_stat_weight': {
        'flower': 7.5,
        'plume': 7.5,
        'sands': 7.5,
        'goblet': 7.5,
        'circlet': 7.5,
    }
}

stats['heal_'] = {
    'good_name': 'heal_',
    'gcsim_name': 'heal',
    'is_percent': True,
    'main_stat': {
        1: [2.4, 3.3, 4.3, 5.2, 6.1],
        2: [3.2, 4.1, 5.1, 6.0, 6.9],
        3: [4.0, 5.2, 6.3, 7.5, 8.6, 9.8, 10.9, 12.0, 13.2, 14.3, 15.5, 16.6, 17.8],
        4: [4.8, 6.2, 7.6, 9.0, 10.3, 11.7, 13.1, 14.4, 15.8, 17.2, 18.6, 19.9, 21.3, 22.7, 24.0, 25.4, 26.8],
        5: [5.4, 6.9, 8.4, 10.0, 11.5, 13.0, 14.5, 16.1, 17.6, 19.1, 20.6, 22.1, 23.7, 25.2, 26.7, 28.2, 29.8, 31.3, 32.8, 34.3, 35.9],
    },
    # NOTE(andre): Not actual substats. These values are based on the main stat values and common stats proportions
    #  For 5-star, hp and atk main stats are worth 16 sub stats. The remaining main stats are worth 8 sub stats
    #  For 1/2/3/4-star, the max sub stat for hp and atk is worth 10%/24%/48%/80% of the 5-star respectively
    #  For 1/2/3/4-star, the max sub stat other than hp and atk is worth 25%/40%/60%/80% of the 5-star respectively
    #  5, 4 and 3-star sub stats follow the pattern of 70%/80%/90%/100% for the possible rolls
    #  2-star sub stats follow the pattern of 70%/85%/100% for the possible rolls
    #  1-star sub stats follow the pattern of 80%/100% for the possible rolls
    'sub_stat': {
        1: [0.9, 1.12],
        2: [1.26, 1.53, 1.80],
        3: [1.88, 2.15, 2.42, 2.69],
        4: [2.51, 2.87, 3.23, 3.59],
        5: [3.14, 3.59, 4.04, 4.49],
    },
    'main_stat_weight': {
        'flower': 0,
        'plume': 0,
        'sands': 0,
        'goblet': 0,
        'circlet': 0.10,
    },
    'sub_stat_weight': {
        'flower': 0,
        'plume': 0,
        'sands': 0,
        'goblet': 0,
        'circlet': 0,
    }
}

# NOTE(andre): adjusts percent stats to store rational values
for stat in stats.values():
    if stat['is_percent']:
        for rarity_key, rarity_value in stat['main_stat'].items():
            stat['main_stat'][rarity_key] = [value / 100 for value in rarity_value]

        for rarity_key, rarity_value in stat['sub_stat'].items():
            stat['sub_stat'][rarity_key] = [value / 100 for value in rarity_value]


ATTRIBUTE_LIST = tuple(stats.keys())
PERCENT_STATS = {key for key, value in stats.items() if value['is_percent']}

STATKEY_TO_GOOD = [
    'n/a',  # 0
    'def_',  # 1
    'def',  # 2
    'hp',  # 3
    'hp_',   # 4
    'atk',   # 5
    'atk_',   # 6
    'enerRech_',   # 7
    'eleMas',   # 8
    'critRate_',   # 9
    'critDMG_',   # 10
    'heal_',   # 11
    'pyro_dmg_',   # 12
    'hydro_dmg_',   # 13
    'cryo_dmg_',   # 14
    'electro_dmg_',   # 15
    'anemo_dmg_',   # 16
    'geo_dmg_',   # 17
    'physical_dmg_',   # 18
    # 'ele_dmg_',
    'dendro_dmg_',   # 19
    'atk_spd_',  # Not represented in GOOD   # 20
    'dmg_',  # Not represented in GOOD   # 21
]
GOOD_TO_STATKEY = {key: i for i, key in enumerate(STATKEY_TO_GOOD)}


def main_stat(key, rarity=5, level=-1): return stats[key]['main_stat'][rarity][level]
def sub_stat(key, rarity=5, quality=-1): return stats[key]['sub_stat'][rarity][quality]
