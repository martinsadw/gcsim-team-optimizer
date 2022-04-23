action_txt = '''
active raiden;

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

xiangling attack:3;
'''

action = {
  'name': 'raiden_national',
  'team': ['RaidenShogun', 'Bennett', 'Xiangling', 'Xingqiu'],
  'simulation_length': 105,
  'mode': 'sl',
  'actions': action_txt,
}
