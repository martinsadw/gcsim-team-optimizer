import json
import os
import re
import subprocess

from artifact_data import artifact_main_stat, percent_stats
from gcsim_names import good_to_gcsim_stats

from actions import actions_dict
import reader


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
        stat_value = artifact_main_stat[artifact['main_stat_key']][artifact['level']]
        if artifact['main_stat_key'] in percent_stats:
            stat_value /= 100
        stats['main_stats'][artifact['main_stat_key']] += stat_value

        for sub_stat_key, sub_stat_value in artifact['sub_stats'].items():
            if sub_stat_key:
                stat_value = sub_stat_value
                if sub_stat_key in percent_stats:
                    stat_value /= 100
                stats['sub_stats'][sub_stat_key] += stat_value

        if artifact['set_key'] in stats['artifact_set']:
            stats['artifact_set'][artifact['set_key']] += 1
        else:
            stats['artifact_set'][artifact['set_key']] = 1

    return stats


def character_to_gcsim(character_info):
    character = character_info['character']
    character_name = character['key'].lower()

    weapon = character_info['weapon']
    weapon_name = weapon['key'].lower()

    # Character base stats
    result = '{name} char lvl={level}/{max_level} cons={cons} talent={t1},{t2},{t3};\n'.format(
        name=character_name, level=character['level'], max_level=character['max_level'],
        cons=character['constellation'], t1=character['talent_1'], t2=character['talent_2'], t3=character['talent_3'])

    # Character Weapon
    result += '{name} add weapon="{weapon}" refine={refine} lvl={level}/{max_level};\n'.format(
        name=character_name, weapon=weapon_name, level=weapon['level'], max_level=weapon['max_level'],
        refine=weapon['refinement'])

    artifact_stats = calculate_artifact_stats(character_info['artifacts'])

    # Character artifact set
    for set_key, set_count in artifact_stats['artifact_set'].items():
        result += '{name} add set="{set}" count={count};\n'.format(
            name=character_name, set=set_key.lower(), count=set_count)

    # Character main stats
    main_stats = '{name} add stats'.format(name=character_name)
    for stats_key, stats_value in artifact_stats['main_stats'].items():
        if stats_value > 0:
            main_stats += ' {key}={value:.2f}'.format(key=good_to_gcsim_stats[stats_key], value=stats_value)
    main_stats += '; #main\n'
    result += main_stats

    # Character sub stats
    sub_stats = '{name} add stats'.format(name=character_name)
    for stats_key, stats_value in artifact_stats['sub_stats'].items():
        if stats_value > 0:
            sub_stats += ' {key}={value:.2f}'.format(key=good_to_gcsim_stats[stats_key], value=stats_value)
    sub_stats += '; #subs\n'
    result += sub_stats

    return result


# def read_good_file(good_data):
#     character_info = dict()
#
#     for character in good_data['characters']:
#         key = character['key']
#         ascension = character['ascension']
#         max_level = (20 + ascension * 20) if ascension <= 1 else (40 + (ascension - 1) * 10)
#
#         character_info[key] = {
#             'key': key,
#             'level': character['level'],
#             'max_level': max_level,
#             'constellation': character['constellation'],
#             'talent_1': character['talent']['auto'],
#             'talent_2': character['talent']['skill'],
#             'talent_3': character['talent']['burst'],
#             'artifact_set': {},
#             'main_stats': {
#                 'hp': 0,
#                 'hp_': 0,
#                 'atk': 0,
#                 'atk_': 0,
#                 'def_': 0,
#                 'eleMas': 0,
#                 'enerRech_': 0,
#                 'heal_': 0,
#                 'critRate_': 0,
#                 'critDMG_': 0,
#                 'physical_dmg_': 0,
#                 'anemo_dmg_': 0,
#                 'geo_dmg_': 0,
#                 'electro_dmg_': 0,
#                 'hydro_dmg_': 0,
#                 'pyro_dmg_': 0,
#                 'cryo_dmg_': 0
#             },
#             'sub_stats': {
#                 'hp': 0,
#                 'hp_': 0,
#                 'atk': 0,
#                 'atk_': 0,
#                 'def': 0,
#                 'def_': 0,
#                 'eleMas': 0,
#                 'enerRech_': 0,
#                 'heal_': 0,
#                 'critRate_': 0,
#                 'critDMG_': 0
#             }
#         }
#
#     for weapon in good_data['weapons']:
#         ascension = weapon['ascension']
#         if weapon['location'] in character_info:
#             max_level = (20 + ascension * 20) if ascension <= 1 else (40 + (ascension - 1) * 10)
#
#             character_info[weapon['location']]['weapon'] = {
#                 'key': weapon['key'],
#                 'level': weapon['level'],
#                 'max_level': max_level,
#                 'refine': weapon['refinement']
#             }
#
#     for artifact in good_data['artifacts']:
#         if artifact['location'] in character_info:
#             character = character_info[artifact['location']]
#             stat_value = artifact_main_stat[artifact['mainStatKey']][artifact['level']]
#             if artifact['mainStatKey'] in percent_stats:
#                 stat_value /= 100
#             character['main_stats'][artifact['mainStatKey']] += stat_value
#
#             for substats in artifact['substats']:
#                 if substats['key']:
#                     stat_value = substats['value']
#                     if substats['key'] in percent_stats:
#                         stat_value /= 100
#                     character['sub_stats'][substats['key']] += stat_value
#
#             if artifact['setKey'] in character['artifact_set']:
#                 character['artifact_set'][artifact['setKey']] += 1
#             else:
#                 character['artifact_set'][artifact['setKey']] = 1
#
#     return character_info


