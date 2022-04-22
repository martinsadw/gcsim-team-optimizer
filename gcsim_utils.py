import os
import re
import subprocess

from artifact import Artifact
from gcsim_names import good_to_gcsim_stats

import reader


def character_to_gcsim(character_info):
    character = character_info['character']
    character_name = character['key'].lower()

    weapon = character_info['weapon']
    weapon_name = weapon.key.lower()

    # Character base stats
    result = '{name} char lvl={level}/{max_level} cons={cons} talent={t1},{t2},{t3};\n'.format(
        name=character_name, level=character['level'], max_level=character['max_level'],
        cons=character['constellation'], t1=character['talent_1'], t2=character['talent_2'], t3=character['talent_3'])

    # Character Weapon
    result += '{name} add weapon="{weapon}" refine={refine} lvl={level}/{max_level};\n'.format(
        name=character_name, weapon=weapon_name, level=weapon.level, max_level=weapon.max_level,
        refine=weapon.refinement)

    artifact_stats = Artifact.calculate_artifact_stats(character_info['artifacts'])

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

    # Additional stats
    if 'extra_stats' in character_info:
        extra_stats = '{name} add stats'.format(name=character_name)
        for stats_key, stats_value in character_info['extra_stats'].items():
            extra_stats += ' {key}={value:.2f}'.format(key=good_to_gcsim_stats[stats_key], value=stats_value)
        extra_stats += '; #extra\n'
        result += extra_stats

    return result


def create_gcsim_file(team_info, actions, filename, iterations=1000):
    with open(filename, 'w') as file:
        file.write('# Character Info\n')
        for character_info in team_info:
            file.write(character_to_gcsim(character_info))
            file.write('\n')
        file.write('\n')

        file.write('# Simulation Config\n')
        file.write('options swap_delay=12 debug=true iteration={iterations} duration={duration} workers=30 mode={mode};\n'.format(
            iterations=iterations, duration=actions['simulation_length'], mode=actions['mode']))
        file.write('target lvl=100 resist=.1;\n')
        file.write('energy every interval=480,720 amount=1;\n')
        file.write('\n\n')

        file.write('# Actions\n')
        file.write(actions['actions'])


def run_team(gcsim_filename):
    gcsim_exec_path = os.path.join('.', 'gcsim')

    dps_regex = r"resulting in (?P<mean>-?[\d\.]+) dps \(min: (?P<min_dps>-?[\d\.]+) max: (?P<max_dps>-?[\d\.]+) std: (?P<std>-?[\d\.]+)\)"
    gcsim_result = subprocess.run([gcsim_exec_path, '-c', gcsim_filename], capture_output=True)
    dps = re.search(dps_regex, gcsim_result.stdout.decode('utf-8'), re.MULTILINE)

    # print('DPS:', dps['mean'])
    # print('Min:', dps['min_dps'])
    # print('Max:', dps['max_dps'])
    # print('Std:', dps['std'])
    return dps


def gcsim_fitness(vector, data, actions, iterations=10, force_write=False, validation_penalty=1, fitness_cache=None,
                  stats=None, temp_actions_path=None):
    cache_key = tuple(vector)
    if fitness_cache is not None:
        if cache_key in fitness_cache:
            return fitness_cache[cache_key]

    characters_data, weapons_data, artifacts_data = data
    team_info = reader.get_team_build_by_vector(characters_data, weapons_data, artifacts_data, actions['team'], vector)

    is_team_valid = reader.validate_team(actions['team'], vector)
    if not is_team_valid:
        if stats is not None:
            if 'invalid' not in stats:
                stats['invalid'] = 0
            stats['invalid'] += 1

        if validation_penalty >= 1:
            return 0

    if temp_actions_path is None:
        temp_actions_path = os.path.join('actions', 'temp_gcsim')
        os.makedirs(temp_actions_path, exist_ok=True)

    gcsim_filename = os.path.join(temp_actions_path, '_'.join([str(x) for x in vector]) + '.txt')
    if force_write or not os.path.exists(gcsim_filename):
        create_gcsim_file(team_info, actions, gcsim_filename, iterations=iterations)
    fitness = run_team(gcsim_filename)

    if stats is not None:
        if 'evaluation' not in stats:
            stats['evaluation'] = 0
        stats['evaluation'] += iterations

    dps = float(fitness['mean'])
    if not is_team_valid:
        dps *= (1 - validation_penalty)

    if fitness_cache is not None:
        fitness_cache[cache_key] = dps

    return dps
