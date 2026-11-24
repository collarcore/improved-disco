import json
d=sorted(json.load(open('data/obcine.json')),key=lambda o:o['p'])
m=open('data/maps.json').read()
t=open('src/game.html',encoding='utf8').read().replace('/*GAME*/',open('src/game.js',encoding='utf8').read())
data=json.dumps([[o['n'],o['p'],o['a'],o['y'],o['r'],1 if o['u'] else 0] for o in d],ensure_ascii=False,separators=(',',':'))
t=t.replace('/*DATA*/',data).replace('/*MAPS*/',m)
# security policy: the page loads only its own files, may not contact any server, and runs only this exact script
import base64, hashlib, re
js=re.search(r'<script>(.*?)</script>',t,re.S).group(1)
h=base64.b64encode(hashlib.sha256(js.encode('utf8')).digest()).decode()
csp=("default-src 'none'; script-src 'sha256-%s'; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self' data:; "
     "manifest-src 'self'; connect-src 'none'; base-uri 'none'; form-action 'none'") % h
t=t.replace('<!--CSP-->','<meta http-equiv="Content-Security-Policy" content="%s">' % csp)
open('index.html','w',encoding='utf8').write(t);print(len(t))
