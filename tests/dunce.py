"""Dunce cap: honest play never gets it; money that was not earned (in a save or changed from outside) always does;
it survives a reset and being deleted from the save; the live site exposes no game state to the console."""
import os, json
from playwright.sync_api import sync_playwright
def run(b, st, extra=None, wait=1200, url='http://localhost:8765/'):
    c=b.new_context(viewport={'width':1600,'height':900})
    if st is not None: c.add_init_script("if(!sessionStorage.x){sessionStorage.x=1;localStorage.setItem('obcine-v2',%s)}"%json.dumps(json.dumps(st)))
    pg=c.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:120]));pg.goto(url);pg.wait_for_timeout(wait)
    if extra: extra(pg)
    r=dict(cap='/O\\' in pg.evaluate("document.getElementById('p-bell').innerText"),toast=pg.evaluate("document.getElementById('toast').hidden?'':document.getElementById('toast').innerText.split('\\n')[0]"),errs=errs)
    return c,pg,r
results={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    own=[60,50,40,30,20,10,5,2,0,0,0,0]
    cases=[
     ('new player', None, None),
     ('honest old save (v4, big)', {"v":4,"sit":4e9,"life":5e9,"all":6e9,"n":120,"own":own,"sound":0}, None),
     ('v5 save, money > earned', {"v":5,"sit":1e100,"life":5e9,"all":6e9,"n":0,"own":[0]*12,"sound":0}, None),
     ('v4 save, money > earned', {"v":4,"sit":1e100,"life":0,"all":0,"n":0,"own":[0]*12,"sound":0}, None),
     ('v5 save, buildings never paid for', {"v":5,"sit":10,"life":100,"all":100,"n":150,"own":own,"sound":0}, None),
     ('v5 honest small', {"v":5,"sit":50,"life":300,"all":300,"n":1,"own":[3,0,0,0,0,0,0,0,0,0,0,0],"sound":0}, None),
     ('console edit (debugger)', {"v":5,"sit":50,"life":300,"all":300,"n":1,"own":[3]+[0]*11,"sound":0}, lambda pg:(pg.evaluate("__dbg.S.sit=1e100"),pg.wait_for_timeout(600))),
    ]
    for name,st,ex in cases:
        c,pg,r=run(b,st,ex);print(f"{name:38s}",r);results[name]=(r["cap"],r["errs"]);c.close()
    # play honestly for a while: ring, buy, unlock - no cap
    def play(pg):
        for i in range(60): pg.keyboard.press('Space'); pg.wait_for_timeout(110)
        for a in ('g0','unlock','g0','g0','unlock'): pg.evaluate(f"__dbg.act('{a}')"); pg.wait_for_timeout(50)
        pg.wait_for_timeout(500)
    want={'new player':False,'honest old save (v4, big)':False,'v5 save, money > earned':True,'v4 save, money > earned':True,
          'v5 save, buildings never paid for':True,'v5 honest small':False,'console edit (debugger)':True}
    for k,v in want.items(): assert results[k][0]==v and not results[k][1], (k,results[k])
    c,pg,r=run(b,{"v":5,"sit":2000,"life":2000,"all":2000,"n":0,"own":[0]*12,"sound":0},play);print(f"{'honest play: ring/buy/unlock':38s}",r);assert not r['cap'] and not r['errs']
    # reload keeps a clean game clean
    pg.reload();pg.wait_for_timeout(1000);x='/O\\' in pg.evaluate("document.getElementById('p-bell').innerText");print(f"{'  ...after reload':38s}",x);assert not x;c.close()
    # cap survives reset and deleting it from the save
    c,pg,r=run(b,{"v":5,"sit":1e100,"life":0,"all":0,"n":0,"own":[0]*12,"sound":0})
    pg.evaluate("__dbg.act('rst');__dbg.act('rstyes');__dbg.render(true)");pg.wait_for_timeout(300)
    x='/O\\' in pg.evaluate("document.getElementById('p-bell').innerText");print(f"{'cap after reset':38s}",x);assert x
    pg.evaluate("const s=JSON.parse(localStorage.getItem('obcine-v2'));s.osel=0;localStorage.setItem('obcine-v2',JSON.stringify(s));");pg.close()
    pg=c.new_page();pg.goto('http://localhost:8765/');pg.wait_for_timeout(900)
    x='/O\\' in pg.evaluate("document.getElementById('p-bell').innerText");print(f"{'cap after deleting it from the save':38s}",x);assert x
    c.close()
    # console on the live site: no game state reachable
    c=b.new_context();pg=c.new_page();pg.goto('http://127.0.0.2:8765/');pg.wait_for_timeout(700)
    x=pg.evaluate("[typeof S,typeof act,typeof earn,typeof led,typeof __dbg].join(' ')");print('live site console:',x);assert set(x.split())=={'undefined'}
print('ALL PASSED')
