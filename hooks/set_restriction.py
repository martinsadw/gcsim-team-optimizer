from gcsim_utils import GcsimData


def set_score_hook(optimizer, score, set_restrictions, score_boost=50):
    if 'set_score' not in optimizer.extra_data:
        set_score = [[1 for _ in range(quant)] for quant in optimizer.quant_options]
        for i, character in enumerate(optimizer.actions['team']):
            char_key = character.lower()
            if char_key in set_restrictions:
                required_sets = set()
                for artifact_sets in set_restrictions[char_key]['sets']:
                    required_sets |= set(artifact_sets.keys())

                for j, slot_name in enumerate(('flower', 'plume', 'sands', 'goblet', 'circlet')):
                    slot_index = i * optimizer.character_length + j + 1
                    slot = score[slot_index]
                    for k, equipment in enumerate(slot):
                        if optimizer.data.artifacts[slot_name][k].set_key.lower() in required_sets:
                            set_score[slot_index][k] *= score_boost

        optimizer.extra_data['set_score'] = set_score

    for i, slot in enumerate(score):
        for j, equipment in enumerate(slot):
            score[i][j] = equipment * optimizer.extra_data['set_score'][i][j]

    return score


def set_penalty_hook(optimizer, penalty, individual, set_restrictions):
    team_info = optimizer.data.get_team_build_by_vector(optimizer.actions['team'], individual)
    gcsim_data = GcsimData(team_info, optimizer.actions)
    for character in gcsim_data.characters:
        if character.key not in set_restrictions:
            continue

        found_set = False
        for artifact_set in set_restrictions[character.key]['sets']:
            is_valid = True
            for set_key, set_amount in artifact_set.items():
                if character.sets[set_key] < set_amount:
                    is_valid = False
                    break

            if is_valid:
                found_set = True
                break

        if not found_set:
            penalty *= set_restrictions[character.key]['penalty']

    return penalty