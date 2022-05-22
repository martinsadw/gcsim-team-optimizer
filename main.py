import datetime
import json
import os
import pickle
import time

import restriction
from gcsim_utils import gcsim_fitness
from genetic_algorithm import GeneticAlgorithm

from artifact import artifact_quality
from gcsim_utils import GcsimData
from good_utils import GoodData
import processing
from stats import Stats
from hooks.gradient import gradient_score_hook
from hooks.set_restriction import set_score_hook, set_penalty_hook

import action_files


def default_json(x):
    if hasattr(x, 'to_json'):
        return x.to_json()
    elif hasattr(x, '__dict__'):
        return x.__dict__
    else:
        return str(x)


def main():
    restrictions = {
        'raw_sets': {
            'hutao': {
                'penalty': 0.0,
                'sets': [
                    {'gladiatorsfinale': 4},
                    {'gladiatorsfinale': 2, 'shimenawasreminiscence': 2},
                    {'wandererstroupe': 4},
                ]
            }
        },
        'sets': {
            '2sets': [
                'gladiatorsfinale',
                'shimenawasreminiscence',
                'crimsonwitchofflames',
            ],
            '4set': [
                'wandererstroupe',
            ],
        },
        'character_lock': [
            'Zhongli',
            'Albedo',
        ],
        'equipment_lock': {
            'Bennett': ['flower', 'plume'],
            'Noelle': ['goblet'],
            'HuTao': ['weapon', 'circlet'],
            'Xingqiu': ['goblet'],
        },
    }

    good_filename = 'data/data.json'
    gcsim_actions = action_files.ayato_electrocharge

    team_slug = '-'.join(gcsim_actions['team'])
    output_dir = os.path.join('output', '{}_{}'.format(
        datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
        team_slug
    ))
    os.makedirs(output_dir)

    gcsim_filename = os.path.join(output_dir, 'actions.txt')

    # TODO(andre): Allow to pass special parameters to the final gcsim file
    #  Examples:
    #  Hu Tao stating HP: 'start_hp=3000'
    #  Husk of Opulent Dreams initial stack: '+params=[stacks=4]'

    data = GoodData.from_filename(good_filename)
    data.upgrade_artifacts()
    data.upgrade_characters()
    data.upgrade_weapons()

    ##########################

    # Add Ayato
    data.add_character('KamisatoAyato')

    # Make Noelle C6
    noelle = data.get_character_by_name('Noelle')
    noelle.constellation = 6

    # # Equip Deathmatch on Hu Tao
    # deathmatch = data.get_weapons_by_name('Deathmatch')[0]
    # hutao_weapon = data.get_weapon_by_character('HuTao')
    # hutao_weapon.location = deathmatch.location
    # deathmatch.location = 'HuTao'

    ##########################

    # # Substat gradient
    # team_vector = data.get_team_vector(gcsim_actions['team'])
    # # team_vector = [0, 4, 6, 6, 0, 4, 3, 10, 8, 3, 20, 19, 4, 19, 31, 18, 16, 17, 5, 12, 13, 12, 37, 11]
    # team_info = data.get_team_build_by_vector(gcsim_actions['team'], team_vector)
    # gcsim_data = GcsimData(team_info, gcsim_actions, iterations=1000)
    # stat_subset = restriction.get_stat_subset(gcsim_actions['team'],
    #                                           character_lock=restrictions['character_lock'],
    #                                           equipment_lock=restrictions['equipment_lock'])
    # team_gradient = processing.sub_stats_gradient(gcsim_data, stat_subset=stat_subset, output_dir=output_dir)

    ##########################

    # # Artifact set count
    # good_filename_2 = 'data/data_2.json'
    # data_2 = GoodData.from_filename(good_filename_2)
    # processing.plot_set_count([data, data_2], ['Data 1', 'Data 2'],
    #                           artifact_quality, thresholds=[0.9, 0.8, 0.7, 0.6, 0.5])

    ##########################

    # Genetic Algorithm Class
    set_restrictions = {
        'noelle': {
            'penalty': 0.0,
            'sets': [
                {'gladiator': 4},
                {'huskofopulentdreams': 4},
            ]
        },
        'zhongli': {
            'penalty': 0.0,
            'sets': [
                {'tenacityofthemillelith': 4},
            ]
        },
    }
    ga = GeneticAlgorithm(data, gcsim_fitness, output_dir=output_dir)
    ga.add_equipment_score_hook(gradient_score_hook, iterations=1000, update_frequency=100)
    ga.add_equipment_score_hook(set_score_hook, set_restrictions)
    ga.add_penalty_hook(set_penalty_hook, set_restrictions, score_boost=50)

    build_vector, fitness = ga.run(gcsim_actions, restrictions)
    team_info = data.get_team_build_by_vector(gcsim_actions['team'], build_vector)

    with open(os.path.join(output_dir, 'build_{}.json'.format(team_slug)), 'w') as build_file:
        json_object = json.dumps(team_info, indent=4, default=default_json)
        build_file.write(json_object)

    with open(os.path.join(output_dir, 'metadata.txt'), 'w') as metadata_file:
        metadata_file.writelines([
            'Best DPS: {}\n'.format(fitness),
            'Build: {}\n'.format(build_vector)
        ])

    gcsim_data = GcsimData(team_info, gcsim_actions, iterations=1000)
    gcsim_data.write_file(os.path.join(output_dir, 'actions_file.txt'))

    # # TODO(rodrigo): Save last gradient instead of first
    # with open(os.path.join(self.output_dir, 'gradient.json'), 'w') as gradient_file:
    #     gradient_data = dict(zip(actions['team'], self.team_gradient))
    #     json_object = json.dumps(gradient_data, indent=4)
    #     gradient_file.write(json_object)

    with open(os.path.join(output_dir, 'ga_debug.pickle'), 'wb') as ga_debug_file:
        pickle.dump(ga, ga_debug_file)

    ##########################

    # # Team Vector
    # team_vector = data.get_team_vector(gcsim_actions['team'])
    # print(team_vector)
    # team_info = data.get_team_build_by_vector(gcsim_actions['team'], team_vector)
    # pprint(team_info)

    ##########################

    # # Validation
    # team_vector = data.get_team_vector(gcsim_actions['team'])
    # print(team_vector)
    # print(data.validate_team(gcsim_actions['team'], team_vector))

    ##########################

    # # Team Reader
    # team_info = data.get_team_build(gcsim_actions['team'])
    # gcsim_data = GcsimData(team_info, gcsim_actions, iterations=100)
    # dps = gcsim_data.run(gcsim_filename, keep_file=True)
    # print(dps['mean'])

    ##########################

    # # Check Vector
    # team_vector = [0, 20, 7, 20, 0, 21, 5, 29, 25, 32, 11, 16, 5, 21, 32, 12, 18, 14, 1, 12, 26, 13, 32, 10]
    # team_info = data.get_team_build_by_vector(gcsim_actions['team'], team_vector)
    # gcsim_data = GcsimData(team_info, gcsim_actions, iterations=100)
    # dps = gcsim_data.run(gcsim_filename, keep_file=True)
    # print(dps['mean'])


if __name__ == '__main__':
    # BUG:(andre): Adding a new character should automaticaly equip a weapon since it's impossible to have a character
    #  with no weapon in game.
    # BUG:(andre): Calculating the gradient of a build with error result in a gradient full of zeros. This gives an
    #  error during normalization.
    # TODO(andre): Add restrictions to the optimization (e.g. fix a 4 piece artifact set)
    # TODO(andre): Allow the optimization of two teams simultaneously (e.g. for the two sides of the spiral abyss)
    # TODO(andre): Instead of using the last population for the final gcsim execution, the result should use the best
    #  individuals found so far. Idealy, all individuals within the standard error should be rerun.
    # TODO(andre): Improve the search to take artifact sets in consideration
    start = time.perf_counter()
    main()
    duration = time.perf_counter() - start
    print('Execution duration: {h:d}:{m:02d}:{s:06.3f}'.format(h=int(duration / 3600),
                                                               m=int((duration % 3600) / 60),
                                                               s=duration % 60))
