import json
import os
import random
import re
import subprocess
from pprint import pprint

import numpy as np

import artifact
import character
import weapon
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


def gcsim_fitness(vector, data, iterations=10, force_write=False, validation_penalty=1):
    characters_data, weapons_data, artifacts_data, actions = data
    team_info = reader.get_team_build_by_vector(characters_data, weapons_data, artifacts_data, actions['team'], vector)

    is_team_valid = reader.validate_team(actions['team'], vector)
    if validation_penalty >= 1 and not is_team_valid:
        return 0

    temp_gcsim_path = os.path.join('actions', 'temp_gcsim')
    gcsim_filename = os.path.join(temp_gcsim_path, '_'.join([str(x) for x in vector]) + '.txt')
    if force_write or not os.path.exists(gcsim_filename):
        create_gcsim_file(team_info, actions, gcsim_filename, iterations=iterations)
    fitness = run_team(gcsim_filename)

    dps = float(fitness['mean'])
    if not is_team_valid:
        dps *= (1 - validation_penalty)

    return dps


def genetic_algorithm(data, fitness_function):
    characters_data, weapons_data, artifacts_data, actions = data

    temp_gcsim_path = os.path.join('actions', 'temp_gcsim')
    os.makedirs(temp_gcsim_path, exist_ok=True)

    quant_options = reader.get_equipment_vector_quant_options(weapons_data, artifacts_data, actions['team'])
    vector_length = len(quant_options)
    character_length = 6
    quant_characters = int(vector_length / character_length)

    best_fitness = -1
    best_vector = []

    num_iterations = 500
    population_size = 200
    selection_size = 40

    population = np.array([[random.randrange(quant) for quant in quant_options] for i in range(population_size)])
    # population[0] = reader.get_team_vector(characters_data, weapons_data, artifacts_data, actions['team'])
    fitness = np.apply_along_axis(fitness_function, 1, population, data, validation_penalty=0.1)

    # Sort the population using the fitness
    population_order = fitness.argsort()[::-1]
    population = population[population_order]
    fitness = fitness[population_order]

    for i in range(num_iterations):
        print('Iteration {i}/{max} ({percent:.2f}%)'
              .format(i=i, max=num_iterations, percent=(i / num_iterations) * 100))

        new_population = population.copy()
        # new_population[selection_size:] = 0

        print(fitness)
        for j in range(selection_size, population_size):
            r = np.arange(vector_length)

            # # Random selection
            # parent_1 = population[random.randrange(population_size)]
            # parent_2 = population[random.randrange(population_size)]

            # Roulette selection
            parents = random.choices(range(len(fitness)), fitness, k=2)
            parent_1 = population[parents[0]]
            parent_2 = population[parents[1]]

            #############

            # # Two points crossover
            # cut_point1 = random.randrange(vector_length)
            # cut_point2 = random.randrange(vector_length)
            #
            # mask1 = r < cut_point1
            # mask2 = r < cut_point2
            # crossover_mask = mask1 ^ mask2
            #
            # new_individual = np.choose(crossover_mask, [parent_1, parent_2])

            # Character crossover
            c = random.randrange(quant_characters)
            character_mask = (r >= c * character_length) & (r < (c + 1) * character_length)

            new_individual = np.choose(character_mask, [parent_1, parent_2])

            #############

            # # Random mutation
            # mutation_chance = 0.1
            # mutation_mask = (np.random.rand(vector_length) < mutation_chance)
            # mutation = np.array([random.randrange(quant) for quant in quant_options])
            #
            # new_individual = np.choose(mutation_mask, [new_individual, mutation])

            # Per character mutation
            c = random.randrange(quant_characters)
            character_mask = (r >= c * character_length) & (r < (c + 1) * character_length)
            mutation_chance = 0.1
            mutation_mask = (np.random.rand(vector_length) < mutation_chance) & character_mask
            mutation = np.array([random.randrange(quant) for quant in quant_options])

            new_individual = np.choose(mutation_mask, [new_individual, mutation])

            new_population[j] = new_individual

        # Calculate the new population fitness
        new_fitness = np.apply_along_axis(fitness_function, 1, new_population, data)

        # Sort the population using the fitness
        population_order = new_fitness.argsort()[::-1]
        new_population = new_population[population_order]
        new_fitness = new_fitness[population_order]

        if best_fitness < new_fitness[0]:
            best_fitness = new_fitness[0]
            best_vector = new_population[0]

        population = new_population
        fitness = new_fitness
        print('Partial Fitness:', best_fitness)
        print('Partial Build:', best_vector)

    final_fitness = np.apply_along_axis(fitness_function, 1, population, data, iterations=1000, force_write=True)
    population_order = final_fitness.argsort()[::-1]
    population = population[population_order]
    final_fitness = final_fitness[population_order]

    print('Final Fitness:', final_fitness)
    print('Final Build:', population[0])

    # return best_vector, best_fitness
    return population[0], final_fitness[0]


def main():
    good_filename = 'data/data.json'
    # team_name = 'hutao_xingqiu_albedo_zhongli'
    # team_name = 'hyper_raiden'
    team_name = 'raiden_national'
    gcsim_filename = os.path.join('actions', team_name + '.txt')

    # TODO(andre): Allow to pass special parameters to the final gcsim file
    # Examples:
    # Hu Tao stating HP: 'start_hp=3000'
    # Husk of Opulent Dreams initial stack: '+params=[stacks=4]'

    # TODO(andre): Allow to change the default passive energy generation
    # i.e. 'energy every interval=240,360 amount=1;'

    with open(good_filename) as good_file:
        good_data = json.load(good_file)

    characters_data = reader.read_characters(good_data)
    weapons_data = reader.read_weapons(good_data)
    artifacts_data = reader.read_artifacts(good_data)

    # Upgrade Characters and Equipments
    character.upgrade_characters(characters_data)
    weapon.upgrade_weapons(weapons_data)
    artifact.upgrade_artifacts(artifacts_data)

    # Genetic Algorithm
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

    # # Team Vector
    # team_vector = reader.get_team_vector(characters_data, weapons_data, artifacts_data,
    #                                      actions_dict[team_name]['team'])
    # print(team_vector)
    # team_info = reader.get_team_build_by_vector(characters_data, weapons_data, artifacts_data,
    #                                             actions_dict[team_name]['team'], team_vector)
    # pprint(team_info)

    # # Validation
    # team_vector = reader.get_team_vector(characters_data, weapons_data, artifacts_data,
    #                                      actions_dict[team_name]['team'])
    # print(reader.validate_team(actions_dict[team_name]['team'], team_vector))

    # # Team Reader
    # team_info = reader.get_team_build(characters_data, weapons_data, artifacts_data, actions_dict[team_name]['team'])
    # create_gcsim_file(team_info, actions_dict[team_name], gcsim_filename, iterations=100)
    # dps = run_team(gcsim_filename)
    # print(dps['mean'])

    # # Check Vector
    # team_vector = [0, 20, 7, 20, 0, 21, 5, 29, 25, 32, 11, 16, 5, 21, 32, 12, 18, 14, 1, 12, 26, 13, 32, 10]
    # team_info = reader.get_team_build_by_vector(characters_data, weapons_data, artifacts_data,
    #                                             actions_dict[team_name]['team'], team_vector)
    # create_gcsim_file(team_info, actions_dict[team_name], gcsim_filename, iterations=100)
    # dps = run_team(gcsim_filename)
    # print(dps['mean'])


if __name__ == '__main__':
    main()
