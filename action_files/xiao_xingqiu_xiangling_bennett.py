action_txt = '''
active xiangling;

xiangling skill;
xingqiu skill,burst,attack;
bennett burst,attack,skill;
xiao skill, attack, skill;
xiangling attack, burst, attack;
bennett skill,attack;
xingqiu attack:3;
bennett attack:2, skill;
xingqiu attack:3;
bennett attack:3, skill;
xingqiu attack:3;
xiao burst, attack;
bennett attack:2, skill;
xiangling attack:2;

restart;
'''

action = {
  'name': 'xiao_xingqiu_xiangling_bennett',
  'team': ['RaidenShogun', 'Xingqiu', 'Xiangling', 'Bennett'],
  'active': 'Xiangling',
  'simulation_length': 100,
  'mode': 'sl',
  'actions': action_txt,
}
