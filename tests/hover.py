"""Sweeping the mouse across the map (and the register) must not flash the legend."""
import os, json
from playwright.sync_api import sync_playwright
st = {"sit": 4e9, "n": 120, "own": [60, 50, 40, 30, 20, 10, 5, 2, 0, 0, 0, 0], "save": 9e15, "sound": 0, "lang": "sl"}
fails = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    for w in (1600, 1024):
        c = b.new_context(viewport={'width': w, 'height': 1000})
        c.add_init_script("localStorage.setItem('obcine-v2',JSON.stringify(%s))" % json.dumps(st))
        pg = c.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('http://localhost:8765/'); pg.wait_for_timeout(800)
        pg.evaluate("document.getElementById('toast').hidden=true")
        g = pg.locator('#mapgrid'); g.scroll_into_view_if_needed(); bb = g.bounding_box()
        # record every change of the info box while sweeping
        pg.evaluate("""window.__seen=[];new MutationObserver(()=>{const t=document.getElementById('mapinfo');if(t)window.__seen.push([t.innerText.includes('premakni'),performance.now()])})
          .observe(document.getElementById('p-map'),{childList:true,subtree:true,characterData:true})""")
        # horizontal, vertical and diagonal sweeps with smooth movement (many intermediate pointer events)
        paths = [((0.05, 0.4), (0.95, 0.4)), ((0.3, 0.1), (0.3, 0.9)), ((0.55, 0.1), (0.55, 0.85)), ((0.1, 0.2), (0.8, 0.9))]
        for (x0, y0), (x1, y1) in paths:
            pg.mouse.move(bb['x'] + bb['width'] * x0, bb['y'] + bb['height'] * y0)
            for k in range(1, 41):
                f = k / 40
                pg.mouse.move(bb['x'] + bb['width'] * (x0 + (x1 - x0) * f), bb['y'] + bb['height'] * (y0 + (y1 - y0) * f), steps=4); pg.wait_for_timeout(12)
        seen = pg.evaluate("window.__seen")
        # a flash = the legend shows for under 0.25 s between two municipalities
        flashes = sum(1 for i in range(1, len(seen) - 1) if seen[i][0] and not seen[i - 1][0] and not seen[i + 1][0] and seen[i + 1][1] - seen[i][1] < 250)
        ok = flashes == 0
        print(('PASS' if ok else 'FAIL') + f' [{w}] sweeping the map: legend flashes {flashes} times ({len(seen)} info updates)', errs)
        if not ok: fails.append(w)
        c.close()
    b.close()
print('ALL PASSED' if not fails else 'FAILED')
