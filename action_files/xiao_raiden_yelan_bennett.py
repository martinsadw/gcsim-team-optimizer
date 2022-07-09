action_txt = '''
active raiden;

raiden skill;
yelan burst, attack, skill, attack;
bennett skill, attack, burst, attack;
xiao skill:2, attack, burst,
attack[delay=40], high_plunge[collision=1],
attack[delay=40], high_plunge[collision=1],
attack[delay=40], high_plunge[collision=1],
attack[delay=40], high_plunge[collision=1],
attack[delay=40], high_plunge[collision=1],
attack[delay=40], high_plunge[collision=1],
attack[delay=40], high_plunge[collision=1],
attack[delay=40], high_plunge[collision=1],
jump, high_plunge[collision=1],
jump, high_plunge[collision=1],
jump, high_plunge[collision=1],
jump, high_plunge[collision=1];
yelan skill;
bennett skill, burst;
raiden skill, burst, charge, attack:3, charge, attack:3, charge, attack:3, charge;

restart;
'''

action = {
  'name': 'xiao_raiden_yelan_bennett',
  'team': ['Xiao', 'RaidenShogun', 'Yelan', 'Bennett'],
  'active': 'RaidenShogun',
  'simulation_length': 100,
  'mode': 'sl',
  'actions': action_txt,
}
