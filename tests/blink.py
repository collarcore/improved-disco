"""The next municipality's '?' blinks steadily: the map is redrawn whenever the seagull, boat or Kurent moves,
and the blink must carry on from the clock instead of restarting with every redraw."""
import os, json
from playwright.sync_api import sync_playwright
sv = {"v": 5, "voteV": 2, "sit": 1e3, "life": 1e9, "all": 1e9, "n": 30, "own": [10, 5, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0], "clicks": 3000,
      "sound": 0, "lang": "sl", "ach": ["o1", "obala"], "amends": [], "first": 1764010000000, "play": 7200}
bad = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    c = b.new_context(viewport={'width': 1600, 'height': 900})
    c.add_init_script("localStorage.setItem('obcine-v2',%s);localStorage.setItem('obcine-hi','1')" % json.dumps(json.dumps(sv)))
    pg = c.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); pg.goto('http://localhost:8765/?debug'); pg.wait_for_timeout(800)
    worst = 0; redraws = 0; last = None
    for _ in range(14):
        r = pg.evaluate("""(()=>{const q=document.querySelector('#mapgrid .q');const a=q&&q.getAnimations()[0];if(!a)return null;
          const t=a.effect.getComputedTiming();return [t.progress, (document.timeline.currentTime%1000)/1000, document.getElementById('mapgrid')]})()""")
        node = pg.evaluate("document.getElementById('mapgrid').getAttribute('style')")
        if node != last: redraws += 1; last = node
        if r: d = abs(r[0] - r[1]); worst = max(worst, min(d, 1 - d))
        pg.wait_for_timeout(370)
    print(f'map redrawn {redraws}× in 5 s (the seagull flapping); the ? blink is off the clock by at most {worst:.3f} of a blink', errs)
    if redraws < 3 or worst > .05 or errs: bad.append((redraws, worst, errs))
assert not bad, bad
print('ALL PASSED')
