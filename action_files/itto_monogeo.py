action_txt = '''
active zhongli;
zhongli skill[hold=1];
gorou skill,burst;

albedo jump;
wait 10;
albedo skill;

itto attack, burst, attack, skill, attack:2, charge:5, attack:4, charge:5, skill, charge, attack:2;
restart;
'''

action = {
  'name': 'itto_monogeo',
  'team': ['AratakiItto', 'Albedo', 'Zhongli', 'Gorou'],
  'active': 'Zhongli',
  'simulation_length': 102,
  'mode': 'sl',
  'actions': action_txt,
}
