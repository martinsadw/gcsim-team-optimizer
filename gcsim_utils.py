from collections import defaultdict
import ctypes
import json
import os
import re
import subprocess

import settings
from stats import Stats


GCSIM_DPS_REGEX = r"resulting in (?P<mean>-?[\d\.]+) dps " \
                  r"\(min: (?P<min>-?[\d\.]+) max: (?P<max>-?[\d\.]+) std: (?P<sd>-?[\d\.]+)\)"


class GcsimExeRunner:
    def __init__(self, exec_path):
        self.exec_path = exec_path
        self.has_parser = False

    def parse_config(self, filename):
        raise NotImplementedError

    def run_json(self, json_data):
        raise NotImplementedError

    def run_file(self, filename):
        result = subprocess.run([self.exec_path, '-c', filename], capture_output=True)
        dps = re.search(GCSIM_DPS_REGEX, result.stdout.decode('utf-8'), re.MULTILINE)

        if dps is None:
            return {
                'mean': 0,
                'min': 0,
                'max': 0,
                'sd': 0,
            }

        return dps.groupdict()


class GoString(ctypes.Structure):
    _fields_ = [('p', ctypes.c_char_p),
                ('n', ctypes.c_int)]


class GcsimLibRunner:
    def __init__(self, lib_path):
        self._lib = ctypes.CDLL(lib_path)
        self._lib.parse_config.restype = ctypes.c_char_p
        self._lib.run_json.restype = ctypes.c_char_p
        self._lib.run_file.restype = ctypes.c_char_p
        self.has_parser = True

    def parse_config(self, filename):
        bytes_filename = bytes(filename, encoding="utf-8")
        result = self._lib.parse_config(GoString(bytes_filename, len(bytes_filename)))
        return json.loads(result)

    def run_json(self, json_data):
        bytes_json_data = bytes(json.dumps(json_data), encoding="utf-8")
        result = self._lib.run_json(GoString(bytes_json_data, len(bytes_json_data)))
        return json.loads(result)

    def run_file(self, filename):
        bytes_filename = bytes(filename, encoding="utf-8")
        result = self._lib.run_file(GoString(bytes_filename, len(bytes_filename)))
        return json.loads(result)


try:
    default_runner = GcsimLibRunner(settings.DEFAULT_LIB_PATH)
except FileNotFoundError:
    print(f"{settings.DEFAULT_LIB_NAME} not found. Using {settings.DEFAULT_EXEC_NAME}")
    default_runner = GcsimExeRunner(settings.DEFAULT_EXEC_PATH)


class GcsimData:
    def __init__(self, team_info, actions, iterations=1000):
        self.characters = [GcsimCharacter(character) for character in team_info]
        self.actions = actions['actions']
        self.config = {
            'swap_delay': 12,
            'iterations': iterations,
            'duration': actions['simulation_length'],
            'workers': 30,
            'mode': actions['mode'],
            'targets': [
                {'level': 100, 'resistance': 0.1}
            ],
            'energy': {
                'min': 480,
                'max': 720,
                'amount': 1,
            },
        }

    def __str__(self):
        text = ''
        text += '# Character Info\n'
        for character_info in self.characters:
            text += str(character_info)
            text += '\n'
        text += '\n'

        text += '# Simulation Config\n'
        text += 'options swap_delay={swap} debug=true iteration={iterations} duration={duration} workers={workers} mode={mode};\n'.format(
                swap=self.config['swap_delay'], iterations=self.config['iterations'], duration=self.config['duration'],
                workers=self.config['workers'], mode=self.config['mode'])
        for target in self.config['targets']:
            text += 'target lvl={lvl} resist={resist};\n'.format(
                    lvl=target["level"], resist=target["resistance"])
        energy = self.config["energy"]
        text += 'energy every interval={min},{max} amount={amount};\n'.format(
                min=energy["min"], max=energy["max"], amount=energy["amount"])
        text += '\n\n'

        text += '# Actions\n'
        text += self.actions

        return text

    def write_file(self, filename):
        with open(filename, 'w') as file:
            file.write(str(self))

    def run(self, temp_file=None, runner=None, keep_file=False):
        if temp_file is None:
            temp_file = os.path.join(settings.DEFAULT_OUTPUT_PATH, 'temp.txt')

        self.write_file(temp_file)
        dps = self.run_file(temp_file, runner=runner)
        if not keep_file:
            try:
                os.remove(temp_file)
            except FileNotFoundError:
                pass

        return dps

    @staticmethod
    def run_file(filename, runner=None):
        if runner is None:
            runner = default_runner

        gcsim_result = runner.run_file(filename)

        return gcsim_result


