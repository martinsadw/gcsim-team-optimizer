from gcsim_utils import GcsimData
import processing
import restriction


def gradient_score_hook(optimizer, score, update_frequency=100, iterations=1000, sub_stat_multiplier=2):
    team_list = optimizer.actions['team']
    stat_subset = restriction.get_stat_subset(team_list, character_lock=optimizer.character_lock,
                                              equipment_lock=optimizer.equipment_lock)

    have_gradient = ('gradient_stat_value' in optimizer.extra_data)
    if not have_gradient or (optimizer.current_iteration + 1) % update_frequency == 0:
        print('{C}alculating team gradient...'.format(C='C' if not have_gradient else 'Rec'))
        team_info = optimizer.data.get_team_build_by_vector(team_list, optimizer.best_key)
        gcsim_data = GcsimData(team_info, optimizer.actions, iterations=iterations, parsed_data=optimizer.parsed_data)
        team_gradient = processing.sub_stats_gradient(gcsim_data, stat_subset=stat_subset,
                                                      output_dir=optimizer.output_dir,
                                                      sub_stat_multiplier=sub_stat_multiplier,
                                                      runner=optimizer.runner)

        gradient_score = optimizer.data.get_equipment_vector_weighted_options(team_list, team_gradient)

        optimizer.extra_data['gradient_stat_value'] = team_gradient
        optimizer.extra_data['gradient_score'] = gradient_score

    for i, slot in enumerate(score):
        for j, equipment in enumerate(slot):
            score[i][j] = equipment * optimizer.extra_data['gradient_score'][i][j]

    return score
