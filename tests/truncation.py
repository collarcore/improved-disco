import os, json
from playwright.sync_api import sync_playwright
import os
LANGX=os.environ.get('LANGX','sl')
S={
 'start':None,
 'mid':{"sit":3.2e6,"all":5e8,"n":75,"own":[60,45,30,20,10,3,0,0,0,0,0,0],"clicks":800,"save":9e15,"sound":0},
 'late':{"sit":4.4e12,"all":9e15,"n":205,"own":[150,140,130,120,110,100,90,80,60,40,10,0],"clicks":20000,"save":9e15,"sound":0,"votes":40,"refs":1},
 'end':{"sit":5e16,"all":5e16,"n":212,"won":1700000500000,"t0":1700000000000,"own":[200]*12,"clicks":20000,"save":9e15,"sound":0},
}
found={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    for st,val in S.items():
        for w in [320,390,768,1024,1280,1440,1920]:
            ctx=b.new_context(viewport={'width':w,'height':900})
            if True: ctx.add_init_script("if(!sessionStorage.getItem('x')){sessionStorage.setItem('x',1);localStorage.setItem('obcine-v2',JSON.stringify(%s))}"%json.dumps(dict(val or {},lang=LANGX,own=(val or {}).get('own',[0]*12))))
            pg=ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
            pg.goto('http://localhost:8765/');pg.wait_for_timeout(1000)
            # page through register and achievements
            for _ in range(16):
                el=pg.locator('[data-a^="pg"]').nth(3)
                if el.count(): el.click(); pg.wait_for_timeout(120)
            for _ in range(10):
                el=pg.locator('[data-a="ach1"]')
                if el.count(): el.click(); pg.wait_for_timeout(80)
            # hover every distinct občina on the map
            pg.evaluate("""async()=>{const seen=new Set();for(const c of document.querySelectorAll('#mapgrid i')){const k=c.className.match(/c(\\d+)/)[1];if(seen.has(k))continue;seen.add(k);c.dispatchEvent(new MouseEvent('mouseover',{bubbles:true}));}}""")
            pg.wait_for_timeout(300)
            tr=pg.evaluate("[...new Set(window.__trunc||[])]")
            for x in tr: found.setdefault(x,set()).add(f'{st}@{w}')
            if errs: print(st,w,errs)
            ctx.close()
    b.close()
print(len(found),'distinct truncations')
for k,v in sorted(found.items(),key=lambda kv:-len(kv[1]))[:40]: print(repr(k[:90]),sorted(v)[:4],len(v))
