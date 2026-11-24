"""The secret achievements: each can be found the way a player would, and none of them breaks anything."""
import os, json
from playwright.sync_api import sync_playwright
fails = []


def check(name, cond, info=''):
    print(('PASS ' if cond else 'FAIL ') + name + (('  ' + str(info)) if info else ''))
    if not cond: fails.append(name)


def open_page(b, w, state, date='2026-11-24T15:00:00'):
    c = b.new_context(viewport={'width': w, 'height': 1000})
    c.add_init_script("window.__date='%s';if(!sessionStorage.getItem('x')){sessionStorage.setItem('x',1);localStorage.setItem('obcine-v2',JSON.stringify(%s))}" % (date, json.dumps(state)))
    pg = c.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://localhost:8765/'); pg.wait_for_timeout(900)
    return c, pg, errs


def ach(pg):
    pg.evaluate("dispatchEvent(new Event('pagehide'))")
    return pg.evaluate("JSON.parse(localStorage.getItem('obcine-v2')).ach")


BASE = {"sit": 4e9, "n": 120, "own": [60, 50, 40, 30, 20, 10, 5, 2, 0, 0, 0, 0], "save": 9e15, "sound": 0, "lang": "sl", "ach": ["o1"]}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    for w in (1600, 390):
        c, pg, errs = open_page(b, w, BASE)
        tag = f'[{w}]'
        # strešica
        widths = lambda: {len(l) for l in pg.evaluate("document.getElementById('head').innerText").split('\n')}
        w0 = widths(); pg.locator('[data-a="hacek"]').click(); pg.wait_for_timeout(1100)
        head = pg.evaluate("document.getElementById('head').innerText").split('\n')
        check(f'{tag} háček knocked off: title Obcine, banner without it', pg.evaluate("__dbg.noHacek") and 'Obcine' in pg.title() and '\\/' not in head[0], head[0].strip())
        check(f'{tag} háček: secret found', 'hac' in ach(pg))
        check(f'{tag} háček: header keeps its width', widths() == w0, (w0, widths()))
        pg.locator('[data-a="hacek"]').click(); pg.wait_for_timeout(1100)
        check(f'{tag} háček put back', not pg.evaluate("__dbg.noHacek") and 'Občine' in pg.title() and '\\/' in pg.evaluate("document.getElementById('head').innerText").split('\n')[0])
        # 47 km obale
        pg.evaluate("document.getElementById('toast').hidden=true")
        sea = pg.locator('#mapgrid .sea').first; sea.scroll_into_view_if_needed()
        for _ in range(10): sea.click(); pg.wait_for_timeout(40)
        check(f'{tag} sea ×10: seagull and secret', 'obala' in ach(pg) and 'burek' in pg.evaluate("document.body.innerText"))
        # triglav still works
        pg.keyboard.type('triglav'); pg.wait_for_timeout(200)
        check(f'{tag} typing triglav still works', 'tri' in ach(pg))
        # panel: unfound secrets stay hidden
        found = ach(pg)
        check(f'{tag} unfound secrets show ???', 'zmaj' not in found and 'Ljubljanski zmaj' not in pg.evaluate("document.body.innerText"))
        check(f'{tag} no script errors', not errs, errs)
        c.close()
    # zmaj: needs Ljubljana unlocked
    c, pg, errs = open_page(b, 1600, dict(BASE, n=211))
    pg.locator('#mapgrid i.c211').first.click(); pg.wait_for_timeout(200)
    check('locked Ljubljana: no dragon yet', 'zmaj' not in ach(pg))
    c.close()
    c, pg, errs = open_page(b, 1600, dict(BASE, n=212, won=1))
    pg.evaluate("document.getElementById('toast').hidden=true")
    pg.locator('#mapgrid i.c211').first.click(); pg.wait_for_timeout(250)
    check('Ljubljana unlocked: dragon appears', 'zmaj' in ach(pg) and 'Zmajskega' in pg.evaluate("document.getElementById('toast').innerText"))
    check('no script errors', not errs, errs)
    c.close()
    # poldne: only during the 12:00 minute, once a day
    c, pg, errs = open_page(b, 1600, BASE, date='2026-11-24T11:59:30')
    pg.keyboard.press('Space'); pg.wait_for_timeout(150)
    check('11:59: no noon bells', 'poldne' not in ach(pg))
    c.close()
    c, pg, errs = open_page(b, 1600, BASE, date='2026-11-24T12:00:30')
    pg.evaluate("document.getElementById('toast').hidden=true")
    pg.keyboard.press('Space'); pg.wait_for_timeout(200)
    check('12:00: noon bells and secret', 'poldne' in ach(pg) and 'poldne' in pg.evaluate("document.getElementById('toast').innerText").lower())
    pg.evaluate("document.getElementById('toast').hidden=true;window.__n=0;new MutationObserver(()=>window.__n++).observe(document.getElementById('toast'),{childList:true})")
    pg.keyboard.press('Space'); pg.wait_for_timeout(200)
    check('12:00 again: only once a day', pg.evaluate("window.__n") == 0)
    check('no script errors', not errs, errs)
    c.close()
    # Piran at sunset: only within half an hour of sunset, only when Piran is unlocked
    for when, want in (('2026-11-24T16:20:00', True), ('2026-11-24T14:00:00', False)):
        c, pg, errs = open_page(b, 1600, dict(BASE, n=200), date=when)
        pg.evaluate("document.getElementById('toast').hidden=true")
        pg.locator('#mapgrid i.c187').first.click(); pg.wait_for_timeout(250)
        check(f'Piran at {when[11:16]}: secret {"found" if want else "not yet"}', ('piran' in ach(pg)) == want)
        check('no script errors', not errs, errs)
        c.close()
    c, pg, errs = open_page(b, 1600, dict(BASE, n=150), date='2026-11-24T16:20:00')
    pg.locator('#mapgrid i.c187').first.click(); pg.wait_for_timeout(250)
    check('locked Piran at sunset: nothing', 'piran' not in ach(pg))
    c.close()
    # 1991 rings
    c, pg, errs = open_page(b, 1600, dict(BASE, clicks=1989))
    pg.evaluate("document.getElementById('toast').hidden=true")
    pg.keyboard.press('Space'); pg.wait_for_timeout(100)
    check('1990 rings: not yet', 'sam' not in ach(pg))
    pg.keyboard.press('Space'); pg.wait_for_timeout(200)
    check('1991 rings: independence secret', 'sam' in ach(pg) and '1991' in pg.evaluate("document.getElementById('toast').innerText"))
    check('no script errors', not errs, errs)
    c.close()
    c, pg, errs = open_page(b, 1600, dict(BASE, clicks=5000))
    pg.keyboard.press('Space'); pg.wait_for_timeout(200)
    check('older save past 1991: found on the next ring', 'sam' in ach(pg))
    c.close()
    # the certificate: winning shows a pop-up and the panel; the result copies
    c, pg, errs = open_page(b, 1600, dict(BASE, n=211, sit=1e40, clicks=777, kur=4, refs=2))
    c.grant_permissions(['clipboard-read', 'clipboard-write'])
    pg.evaluate("document.getElementById('toast').hidden=true")
    pg.locator('[data-a="unlock"]').first.click(); pg.wait_for_timeout(400)
    body = pg.evaluate("document.body.innerText")
    check('win: certificate pop-up', 'ČESTITKE' in pg.evaluate("document.getElementById('toast').innerText"))
    check('win: certificate panel with stats', 'LISTINA' in body and 'ujetih kurentov' in body and 'skrivnosti' in body)
    pg.locator('[data-a="share"]').first.click(); pg.wait_for_timeout(300)
    clip = pg.evaluate("navigator.clipboard.readText()")
    check('copy result: text on the clipboard', 'vseh 212' in clip and 'collarcore.github.io' in clip, clip)
    check('copy result: button says copied', 'KOPIRANO' in pg.evaluate("document.body.innerText"))
    check('no script errors', not errs, errs)
    c.close()
    b.close()
print('\nFAILED:' if fails else '\nALL PASSED', fails if fails else '')
