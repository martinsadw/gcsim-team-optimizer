action_txt = '''
active rosaria;

rosaria skill;
bennett burst, skill;
rosaria burst;
xiangling attack, burst, skill;
rosaria skill;
kamisatoayaka skill, dash, burst;
bennett skill, attack;
xiangling attack:3;
rosaria attack, skill;
bennett attack:2, skill;
kamisatoayaka attack:2, dash, attack:2, skill, dash, attack:2, charge;

restart;
'''

action = {
  'name': 'reverse_melt_ayaka',
  'team': ['KamisatoAyaka', 'Rosaria', 'Xiangling', 'Bennett'],
  'active': 'Rosaria',
  'simulation_length': 100,
  'mode': 'sl',
  'actions': action_txt,
}
