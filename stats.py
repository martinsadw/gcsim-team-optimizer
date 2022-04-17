import math
import os
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

from artifact_data import artifact_set_readable_short,  artifact_set_readable, artifact_max_sub_stat
from gcsim_utils import create_gcsim_file, run_team
import reader


def artifacts_set_count(artifacts_data, weight_function=None):
    if weight_function is None:
        def weight_function(artifact): return 1

    set_count = defaultdict(int)
    for artifacts_piece in artifacts_data.values():
        for artifact_piece in artifacts_piece:
            if artifact_piece['level'] >= 20 and artifact_piece['rarity'] >= 5:
                key = artifact_set_readable_short[artifact_piece['set_key']]
                set_count[key] += weight_function(artifact_piece)

    return set_count


def artifacts_set_count_threshold(artifacts_data, thresholds, weight_function):
    set_count = defaultdict(lambda: [0] * len(thresholds))
    for artifacts_piece in artifacts_data.values():
        for artifact_piece in artifacts_piece:
            if artifact_piece['level'] >= 0 and artifact_piece['rarity'] >= 5:
                key = artifact_set_readable_short[artifact_piece['set_key']]
                for bin_number, threshold in enumerate(thresholds):
                    if weight_function(artifact_piece) > threshold:
                        set_count[key][bin_number] += 1

    return set_count


def plot_set_count(data, labels, weight_function, thresholds=None):
    if thresholds is None:
        thresholds = [0]

    fig, ax = plt.subplots()

    quant_data = len(data)
    quant_bins = len(thresholds)

    bar_spacing = 0.2
    bar_size = (1 - bar_spacing) / quant_data
    bar_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    thresholds_alphas = np.linspace(1, 0, quant_bins + 1)

    set_counts = []
    names = set()
    for good_data in data:
        artifacts_data = reader.read_artifacts(good_data)
        artifacts_set = artifacts_set_count_threshold(artifacts_data, thresholds, weight_function)
        set_counts.append(artifacts_set)
        names.update(artifacts_set.keys())

    names = sorted(names, reverse=True)
    yticks = np.arange(len(names))

    for i in range(quant_data):
        set_count = set_counts[i]
        label = labels[i]

        for j in range(quant_bins):
            values = [set_count[key][j] for key in names]
            bin_label = (label if j == 0 else None)
            # bin_size = bar_size * ((quant_bins - j + 1) / quant_bins)
            bin_size = bar_size
            ax.barh(yticks - bar_size * i + bar_spacing, values, alpha=thresholds_alphas[j],
                    height=bin_size, label=bin_label, color=bar_colors[i])

    ax.set_yticks(yticks, names)

    ax.legend()
    if weight_function is None:
        ax.set_title('Number of artifacts')
    elif weight_function.__name__ == '<lambda>':
        ax.set_title(f'Number of artifacts by custom function')
    else:
        ax.set_title(f'Number of artifacts by {weight_function.__name__}()')
    fig.tight_layout()
    plt.show()


def sub_stats_gradient(data, actions, vector, iterations=1000):
    characters_data, weapons_data, artifacts_data = data

    team_gradient = []

    temp_actions_path = os.path.join('actions', 'temp_sub_stats')
    os.makedirs(temp_actions_path, exist_ok=True)

    temp_actions_filename = os.path.join(temp_actions_path, 'base.txt')
    team_info = reader.get_team_build_by_vector(characters_data, weapons_data, artifacts_data, actions['team'], vector)
    create_gcsim_file(team_info, actions, temp_actions_filename, iterations=iterations)
    base_dps = run_team(temp_actions_filename)
    # print('Base dps:', base_dps['mean'])
    # print('Std. dev.:', base_dps['std'])
    # print('Error:', float(base_dps['std']) / math.sqrt(iterations))

    sub_stat_rarity = 5
    sub_stat_multiplier = 2

    # Finite Difference Coefficients Calculator
    # https://web.media.mit.edu/~crtaylor/calculator.html
    calculation_points = [0, 1]
    points_coefficients = [-1, 1]
    # calculation_points = [-1, 1]
    # points_coefficients = [-1/2, 1/2]
    for i, character in enumerate(actions['team']):
        character_gradient = dict()
        for sub_stat, sub_stat_values in artifact_max_sub_stat.items():
            deviation = 0
            for point, coefficient in zip(calculation_points, points_coefficients):
                # The point 0 don't need to be recalculated every time for each substat
                if point == 0:
                    deviation += float(base_dps['mean']) * coefficient
                    continue

                point_str = ('m' + str(-point) if point < 0 else 'p' + str(point))
                filename = character + '_' + point_str + '_' + sub_stat + '.txt'
                temp_actions_filename = os.path.join(temp_actions_path, filename)
                team_info = reader.get_team_build_by_vector(characters_data, weapons_data, artifacts_data,
                                                            actions['team'], vector)

                team_info[i]['extra_stats'] = {
                    sub_stat: sub_stat_values[str(sub_stat_rarity)] * sub_stat_multiplier * point
                }

                create_gcsim_file(team_info, actions, temp_actions_filename, iterations=iterations)
                dps = float(run_team(temp_actions_filename)['mean'])
                deviation += dps * coefficient

            deviation /= sub_stat_multiplier
            # print(f'{character:18} {sub_stat:10} {deviation:8.2f}')
            character_gradient[sub_stat] = deviation

        team_gradient.append(character_gradient)

    return team_gradient
