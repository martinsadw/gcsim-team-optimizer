action_txt = '''
active ayato;

ayato burst;
beidou skill;
kazuha skill, high_plunge, burst;
fischl skill;
beidou burst, attack;
ayato skill, attack:15;
beidou attack, skill[counter=2], attack:2;
kazuha attack, skill, high_plunge, attack;
fischl attack, burst;
ayato attack:2, dash, attack:2, skill, attack:15;

restart;
'''

action = {
  'name': 'ayato_electrocharge',
  'team': ['KamisatoAyato', 'Beidou', 'Fischl', 'KaedeharaKazuha'],
  'simulation_length': 125,
  'mode': 'sl',
  'actions': action_txt,
}
