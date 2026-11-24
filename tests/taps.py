"""Phones: fast taps on the bell, a [KUPI] and a pop-up all register, and the page neither zooms nor moves."""
import os, json, random
from playwright.sync_api import sync_playwright
st={"sit":4e12,"n":120,"own":[60,50,40,30,20,10,5,2,0,0,0,0],"save":9e15,"sound":0,"lang":"sl","ach":["o1"],"clicks":0,"amt":1}
with sync_playwright() as p:
  b=p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
  c=b.new_context(viewport={'width':390,'height':844},device_scale_factor=3,is_mobile=True,has_touch=True)
  c.add_init_script("localStorage.setItem('obcine-v2',JSON.stringify(%s))"%json.dumps(st))
  pg=c.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.goto('http://localhost:8765/');pg.wait_for_timeout(900)
  pg.evaluate("document.getElementById('toast').hidden=true")
  pg.evaluate("document.querySelector('#p-bell .ring').scrollIntoView({block:'center'})");pg.wait_for_timeout(300)
  y0=pg.evaluate("scrollY");bb=pg.locator('#p-bell .ring').bounding_box()
  for i in range(30): pg.touchscreen.tap(bb['x']+bb['width']*random.random(),bb['y']+bb['height']*random.random()); pg.wait_for_timeout(60)
  pg.wait_for_timeout(200);pg.evaluate("dispatchEvent(new Event('pagehide'))")
  print('bell: 30 fast taps ->',pg.evaluate("JSON.parse(localStorage.getItem('obcine-v2')).clicks"),'rings; scale',pg.evaluate("visualViewport.scale"),'page moved',pg.evaluate("scrollY")-y0)
  el=pg.locator('[data-a="g0"]').first;el.scroll_into_view_if_needed();pg.wait_for_timeout(200);y0=pg.evaluate("scrollY");bb=el.bounding_box()
  o0=pg.evaluate("(dispatchEvent(new Event('pagehide')),JSON.parse(localStorage.getItem('obcine-v2')).own[0])")
  for i in range(5): pg.touchscreen.tap(bb['x']+bb['width']/2,bb['y']+bb['height']/2); pg.wait_for_timeout(80)
  pg.wait_for_timeout(200);o1=pg.evaluate("(dispatchEvent(new Event('pagehide')),JSON.parse(localStorage.getItem('obcine-v2')).own[0])")
  print('KUPI: 5 fast taps ->',o1-o0,'bought; page moved',pg.evaluate("scrollY")-y0)
  pg.evaluate("__dbg.toast('ach','Test','besedilo')");pg.wait_for_timeout(300);tb=pg.locator('#toast').bounding_box()
  pg.touchscreen.tap(tb['x']+40,tb['y']+40);pg.wait_for_timeout(200);print('tap closes pop-up:',pg.evaluate("document.getElementById('toast').hidden"))
  print('errors',errs)
