import os, json,sys
from playwright.sync_api import sync_playwright
import os
LANGX=os.environ.get('LANGX','sl')
S={
 'start':None,
 'mid':{"sit":3.2e6,"all":5e8,"n":75,"own":[60,45,30,20,10,3,0,0,0,0,0,0],"ups":["t0_0","t1_0","k1"],"clicks":800,"kur":2,"t0":1700000000000,"save":9e15,"sound":0,"ach":["o1","o10","o25","o50","c100"]},
 'late':{"sit":4.4e12,"all":9e15,"n":188,"own":[150,140,130,120,110,100,90,80,60,40,10,0],"ups":[],"clicks":9000,"kur":20,"t0":1700000000000,"save":9e15,"sound":0,"votes":40,"refs":1},
 'end':{"sit":5e16,"all":5e16,"n":212,"won":1700000500000,"own":[200]*12,"clicks":20000,"t0":1700000000000,"save":9e15,"sound":0},
 'light':{"sit":3.2e6,"all":5e8,"n":75,"own":[60,45,30,20,10,3,0,0,0,0,0,0],"save":9e15,"sound":0,"light":1},
}
widths=[320,360,390,600,768,1024,1280,1366,1440,1920]
out=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    for st,val in S.items():
        for w in (widths if st in('start','mid') else [390,1280,1920]):
            ctx=b.new_context(viewport={'width':w,'height':900})
            if True: ctx.add_init_script("if(!sessionStorage.getItem('x')){sessionStorage.setItem('x',1);localStorage.setItem('obcine-v2',JSON.stringify(%s))}"%json.dumps(dict(val or {},lang=LANGX,own=(val or {}).get('own',[0]*12))))
            pg=ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
            pg.goto('http://localhost:8765/');pg.wait_for_timeout(1300)
            r=pg.evaluate("""()=>{const r={};const bad=[];document.querySelectorAll('pre').forEach(p=>{if(p.hidden)return;const ls=p.innerText.replace(/\\n$/,'').split('\\n');const w=[...ls[0]].length;ls.forEach((l,i)=>{if(p.id!=='p-set'&&[...l].length!==w)bad.push(p.id+':'+i+':'+[...l].length+'/'+w)});const rc=p.getBoundingClientRect();if(rc.right>innerWidth+0.5||rc.left<-0.5)bad.push(p.id+' outside '+Math.round(rc.left)+'..'+Math.round(rc.right))});
              r.bad=bad;r.over=document.documentElement.scrollWidth-document.documentElement.clientWidth;r.fs=getComputedStyle(document.body).fontSize;r.cols=document.querySelectorAll('.col').length;return r}""")
            out.append((st,w,errs,r))
            if w in (320,390,1024,1440,1920): pg.screenshot(path=f'/tmp/sweep/{st}-{w}.png',full_page=False)
            ctx.close()
    b.close()
for o in out: print(o[0],o[1],o[3]['fs'],o[3]['cols'],'over=%d'%o[3]['over'],o[2],o[3]['bad'][:6])
