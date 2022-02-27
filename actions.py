actions_dict = dict()

actions_dict['hyper_raiden'] = {
  'team': ['RaidenShogun', 'YaeMiko', 'KaedeharaKazuha', 'Bennett'],
  'simulation_length': 115,
  'mode': 'sl',
  'actions': '''active raidenshogun;
  
raidenshogun skill;
yaemiko skill:3;
kaedeharakazuha skill[hold=1], high_plunge;
bennett burst;
yaemiko attack:2, burst, skill:3;
kaedeharakazuha burst;
raidenshogun burst, attack:3, charge, attack:3, charge, attack:3, charge, skill;
kaedeharakazuha skill, high_plunge;
bennett skill;
yaemiko skill:3;
bennett burst;
kaedeharakazuha skill, high_plunge, burst;
raidenshogun burst, attack:3, charge, attack:3, charge, attack:3, charge;
restart;'''
}