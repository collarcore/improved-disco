"""The Kurent's doughnut pays 3 minutes of what you earn right now, the ringing multiplier included."""
import os, json
from playwright.sync_api import sync_playwright
sv = {"v": 5, "runV": 5, "sit": 1e6, "life": 9e10, "all": 9e10, "n": 60, "own": [20, 15, 10, 8, 5, 3, 0, 0, 0, 0, 0, 0], "clicks": 3000,
      "sound": 0, "lang": "sl", "ach": ["o1"], "amends": [], "first": 1764010000000, "play": 7200}
bad = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    for ring in (0, 60):
        c = b.new_context(viewport={'width': 1600, 'height': 900})
        c.add_init_script("localStorage.setItem('obcine-v2',%s);localStorage.setItem('obcine-hi','1')" % json.dumps(json.dumps(sv)))
        pg = c.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); pg.goto('http://localhost:8765/?debug'); pg.wait_for_timeout(700)
        for _ in range(ring): pg.keyboard.press(' '); pg.wait_for_timeout(105)
        # the rate as the player sees it, then a doughnut straight away
        r = pg.evaluate("""(()=>{const S=__dbg.S;const before=S.sit;Math.random=()=>.6;__dbg.spawn();
            const ips0=__dbg.ips();__dbg.act('kurent');return [S.sit-before, ips0]})()""")
        got, ips = r; ratio = (got - 25) / ips
        print(f'rang {ring:2}×: income {ips:,.0f}/s, doughnut {got:,.0f} = {ratio:.1f} s of it', errs)
        if abs(ratio - 180) > 3 or errs: bad.append((ring, ratio, errs))
        c.close()
assert not bad, bad
print('ALL PASSED')
