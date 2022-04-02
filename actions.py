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

actions_dict['hutao_xingqiu_albedo_zhongli'] = {
  'team': ['HuTao', 'Xingqiu', 'Albedo', 'Zhongli'],
  'simulation_length': 90,
  'mode': 'apl',
  'actions': '''active xingqiu;

# Drops 1 N2C if you uncomment - check ability usage figures to confirm
# hutao jump +if=.status.paramita>300&&.status.paramita<350;

# Hu Tao sequence - gets you 7N2CD + 1N1C PP Burst if available
# Optimally you only burst every other rotation
hutao burst
      +if=.status.paramita<20
      && .status.paramita>0;
hutao attack,charge
      +if=.status.paramita>20
      && .status.paramita<=60;
hutao attack:2,charge,dash
      +if=.status.paramita>60
      && .stam.hutao>180;
hutao attack:2,charge,jump
      +if=.status.paramita>60;

# Second skill for sac sword if needed
xingqiu skill[orbital=1],burst[orbital=1],attack;
xingqiu skill[orbital=1]
        +if=.cd.xingqiu.burst > 300;

# zhongli skill[hold_nostele=1],attack
zhongli skill,attack
        +swap_to=albedo
        +if=.status.xqburst>300;

albedo skill,attack,burst,attack
       +swap_to=zhongli
       +if=.cd.hutao.skill<120
       && .status.xqburst>300;

albedo skill,attack
       +swap_to=zhongli
       +if=.cd.hutao.skill<120
       && .status.xqburst>300;

zhongli burst,attack
        +swap_to=hutao
        +if=.cd.hutao.skill<120;

hutao skill +if=.status.xqburst>300;

xingqiu attack;'''
}

actions_dict['raiden_national'] = {
  'team': ['RaidenShogun', 'Bennett', 'Xiangling', 'Xingqiu'],
  'simulation_length': 105,
  'mode': 'sl',
  'actions': '''active raiden;

raiden skill;

#------------------------------------------------------

xingqiu skill, burst, attack;

bennett burst, attack, skill;

xiangling attack, burst, attack, skill;

#raiden attack, burst, attack:3, charge, attack:3, charge, attack:3, charge, attack:1, charge;
raiden attack, burst, attack:5, dash, attack:5, dash, attack:4, skill, attack;

bennett skill, attack;

xiangling attack:3;

#------------------------------------------------------

xingqiu skill, burst, attack;

bennett burst, attack, skill;

xiangling attack, burst, attack, skill;

#raiden attack, burst, attack:3, charge, attack:3, charge, attack:3, charge, attack:1, charge;
raiden attack, burst, attack:5, dash, attack:5, dash, attack:4, skill, attack;


bennett skill, attack;

xiangling attack:3;

#------------------------------------------------------

xingqiu skill, burst, attack;

bennett burst, attack, skill;

xiangling attack, burst, attack, skill;

#raiden attack, burst, attack:3, charge, attack:3, charge, attack:3, charge, attack:1, charge;
raiden attack, burst, attack:5, dash, attack:5, dash, attack:4, skill, attack;

bennett skill, attack;

xiangling attack:3;

#------------------------------------------------------

xingqiu skill, burst, attack;

bennett burst, attack, skill;

xiangling attack, burst, attack, skill;

#raiden attack, burst, attack:3, charge, attack:3, charge, attack:3, charge, attack:1, charge;
raiden attack, burst, attack:5, dash, attack:5, dash, attack:4, skill, attack;

bennett skill, attack;

xiangling attack:3;

#------------------------------------------------------

xingqiu skill, burst, attack;

bennett burst, attack, skill;

xiangling attack, burst, attack, skill;

#raiden attack, burst, attack:3, charge, attack:3, charge, attack:3, charge, attack:1, charge;
raiden attack, burst, attack:5, dash, attack:5, dash, attack:4, skill, attack;

bennett skill, attack;

xiangling attack:3;'''
}

actions_dict['kokomi_electrocharged'] = {
  'team': ['YaeMiko', 'KaedeharaKazuha', 'Fischl', 'SangonomiyaKokomi'],
  'simulation_length': 100,
  'mode': 'sl',
  'actions': '''active yaemiko;

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
restart;'''
}

actions_dict['eula_shield'] = {
  'team': ['Eula', 'RaidenShogun', 'Rosaria', 'Zhongli'],
  'simulation_length': 102,
  'mode': 'sl',
  'actions': '''active raiden;

raiden skill;
zhongli skill[hold=1];
rosaria skill;
eula skill;
rosaria burst;
eula burst,attack:4,skill[hold=1],attack:4;
rosaria skill;
eula attack:2;
raiden burst,attack:3,charge,attack:3,charge,attack:3,charge;
restart;'''
}

actions_dict['eula_bennett'] = {
  'team': ['Eula', 'RaidenShogun', 'Bennett', 'Rosaria'],
  'simulation_length': 110,
  'mode': 'sl',
  'actions': '''active raiden;

raiden skill;
rosaria skill,burst;
eula skill;
bennett skill,burst;
eula burst,attack:4,skill[hold=1],attack:4;
rosaria skill,attack;
raiden burst,attack:3,charge,attack:3,charge,attack:3,charge;
restart;
'''
}

actions_dict['ayato_overvape'] = {
  'team': ['Fischl', 'Bennett', 'Xiangling', 'KamisatoAyato'],
  'simulation_length': 100,
  'mode': 'sl',
  'actions': '''active bennett;

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

restart;'''
}

actions_dict['ayato_electrocharge'] = {
  'team': ['KamisatoAyato', 'Beidou', 'Fischl', 'KaedeharaKazuha'],
  'simulation_length': 125,
  'mode': 'sl',
  'actions': '''active ayato;

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

restart;'''
}