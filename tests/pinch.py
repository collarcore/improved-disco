"""Phones: two or three fingers on anything you play with (the bell, a Kurent, a pop-up, a button) can't start
a pinch-zoom, while a pinch on plain text still can (Chromium phone mode: WebKit on Linux can't make touch points);
and in WebKit's iPhone mode the page sets the iOS-only zoom limit."""
import os, json
from playwright.sync_api import sync_playwright
sv = {"v": 5, "voteV": 2, "sit": 1e6, "life": 1e9, "all": 1e9, "n": 30, "own": [10, 5, 3] + [0] * 9, "clicks": 3000, "sound": 0,
      "lang": "sl", "ach": ["o1"], "amends": [], "first": 1795608000000, "play": 7200}
bad = []
with sync_playwright() as p:
    wk = p.webkit.launch(); wc = wk.new_context(**p.devices['iPhone 13']); wp = wc.new_page(); wp.goto('http://127.0.0.1:8765/'); wp.wait_for_timeout(800)
    meta = wp.evaluate("document.querySelector('meta[name=viewport]').content"); wk.close()
    b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None); c = b.new_context(**p.devices['Pixel 7'])
    c.add_init_script("localStorage.setItem('obcine-v2',%s);localStorage.setItem('obcine-hi','1')" % json.dumps(json.dumps(sv)))
    pg = c.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); pg.goto('http://127.0.0.1:8765/?debug'); pg.wait_for_timeout(1000)
    pg.evaluate("__dbg.spawn();__dbg.toast('kurent','Pustni krof','test','');0"); pg.wait_for_timeout(500)
    def two_fingers(sel):
        return pg.evaluate("""sel=>{const el=document.querySelector(sel);if(!el)return null;el.scrollIntoView({block:'center'});const r=el.getBoundingClientRect();
          const mk=(id,dx)=>new Touch({identifier:id,target:el,clientX:r.x+4+dx,clientY:r.y+4});
          const ts=[mk(1,0),mk(2,6)];const ev=new TouchEvent('touchstart',{touches:ts,targetTouches:ts,changedTouches:ts,cancelable:true,bubbles:true});
          el.dispatchEvent(ev);const r2=ev.defaultPrevented;
          el.dispatchEvent(new TouchEvent('touchend',{touches:[],targetTouches:[],changedTouches:ts,cancelable:true,bubbles:true}));return r2}""", sel)
    res = {name: two_fingers(sel) for name, sel in (('bell (ZVONI)', '.ring'), ('Kurent', '.kur'), ('pop-up', '#toast'), ('a buy button', '[data-a^="u"],[data-a^="b"]'), ('plain text', '#p-log'))}
    print('iOS zoom limit (WebKit, iPhone):', 'maximum-scale=1' in meta); print('two fingers blocked:', res, errs)
    if 'maximum-scale=1' not in meta: bad.append('meta')
    for k, v in res.items():
        if (k == 'plain text') == bool(v) or v is None: bad.append(k)
    if errs: bad.append(errs)
assert not bad, bad
print('ALL PASSED')
