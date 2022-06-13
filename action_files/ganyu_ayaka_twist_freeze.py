action_txt = '''
active ayaka;

ayaka skill;
ganyu burst[radius=2], skill;     # ruin guard should be about radius=2. In ST, this results in 18-20 icicle hits.
venti burst, attack[delay=10];
mona skill, burst;
ayaka dash, skill, burst;
ganyu skill[delay=10];
venti skill, attack;
mona attack:2;
ganyu aim[weakspot=1]:2;

restart;
'''

action = {
  'name': 'ganyu_ayaka_twist_freeze',
  'team': ['Ganyu', 'Venti', 'Mona', 'KamisatoAyaka'],
  'active': 'Ganyu',
  'simulation_length': 100,
  'mode': 'sl',
  'actions': action_txt,
}
