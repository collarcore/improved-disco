import json
d=sorted(json.load(open('data/obcine.json')),key=lambda o:o['p'])
m=open('data/maps.json').read()
t=open('src/game.html',encoding='utf8').read().replace('/*GAME*/',open('src/game.js',encoding='utf8').read())
data=json.dumps([[o['n'],o['p'],o['a'],o['y'],o['r'],1 if o['u'] else 0] for o in d],ensure_ascii=False,separators=(',',':'))
t=t.replace('/*DATA*/',data).replace('/*MAPS*/',m)
import os;
open('index.html','w',encoding='utf8').write(t);print(len(t))
