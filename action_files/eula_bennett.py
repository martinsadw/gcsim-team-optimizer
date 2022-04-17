action_txt = '''
active raiden;

raiden skill;
rosaria skill,burst;
eula skill;
bennett skill,burst;
eula burst,attack:4,skill[hold=1],attack:4;
rosaria skill,attack;
raiden burst,attack:3,charge,attack:3,charge,attack:3,charge;
restart;
'''

action = {
  'team': ['Eula', 'RaidenShogun', 'Bennett', 'Rosaria'],
  'simulation_length': 110,
  'mode': 'sl',
  'actions': action_txt,
}
