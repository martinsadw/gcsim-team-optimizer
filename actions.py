actions_dict = dict()

actions_dict['hyper_raiden'] = {
  'team': ['RaidenShogun', 'YaeMiko', 'KaedeharaKazuha', 'Bennett'],
  'simulation_length': 115,
  'mode': 'sl',
  'actions': '''active raidenshogun;
  
raidenshogun skill;
yaemiko skill:3, burst, skill:3;
bennett skill, burst;
kaedeharakazuha skill[hold=1], high_plunge, burst;
raidenshogun burst, attack:3, charge, attack:3, charge, attack:3, charge;
restart;'''
}