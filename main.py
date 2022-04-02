import json
import os
import time
from pprint import pprint

from gcsim_utils import gcsim_fitness
from genetic_algorithm import genetic_algorithm
from gcsim_utils import create_gcsim_file, run_team

import artifact
import character
import reader
import stats
import weapon

from actions import actions_dict


def main():
    good_filename = 'data/data.json'
    # team_name = 'hutao_xingqiu_albedo_zhongli'
    # team_name = 'hyper_raiden'
    # team_name = 'raiden_national'
    # team_name = 'kokomi_electrocharged'
    # team_name = 'eula_shield'
    # team_name = 'eula_bennett'
    # team_name = 'ayato_overvape'
    team_name = 'ayato_electrocharge'
    gcsim_filename = os.path.join('actions', team_name + '.txt')

    # TODO(andre): Allow to pass special parameters to the final gcsim file
    #  Examples:
    #  Hu Tao stating HP: 'start_hp=3000'
    #  Husk of Opulent Dreams initial stack: '+params=[stacks=4]'

    # TODO(andre): Allow to change the default passive energy generation
    #  i.e. 'energy every interval=240,360 amount=1;'

    with open(good_filename) as good_file:
        good_data = json.load(good_file)

    characters_data = reader.read_characters(good_data)
    weapons_data = reader.read_weapons(good_data)
    artifacts_data = reader.read_artifacts(good_data)

    # Upgrade Characters and Equipments
    character.upgrade_characters(characters_data)
    weapon.upgrade_weapons(weapons_data)
    artifact.upgrade_artifacts(artifacts_data)

    character.add_character(characters_data, 'KamisatoAyato')

    # Substat gradient
    # data = (characters_data, weapons_data, artifacts_data, actions_dict[team_name])
    # team_vector = reader.get_team_vector(characters_data, weapons_data, artifacts_data, actions_dict[team_name]['team'])
    # # team_vector = [0, 4, 6, 6, 0, 4, 3, 10, 8, 3, 20, 19, 4, 19, 31, 18, 16, 17, 5, 12, 13, 12, 37, 11]
    # team_gradient = stats.sub_stats_gradient(data, team_vector, iterations=1000)

    # # Artifact set count
    # good_filename_2 = 'data/data_2.json'
    # with open(good_filename_2) as good_file_2:
    #     good_data_2 = json.load(good_file_2)
    # stats.plot_set_count([good_data, good_data_2], ['Data 1', 'Data 2'],
    #                      artifact.artifact_quality, thresholds=[0.9, 0.8, 0.7, 0.6, 0.5])

    # Genetic Algorithm
    data = (characters_data, weapons_data, artifacts_data, actions_dict[team_name])
    build_vector, fitness = genetic_algorithm(data, gcsim_fitness)
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
    # print(team_vector)
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
    # TODO(andre): Instead of consulting the cache to prevent a gcsim execution, the result should rerun and update the
    #  cache with a new average
    # TODO(andre): Instead of using the last population for the final gcsim execution, the result should use the best
    #  individuals found so far. Idealy, all individuals within the standard error should be rerun.
    # TODO(andre): Improve the search to take artifact sets in consideration
    start = time.perf_counter()
    main()
    duration = time.perf_counter() - start
    print('Execution duration: {h:d}:{m:02d}:{s:06.3f}'.format(h=int(duration / 3600),
                                                               m=int((duration % 3600) / 60),
                                                               s=duration % 60))
