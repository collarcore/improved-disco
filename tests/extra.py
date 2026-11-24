"""More checks: other layouts, keyboard, performance, offline income, meter drain,
English UI, light theme, map highlighting, referendum pop-up, console warnings."""
import os, json, time
from playwright.sync_api import sync_playwright

URL = 'http://localhost:8765/'
BASE = {"sit": 5e12, "all": 5e15, "n": 120, "own": [60, 50, 40, 30, 20, 10, 5, 2, 0, 0, 0, 0], "ups": ["k1"], "clicks": 3000,
        "save": 9e15, "sound": 0, "lang": "sl", "ach": ["o1", "o10", "o25", "o50", "o75", "o100", "c100", "c1000", "l1000000", "l1000000000", "l1000000000000", "g0", "g1", "g2", "g3", "ev", "wk7", "mtr", "k1"], "days": [0, 1, 2, 3, 4, 5, 6]}
fails = []


def check(name, cond, info=''):
    print(('PASS ' if cond else 'FAIL ') + name + (('  ' + str(info)) if info else ''))
    if not cond: fails.append(name)


def open_page(b, w, h, state, touch=False, keep_save=False):
    c = b.new_context(viewport={'width': w, 'height': h}, has_touch=touch, is_mobile=touch)
    c.add_init_script("window.__date='2026-11-24T12:00:00';" + ("" if keep_save else "if(!sessionStorage.getItem('x')){sessionStorage.setItem('x',1);") +
                      "localStorage.setItem('obcine-v2',JSON.stringify(%s))" % json.dumps(state) + ("" if keep_save else "}"))
    pg = c.new_page(); errs = []; warns = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: (errs if m.type == 'error' else warns).append(m.text) if m.type in ('error', 'warning') else None)
    pg.goto(URL); pg.wait_for_timeout(1200)
    return c, pg, errs, warns


def S(pg, key):
    pg.evaluate("dispatchEvent(new Event('pagehide'))")
    return pg.evaluate(f"JSON.parse(localStorage.getItem('obcine-v2'))['{key}']")


