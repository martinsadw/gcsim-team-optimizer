from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

from artifact_data import artifact_set_readable_short,  artifact_set_readable
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
