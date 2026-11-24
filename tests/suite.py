import os, json, sys
from playwright.sync_api import sync_playwright

URL = 'http://localhost:8765/'
FAKE_AUDIO = """
window.__osc=[];class FP{constructor(){this.value=0}setValueAtTime(){}exponentialRampToValueAtTime(){}cancelScheduledValues(){}}
class FN{constructor(){this.gain=new FP();this.frequency=new FP();this.delayTime=new FP();this.threshold=new FP();this.ratio=new FP();this.type=''}connect(n){return n}disconnect(){}start(t){window.__osc.push(this.frequency.value)}stop(){}}
class FAC{constructor(){this.currentTime=0;this.state='running';this.destination=new FN();setInterval(()=>this.currentTime+=.05,50)}resume(){}createGain(){return new FN()}createOscillator(){return new FN()}createDynamicsCompressor(){return new FN()}createDelay(){return new FN()}createBiquadFilter(){return new FN()}}
window.AudioContext=FAC;"""
BASE = {"sit": 9e5, "all": 5e8, "n": 45, "own": [40, 30, 20, 12, 8, 0, 0, 0, 0, 0, 0, 0], "ups": ["k1"], "clicks": 800,
        "save": 9e15, "sound": 1, "lang": "sl", "ach": ["o1", "o10", "o25", "c100", "l1000000", "g0", "ev", "wk7", "mtr"], "days": [0, 1, 2, 3, 4, 5, 6]}
fails = []


def check(name, cond, info=''):
    print(('PASS ' if cond else 'FAIL ') + name + (('  ' + str(info)) if info else ''))
    if not cond: fails.append(name)


def open_page(b, w, h, state, touch=False):
    c = b.new_context(viewport={'width': w, 'height': h}, has_touch=touch, is_mobile=touch)
    c.add_init_script(FAKE_AUDIO + "window.__date='2026-11-24T12:00:00';if(!sessionStorage.getItem('x')){sessionStorage.setItem('x',1);localStorage.setItem('obcine-v2',JSON.stringify(%s))}" % json.dumps(state))
    pg = c.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    pg.goto(URL); pg.wait_for_timeout(1200)
    pg.evaluate("document.getElementById('toast').hidden=true")
    return c, pg, errs


def own(pg, k):
    pg.evaluate("dispatchEvent(new Event('pagehide'))")
    return pg.evaluate(f"JSON.parse(localStorage.getItem('obcine-v2')).own[{k}]")


def state(pg, key):
    pg.evaluate("dispatchEvent(new Event('pagehide'))")
    return pg.evaluate(f"JSON.parse(localStorage.getItem('obcine-v2'))['{key}']")


def press(pg, sel, hold=0, touch=False):
    pg.evaluate("document.getElementById('toast').hidden=true")
    el = pg.locator(sel).first
    el.scroll_into_view_if_needed(); bb = el.bounding_box()
    x, y = bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2
    if touch:
        pg.touchscreen.tap(x, y)
    else:
        pg.mouse.move(x, y); pg.mouse.down(); pg.wait_for_timeout(hold); pg.mouse.up()
    pg.wait_for_timeout(150)


