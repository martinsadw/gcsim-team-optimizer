EQUIPMENT_NAME = ['weapon', 'flower', 'plume', 'sands', 'goblet', 'circlet']
EQUIPMENT_ID = {key: i for i, key in enumerate(EQUIPMENT_NAME)}

MAIN_STAT = {
    'hp': [717, 920, 1123, 1326, 1530, 1733, 1936, 2139, 2342, 2545, 2749, 2952, 3155, 3358, 3561, 3764, 3967, 4171, 4374, 4577, 4780],
    'hp_': [0.07, 0.09, 0.110, 0.129, 0.149, 0.169, 0.189, 0.209, 0.228, 0.248, 0.268, 0.288, 0.308, 0.328, 0.347, 0.367, 0.387, 0.407, 0.427, 0.446, 0.466],
    'atk': [47, 60, 73, 86, 100, 113, 126, 139, 152, 166, 179, 192, 205, 219, 232, 245, 258, 272, 285, 298, 311],
    'atk_': [0.07, 0.09, 0.110, 0.129, 0.149, 0.169, 0.189, 0.209, 0.228, 0.248, 0.268, 0.288, 0.308, 0.328, 0.347, 0.367, 0.387, 0.407, 0.427, 0.446, 0.466],
    'def_': [0.087, 0.112, 0.137, 0.162, 0.186, 0.211, 0.236, 0.261, 0.286, 31, 0.335, 36, 0.385, 0.409, 0.434, 0.459, 0.484, 0.508, 0.533, 0.558, 0.583],
    'eleMas': [28, 36, 44, 52, 60, 68, 76, 84, 91, 99, 107, 115, 123, 131, 139, 147, 155, 163, 171, 179, 187],
    'enerRech_': [0.078, 0.100, 0.122, 0.144, 0.166, 0.188, 0.210, 0.232, 0.254, 0.276, 0.298, 0.320, 0.342, 0.364, 0.386, 0.408, 0.430, 0.452, 0.474, 0.496, 0.518],
    'heal_': [0.054, 0.069, 0.084, 0.100, 0.115, 0.130, 0.145, 0.161, 0.176, 0.191, 0.206, 0.222, 0.237, 0.252, 0.267, 0.283, 0.298, 0.313, 0.328, 0.344, 0.359],
    'critRate_': [0.047, 0.060, 0.074, 0.087, 0.100, 0.114, 0.127, 0.140, 0.154, 0.167, 0.180, 0.193, 0.207, 0.220, 0.233, 0.247, 0.260, 0.273, 0.287, 0.300, 0.311],
    'critDMG_': [0.093, 0.119, 0.146, 0.172, 0.199, 0.225, 0.252, 0.278, 0.305, 0.331, 0.358, 0.384, 0.411, 0.437, 0.463, 0.490, 0.516, 0.543, 0.569, 0.596, 0.622],
    'physical_dmg_': [0.087, 0.112, 0.137, 0.162, 0.162, 0.211, 0.236, 0.261, 0.286, 31, 0.335, 36, 0.385, 0.409, 0.434, 0.459, 0.484, 0.508, 0.533, 0.558, 0.583],
    'anemo_dmg_': [0.07, 0.09, 0.110, 0.129, 0.149, 0.169, 0.189, 0.209, 0.228, 0.248, 0.268, 0.288, 0.308, 0.328, 0.347, 0.367, 0.387, 0.407, 0.427, 0.446, 0.466],
    'geo_dmg_': [0.07, 0.09, 0.110, 0.129, 0.149, 0.169, 0.189, 0.209, 0.228, 0.248, 0.268, 0.288, 0.308, 0.328, 0.347, 0.367, 0.387, 0.407, 0.427, 0.446, 0.466],
    'electro_dmg_': [0.07, 0.09, 0.110, 0.129, 0.149, 0.169, 0.189, 0.209, 0.228, 0.248, 0.268, 0.288, 0.308, 0.328, 0.347, 0.367, 0.387, 0.407, 0.427, 0.446, 0.466],
    'hydro_dmg_': [0.07, 0.09, 0.110, 0.129, 0.149, 0.169, 0.189, 0.209, 0.228, 0.248, 0.268, 0.288, 0.308, 0.328, 0.347, 0.367, 0.387, 0.407, 0.427, 0.446, 0.466],
    'pyro_dmg_': [0.07, 0.09, 0.110, 0.129, 0.149, 0.169, 0.189, 0.209, 0.228, 0.248, 0.268, 0.288, 0.308, 0.328, 0.347, 0.367, 0.387, 0.407, 0.427, 0.446, 0.466],
    'cryo_dmg_': [0.07, 0.09, 0.110, 0.129, 0.149, 0.169, 0.189, 0.209, 0.228, 0.248, 0.268, 0.288, 0.308, 0.328, 0.347, 0.367, 0.387, 0.407, 0.427, 0.446, 0.466]
}

