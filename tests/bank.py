"""Ringing on a full meter banks time (1 s per paid ring, max 10 min): when you stop, the meter stays full while the
bank runs down, then the usual 5 s grace, then it drains. The bank survives a reload (meter full again) and is capped."""
import os, json
from playwright.sync_api import sync_playwright
bad = []
st = {"v": 5, "runV": 5, "sit": 2e6, "life": 5e7, "all": 8e7, "n": 14, "own": [30, 20, 12, 6, 2] + [0] * 7, "clicks": 800, "sound": 0, "lang": "sl", "ach": ["o1"]}
def rows(pg):
    t = pg.evaluate("document.getElementById('p-bell').innerText").split('\n')
    m = [l for l in t if 'zvonjenje' in l][0]; k = [l for l in t if 'polno' in l][0]
    full = '.' not in m.split('[')[1].split(']')[0]
    mm, ss = k.strip('| ').split()[-1].split(':'); return full, int(mm) * 60 + int(ss)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    c = b.new_context(viewport={'width': 1600, 'height': 900})
    c.add_init_script("if(!sessionStorage.x){sessionStorage.x=1;localStorage.setItem('obcine-v2',%s)};localStorage.setItem('obcine-hi','1')" % json.dumps(json.dumps(st)))
    pg = c.new_page(); pg.goto('http://localhost:8765/'); pg.wait_for_timeout(600)
    for i in range(55): pg.keyboard.press('Space'); pg.wait_for_timeout(105)
    full, bank = rows(pg); print('after ~6 s of ringing: meter full', full, '| bank', bank, 's')
    if not (full and 5 <= bank <= 20): bad.append('charge')
    pg.wait_for_timeout((bank + 1) * 1000)
    full2, bank2 = rows(pg); print('when the bank has run out: meter still full', full2, '| bank', bank2)
    if not (full2 and bank2 == 0): bad.append('hold')
    pg.wait_for_timeout(4000); full3, _ = rows(pg); print('4 s into the grace: still full', full3)
    if not full3: bad.append('grace')
    pg.wait_for_timeout(4000); full4, _ = rows(pg); print('after the grace: draining', not full4)
    if full4: bad.append('drain')
    # a bank survives a reload, with the meter full
    for i in range(45): pg.keyboard.press('Space'); pg.wait_for_timeout(105)
    pg.evaluate("dispatchEvent(new Event('pagehide'))"); pg.reload(); pg.wait_for_timeout(800)
    full5, bank5 = rows(pg); print('after a reload: meter full', full5, '| bank', bank5)
    if not (full5 and bank5 > 0): bad.append('reload')
    c.close()
    # capped at 10 minutes, also for a save that says otherwise
    c = b.new_context(viewport={'width': 1600, 'height': 900}); c.add_init_script("localStorage.setItem('obcine-v2',%s);localStorage.setItem('obcine-hi','1')" % json.dumps(json.dumps(dict(st, bank=99999))))
    pg = c.new_page(); pg.goto('http://localhost:8765/'); pg.wait_for_timeout(800); _, bank6 = rows(pg); print('a save claiming 99999 s: bank', bank6)
    if bank6 > 600: bad.append('cap')
assert not bad, bad
print('ALL PASSED')
