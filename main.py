# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import json
import math
import os
import re
import subprocess

from artifact_data import artifact_main_stat, percent_stats
from gcsim_names import good_to_gcsim_stats

from actions import actions_dict


def character_to_gcsim(character):
    weapon = character['weapon']
    character_name = character['key'].lower()
    weapon_name = weapon['key'].lower()

    # Character base stats
    result = '{name} char lvl={level}/{max_level} cons={cons} talent={t1},{t2},{t3};\n'.format(
        name=character_name, level=character['level'], max_level=character['max_level'],
        cons=character['constellation'], t1=character['talent_1'], t2=character['talent_2'], t3=character['talent_3'])

    # Character Weapon
    result += '{name} add weapon="{weapon}" refine={refine} lvl={level}/{max_level};\n'.format(
        name=character_name, weapon=weapon_name, level=weapon['level'], max_level=weapon['max_level'],
        refine=weapon['refine'])

    # Character artifact set
    for set_key, set_count in character['artifact_set'].items():
        result += '{name} add set="{set}" count={count};\n'.format(
            name=character_name, set=set_key.lower(), count=set_count)

    # Character main stats
    main_stats = '{name} add stats'.format(name=character_name)
    for stats_key, stats_value in character['main_stats'].items():
        if stats_value > 0:
            main_stats += ' {key}={value:.2f}'.format(key=good_to_gcsim_stats[stats_key], value=stats_value)
    main_stats += '; #main\n'
    result += main_stats

    # Character sub stats
    sub_stats = '{name} add stats'.format(name=character_name)
    for stats_key, stats_value in character['sub_stats'].items():
        if stats_value > 0:
            sub_stats += ' {key}={value:.2f}'.format(key=good_to_gcsim_stats[stats_key], value=stats_value)
    sub_stats += '; #subs\n'
    result += sub_stats

    return result


def gcsim_team(character_info, character_list):
    result = ''
    for character in character_list:
        result += character_to_gcsim(character_info[character])
        result += '\n'

    return result


def read_good_file(good_data):
    character_info = dict()

    for character in good_data['characters']:
        key = character['key']
        ascension = character['ascension']
        max_level = (20 + ascension * 20) if ascension <= 1 else (40 + (ascension - 1) * 10)

        character_info[key] = {
            'key': key,
            'level': character['level'],
            'max_level': max_level,
            'constellation': character['constellation'],
            'talent_1': character['talent']['auto'],
            'talent_2': character['talent']['skill'],
            'talent_3': character['talent']['burst'],
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

    for weapon in good_data['weapons']:
        ascension = weapon['ascension']
        if weapon['location'] in character_info:
            max_level = (20 + ascension * 20) if ascension <= 1 else (40 + (ascension - 1) * 10)

            character_info[weapon['location']]['weapon'] = {
                'key': weapon['key'],
                'level': weapon['level'],
                'max_level': max_level,
                'refine': weapon['refinement']
            }

    for artifact in good_data['artifacts']:
        if artifact['location'] in character_info:
            character = character_info[artifact['location']]
            stat_value = artifact_main_stat[artifact['mainStatKey']][artifact['level']]
            if artifact['mainStatKey'] in percent_stats:
                stat_value /= 100
            character['main_stats'][artifact['mainStatKey']] += stat_value

            for substats in artifact['substats']:
                if substats['key']:
                    stat_value = substats['value']
                    if substats['key'] in percent_stats:
                        stat_value /= 100
                    character['sub_stats'][substats['key']] += stat_value

            if artifact['setKey'] in character['artifact_set']:
                character['artifact_set'][artifact['setKey']] += 1
            else:
                character['artifact_set'][artifact['setKey']] = 1

    return character_info


def create_gcsim_file(character_info, actions, filename, iterations=1000):
    with open(filename, 'w') as file:
        file.write('# Character Info\n')
        file.write(gcsim_team(character_info, actions['team']))
        file.write('\n')

        file.write('# Simulation Config\n')
        file.write('options debug=true iteration={iterations} duration={duration} workers=30 mode={mode};\n'.format(
            iterations=iterations, duration=actions['simulation_length'], mode=actions['mode']))
        file.write('target lvl=100 resist=.1;\n')
        file.write('energy every interval=240,360 amount=1;\n')
        file.write('\n\n')

        file.write('# Actions\n')
        file.write(actions['actions'])


def run_team(character_info, team_name, iterations=1000):
    gcsim_exec_path = os.path.join('.', 'gcsim')
    actions_path = os.path.join('actions', team_name + '.txt')
    create_gcsim_file(character_info, actions_dict[team_name], actions_path, iterations=iterations)

    dps_regex = r"resulting in (?P<mean>[\d\.]+) dps \(min: (?P<min_dps>[\d\.]+) max: (?P<max_dps>[\d\.]+) std: (?P<std>[\d\.]+)\)"
    gcsim_result = subprocess.run([gcsim_exec_path, '-c', actions_path], capture_output=True)
    dps = re.search(dps_regex, gcsim_result.stdout.decode('utf-8'), re.MULTILINE)

    print('DPS:', dps['mean'])
    print('Min:', dps['min_dps'])
    print('Max:', dps['max_dps'])
    print('Std:', dps['std'])


def read_artifacts(good_data):
    artifact_data = {
        'flower': [],
        'plume': [],
        'sands': [],
        'goblet': [],
        'circlet': []
    }

    for artifact in good_data['artifacts']:
        new_artifact = {
            'id': artifact['Id'],
            'level': artifact['level'],
            'set_key': artifact['setKey'],
            'main_stat_key': artifact['mainStatKey'],
            'sub_stats': {},
            'empty_sub_stats': 0,
            'missing_sub_stats': math.ceil((20 - artifact['level']) / 4)
        }
        for sub_stat in artifact['substats']:
            if sub_stat['key'] is None:
                new_artifact['empty_sub_stats'] += 1
            elif sub_stat['key'] in percent_stats:
                new_artifact['sub_stats'][sub_stat['key']] = sub_stat['value'] / 100
            else:
                new_artifact['sub_stats'][sub_stat['key']] = sub_stat['value']

        artifact_data[artifact['slotKey']].append(new_artifact)

    return artifact_data


def main():
    good_filename = 'data/data.json'
    team_name = 'hyper_raiden'

    with open(good_filename) as good_file:
        good_data = json.load(good_file)

    artifact_data = read_artifacts(good_data)

    character_info = read_good_file(good_data)
    run_team(character_info, team_name, iterations=100)


if __name__ == '__main__':
    main()