MAX_SUB_STAT = {
    'hp': {
        1: 29.88,
        2: 71.70,
        3: 143.40,
        4: 239.00,
        5: 298.75
    },
    'hp_': {
        1: 0.0146,
        2: 0.0233,
        3: 0.035,
        4: 0.0466,
        5: 0.0583
    },
    'atk': {
        1: 1.95,
        2: 4.67,
        3: 9.34,
        4: 15.56,
        5: 19.45
    },
    'atk_': {
        1: 0.0146,
        2: 0.0233,
        3: 0.035,
        4: 0.0466,
        5: 0.0583
    },
    'def': {
        1: 2.31,
        2: 5.56,
        3: 11.11,
        4: 18.52,
        5: 23.15
    },
    'def_': {
        1: 0.0182,
        2: 0.0291,
        3: 0.0437,
        4: 0.0583,
        5: 0.0729
    },
    'eleMas': {
        1: 5.83,
        2: 9.33,
        3: 13.99,
        4: 18.56,
        5: 23.31
    },
    'enerRech_': {
        1: 0.0162,
        2: 0.0259,
        3: 0.0389,
        4: 0.0518,
        5: 0.0648
    },
    'critRate_': {
        1: 0.0097,
        2: 0.0155,
        3: 0.0233,
        4: 0.0311,
        5: 0.0389
    },
    'critDMG_': {
        1: 0.0194,
        2: 0.0311,
        3: 0.0466,
        4: 0.0622,
        5: 0.0777
    },
    # Not actual substats. These values are based on the max value for the main stat.
    'anemo_dmg_': {
        1: 0.0146,
        2: 0.0233,
        3: 0.035,
        4: 0.0466,
        5: 0.0583
    },
    'geo_dmg_': {
        1: 0.0146,
        2: 0.0233,
        3: 0.035,
        4: 0.0466,
        5: 0.0583
    },
    'electro_dmg_': {
        1: 0.0146,
        2: 0.0233,
        3: 0.035,
        4: 0.0466,
        5: 0.0583
    },
    'hydro_dmg_': {
        1: 0.0146,
        2: 0.0233,
        3: 0.035,
        4: 0.0466,
        5: 0.0583
    },
    'pyro_dmg_': {
        1: 0.0146,
        2: 0.0233,
        3: 0.035,
        4: 0.0466,
        5: 0.0583
    },
    'cryo_dmg_': {
        1: 0.0146,
        2: 0.0233,
        3: 0.035,
        4: 0.0466,
        5: 0.0583
    },
    'physical_dmg_': {
        1: 0.0182,
        2: 0.0291,
        3: 0.0437,
        4: 0.0583,
        5: 0.0729
    },
    'heal_': {
        5: 0.0449
    },
}

ATTRIBUTE_LIST = ('hp', 'hp_', 'atk', 'atk_', 'def', 'def_', 'eleMas', 'enerRech_', 'heal_', 'critRate_', 'critDMG_',
                  'physical_dmg_', 'anemo_dmg_', 'geo_dmg_', 'electro_dmg_', 'hydro_dmg_', 'pyro_dmg_', 'cryo_dmg_')

PERCENT_STATS = {'hp_', 'atk_', 'def_', 'enerRech_', 'heal_', 'critRate_', 'critDMG_', 'physical_dmg_', 'anemo_dmg_',
                 'geo_dmg_', 'electro_dmg_', 'hydro_dmg_', 'pyro_dmg_', 'cryo_dmg_'}

