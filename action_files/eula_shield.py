action_txt = '''
active raiden;

raiden skill;
zhongli skill[hold=1];
rosaria skill;
eula skill;
rosaria burst;
eula burst,attack:4,skill[hold=1],attack:4;
rosaria skill;
eula attack:2;
raiden burst,attack:3,charge,attack:3,charge,attack:3,charge;
restart;
'''

action = {
  'name': 'eula_shield',
  'team': ['Eula', 'RaidenShogun', 'Rosaria', 'Zhongli'],
  'active': 'RaidenShogun',
  'simulation_length': 102,
  'mode': 'sl',
  'actions': action_txt,
}
