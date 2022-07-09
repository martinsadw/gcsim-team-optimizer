action_txt = '''
active xingqiu;

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

xingqiu attack;
'''

action = {
  'name': 'hutao_geobros',
  'team': ['HuTao', 'Xingqiu', 'Albedo', 'Zhongli'],
  'active': 'Xingqiu',
  'simulation_length': 90,
  'mode': 'apl',
  'actions': action_txt,
}
