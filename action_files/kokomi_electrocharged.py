action_txt = '''
active yaemiko;

yaemiko skill:3;
kaedeharakazuha skill[hold=1], high_plunge;
fischl attack:2, skill;
kokomi attack:2, skill;
yaemiko burst, skill:3;
kaedeharakazuha burst, skill[hold=1], high_plunge;
fischl attack:2, burst;
kokomi burst,
       attack:2, charge,
       attack:2, charge,
       attack:2, charge,
       attack:2, charge,
       attack:3,
       attack:2, charge;
restart;
'''

action = {
  'name': 'kokomi_electrocharged',
  'team': ['YaeMiko', 'KaedeharaKazuha', 'Fischl', 'SangonomiyaKokomi'],
  'simulation_length': 100,
  'mode': 'sl',
  'actions': action_txt,
}
