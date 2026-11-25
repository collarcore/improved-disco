"""All 20 amendments: offered three at a time from those not yet adopted; each one does what it says."""
import os, json, re
from playwright.sync_api import sync_playwright
bad = []
def save(am, **kw): return json.dumps(json.dumps(dict({"v": 5, "runV": 5, "sit": 5e9, "life": 9e10, "all": 9e10, "n": 60, "own": [20, 15, 10, 8, 5, 3, 0, 0, 0, 0, 0, 0], "clicks": 3000, "sound": 0, "lang": "sl", "ach": ["o1"], "amends": am, "first": 1764010000000}, **kw)))
def page(b, am, date='2026-11-25T15:00:00', **kw):
    c = b.new_context(viewport={'width': 1600, 'height': 900})
    c.add_init_script("window.__date='%s';localStorage.setItem('obcine-v2',%s);localStorage.setItem('obcine-hi','1')" % (date, save(am, **kw)))
    pg = c.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:100])); pg.goto('http://localhost:8765/'); pg.wait_for_timeout(700); return c, pg, errs
def stat(pg, label):
    t = pg.evaluate("document.getElementById('p-stat').innerText")
    for l in t.split('\n'):
        if label in l: return l.strip('| ').split()[-1]
    return None
def num(x): return float(x.replace('.', '').replace(',', '.').replace('×', ''))
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    # night shift: ×1.5 at 22:00, nothing at 15:00
    c, pg, e = page(b, ['a18'], '2026-11-25T22:00:00'); night = stat(pg, 'nočna izmena'); c.close()
    c, pg, e = page(b, ['a18'], '2026-11-25T15:00:00'); day = stat(pg, 'nočna izmena'); c.close()
    print('night shift at 22:00:', night, '| at 15:00:', day); 
    if night != '×1,50' or day is not None: bad.append('a18')
    # urban municipalities: +5 % each
    c, pg, e = page(b, ['a20'], n=212, life=1e16, all=1e16, sit=1e12); u = pg.evaluate("document.getElementById('p-stat').innerText"); c.close()
    m = re.search(r'mestne občine \((\d+)\)\s+×([\d,]+)', u); print('urban municipalities:', m.group(0) if m else None)
    if not m or abs(num(m.group(2)) - (1 + .05 * int(m.group(1)))) > .006: bad.append('a20')
    # cooperatives: production upgrades half price
    def upcost(am):
        c, pg, e = page(b, am); t = pg.evaluate("document.getElementById('p-ups').innerText"); c.close()
        mm = re.search(r'Njiva: boljše orodje\s+([\d.,]+)', t); return num(mm.group(1)) if mm else None
    a, z = upcost([]), upcost(['a19']); print('field tool upgrade:', a, '-> with cooperatives', z)
    if not (a and z and abs(z - a / 2) < 1): bad.append('a19')
    # market days double a weekday's bonus (Sunday: clicks ×3 -> ×5, meter ×2 -> ×3); holiday law a holiday's (Prešeren Day: clicks ×3 -> ×5)
    for am, date, what in (([], '2026-11-29T15:00:00', 'Sunday'), (['a16'], '2026-11-29T15:00:00', 'Sunday, market days'),
                           ([], '2027-02-08T15:00:00', 'Prešeren Day'), (['a17'], '2027-02-08T15:00:00', 'Prešeren Day, holiday law'), (['a16'], '2027-02-08T15:00:00', 'Prešeren Day, market days')):
        c, pg, e = page(b, am, date); ev = pg.evaluate("__dbg.ev()"); c.close(); print(f'{what}: clicks ×{ev["click"]:g}, meter fill ×{ev["fill"]:g}')
    def ev(am, date): c, pg, e = page(b, am, date); r = pg.evaluate("__dbg.ev()"); c.close(); return r
    if not (ev(['a16'], '2026-11-29T15:00:00')['click'] == 5 and ev(['a16'], '2026-11-29T15:00:00')['fill'] == 3 and ev(['a17'], '2027-02-08T15:00:00')['click'] >= 5): bad.append('a16/a17')
    # bank cap: 30 min with bell-ringing tradition
    c, pg, e = page(b, ['a14'], bank=99999); bk = [l for l in pg.evaluate("document.getElementById('p-bell').innerText").split('\n') if 'polno' in l][0]; c.close()
    print('bank with bell-ringing tradition:', bk.strip('| '))
    if '30:00' not in bk and '29:5' not in bk: bad.append('a14')
    # offers: three, never one already adopted; and with all 20 adopted, none
    c, pg, e = page(b, ['a%d' % i for i in range(1, 18)], n=150, life=1e15, all=1e15, sit=1e12, votes=0)
    offered = set()
    for _ in range(15):
        pg.evaluate("__dbg.act('ref');__dbg.render(true);0"); t = pg.evaluate("document.getElementById('p-ref').innerText")
        offered |= {x for x in ('Nočna izmena', 'Zadružništvo', 'Mestne občine') if x in t}
        if any(x in t for x in ('Cenejša proizvodnja', 'Dežurstvo', 'Praznični zakon')): bad.append('offered an adopted one')
        pg.evaluate("__dbg.act('refno')")
    print('with 17 adopted, offers come only from the 3 left:', sorted(offered))
    if offered != {'Nočna izmena', 'Zadružništvo', 'Mestne občine'}: bad.append('offer')
    c.close()
    for errs in (e,):
        if errs: bad.append(('errors', errs))
assert not bad, bad
print('ALL PASSED')
