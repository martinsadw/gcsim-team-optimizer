action_txt = '''
active raidenshogun;
raidenshogun skill;
yaemiko skill:3;
kaedeharakazuha skill[hold=1], high_plunge;
bennett burst;
yaemiko burst, skill:3;
kaedeharakazuha burst;
raidenshogun burst, attack:3, charge, attack:3, charge, attack:2, charge, attack, charge, skill;
kaedeharakazuha skill, high_plunge;
yaemiko skill:3;
bennett skill, burst;
kaedeharakazuha skill, high_plunge, burst;
raidenshogun burst, attack:3, charge, attack:3, charge, attack:2, charge, attack, charge;
restart;
'''

action = {
  'name': 'hyper_raiden',
  'team': ['RaidenShogun', 'YaeMiko', 'KaedeharaKazuha', 'Bennett'],
  'active': 'RaidenShogun',
  'simulation_length': 99,
  'mode': 'sl',
  'actions': action_txt,
}
