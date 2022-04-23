action_txt = '''
active raidenshogun;
  
raidenshogun skill;
yaemiko skill:3, burst, skill:3;
bennett skill, burst;
kaedeharakazuha skill[hold=1], high_plunge, burst;
raidenshogun burst, attack:3, charge, attack:3, charge, attack:3, charge;
restart;
'''

action = {
  'name': 'hyper_raiden',
  'team': ['RaidenShogun', 'YaeMiko', 'KaedeharaKazuha', 'Bennett'],
  'simulation_length': 115,
  'mode': 'sl',
  'actions': action_txt,
}
