from artifact_data import artifact_main_stat, artifact_max_sub_stat


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

        stat_value = artifact_main_stat[artifact['main_stat_key']][artifact['level']]
        stats['main_stats'][artifact['main_stat_key']] += stat_value

        for sub_stat_key, sub_stat_value in artifact['sub_stats'].items():
            if sub_stat_key:
                stat_value = sub_stat_value
                stats['sub_stats'][sub_stat_key] += stat_value

        if artifact['set_key'] in stats['artifact_set']:
            stats['artifact_set'][artifact['set_key']] += 1
        else:
            stats['artifact_set'][artifact['set_key']] = 1

    return stats


def upgrade_artifacts(artifacts_data):
    for artifacts_piece in artifacts_data.values():
        for artifact in artifacts_piece:
            artifact['level'] = 20


def artifact_quality(artifact_piece):
    quality = 0
    for key, sub_stat in artifact_piece['sub_stats'].items():
        quality += float(sub_stat) / artifact_max_sub_stat[key][str(artifact_piece['rarity'])]
    return quality / 9


def artifact_score(artifact_piece, normalized_weights):
    level = artifact_piece['level']
    rarity = str(artifact_piece['rarity'])
    main_stat_key = artifact_piece['main_stat_key']

    quality = 0

    main_stat_value = artifact_main_stat[main_stat_key][level]
    main_stat_max_value = artifact_max_sub_stat[main_stat_key][rarity]
    quality += (main_stat_value / main_stat_max_value) * normalized_weights[main_stat_key]

    for key, sub_stat in artifact_piece['sub_stats'].items():
        max_value = artifact_max_sub_stat[key][rarity]
        quality += (float(sub_stat) / max_value) * normalized_weights[key]

    epsilon = 0.01
    return max(quality, epsilon)