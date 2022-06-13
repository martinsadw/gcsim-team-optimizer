action_txt = '''
active xingqiu;

xingqiu skill, burst, attack;
bennett skill, burst;
fischl attack:2, skill;
diluc skill, burst, attack, 
	skill, attack:2, 
	skill, attack:2,
	skill, attack:2,
	skill, attack,
	skill, attack;
bennett attack, skill, attack;
diluc attack:3;

xingqiu skill, burst, attack;
bennett skill, burst;
fischl attack:2, burst;
diluc skill, burst, attack, 
	skill, attack:2, 
	skill, attack:2,
	skill, attack:2,
	skill, attack,
	skill, attack;
bennett attack, skill, attack;
diluc attack:3;

restart;
'''

action = {
  'name': 'diluc_xingqiu_fischl_bennett',
  'team': ['Diluc', 'Xingqiu', 'Fischl', 'Bennett'],
  'active': 'Xingqiu',
  'simulation_length': 100,
  'mode': 'sl',
  'actions': action_txt,
}
