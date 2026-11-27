"""Cheats that keep every number consistent (like a hand-edited save with matching earnings and votes) are caught by
real-time limits; honest saves, also casual and old ones, never are; scripted input is ignored; hijacking built-ins after
load gets nothing."""
import os, json, time
from playwright.sync_api import sync_playwright
now=int(time.time()*1000)
MAX=9007199254740991
own=[60,50,40,30,20,10,5,2,0,0,0,0]
def cap(pg): return '/O\\' in pg.evaluate("document.getElementById('p-bell').innerText")
cases={
 # Aiken's save, as in the screenshot: every number consistent with every other
 'aiken (consistent fake save)':({"v":5,"sit":1e300,"life":1e300,"all":1e300,"votes":int(1e97),"n":212,"own":[1e6]*12,"clicks":MAX,"kur":MAX,"refs":MAX,"t0":now-14000,"won":now,"first":now-3600e3,"play":100,"sound":0},True),
 'same but modest counters':({"v":5,"sit":1e300,"life":1e300,"all":1e300,"votes":int(1e97),"n":212,"own":[1e6]*12,"clicks":100,"kur":1,"refs":1,"first":now-3600e3,"play":100,"sound":0},True),
 'votes beyond earnings':({"v":5,"sit":10,"life":100,"all":1e12,"votes":5000,"n":5,"own":[3]+[0]*11,"first":now-48*3600e3,"play":3600,"sound":0},True),
 'old first date (1970)':({"v":5,"sit":1e40,"life":1e40,"all":1e40,"votes":0,"n":0,"own":[0]*12,"first":1,"play":0,"sound":0},True),
 # votes got 40× harder to earn on 26 Nov 2026: saves from before keep votes earned at the old rate, new saves can't
 'honest: finished before the vote change (old rate)':({"v":5,"sit":1e15,"life":6.4e19,"all":6.4e19,"votes":4000,"n":212,"own":[40,30,20,12,8,4,0,0,0,0,0,0],"clicks":60000,"kur":100,"refs":3,"first":1795608000000,"play":13*3600,"sound":0},False),  # began 25 Nov 2026, before the change
 'cheat: same votes on a new-rate save':({"v":5,"voteV":2,"sit":1e15,"life":6.4e19,"all":6.4e19,"votes":4000,"n":212,"own":[40,30,20,12,8,4,0,0,0,0,0,0],"clicks":60000,"kur":100,"refs":3,"first":now-31*3600e3,"play":13*3600,"sound":0},True),
 'honest: perfect 21 h player':({"v":5,"voteV":2,"sit":1e15,"life":1e16,"all":2.6e17,"votes":180,"n":42,"own":[40,30,20,12,8,4,0,0,0,0,0,0],"clicks":600000,"kur":200,"refs":5,"first":now-21*3600e3,"play":21*3600,"sound":0},False),
 'honest: casual, a week in, mostly away':({"v":5,"voteV":2,"sit":1e12,"life":5e12,"all":4e13,"votes":10,"n":100,"own":own,"clicks":20000,"kur":40,"refs":1,"first":now-7*24*3600e3,"play":3*3600,"sound":0},False),
 'honest: old v4 save, big':({"v":4,"sit":4e9,"life":5e9,"all":6e9,"n":120,"own":own,"first":now-30*3600e3,"play":20*3600,"sound":0},False),
 'honest: earlier-today v5 save, no runV':({"v":5,"sit":4e9,"life":5e9,"all":6e9,"n":160,"own":own,"first":now-30*3600e3,"play":20*3600,"sound":0},False),
 'new player':(None,False),
}
with sync_playwright() as p:
  b=p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
  bad=[]
  for name,(st,want) in cases.items():
    c=b.new_context(viewport={'width':1600,'height':900})
    if st: c.add_init_script("if(!sessionStorage.x){sessionStorage.x=1;localStorage.setItem('obcine-v2',%s)}"%json.dumps(json.dumps(st)))
    pg=c.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:100]));pg.goto('http://localhost:8765/');pg.wait_for_timeout(900)
    got=cap(pg);print(f'{name:42s} cap={got} want={want} {errs or ""}');
    if got!=want or errs: bad.append(name)
    c.close()
  # scripted input is ignored; real input works
  c=b.new_context(viewport={'width':1600,'height':900});pg=c.new_page();pg.goto('http://localhost:8765/');pg.wait_for_timeout(800)
  clicks=lambda:pg.evaluate("(dispatchEvent(new Event('pagehide')),JSON.parse(localStorage.getItem('obcine-v2')).clicks)")
  c0=clicks();pg.evaluate("""()=>{for(let i=0;i<50;i++){document.dispatchEvent(new KeyboardEvent('keydown',{key:' ',code:'Space',bubbles:true}));
    const r=document.querySelector('#p-bell .ring');r.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,clientX:1,clientY:1}));r.dispatchEvent(new PointerEvent('pointerup',{bubbles:true}));r.click()}}""")
  pg.wait_for_timeout(200);c1=clicks();pg.keyboard.press('Space');pg.wait_for_timeout(200);c2=clicks()
  print('script input rang:',c1-c0,'| real key rang:',c2-c1); 
  if c1-c0!=0 or c2-c1!=1: bad.append('input')
  # hijacking JSON.stringify after load doesn't hand over the game state
  pg.evaluate("window.__got=null;const f=JSON.stringify;JSON.stringify=function(o,...a){if(o&&o.own)window.__got=o;return f.call(this,o,...a)};const g=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){window.__set=(window.__set||0)+1;return g.call(this,k,v)};0")
  pg.keyboard.press('Space');pg.evaluate("dispatchEvent(new Event('pagehide'))");pg.wait_for_timeout(300)
  got=pg.evaluate("!!window.__got||!!window.__set");print('hijacked built-ins caught the state or the save:',got)
  if got: bad.append('hijack')
  print('BAD' if bad else 'ALL PASSED', bad)
assert not bad, bad
