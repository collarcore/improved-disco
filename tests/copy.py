"""Copy buttons (save code, certificate result) work on phones and desktops: they run inside the tap's click (iOS
refuses the clipboard otherwise), fall back to an older copy method, and as a last resort select the code in the
paste field for copying by hand. Each press copies once."""
import os, json
from playwright.sync_api import sync_playwright
bad = []
def press(pg, sel, touch):
    pg.locator(sel).first.scroll_into_view_if_needed(); pg.wait_for_timeout(200)
    bb = pg.locator(sel).first.bounding_box(); x, y = bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2
    if touch: pg.touchscreen.tap(x, y)
    else: pg.mouse.click(x, y)
    pg.wait_for_timeout(400)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    for touch in (False, True):
        kw = dict(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True) if touch else dict(viewport={'width': 1600, 'height': 900})
        # 1) clipboard works
        c = b.new_context(permissions=['clipboard-read', 'clipboard-write'], **kw); pg = c.new_page(); pg.goto('http://localhost:8765/'); pg.wait_for_timeout(700)
        pg.evaluate("navigator.clipboard.writeText('')")
        pg.evaluate("window.__n=0;const w=navigator.clipboard.writeText.bind(navigator.clipboard);navigator.clipboard.writeText=t=>{window.__n++;return w(t)};0")
        press(pg, '[data-a="exp"]', touch)
        clip = pg.evaluate("navigator.clipboard.readText()"); n = pg.evaluate("window.__n")
        ok = clip.startswith('OB1.') and n == 1
        print(f"{'touch' if touch else 'mouse'}: save code copied={clip.startswith('OB1.')} times={n}")
        if not ok: bad.append(('clip', touch))
        c.close()
        # 2) clipboard refused (like a strict iPhone browser): the older method or the paste field takes over
        c = b.new_context(**kw); pg = c.new_page(); pg.goto('http://localhost:8765/'); pg.wait_for_timeout(700)
        pg.evaluate("navigator.clipboard.writeText=()=>Promise.reject(new Error('NotAllowed'));document.execCommand=()=>false;0")
        press(pg, '[data-a="exp"]', touch)
        v = pg.evaluate("(document.getElementById('impin')||{}).value||''")
        sel = pg.evaluate("(()=>{const i=document.getElementById('impin');return i&&i.selectionStart===0&&i.selectionEnd===i.value.length&&i.value.length>10})()")
        msg = 'ročno' in pg.evaluate("document.body.innerText")
        print(f"{'touch' if touch else 'mouse'}: refused -> code in paste field={v.startswith('OB1.')} selected={sel} message={msg}")
        if not (v.startswith('OB1.') and sel and msg): bad.append(('manual', touch))
        c.close()
assert not bad, bad
print('ALL PASSED')