with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)

    # ---- clicks: every press must register, also slow ones while the page redraws
    for w, h, touch in [(1600, 1000, False), (390, 844, True)]:
        c, pg, errs = open_page(b, w, h, dict(BASE, sit=5e12), touch)
        for _ in range(30): pg.keyboard.press('Space')
        tag = f'[{w}{" touch" if touch else ""}]'
        for k in (0, 1, 2):
            n0 = own(pg, k); ok = 0
            for hold in (0, 120, 300, 600) if not touch else (0, 0, 0, 0):
                before = own(pg, k); press(pg, f'[data-a="g{k}"]', hold, touch); ok += own(pg, k) > before
            check(f'{tag} producer g{k}: 4/4 presses buy', ok == 4, f'{ok}/4')
        u0 = len(state(pg, 'ups')); press(pg, '[data-a^="u"]:not([data-a="unlock"]):not([data-a="upall"])', 300, touch)
        check(f'{tag} upgrade bought with a slow press', len(state(pg, 'ups')) == u0 + 1)
        n0 = state(pg, 'n'); press(pg, '[data-a="unlock"]', 300, touch)
        check(f'{tag} občina unlocked with a slow press', state(pg, 'n') == n0 + 1)
        press(pg, '[data-a="amt10"]', 0, touch); n0 = own(pg, 0); press(pg, '[data-a="g0"]', 0, touch)
        check(f'{tag} ×10 buys ten', own(pg, 0) == n0 + 10, own(pg, 0) - n0)
        press(pg, '[data-a="amt1"]', 0, touch)
        l0 = state(pg, 'light'); press(pg, '[data-a="thm"]', 200, touch)
        check(f'{tag} theme toggle', state(pg, 'light') != l0); press(pg, '[data-a="thm"]', 0, touch)
        if not touch:
            c0 = state(pg, 'clicks'); press(pg, '[data-a="g0"]', 0); pg.keyboard.press('Space'); pg.wait_for_timeout(100)
            check(f'{tag} Space still rings after clicking a button', state(pg, 'clicks') == c0 + 1)
        check(f'{tag} no script errors', not errs, errs)
        c.close()

    # ---- stability: nothing moves while buying, unlocking and crossing a million
    for w, h in [(1600, 1000), (1280, 900), (390, 844)]:
        c, pg, errs = open_page(b, w, h, dict(BASE, sit=1.05e6))
        tag = f'[{w}]'
        for ref in ('p-gen', 'p-next', 'p-stat', 'p-ups'):
            pg.evaluate(f"document.getElementById('{ref}').scrollIntoView({{block:'center'}})"); pg.wait_for_timeout(300)
            pos = set(); y0 = pg.evaluate("scrollY")
            for i in range(10):
                sel = ['[data-a="g0"]', '[data-a="g1"]', '[data-a="unlock"]', '[data-a="g2"]'][i % 4]
                if pg.locator(sel).count():
                    el = pg.locator(sel).first; bb = el.bounding_box()
                    # tap where it is, like a person; el.click() would first scroll it into view itself
                    if bb and 0 < bb['y'] and bb['y'] + bb['height'] < h: pg.mouse.click(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2)
                for _ in range(3):
                    pos.add(round(pg.evaluate(f"document.getElementById('{ref}').getBoundingClientRect().top"))); pg.wait_for_timeout(70)
            check(f'{tag} {ref} stays put while buying/unlocking', len(pos) == 1 and pg.evaluate("scrollY") == y0, sorted(pos))
        check(f'{tag} no script errors', not errs, errs)
        c.close()

    # ---- pop-up does not move while scrolling; dismisses on click; survives a layout change
    c, pg, errs = open_page(b, 1600, 900, dict(BASE, ach=[]))
    pg.evaluate("document.getElementById('toast').hidden=false")
    pg.wait_for_timeout(800); bots = set()  # let it settle onto the grid first
    for _ in range(25):
        pg.mouse.wheel(0, 41); pg.wait_for_timeout(25); bots.add(round(pg.evaluate("document.getElementById('toast').getBoundingClientRect().bottom")))
    check('pop-up stays still while scrolling', len(bots) == 1, sorted(bots))
    pg.wait_for_timeout(400)
    off = pg.evaluate("""()=>{const t=document.getElementById('toast').getBoundingClientRect();const r=document.getElementById('root').getBoundingClientRect();
      const lh=parseFloat(getComputedStyle(document.body).lineHeight);const o=((t.top-r.top)%lh+lh)%lh;return Math.min(o,lh-o)}""")
    check('pop-up settles onto the line grid when scrolling stops', off < 0.6, off)
    # after a reset the page changes under a pop-up that is already showing; it must stay on the grid
    pg.evaluate("act('rst');act('rstyes');render(true)"); pg.wait_for_timeout(1200)
    off = pg.evaluate("""()=>{const t=document.getElementById('toast');if(t.hidden)return 0;const b=t.getBoundingClientRect();const r=document.getElementById('root').getBoundingClientRect();
      const lh=parseFloat(getComputedStyle(document.body).lineHeight);const o=((b.top-r.top)%lh+lh)%lh;return Math.min(o,lh-o)}""")
    check('pop-up on the line grid after a reset', off < 0.6, off)
    pg.set_viewport_size({'width': 390, 'height': 844}); pg.wait_for_timeout(500)
    r = pg.evaluate("(()=>{const t=document.getElementById('toast');if(t.hidden)return 'hidden';const b=t.getBoundingClientRect();return [Math.round(b.left),Math.round(b.right),innerWidth]})()")
    check('pop-up fits the screen after switching to phone width', r == 'hidden' or (r[0] >= 0 and r[1] <= r[2]), r)
    if r != 'hidden':
        q0 = pg.evaluate("document.getElementById('toast').innerText"); pg.locator('#toast').click(); pg.wait_for_timeout(200)
        check('pop-up dismisses on click', pg.evaluate("document.getElementById('toast').hidden||document.getElementById('toast').innerText") != q0)
    check('no script errors', not errs, errs)
    c.close()

    # ---- sound: Kurent bells during both boosts, voice pools capped
    c, pg, errs = open_page(b, 1600, 900, dict(BASE, ups=["k1", "k2", "k3", "k4", "k5"]))
    pg.mouse.click(3, 3)
    def rings(n, gap):
        pg.evaluate("window.__osc.length=0")
        for _ in range(n): pg.keyboard.press('Space'); pg.wait_for_timeout(gap)
        return pg.evaluate("window.__osc.slice()")
    plain = rings(20, 40)
    pg.evaluate("__dbg.boost('kur',60000)"); kur = rings(20, 40)
    pg.evaluate("__dbg.boost('kur',0);__dbg.boost('clk',60000)"); clk = rings(20, 40)
    jk = sum(1 for f in kur if 900 <= f < 1400); jc = sum(1 for f in clk if 2400 <= f < 4200)
    check('every ring sounds a bell (20 fast rings)', len(plain) >= 20 * 9, len(plain))
    check('Kurentovanje: cowbells on every ring', jk >= 20 * 2, jk)
    check('zvonci: jingles on every ring', jc >= 20 * 3, jc)
    vmax = 0
    for _ in range(40): pg.keyboard.press('Space'); vmax = max(vmax, pg.evaluate("__dbg.voices"))
    check('bell voices stay within the cap while spamming', vmax <= 10, vmax)
    check('no script errors', not errs, errs)
    c.close()

    # ---- Kurent: spawn and catch on desktop and touch
    for w, h, touch in [(1600, 1000, False), (390, 844, True)]:
        c, pg, errs = open_page(b, w, h, BASE, touch)
        pg.evaluate("__dbg.spawn()"); pg.wait_for_timeout(200)
        k0 = state(pg, 'kur'); press(pg, '.kur', 0, touch)
        check(f'[{w}] Kurent can be caught', state(pg, 'kur') == k0 + 1)
        check(f'[{w}] no script errors', not errs, errs)
        c.close()

    # ---- save copy / load round trip
    c, pg, errs = open_page(b, 1600, 1000, BASE)
    c.grant_permissions(['clipboard-read', 'clipboard-write'])
    pg.locator('[data-a="exp"]').click(); pg.wait_for_timeout(300)
    txt = pg.evaluate("navigator.clipboard.readText()")
    pg.locator('#impin').fill(txt); pg.locator('[data-a="imp"]').click(); pg.wait_for_timeout(300)
    check('save copies and loads back', 'igra naložena' in pg.evaluate("document.getElementById('p-set').innerText"))
    pg.locator('#impin').fill('nonsense'); pg.locator('[data-a="imp"]').click(); pg.wait_for_timeout(300)
    check('a broken save is refused politely', 'ni veljavna' in pg.evaluate("document.getElementById('p-set').innerText"))
    check('no script errors', not errs, errs)
    c.close()
    b.close()

print('\nFAILED:' if fails else '\nALL PASSED', fails if fails else '')
