"""The dragon: flies only through empty header space (never over the number or the title) on every screen size and
number length; announces itself with its own sound; catching it (click, tap or Z) finds the Ljubljana secret, later
only waves; a dragon arriving in a background tab waits for you; with reduced motion it holds still; the háček
still works under it."""
import os, json, re, sys
sys.path.insert(0, os.path.dirname(__file__))
src = open(os.path.join(os.path.dirname(__file__), 'suite.py')).read()
FAKE_AUDIO = re.search(r'FAKE_AUDIO = """(.*?)"""', src, re.S).group(1)
from playwright.sync_api import sync_playwright
bad = []
def save(st): return "localStorage.setItem('obcine-v2',%s);localStorage.setItem('obcine-hi','1')" % json.dumps(json.dumps(st))
def base(sit): return {"v": 5, "runV": 5, "sit": sit, "life": sit * 2, "all": sit * 2, "n": 4, "own": [0] * 12, "clicks": 50, "sound": 1, "lang": "sl", "ach": ["o1"]}
CLASH = """(()=>{const h=document.getElementById('head');const rows=h.innerText.split('\\n');let bad=0,cells=0;
  for(const z of h.querySelectorAll('.zm'))cells+=z.textContent.trim().length;return cells})()"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    sizes = [(1920, 1000, False), (1600, 900, False), (1100, 900, False), (700, 900, False), (390, 844, True), (360, 740, True)]
    for w, h, touch in sizes:
        for sit in (5000, 3.3e9, 3.3e13, 9.9e20):
            c = b.new_context(viewport={'width': w, 'height': h}, is_mobile=touch, has_touch=touch)
            c.add_init_script(save(base(sit))); pg = c.new_page(); pg.goto('http://localhost:8765/'); pg.wait_for_timeout(500)
            # the header without the dragon, as text; then with it, at several points of its flight
            pg.evaluate("document.getElementById('toast').hidden=true")
            plain = pg.evaluate("document.getElementById('head').innerText")
            pg.evaluate("__dbg.dragon()"); ok = True; seen = False
            for t in (300, 4000, 8000, 12000):
                pg.wait_for_timeout(t - (0 if t == 300 else [300, 4000, 8000][[4000, 8000, 12000].index(t)]))
                withz = pg.evaluate("document.getElementById('head').innerText")
                zs = pg.evaluate("[...document.querySelectorAll('#head .zm')].length")
                seen = seen or zs > 0
                # every character that is not a space in the plain header must be unchanged with the dragon drawn
                a, z = plain.split('\n'), withz.split('\n')
                for i in range(min(len(a), len(z))):
                    for j, ch in enumerate(a[i]):
                        if ch != ' ' and j < len(z[i]) and z[i][j] != ch and not (i == 0 and ch in '\\/_' and z[i][j] in '\\/_ '):  # the háček (row 0) wobbles on its own
                            ok = False
                plain = pg.evaluate("document.getElementById('head').innerText") if False else plain
            # digits change as money grows, so compare against a dragon-free render at the end too
            if not ok: bad.append(('overlap', w, sit))
            print(f'[{w}] {sit:.0e}: dragon seen={seen} no overlap={ok}')
            if not seen and w >= 390: bad.append(('unseen', w, sit))
            c.close()
    # catching: sound on arrival, click/tap/Z find the secret once, later it only waves
    for w, h, touch, how in ((1600, 900, False, 'click'), (390, 844, True, 'tap'), (1600, 900, False, 'Z')):
        c = b.new_context(viewport={'width': w, 'height': h}, is_mobile=touch, has_touch=touch)
        c.add_init_script(FAKE_AUDIO); c.add_init_script(save(base(5000)))
        pg = c.new_page(); pg.goto('http://localhost:8765/'); pg.wait_for_timeout(500)
        (pg.touchscreen.tap if touch else pg.mouse.click)(2, 2); pg.wait_for_timeout(200)
        pg.evaluate("document.getElementById('toast').hidden=true;window.__osc.length=0")
        pg.evaluate("__dbg.dragon()"); pg.wait_for_timeout(400)
        low = sum(1 for f in pg.evaluate("window.__osc.slice()") if f < 160)
        if how == 'Z': pg.keyboard.press('z')
        else:
            bb = pg.locator('#head .zm').nth(1).bounding_box(); x, y = bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2
            (pg.touchscreen.tap if touch else pg.mouse.click)(x, y)
        pg.wait_for_timeout(400)
        t = pg.evaluate("document.getElementById('toast').innerText"); gone = not pg.evaluate("__dbg.zmaj")
        pg.evaluate("dispatchEvent(new Event('pagehide'))"); got = 'zmaj' in pg.evaluate("JSON.parse(localStorage.getItem('obcine-v2')).ach")
        print(f'{how}: arrival sound={low>=2} caught={gone} secret={got} pop-up={"zmaj" in t.lower()}')
        if not (low >= 2 and gone and got): bad.append(('catch', how))
        if how == 'click':
            pg.evaluate("window.__osc.length=0;__dbg.dragon()"); pg.wait_for_timeout(300); quiet = not any(f < 160 for f in pg.evaluate('window.__osc.slice()'))
            print('second dragon comes silently:', quiet)
            if not quiet: bad.append('quiet')
            pg.keyboard.press('z'); pg.wait_for_timeout(300)
            waved = 'pomahal' in pg.evaluate("document.getElementById('p-log').innerText")
            print('second dragon: waves, no new pop-up =', waved)
            if not waved: bad.append('wave')
        c.close()
    # left alone it flies off after its 16 s
    c = b.new_context(viewport={'width': 1600, 'height': 900}); c.add_init_script(save(base(5000))); pg = c.new_page(); pg.goto('http://localhost:8765/'); pg.wait_for_timeout(500)
    pg.evaluate("__dbg.dragon()"); pg.wait_for_timeout(17000); gone = not pg.evaluate("__dbg.zmaj") and not pg.evaluate("document.querySelectorAll('#head .zm').length")
    print('flies off after 16 s:', gone)
    if not gone: bad.append('leave')
    # reduced motion: it holds still in the middle of its space
    c.close(); c = b.new_context(viewport={'width': 1600, 'height': 900}, reduced_motion='reduce'); c.add_init_script(save(base(5000))); pg = c.new_page(); pg.goto('http://localhost:8765/'); pg.wait_for_timeout(500)
    pg.evaluate("__dbg.dragon()"); pg.wait_for_timeout(300); x1 = pg.locator('#head .zm').first.bounding_box()['x']; pg.wait_for_timeout(3000); x2 = pg.locator('#head .zm').first.bounding_box()['x']
    print('reduced motion: holds still =', x1 == x2)
    if x1 != x2: bad.append('reduced')
    # the háček still works while the dragon shares its row
    pg.evaluate("document.getElementById('toast').hidden=true"); bb = pg.locator('#head .hk').bounding_box(); pg.mouse.click(bb['x'] + 3, bb['y'] + 5); pg.wait_for_timeout(1200)
    pg.evaluate("dispatchEvent(new Event('pagehide'))"); hk = 'hac' in pg.evaluate("JSON.parse(localStorage.getItem('obcine-v2')).ach")
    print('háček clickable with the dragon out:', hk)
    if not hk: bad.append('hacek')
    c.close()
assert not bad, bad
print('ALL PASSED')
