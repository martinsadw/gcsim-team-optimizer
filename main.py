import json
import os
import time
from pprint import pprint

from gcsim_utils import gcsim_fitness
from genetic_algorithm import genetic_algorithm
from gcsim_utils import create_gcsim_file, run_team

import reader
import artifact
import character
import weapon

from actions import actions_dict


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
    start = time.perf_counter()
    main()
    duration = time.perf_counter() - start
    print('Execution duration: {h:d}:{m:02d}:{s:.3f}'.format(h=int(duration / 3600),
                                                             m=int((duration % 3600) / 60),
                                                             s=duration % 60))
