"""A friend's real console script (from his screen recording): rewrites the save, deletes the cap marker, blocks the
game's save-on-leave handlers and reloads. Every variant, including a claimed 10^300 seconds of play, must get the cap."""
import os, json, time
from playwright.sync_api import sync_playwright
SCRIPT=r"""
(() => {
 const KEY="obcine-v2"; const s=JSON.parse(localStorage.getItem(KEY)); const now=Date.now(); const range=n=>[...Array(n).keys()];
 const MAX=Number.MAX_SAFE_INTEGER;
 Object.assign(s, %s);
 s.n=212; s.own=range(12).map(()=>OWNV);
 s.amends=range(12).map(i=>`a${i+1}`);
 s.ups=[...new Set([...(s.ups||[]),...range(12).flatMap(g=>range(6).map(t=>`t${g}_${t}`)),...range(212).map(i=>`lm${i}`),...range(5).map(i=>`k${i+1}`)])];
 s.ach=[...[1,10,25,50,75,100,125,150,175,200,212].map(n=>`o${n}`),...range(12).map(i=>`r${i}`),...[100,1000,10000,50000].map(n=>`c${n}`),...[1,10,50].map(n=>`k${n}`),...range(12).map(i=>`g${i}`),...[1e6,1e9,1e12,1e15,1e18].map(n=>`l${n}`),"ref1","ref5","am1","am12","ev","wk7","mtr","tri","hac","zmaj","obala","poldne","piran","sam"];
 s.achT=Object.fromEntries(s.ach.map(id=>[id,now]));
 const patched=JSON.stringify(s); const commit=()=>{localStorage.setItem(KEY,patched);localStorage.removeItem("obcine-osel")};
 const guard=e=>{e.stopImmediatePropagation();commit()};
 window.addEventListener("pagehide",guard,{capture:true});window.addEventListener("visibilitychange",guard,{capture:true});
 commit(); location.reload();
})(); 0
"""
MAX=9007199254740991
variants={
 'modest buildings + play huge':{"sit":1e300,"life":1e300,"all":1e300,"votes":1e97,"clicks":MAX,"kur":MAX,"refs":MAX,"play":1e300,"__own":150},
 'modest buildings only':{"sit":1e300,"life":1e300,"all":1e300,"votes":1e97,"clicks":MAX,"kur":MAX,"refs":MAX,"__own":150},
 'numbers only':{"sit":1e300,"life":1e300,"all":1e300,"votes":1e97,"clicks":MAX,"kur":MAX,"refs":MAX},
 '+ play huge':{"sit":1e300,"life":1e300,"all":1e300,"votes":1e97,"clicks":MAX,"kur":MAX,"refs":MAX,"play":1e300},
 '+ first in 1970':{"sit":1e300,"life":1e300,"all":1e300,"votes":1e97,"clicks":MAX,"kur":MAX,"refs":MAX,"first":1},
 '+ runV/v removed':{"sit":1e300,"life":1e300,"all":1e300,"votes":1e97,"clicks":MAX,"kur":MAX,"refs":MAX,"v":None,"runV":None},
}
with sync_playwright() as p:
  b=p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
  bad=[]
  for name,patch in variants.items():
    c=b.new_context(viewport={'width':1600,'height':900});pg=c.new_page();pg.goto('http://127.0.0.2:8765/');pg.wait_for_timeout(800);pg.keyboard.press('Space');pg.evaluate("dispatchEvent(new Event('pagehide'))")
    pg.evaluate((SCRIPT % json.dumps(patch)).replace('OWNV',str(patch.pop('__own',1000000))) if False else (SCRIPT % json.dumps({k:v for k,v in patch.items() if k!='__own'})).replace('OWNV',str(patch.get('__own',1000000))));pg.wait_for_timeout(1500)
    txt=pg.evaluate("document.getElementById('p-bell').innerText")
    got="/O" in txt; print(f"{name:30s} cap={got}")
    if not got: bad.append(name)
    c.close()
  assert not bad, bad
print('ALL PASSED')
