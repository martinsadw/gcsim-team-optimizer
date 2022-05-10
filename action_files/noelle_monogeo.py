action_txt = '''
active zhongli;

zhongli skill[hold=1];

gorou skill, burst;

albedo jump;
wait 10;
albedo skill;

noelle skill, attack, burst , attack:3, dash, attack:3, dash, attack:3, dash;

gorou skill;

noelle attack:3, dash, attack:3, dash;

restart;
'''

action = {
  'name': 'noelle_monogeo',
  'team': ['Noelle', 'Albedo', 'Zhongli', 'Gorou'],
  'simulation_length': 90,
  'mode': 'sl',
  'actions': action_txt,
}
