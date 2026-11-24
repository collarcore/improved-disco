"""The boat: sails on the map's sea (a sailboat on the big map, a hull on the phone map); its horn announces it;
tapping it (or J) finds the Piran secret with its own text, later it only sails off; it leaves after 25 s."""
import os, json, re
src = open(os.path.join(os.path.dirname(__file__), 'suite.py')).read()
FAKE_AUDIO = re.search(r'FAKE_AUDIO = """(.*?)"""', src, re.S).group(1)
from playwright.sync_api import sync_playwright
bad = []
st = {"v": 5, "runV": 5, "sit": 5000, "life": 1e4, "all": 1e4, "n": 4, "own": [0] * 12, "clicks": 50, "sound": 1, "lang": "sl", "ach": ["o1"]}
def ach(pg): pg.evaluate("dispatchEvent(new Event('pagehide'))"); return pg.evaluate("JSON.parse(localStorage.getItem('obcine-v2')).ach")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    for w, h, touch, how in ((1600, 900, False, 'click'), (390, 844, True, 'tap'), (1600, 900, False, 'J')):
        c = b.new_context(viewport={'width': w, 'height': h}, is_mobile=touch, has_touch=touch)
        c.add_init_script(FAKE_AUDIO); c.add_init_script("localStorage.setItem('obcine-v2',%s);localStorage.setItem('obcine-hi','1')" % json.dumps(json.dumps(st)))
        pg = c.new_page(); pg.goto('http://localhost:8765/'); pg.wait_for_timeout(500)
        (pg.touchscreen.tap if touch else pg.mouse.click)(2, 2); pg.wait_for_timeout(200)
        pg.evaluate("document.getElementById('toast').hidden=true;window.__osc.length=0")
        pg.evaluate("__dbg.boat()"); pg.wait_for_timeout(500)
        horn = sum(1 for f in pg.evaluate("window.__osc.slice()") if f < 120)
        n = pg.evaluate("document.querySelectorAll('#mapgrid .boat').length")
        txt = pg.evaluate("[...document.querySelectorAll('#mapgrid .boat')].map(e=>e.textContent).join('')")
        if how == 'J': pg.keyboard.press('j')
        else:
            pg.evaluate("document.querySelector('#mapgrid .boat').scrollIntoView({block:'center'})"); pg.wait_for_timeout(200)
            cells = pg.locator('#mapgrid .boat'); k = [i for i in range(cells.count()) if cells.nth(i).text_content().strip() in ('|', '\\', '/', '_')][0]
            bb = cells.nth(k).bounding_box(); (pg.touchscreen.tap if touch else pg.mouse.click)(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2)
        pg.wait_for_timeout(400)
        t = pg.evaluate("document.getElementById('toast').innerText"); got = 'piran' in ach(pg)
        print(f'[{w}] {how}: horn={horn>=2} boat cells={n} drawn={txt.strip()!r} caught->secret={got} boat text={"Jadrnica" in t}')
        if not (horn >= 2 and n and got and 'Jadrnica' in t): bad.append(how)
        if how == 'click':
            pg.evaluate("__dbg.boat()"); pg.wait_for_timeout(300); pg.keyboard.press('j'); pg.wait_for_timeout(300)
            sailed = 'odplula' in pg.evaluate("document.getElementById('p-log').innerText"); print('second boat: sails off, no new pop-up =', sailed)
            if not sailed: bad.append('again')
        c.close()
    c = b.new_context(viewport={'width': 1600, 'height': 900}); c.add_init_script("localStorage.setItem('obcine-v2',%s);localStorage.setItem('obcine-hi','1')" % json.dumps(json.dumps(st)))
    pg = c.new_page(); pg.goto('http://localhost:8765/'); pg.wait_for_timeout(500); pg.evaluate("__dbg.boat()"); pg.wait_for_timeout(26000)
    gone = not pg.evaluate("__dbg.boatOut") and not pg.evaluate("document.querySelectorAll('#mapgrid .boat').length"); print('leaves after 25 s:', gone)
    if not gone: bad.append('leave')
assert not bad, bad
print('ALL PASSED')
