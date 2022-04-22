import json
import os
import time
from pprint import pprint

from gcsim_utils import gcsim_fitness
from genetic_algorithm import GeneticAlgorithm
from gcsim_utils import create_gcsim_file, run_team

from artifact import artifact_quality
from good_utils import GoodData
import stats

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

    data = GoodData.from_filename(good_filename)
    data.upgrade_artifacts()
    data.upgrade_characters()
    data.upgrade_weapons()

    data.add_character('KamisatoAyato')

    ##########################

    # # Substat gradient
    # team_vector = data.get_team_vector(actions_dict[team_name]['team'])
    # # team_vector = [0, 4, 6, 6, 0, 4, 3, 10, 8, 3, 20, 19, 4, 19, 31, 18, 16, 17, 5, 12, 13, 12, 37, 11]
    # team_gradient = stats.sub_stats_gradient(data, actions_dict[team_name], team_vector, iterations=1000)

    ##########################

    # # Artifact set count
    # good_filename_2 = 'data/data_2.json'
    # data_2 = GoodData.from_filename(good_filename_2)
    # stats.plot_set_count([data, data_2], ['Data 1', 'Data 2'],
    #                      artifact_quality, thresholds=[0.9, 0.8, 0.7, 0.6, 0.5])

    ##########################

    # # Genetic Algorithm Class
    # ga = GeneticAlgorithm(data, gcsim_fitness)
    # build_vector, fitness = ga.run(actions_dict[team_name])
    # team_info = data.get_team_build_by_vector(actions_dict[team_name]['team'], build_vector)
    # pprint(team_info)
    #
    # print('Best DPS:', fitness)
    # print('Build:', build_vector)

    ##########################

    # # Team Vector
    # team_vector = data.get_team_vector(actions_dict[team_name]['team'])
    # print(team_vector)
    # team_info = data.get_team_build_by_vector(actions_dict[team_name]['team'], team_vector)
    # pprint(team_info)

    ##########################

    # # Validation
    # team_vector = data.get_team_vector(actions_dict[team_name]['team'])
    # print(team_vector)
    # print(data.validate_team(actions_dict[team_name]['team'], team_vector))

    ##########################

    # # Team Reader
    # team_info = data.get_team_build(actions_dict[team_name]['team'])
    # create_gcsim_file(team_info, actions_dict[team_name], gcsim_filename, iterations=100)
    # dps = run_team(gcsim_filename)
    # print(dps['mean'])

    ##########################

    # # Check Vector
    # team_vector = [0, 20, 7, 20, 0, 21, 5, 29, 25, 32, 11, 16, 5, 21, 32, 12, 18, 14, 1, 12, 26, 13, 32, 10]
    # team_info = data.get_team_build_by_vector(actions_dict[team_name]['team'], team_vector)
    # create_gcsim_file(team_info, actions_dict[team_name], gcsim_filename, iterations=100)
    # dps = run_team(gcsim_filename)
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