SET_READABLE = {
  "Adventurer": "Adventurer",
  "ArchaicPetra": "Archaic Petra",
  "Berserker": "Berserker",
  "BlizzardStrayer": "Blizzard Strayer",
  "BloodstainedChivalry": "Bloodstained Chivalry",
  "BraveHeart": "Brave Heart",
  "CrimsonWitchOfFlames": "Crimson Witch of Flames",
  "DefendersWill": "Defender's Will",
  "EchoesOfAnOffering": "Echoes of an Offering",
  "EmblemOfSeveredFate": "Emblem of Severed Fate",
  "Gambler": "Gambler",
  "GladiatorsFinale": "Gladiator's Finale",
  "HeartOfDepth": "Heart of Depth",
  "HuskOfOpulentDreams": "Husk of Opulent Dreams",
  "Instructor": "Instructor",
  "Lavawalker": "Lavawalker",
  "LuckyDog": "Lucky Dog",
  "MaidenBeloved": "Maiden Beloved",
  "MartialArtist": "Martial Artist",
  "NoblesseOblige": "Noblesse Oblige",
  "OceanHuedClam": "Ocean-Hued Clam",
  "PaleFlame": "Pale Flame",
  "PrayersForDestiny": "Prayers for Destiny",
  "PrayersForIllumination": "Prayers for Illumination",
  "PrayersForWisdom": "Prayers for Wisdom",
  "PrayersToSpringtime": "Prayers to Springtime",
  "ResolutionOfSojourner": "Resolution of Sojourner",
  "RetracingBolide": "Retracing Bolide",
  "Scholar": "Scholar",
  "ShimenawasReminiscence": "Shimenawa's Reminiscence",
  "TenacityOfTheMillelith": "Tenacity of the Millelith",
  "TheExile": "The Exile",
  "ThunderingFury": "Thundering Fury",
  "Thundersoother": "Thundersoother",
  "TinyMiracle": "Tiny Miracle",
  "TravelingDoctor": "Traveling Doctor",
  "VermillionHereafter": "Vermillion Hereafter",
  "ViridescentVenerer": "Viridescent Venerer",
  "WanderersTroupe": "Wanderer's Troupe",
}

SET_READABLE_SHORT = {
  "Adventurer": "Adventurer",
  "ArchaicPetra": "Archaic Petra",
  "Berserker": "Berserker",
  "BlizzardStrayer": "Blizzard Strayer",
  "BloodstainedChivalry": "Bloodstained",
  "BraveHeart": "Brave Heart",
  "CrimsonWitchOfFlames": "Crimson Witch",
  "DefendersWill": "Defender",
  "EchoesOfAnOffering": "Echoes",
  "EmblemOfSeveredFate": "Severed Fate",
  "Gambler": "Gambler",
  "GladiatorsFinale": "Gladiator",
  "HeartOfDepth": "Heart of Depth",
  "HuskOfOpulentDreams": "Husk",
  "Instructor": "Instructor",
  "Lavawalker": "Lavawalker",
  "LuckyDog": "Lucky Dog",
  "MaidenBeloved": "Maiden",
  "MartialArtist": "Martial Artist",
  "NoblesseOblige": "Noblesse",
  "OceanHuedClam": "Ocean-Hued",
  "PaleFlame": "Pale Flame",
  "PrayersForDestiny": "Prayers for Destiny",
  "PrayersForIllumination": "Prayers for Illumination",
  "PrayersForWisdom": "Prayers for Wisdom",
  "PrayersToSpringtime": "Prayers to Springtime",
  "ResolutionOfSojourner": "Resolution of Sojourner",
  "RetracingBolide": "Retracing Bolide",
  "Scholar": "Scholar",
  "ShimenawasReminiscence": "Shimenawa",
  "TenacityOfTheMillelith": "Millelith",
  "TheExile": "Exile",
  "ThunderingFury": "Thundering Fury",
  "Thundersoother": "Thundersoother",
  "TinyMiracle": "Tiny Miracle",
  "TravelingDoctor": "Traveling Doctor",
  "VermillionHereafter": "Vermillion",
  "ViridescentVenerer": "Viridescent",
  "WanderersTroupe": "Wanderer",
}

gcsim_stat_to_string = [
    'n/a',
    'def_',
    'def',
    'hp',
    'hp_',
    'atk',
    'atk_',
    'enerRech_',
    'eleMas',
    'critRate_',
    'critDMG_',
    'heal_',
    'pyro_dmg_',
    'hydro_dmg_',
    'cryo_dmg_',
    'electro_dmg_',
    'anemo_dmg_',
    'geo_dmg_',
    'physical_dmg_',
    # 'ele_dmg_',
    'dendro_dmg_',
    'atk_spd_',  # Not represented in GOOD
    'dmg_',  # Not represented in GOOD
]
string_to_gcsim_stat = {key: i for i, key in enumerate(gcsim_stat_to_string)}