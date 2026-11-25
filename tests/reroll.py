"""The three amendments on offer stay put until a referendum is held: cancelling, calling again or reloading doesn't redeal them."""
import os, json, re
from playwright.sync_api import sync_playwright
sv = {"v": 5, "runV": 5, "sit": 1e12, "life": 9e18, "all": 9e18, "n": 150, "own": [20, 15, 10, 8, 5, 3, 0, 0, 0, 0, 0, 0], "clicks": 30000,
      "sound": 0, "lang": "sl", "ach": ["o1"], "amends": [], "first": 1764010000000, "play": 72000}
bad = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    c = b.new_context(viewport={'width': 1600, 'height': 900})
    c.add_init_script("if(!sessionStorage.getItem('x')){sessionStorage.setItem('x',1);localStorage.setItem('obcine-v2',%s);localStorage.setItem('obcine-hi','1')}" % json.dumps(json.dumps(sv)))
    pg = c.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); pg.goto('http://localhost:8765/?debug'); pg.wait_for_timeout(700)
    def offer():
        pg.evaluate("__dbg.act('ref');__dbg.render(true);0")
        o = pg.evaluate("__dbg.S.offer.slice()"); pg.evaluate("__dbg.act('refno');__dbg.render(true);0"); return o
    first = offer(); again = [offer() for _ in range(5)]
    print('first offer:', first, '| after 5 cancels:', 'same' if all(a == first for a in again) else again)
    if any(a != first for a in again) or len(first) != 3: bad.append('cancel redeals')
    pg.evaluate("dispatchEvent(new Event('pagehide'))"); pg.reload(); pg.wait_for_timeout(800)
    after = offer(); print('after a reload:', after)
    if after != first: bad.append('reload redeals')
    pg.evaluate("__dbg.act('ref');0"); pg.evaluate("__dbg.act('am%s');__dbg.render(true);0" % first[0]); pg.wait_for_timeout(300)
    adopted = pg.evaluate("__dbg.S.amends.slice()"); nxt = pg.evaluate("__dbg.S.offer"); print('adopted:', adopted, '| offer cleared:', nxt in (None, []) )
    if adopted != [first[0]] or nxt not in (None, []): bad.append('adopt')
    if errs: bad.append(errs)
    c.close()
assert not bad, bad
print('ALL PASSED')
