"""Found secrets leave something behind: the M on Triglav, the seagull over the coast, the flag on the belfry, the
perched dragon, the anchored boat, and the noon bells ringing by themselves. None of them appear before their
secret is found; the dunce cap still wins over the flag."""
import os, json, re
src = open(os.path.join(os.path.dirname(__file__), 'suite.py')).read()
FAKE_AUDIO = re.search(r'FAKE_AUDIO = """(.*?)"""', src, re.S).group(1)
from playwright.sync_api import sync_playwright
bad = []
ALL = ["o1", "tri", "obala", "piran", "sam", "zmaj", "poldne", "hac"]
def save(ach, **kw): return dict({"v": 5, "runV": 5, "sit": 5000, "life": 5e9, "all": 5e9, "n": 40, "own": [0] * 12, "clicks": 2000, "sound": 1, "lang": "sl", "ach": ach, "first": 1764010000000}, **kw)
def look(pg): return pg.evaluate("""({M:document.querySelectorAll('#mapgrid .tm').length,gull:document.querySelectorAll('#mapgrid .gull').length,
  boat:document.querySelectorAll('#mapgrid .boat').length,dragon:document.querySelectorAll('#head .zm').length,flag:document.getElementById('p-bell').innerText.includes('|>')})""")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    for w, h, touch in ((1600, 900, False), (390, 844, True)):
        for ach, want in ((["o1"], 0), (ALL, 1)):
            c = b.new_context(viewport={'width': w, 'height': h}, is_mobile=touch, has_touch=touch)
            c.add_init_script("localStorage.setItem('obcine-v2',%s);localStorage.setItem('obcine-hi','1')" % json.dumps(json.dumps(save(ach))))
            pg = c.new_page(); pg.goto('http://localhost:8765/'); pg.wait_for_timeout(800); r = look(pg)
            ok = all(bool(v) == bool(want) for v in r.values())
            print(f'[{w}] {"all found" if want else "none found"}: {r} -> {"ok" if ok else "WRONG"}')
            if not ok: bad.append((w, want))
            if want:
                pg.evaluate("document.getElementById('toast').hidden=true;document.querySelector('#mapgrid .gull').scrollIntoView({block:'center'})"); pg.wait_for_timeout(300); bb = pg.locator('#mapgrid .gull').bounding_box()
                (pg.touchscreen.tap if touch else pg.mouse.click)(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2); pg.wait_for_timeout(300)
                g = 'galeb' in pg.evaluate("document.getElementById('p-log').innerText"); print('   tapping the gull:', g)
                if not g: bad.append(('gull-tap', w))
            c.close()
    # the dunce cap wins over the flag
    c = b.new_context(viewport={'width': 1600, 'height': 900}); c.add_init_script("localStorage.setItem('obcine-v2',%s);localStorage.setItem('obcine-hi','1')" % json.dumps(json.dumps(save(ALL, osel=1764010000000))))
    pg = c.new_page(); pg.goto('http://localhost:8765/'); pg.wait_for_timeout(800); t = pg.evaluate("document.getElementById('p-bell').innerText")
    print('dunce cap over the flag:', '/O\\' in t and '|>' not in t)
    if not ('/O\\' in t and '|>' not in t): bad.append('cap')
    c.close()
    # noon rings by itself once found (and only then), once a day
    for ach, want in ((["o1"], False), (ALL, True)):
        c = b.new_context(viewport={'width': 1600, 'height': 900}); c.add_init_script(FAKE_AUDIO)
        c.add_init_script("window.__date='2026-11-25T12:00:20';localStorage.setItem('obcine-v2',%s);localStorage.setItem('obcine-hi','1')" % json.dumps(json.dumps(save(ach))))
        pg = c.new_page(); pg.goto('http://localhost:8765/'); pg.mouse.click(3, 3); pg.wait_for_timeout(1500)
        pg.evaluate("dispatchEvent(new Event('pagehide'))")  # the whole saved log: the panel shows only the newest 8 lines
        rang = any('poldne: zvonijo' in l for l in pg.evaluate("JSON.parse(localStorage.getItem('obcine-v2')).log"))
        great = sum(1 for f in pg.evaluate("window.__osc.slice()") if f in (196, 262, 220))
        print(f'noon at 12:00 with {"the secret" if want else "no secret"}: bells rang by themselves = {rang}')
        if rang != want: bad.append(('noon', want))
        c.close()
assert not bad, bad
print('ALL PASSED')
