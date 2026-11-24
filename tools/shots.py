"""Renders the README screenshot (docs/screenshot.png) and the link preview (og.png) from the game.
Needs the built index.html served on :8765 (python3 -m http.server 8765) and Playwright."""
import os, json, io
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OWN = [60, 50, 40, 30, 20, 10, 5, 2, 0, 0, 0, 0]
# a Tuesday in November: crafts day and Martinovanje; the day's pop-up already seen, so the holiday shows
DATE = '2026-11-24T15:00:00'
MID = {"sit": 3.7e6, "life": 4e9, "all": 4e9, "first": 1764010000000, "play": 50000, "n": 75, "own": [40, 30, 20, 12, 8, 4, 0, 0, 0, 0, 0, 0], "ups": [], "save": 9e15, "sound": 0, "lang": "sl",
       "ach": ["o1", "o10", "o25", "o50", "o75", "c100", "c1000", "tri", "ev"], "clicks": 1500, "evSeen": {"day": "Tue Nov 24 2026"}}
LATE = {"sit": 4e12, "life": 9e14, "all": 9e14, "votes": 40, "refs": 2, "first": 1764010000000, "play": 90000, "n": 128, "own": OWN, "ups": ["k1", "k2", "k3"], "ach": ["o1", "ev"], "save": 9e15, "sound": 0, "lang": "sl", "clicks": 9000,
        "evSeen": {"day": "Tue Nov 24 2026", "martin": 2026}}


def page(b, state, w, h):
    c = b.new_context(viewport={'width': w, 'height': h})
    c.add_init_script("window.__date='%s';localStorage.setItem('obcine-v2',JSON.stringify(%s));localStorage.setItem('obcine-hi','1')" % (DATE, json.dumps(state)))
    pg = c.new_page(); pg.goto('http://localhost:8765/'); pg.wait_for_timeout(1000)
    return c, pg


def shot(loc):
    return Image.open(io.BytesIO(loc.screenshot()))


with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    # README: mid-run, with the Martinovanje pop-up and a few rings floating off the bell
    c, pg = page(b, MID, 1600, 1000)
    pg.wait_for_timeout(600)
    pg.evaluate("__dbg.dragon()"); pg.wait_for_timeout(6500)
    for _ in range(12): pg.keyboard.press('Space'); pg.wait_for_timeout(130)
    pg.screenshot(path=os.path.join(ROOT, 'docs/screenshot.png'))
    c.close()
    # link preview: banner, bell tower with a full meter, the map at 128/212 with the Kurent on it
    c, pg = page(b, LATE, 1600, 1100)
    pg.evaluate("document.getElementById('toast').hidden=true")
    for _ in range(80): pg.keyboard.press('Space'); pg.wait_for_timeout(15)
    pg.wait_for_timeout(2200)  # let the floating numbers fade
    pg.evaluate("__dbg.spawn();__dbg.boat()"); pg.wait_for_timeout(9000)
    pg.evaluate("document.getElementById('toast').hidden=true")
    head = shot(pg.locator('#head'))
    bell = shot(pg.locator('#p-bell'))
    mp = shot(pg.locator('#p-map'))
    c.close()
    b.close()

# the banner is the left part of the header, down to the subtitle
px = head.convert('L').load()
x1 = max(x for x in range(min(head.width, 500)) for y in range(head.height) if px[x, y] > 80) + 2
rows = [y for y in range(head.height) if any(px[x, y] > 80 for x in range(x1))]
blocks = []
for y in rows:
    if blocks and y - blocks[-1][1] <= 8: blocks[-1][1] = y
    else: blocks.append([y, y])
logo = max(range(len(blocks)), key=lambda i: blocks[i][1] - blocks[i][0])  # the tallest block is the logo; the subtitle follows it
gap = blocks[logo + 1][1] + 6 if logo + 1 < len(blocks) else head.height
banner = head.crop((0, 0, x1, gap))
og = Image.new('RGB', (1200, 630), 'black')
og.paste(banner, (40, 30))
og.paste(bell.crop((0, 0, bell.width, min(bell.height, 630 - 60 - banner.height))), (40, 30 + banner.height + 20))
og.paste(mp.crop((0, 0, min(mp.width, 1200 - 430), min(mp.height, 610))), (430, 10))
og.save(os.path.join(ROOT, 'og.png'))
print('docs/screenshot.png', Image.open(os.path.join(ROOT, 'docs/screenshot.png')).size, 'og.png', og.size, 'banner', banner.size, 'bell', bell.size, 'map', mp.size)