def create_gcsim_file(team_info, actions, filename, iterations=1000):
    with open(filename, 'w') as file:
        file.write('# Character Info\n')
        for character_info in team_info:
            file.write(character_to_gcsim(character_info))
            file.write('\n')
        file.write('\n')

        file.write('# Simulation Config\n')
        file.write('options debug=true iteration={iterations} duration={duration} workers=30 mode={mode};\n'.format(
            iterations=iterations, duration=actions['simulation_length'], mode=actions['mode']))
        file.write('target lvl=100 resist=.1;\n')
        file.write('energy every interval=240,360 amount=1;\n')
        file.write('\n\n')

        file.write('# Actions\n')
        file.write(actions['actions'])


def run_team(gcsim_filename):
    gcsim_exec_path = os.path.join('.', 'gcsim')

    dps_regex = r"resulting in (?P<mean>[\d\.]+) dps \(min: (?P<min_dps>[\d\.]+) max: (?P<max_dps>[\d\.]+) std: (?P<std>[\d\.]+)\)"
    gcsim_result = subprocess.run([gcsim_exec_path, '-c', gcsim_filename], capture_output=True)
    dps = re.search(dps_regex, gcsim_result.stdout.decode('utf-8'), re.MULTILINE)

    print('DPS:', dps['mean'])
    print('Min:', dps['min_dps'])
    print('Max:', dps['max_dps'])
    print('Std:', dps['std'])


def main():
    good_filename = 'data/data.json'
    team_name = 'hyper_raiden'
    gcsim_filename = os.path.join('actions', team_name + '.txt')

    with open(good_filename) as good_file:
        good_data = json.load(good_file)

    artifacts_data = reader.read_artifacts(good_data)
    weapons_data = reader.read_weapons(good_data)
    characters_data = reader.read_characters(good_data)

    raiden_build = {
        'character': reader.get_character_by_name(characters_data, 'RaidenShogun'),
        'weapon': reader.get_weapon_by_character(weapons_data, 'RaidenShogun'),

        'artifacts': {
            'flower': artifacts_data['flower'][0],
            'plume': artifacts_data['plume'][0],
            'sands': artifacts_data['sands'][0],
            'goblet': artifacts_data['goblet'][0],
            'circlet': artifacts_data['circlet'][0]
        }
    }
    yae_build = {
        'character': reader.get_character_by_name(characters_data, 'YaeMiko'),
        'weapon': reader.get_weapon_by_character(weapons_data, 'YaeMiko'),
        'artifacts': {
            'flower': artifacts_data['flower'][1],
            'plume': artifacts_data['plume'][1],
            'sands': artifacts_data['sands'][1],
            'goblet': artifacts_data['goblet'][1],
            'circlet': artifacts_data['circlet'][1]
        }
    }
    bennett_build = {
        'character': reader.get_character_by_name(characters_data, 'Bennett'),
        'weapon': reader.get_weapon_by_character(weapons_data, 'Bennett'),
        'artifacts': {
            'flower': artifacts_data['flower'][2],
            'plume': artifacts_data['plume'][2],
            'sands': artifacts_data['sands'][2],
            'goblet': artifacts_data['goblet'][2],
            'circlet': artifacts_data['circlet'][2]
        }
    }
    kazuha_build = {
        'character': reader.get_character_by_name(characters_data, 'KaedeharaKazuha'),
        'weapon': reader.get_weapon_by_character(weapons_data, 'KaedeharaKazuha'),
        'artifacts': {
            'flower': artifacts_data['flower'][3],
            'plume': artifacts_data['plume'][3],
            'sands': artifacts_data['sands'][3],
            'goblet': artifacts_data['goblet'][3],
            'circlet': artifacts_data['circlet'][3]
        }
    }
    team_info = [raiden_build, yae_build, bennett_build, kazuha_build]

    create_gcsim_file(team_info, actions_dict[team_name], gcsim_filename, iterations=100)
    run_team(gcsim_filename)


if __name__ == '__main__':
    main()
