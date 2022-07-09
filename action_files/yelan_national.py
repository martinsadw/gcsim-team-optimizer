action_txt = '''
active yelan;

yelan skill, burst, attack;
xingqiu burst, attack;
#enable double rainswords, yelan catches her own particles

bennett burst, attack, skill;
xiangling attack, burst, attack, skill;
#snapshot pyronado and guoba

xingqiu attack:2;
#acquire bennett buff on xq to buff rainswords
bennett attack, skill;

yelan attack, skill;
#cast yelan e on cd

xingqiu attack:3, skill, dash, attack:2, jump, attack;
#forward vapes a hit of xq e

bennett skill, attack:2;
xiangling attack:2;
#funnel Xiangling best dps in Teyvat

bennett skill, attack:2, dash, attack:2, skill;
#go ham on bennett, basically you can funnel whoever needs it if you have to

yelan attack:2;

restart;
'''

action = {
  'name': 'yelan_national',
  'team': ['Bennett', 'Xiangling', 'Yelan', 'Xingqiu'],
  'active': 'Yelan',
  'simulation_length': 106,
  'mode': 'sl',
  'actions': action_txt,
}
