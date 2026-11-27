"""Sound comes back by itself: after an interruption (iOS suspends audio for a call, Siri or switching apps)
the next tap, click or key resumes it; turning sound on in Settings wakes it at once."""
import os, json
from playwright.sync_api import sync_playwright
sv = {"v": 5, "voteV": 2, "sit": 1e6, "life": 1e9, "all": 1e9, "n": 30, "own": [10, 5, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0], "clicks": 3000,
      "sound": 1, "lang": "sl", "ach": ["o1"], "amends": [], "first": 1764010000000, "play": 7200}
bad = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    for touch in (False, True):
        c = b.new_context(viewport={'width': 390, 'height': 844} if touch else {'width': 1600, 'height': 900}, has_touch=touch, is_mobile=touch)
        c.add_init_script("localStorage.setItem('obcine-v2',%s);localStorage.setItem('obcine-hi','1')" % json.dumps(json.dumps(sv)))
        pg = c.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); pg.goto('http://localhost:8765/?debug'); pg.wait_for_timeout(700)
        tap = (lambda: pg.touchscreen.tap(200, 300)) if touch else (lambda: pg.mouse.click(200, 300))
        tap(); pg.wait_for_timeout(300); first = pg.evaluate("__dbg.audio()")
        pg.evaluate("__dbg.hush();0"); pg.wait_for_timeout(300); hushed = pg.evaluate("__dbg.audio()")
        tap(); pg.wait_for_timeout(300); back = pg.evaluate("__dbg.audio()")
        # sound off, interrupted, then switched on from Settings: wakes on that same click
        pg.evaluate("__dbg.S.sound=0;__dbg.hush();0"); pg.wait_for_timeout(300)
        pg.evaluate("__dbg.act('snd');0"); pg.wait_for_timeout(300); toggled = pg.evaluate("__dbg.audio()")
        kind = 'phone (touch)' if touch else 'desktop (mouse)'
        print(f'{kind}: after first tap {first} | interrupted {hushed} | next tap {back} | sound switched on {toggled}', errs)
        if not (first == 'running' and hushed == 'suspended' and back == 'running' and toggled == 'running') or errs: bad.append(kind)
        c.close()
assert not bad, bad
print('ALL PASSED')
