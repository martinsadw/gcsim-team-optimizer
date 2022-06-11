action_txt = '''
active yelan;

yelan skill, attack, burst, attack;
kazuha burst, attack;
bennett burst, skill, attack;
kazuha skill[hold=1], high_plunge;
hutao skill,
    attack:1, charge, jump,
    attack:1, charge, jump,
    attack:1, charge, jump,
    attack:1, charge, jump,
    attack:1, charge, jump,
    attack:1, charge, jump,
    attack:1, charge, jump,
    attack:1, charge, jump,
    attack:1, charge, jump;
kazuha attack, skill, high_plunge;
bennett skill, dash;
restart;
'''

action = {
  'name': 'hutao_yelan',
  'team': ['Bennett', 'HuTao', 'KaedeharaKazuha', 'Yelan'],
  'active': 'Yelan',
  'simulation_length': 101,
  'mode': 'sl',
  'actions': action_txt,
}
