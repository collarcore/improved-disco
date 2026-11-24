"""First visit: one welcome pop-up and a blinking ZVONI button until the first ring. Never again after that, and
never for someone who already plays."""
import os, json
from playwright.sync_api import sync_playwright
bad = []
def toast(pg): return pg.evaluate("document.getElementById('toast').hidden?'':document.getElementById('toast').innerText")
def nudge(pg): return pg.evaluate("!!document.querySelector('#p-bell .ring.nudge')")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    for w, h, touch in ((1600, 900, False), (390, 844, True)):
        c = b.new_context(viewport={'width': w, 'height': h}, is_mobile=touch, has_touch=touch); pg = c.new_page()
        pg.goto('http://localhost:8765/'); pg.wait_for_timeout(800)
        t = toast(pg); first = 'DOBRODOŠEL' in t and 'Klikaj zvon' in t; blinking = nudge(pg)
        el = pg.locator('#p-bell .ring.nudge').first; el.scroll_into_view_if_needed(); bb = el.bounding_box()
        (pg.touchscreen.tap if touch else pg.mouse.click)(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2); pg.wait_for_timeout(300)
        stopped = not nudge(pg)
        pg.evaluate("dispatchEvent(new Event('pagehide'))"); pg.reload(); pg.wait_for_timeout(800)
        again = 'DOBRODOŠEL' in toast(pg)
        print(f'[{w}] first visit: welcome={first} button blinks={blinking} | after first ring: blinking stopped={stopped} | after reload: welcome again={again}')
        if not (first and blinking and stopped and not again): bad.append(w)
        c.close()
    # someone who already plays never sees it
    c = b.new_context(viewport={'width': 1600, 'height': 900})
    c.add_init_script("localStorage.setItem('obcine-v2',JSON.stringify({v:5,runV:5,sit:50,life:300,all:300,n:1,own:[3,0,0,0,0,0,0,0,0,0,0,0],clicks:120,sound:0}))")
    pg = c.new_page(); pg.goto('http://localhost:8765/'); pg.wait_for_timeout(800)
    seen = 'DOBRODOŠEL' in toast(pg) or nudge(pg); print('existing player: welcome or blinking =', seen)
    if seen: bad.append('existing')
assert not bad, bad
print('ALL PASSED')
