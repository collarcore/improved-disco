import base64, hashlib, re
import json
d=sorted(json.load(open('data/obcine.json')),key=lambda o:o['p'])
m=open('data/maps.json').read()
# the game runs inside a closure, so its state (S) and functions can't be reached from the browser console
t=open('src/game.html',encoding='utf8').read().replace('/*GAME*/',"(()=>{'use strict';\n"+open('src/game.js',encoding='utf8').read()+"\n})();")
data=json.dumps([[o['n'],o['p'],o['a'],o['y'],o['r'],1 if o['u'] else 0] for o in d],ensure_ascii=False,separators=(',',':'))
t=t.replace('/*DATA*/',data).replace('/*MAPS*/',m)
# version: a short hash of the page, shown to the game and published as version.json, so open tabs notice an update
build=hashlib.sha256(t.encode('utf8')).hexdigest()[:10]
t=t.replace("'/*BUILD*/'","'%s'" % build)
open('version.json','w').write(json.dumps({'build':build}))
# the shipped script carries no comments (the source on GitHub keeps them): terser only reprints the code,
# names and logic unchanged. Without terser installed (npm i -g terser) the page is built with comments.
import shutil, subprocess
if shutil.which('terser'):
    m_=re.search(r'<script>(.*?)</script>',t,re.S)
    out=subprocess.run(['terser','--format','comments=false,ascii_only=false'],input=m_.group(1),capture_output=True,text=True,encoding='utf8')
    if out.returncode==0 and out.stdout.strip(): t=t[:m_.start(1)]+out.stdout.strip()+t[m_.end(1):]
    else: print('terser failed, keeping comments:',out.stderr[:300])
else: print('terser not found: building with comments')
# security policy: the page loads only its own files, may not contact any server, and runs only this exact script
js=re.search(r'<script>(.*?)</script>',t,re.S).group(1)
h=base64.b64encode(hashlib.sha256(js.encode('utf8')).digest()).decode()
csp=("default-src 'none'; script-src 'sha256-%s'; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self' data:; "
     "manifest-src 'self'; connect-src 'self'; base-uri 'none'; form-action 'none'") % h
t=t.replace('<!--CSP-->','<meta http-equiv="Content-Security-Policy" content="%s">' % csp)
# styles and markup ship without comments too
t=re.sub(r'<style>(.*?)</style>',lambda m:'<style>'+re.sub(r'/\*.*?\*/','',m.group(1),flags=re.S)+'</style>',t,flags=re.S)
t=re.sub(r'<!--.*?-->','',t,flags=re.S)
open('index.html','w',encoding='utf8').write(t);print(len(t))
