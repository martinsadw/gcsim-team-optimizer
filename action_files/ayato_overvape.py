action_txt = '''
active bennett;

bennett skill, burst;

#attack ensures bennett buff is snapped onto Oz.
fischl attack:2, skill, attack;

ayato burst[radius=2];

xiangling burst, attack, skill;

ayato skill, attack:15;

#attack ensures bennett buff is snapped onto Oz. Also NA weave for XQ Q
fischl attack:2, burst;

#stay on XL so that Fischl A4 procs for damage, and refreshes electro for XL to OL again. Bennett field is basically gone now.
xiangling attack:4, dash, attack:4;

xiangling skill;

ayato skill, attack:15;

restart;
'''

action = {
  'name': 'ayato_overvape',
  'team': ['Fischl', 'Bennett', 'Xiangling', 'KamisatoAyato'],
  'simulation_length': 100,
  'mode': 'sl',
  'actions': action_txt,
}