class GcsimCharacter:
    def __init__(self, character_data):
        character = character_data['character']
        self.key = character.key.lower()
        self.level = character.level
        self.max_level = character.max_level
        self.cons = character.constellation
        self.talent_1 = character.talent_1
        self.talent_2 = character.talent_2
        self.talent_3 = character.talent_3

        weapon = character_data['weapon']
        self.weapon = {
            'key': weapon.key.lower(),
            'level': weapon.level,
            'max_level': weapon.max_level,
            'refine': weapon.refinement,
        }

        artifacts = character_data['artifacts']
        self.sets = defaultdict(int)
        self.main_stats = Stats()
        self.sub_stats = Stats()
        for artifact in artifacts.values():
            if artifact is None:
                continue

            self.sets[artifact.set_key.lower()] += 1
            self.main_stats += Stats.by_artifact_main_stat(artifact.main_stat_key, artifact.level)
            self.sub_stats += artifact.sub_stats

        if 'extra_stats' in character_data:
            self.extra_stats = character_data['extra_stats']
        else:
            self.extra_stats = Stats()

    def __str__(self):
        # Character base stats
        result = '{name} char lvl={level}/{max_level} cons={cons} talent={t1},{t2},{t3};\n'.format(
            name=self.key, level=self.level, max_level=self.max_level,
            cons=self.cons, t1=self.talent_1, t2=self.talent_2, t3=self.talent_3)

        # Character Weapon
        result += '{name} add weapon="{weapon}" refine={refine} lvl={level}/{max_level};\n'.format(
            name=self.key, weapon=self.weapon['key'], level=self.weapon['level'], max_level=self.weapon['max_level'],
            refine=self.weapon['refine'])

        # Character artifact set
        for set_key, set_count in self.sets.items():
            result += '{name} add set="{set}" count={count};\n'.format(
                name=self.key, set=set_key, count=set_count)

        # Character main stats
        main_stats = '{name} add stats '.format(name=self.key)
        main_stats += self.main_stats.to_gcsim_text()
        main_stats += '; #main\n'
        result += main_stats

        # Character sub stats
        sub_stats = '{name} add stats '.format(name=self.key)
        sub_stats += self.sub_stats.to_gcsim_text()
        sub_stats += '; #subs\n'
        result += sub_stats

        # Additional stats
        if self.extra_stats is not None:
            extra_stats = '{name} add stats '.format(name=self.key)
            extra_stats += self.extra_stats.to_gcsim_text()
            extra_stats += '; #extra\n'
            result += extra_stats

        return result


def gcsim_fitness(vector, data, actions, iterations=10, force_write=True, validation_penalty=1, stats=None,
                  temp_actions_path=None):
    team_info = data.get_team_build_by_vector(actions['team'], vector)

    is_team_valid = data.validate_team(actions['team'], vector)
    if not is_team_valid:
        if stats is not None:
            if 'invalid' not in stats:
                stats['invalid'] = 0
            stats['invalid'] += 1

        if validation_penalty >= 1:
            return {'mean': '0', 'min': '0.00', 'max': '0.00', 'sd': '0.00'}

    if temp_actions_path is None:
        temp_actions_path = os.path.join('actions', 'temp_gcsim')
        os.makedirs(temp_actions_path, exist_ok=True)

    gcsim_filename = os.path.join(temp_actions_path, '_'.join([str(x) for x in vector]) + '.txt')
    if not force_write and os.path.exists(gcsim_filename):
        fitness = GcsimData.run_file(gcsim_filename)
    else:
        gcsim_data = GcsimData(team_info, actions, iterations=iterations)
        fitness = gcsim_data.run(gcsim_filename, keep_file=True)

    if stats is not None:
        if 'evaluation' not in stats:
            stats['evaluation'] = 0
        stats['evaluation'] += iterations

    # dps = float(fitness['mean'])
    # if not is_team_valid:
    #     dps *= (1 - validation_penalty)
    #
    # return dps

    return fitness
