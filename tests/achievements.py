"""The 14 achievements (all 20 amendments among them) added on top of the first 61: each unlocks when its condition holds, and not before. 75 in all."""
import os, json
from playwright.sync_api import sync_playwright
bad = []
BASE = {"v": 5, "runV": 5, "sit": 5e9, "life": 9e10, "all": 9e10, "n": 60, "own": [20, 15, 10, 8, 5, 3, 0, 0, 0, 0, 0, 0], "clicks": 3000,
        "sound": 0, "lang": "sl", "ach": ["o1"], "amends": [], "first": 1764010000000, "play": 7200}
def got(b, date='2026-11-25T15:00:00', away_h=0, ring=0, **kw):
    sv = dict(BASE, **kw)
    if away_h: sv['save'] = 0  # filled in below, relative to the fake clock
    c = b.new_context(viewport={'width': 1600, 'height': 900})
    pre = "window.__date='%s';" % date
    if away_h: pre += "var __s=%s;__s.save=new Date('%s').getTime()-%d;" % (json.dumps(sv), date, away_h * 3600e3)
    else: pre += "var __s=%s;" % json.dumps(sv)
    c.add_init_script(pre + "localStorage.setItem('obcine-v2',JSON.stringify(__s));localStorage.setItem('obcine-hi','1')")
    pg = c.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:120])); pg.goto('http://localhost:8765/?debug'); pg.wait_for_timeout(700)
    for _ in range(ring): pg.keyboard.press(' '); pg.wait_for_timeout(120)
    pg.wait_for_timeout(1500); a = pg.evaluate("__dbg.S.ach.slice()"); total = pg.evaluate("document.getElementById('p-ach').innerText")
    c.close()
    if errs: bad.append(('errors', errs))
    return set(a), total
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    a0, total = got(b, bank=500, ring=4)
    print('total shown:', [l for l in total.split('\n') if '/75' in l][:1])
    if '/75' not in total: bad.append('total')
    new = ['c100000', 'k100', 'ref10', 'am20', 'play10', 'allgen', 'alllm', 'allbell', 'urb', 'sec', 'bank', 'jutro', 'noc', 'hol4']
    early = a0 & set(new); print('a fresh mid-game save already has:', sorted(early) or 'none of the new ones')
    if early: bad.append(('too early', early))
    ALLSEC = ['tri', 'hac', 'zmaj', 'obala', 'poldne', 'piran', 'sam']
    cases = [('c100000', dict(clicks=100000, life=9e14, all=9e14)), ('k100', dict(kur=100)), ('ref10', dict(refs=10, votes=200, life=9e20, all=9e20)),
             ('am20', dict(amends=['a%d' % i for i in range(1, 21)], refs=20, votes=300, life=9e20, all=9e20)), ('play10', dict(play=36000)),
             ('allgen', dict(n=212, own=[1] * 12, life=9e20, all=9e20)), ('urb', dict(n=190, life=9e18, all=9e18)),
             ('sec', dict(ach=['o1'] + ALLSEC)), ('bank', dict(bank=600, ring=4)), ('hol4', dict(evSeen={'pust': 2026, 'kultura': 2026, 'drzava': 2026, 'bozic': 2025}))]
    for id_, kw in cases:
        r = kw.pop('ring', 0); a, _ = got(b, ring=r, **kw); ok = id_ in a; print(f'{id_:8} unlocked: {ok}')
        if not ok: bad.append(id_)
    a, _ = got(b, away_h=9); print('jutro after 9 h away:', 'jutro' in a); bad += [] if 'jutro' in a else ['jutro']
    a, _ = got(b, away_h=3); print('jutro after 3 h away (should be no):', 'jutro' in a); bad += ['jutro early'] if 'jutro' in a else []
    a, _ = got(b, date='2026-11-25T02:30:00', ring=3); print('noc ringing at 02:30:', 'noc' in a); bad += [] if 'noc' in a else ['noc']
    a, _ = got(b, date='2026-11-25T05:30:00', ring=3); print('noc ringing at 05:30 (should be no):', 'noc' in a); bad += ['noc early'] if 'noc' in a else []
assert not bad, bad
print('ALL PASSED')