with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)

    # ---- two-column layouts: clicks register
    for w in (1024, 1280):
        c, pg, errs, warns = open_page(b, w, 900, BASE)
        pg.evaluate("document.getElementById('toast').hidden=true")
        o0 = S(pg, 'own')[0]
        for hold in (0, 250):
            el = pg.locator('[data-a="g0"]').first; el.scroll_into_view_if_needed(); bb = el.bounding_box()
            pg.mouse.move(bb['x'] + 5, bb['y'] + 5); pg.mouse.down(); pg.wait_for_timeout(hold); pg.mouse.up(); pg.wait_for_timeout(150)
        check(f'[{w}] producer presses register', S(pg, 'own')[0] == o0 + 2, S(pg, 'own')[0] - o0)
        n0 = S(pg, 'n'); pg.locator('[data-a="unlock"]').click(); pg.wait_for_timeout(150)
        check(f'[{w}] unlock', S(pg, 'n') == n0 + 1)
        u0 = len(S(pg, 'ups'))
        if pg.locator('[data-a="upall"]').count(): pg.locator('[data-a="upall"]').click(); pg.wait_for_timeout(150)
        check(f'[{w}] buy all upgrades', len(S(pg, 'ups')) > u0, len(S(pg, 'ups')) - u0)
        row = pg.locator('[data-o]').nth(2); oi = row.get_attribute('data-o'); row.scroll_into_view_if_needed(); row.hover(); pg.wait_for_timeout(150)
        check(f'[{w}] register row highlights the map', f'.c{oi}' in pg.evaluate("document.getElementById('hov').textContent"), oi)
        check(f'[{w}] no script errors', not errs, errs)
        c.close()

    # ---- keyboard only: Tab to a button, Enter buys; Space rings; N unlocks
    c, pg, errs, warns = open_page(b, 1600, 1000, BASE)
    pg.evaluate("document.getElementById('toast').hidden=true")
    pg.evaluate("document.querySelector('[data-a=\"g0\"]').focus()")
    o0 = S(pg, 'own')[0]; pg.keyboard.press('Enter'); pg.wait_for_timeout(150)
    check('keyboard: Enter on a focused button buys', S(pg, 'own')[0] == o0 + 1)
    check('keyboard: focus stays on that button after the redraw', pg.evaluate("document.activeElement&&document.activeElement.dataset.a") == 'g0')
    pg.evaluate("document.activeElement.blur()")
    k0 = S(pg, 'clicks'); pg.keyboard.press('Space'); pg.wait_for_timeout(100)
    check('keyboard: Space rings', S(pg, 'clicks') == k0 + 1)
    n0 = S(pg, 'n'); pg.keyboard.press('n'); pg.wait_for_timeout(100)
    check('keyboard: N unlocks', S(pg, 'n') == n0 + 1)
    tabbable = pg.evaluate("[...document.querySelectorAll('[tabindex=\"0\"]')].length")
    check('keyboard: buttons are reachable with Tab', tabbable > 20, tabbable)

    # ---- performance: long tasks while idle and while spamming the bell
    pg.evaluate("window.__lt=0;new PerformanceObserver(l=>{window.__lt+=l.getEntries().length}).observe({entryTypes:['longtask']})")
    pg.wait_for_timeout(3000); idle = pg.evaluate("window.__lt")
    for _ in range(60): pg.keyboard.press('Space'); pg.wait_for_timeout(30)
    spam = pg.evaluate("window.__lt") - idle
    check('performance: no long tasks while idle (3 s)', idle == 0, idle)
    check('performance: at most a few long tasks while spamming 60 rings', spam <= 3, spam)

    # ---- ringing meter fills and then drains after the pause
    m1 = pg.evaluate("__dbg.meter"); pg.wait_for_timeout(8000); m2 = pg.evaluate("__dbg.meter")
    check('meter filled by ringing', m1 > .5, round(m1, 2))
    check('meter drains after a pause', m2 < m1, (round(m1, 2), round(m2, 2)))
    check('no script errors', not errs, errs)
    check('no console warnings', not warns, warns[:3])
    c.close()

    # ---- offline income on load
    st = dict(BASE, save=int(time.time() * 1000) - 2 * 3600 * 1000, sit=0)
    c, pg, errs, warns = open_page(b, 1600, 1000, st, keep_save=True)
    log0 = pg.evaluate("document.getElementById('p-log').innerText")
    check('offline income paid and logged', S(pg, 'sit') > 0 and 'odsotnost' in log0, log0.split('\n')[1].strip()[:70])
    c.close()

    # ---- English UI end to end
    c, pg, errs, warns = open_page(b, 1600, 1000, dict(BASE, lang='en'))
    txt = pg.evaluate("document.body.innerText")
    sl_words = [w for w in ('občine', 'naslednja', 'zvonjenje', 'KUPI', 'odkleni', 'tolarji', 'dohodek', 'izboljšave') if w in txt.replace('Občine:', '')]
    check('English: no Slovenian UI words left', not sl_words, sl_words)
    pg.evaluate("__dbg.spawn()"); pg.wait_for_timeout(150); pg.locator('.kur').first.click(); pg.wait_for_timeout(250)
    check('English: Kurent pop-up in English', any(s in pg.evaluate("document.getElementById('toast').innerText") for s in ('Income', 'doughnut', 'Clicks')))
    check('English: number format', '5.00 T' in pg.evaluate("document.getElementById('p-stat').innerText") or ' T' in pg.evaluate("document.getElementById('p-stat').innerText"))
    check('no script errors', not errs, errs)
    c.close()

    # ---- light theme
    c, pg, errs, warns = open_page(b, 1600, 1000, dict(BASE, light=1))
    bg = pg.evaluate("getComputedStyle(document.body).backgroundColor"); fg = pg.evaluate("getComputedStyle(document.body).color")
    check('light theme: black on white', bg == 'rgb(255, 255, 255)' and fg == 'rgb(0, 0, 0)', (bg, fg))
    c.close()

    # ---- referendum: offer, adopt, pop-up, reset
    c, pg, errs, warns = open_page(b, 1600, 1000, BASE)
    pg.evaluate("document.getElementById('toast').hidden=true")
    pg.locator('[data-a="ref"]').click(); pg.wait_for_timeout(150)
    offers = pg.evaluate("[...document.querySelectorAll('[data-a^=ama]')].map(e=>e.dataset.a)")
    check('referendum offers 3 amendments', len(offers) == 3, offers)
    pg.locator(f'[data-a="{offers[0]}"]').click(); pg.wait_for_timeout(300)
    check('referendum resets the run and keeps the amendment', S(pg, 'n') == 0 and offers[0][2:] in S(pg, 'amends'))
    check('amendment pop-up shown', 'REFERENDUM' in pg.evaluate("document.getElementById('toast').innerText"))
    check('no script errors', not errs, errs)
    c.close()
    b.close()

print('\nFAILED:' if fails else '\nALL PASSED', fails if fails else '')
