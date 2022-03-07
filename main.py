import json
import os
import random
import re
import subprocess
from pprint import pprint

from artifact_data import artifact_main_stat
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

    # print('DPS:', dps['mean'])
    # print('Min:', dps['min_dps'])
    # print('Max:', dps['max_dps'])
    # print('Std:', dps['std'])
    return dps


def gcsim_fitness(data, vector):
    characters_data, weapons_data, artifacts_data, actions = data
    team_info = reader.get_team_build_by_vector(characters_data, weapons_data, artifacts_data, actions['team'], vector)

    temp_gcsim_path = os.path.join('actions', 'temp_gcsim')
    gcsim_filename = os.path.join(temp_gcsim_path, '_'.join([str(x) for x in vector]) + '.txt')
    if not os.path.exists(gcsim_filename):
        create_gcsim_file(team_info, actions, gcsim_filename, iterations=10)
    fitness = run_team(gcsim_filename)

    return float(fitness['mean'])


def genetic_algorithm(data, fitness_function):
    characters_data, weapons_data, artifacts_data, actions = data

    temp_gcsim_path = os.path.join('actions', 'temp_gcsim')
    os.makedirs(temp_gcsim_path, exist_ok=True)

    quant_options = reader.get_equipment_vector_quant_options(weapons_data, artifacts_data, actions['team'])

    best_fitness = 0
    best_vector = []
    num_iterations = 100
    for i in range(num_iterations):
        if i % 5 == 0:
            print('Iteration {i}/{max} ({percent:.2f}%)'.format(i=i, max=num_iterations,
                                                                percent=(i / num_iterations) * 100))

        solution = [random.randrange(quant) for quant in quant_options]
        fitness = fitness_function(data, solution)

        if best_fitness < fitness:
            best_fitness = fitness
            best_vector = solution

    return best_vector, best_fitness


def main():
    good_filename = 'data/data.json'
    team_name = 'hutao_xingqiu_albedo_zhongli'
    gcsim_filename = os.path.join('actions', team_name + '.txt')

    # TODO(andre): Allow to pass special parameters to the final gcsim file
    # Examples:
    # Hu Tao stating HP: 'start_hp=3000'
    # Husk of Opulent Dreams initial stack: '+params=[stacks=4]'

    # TODO(andre): Allow to change the default passive energy generation
    # i.e. 'energy every interval=240,360 amount=1;'

    with open(good_filename) as good_file:
        good_data = json.load(good_file)

    artifacts_data = reader.read_artifacts(good_data)
    weapons_data = reader.read_weapons(good_data)
    characters_data = reader.read_characters(good_data)

    data = (characters_data, weapons_data, artifacts_data, actions_dict[team_name])
    build_vector, fitness = genetic_algorithm(data, gcsim_fitness)

    # solution = [0,  15, 15, 18,  8, 13,
    #             6,   5,  6,  4,  6,  4,
    #             0,   1,  1,  0,  2,  2,
    #             10,  9,  9,  6, 19,  6]
    team_info = reader.get_team_build_by_vector(characters_data, weapons_data, artifacts_data,
                                                actions_dict[team_name]['team'], build_vector)
    pprint(team_info)

    print('Best DPS:', fitness)
    print('Build:', build_vector)

    # team_info = reader.get_team_build(characters_data, weapons_data, artifacts_data, actions_dict[team_name]['team'])
    # create_gcsim_file(team_info, actions_dict[team_name], gcsim_filename, iterations=100)
    # run_team(gcsim_filename)


if __name__ == '__main__':
    main()
