"""Votes earned before the 26 Nov change: kept in full, and the referendum panel offers new votes again
from the point a new player with the same lifetime earnings would get them (not '+0' for weeks)."""
import os, json, re
from playwright.sync_api import sync_playwright
OLD = 1795608000000   # began 25 Nov 2026, before the change
def save(**kw):
    s = {"v": 5, "sit": 1e12, "n": 150, "own": [40, 30, 20, 12, 8, 4, 0, 0, 0, 0, 0, 0], "clicks": 60000, "kur": 50, "refs": 1,
         "sound": 0, "lang": "sl", "ach": ["o1"], "amends": [], "first": OLD, "play": 10 * 3600}
    s.update(kw); return s
def panel(b, sv):
    c = b.new_context(viewport={'width': 1600, 'height': 900})
    c.add_init_script("if(!sessionStorage.x){sessionStorage.x=1;localStorage.setItem('obcine-v2',%s);localStorage.setItem('obcine-hi','1')}" % json.dumps(json.dumps(sv)))
    pg = c.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); pg.goto('http://localhost:8765/?debug'); pg.wait_for_timeout(800)
    t = pg.evaluate("document.getElementById('p-ref').innerText"); S = pg.evaluate("[__dbg.S.votes,__dbg.S.oldVotes,__dbg.S.osel]")
    pg.evaluate("dispatchEvent(new Event('pagehide'))"); pg.reload(); pg.wait_for_timeout(800)
    S2 = pg.evaluate("[__dbg.S.votes,__dbg.S.oldVotes]"); c.close()
    g = int(re.search(r'dobiš\s+\+(\d+)', t).group(1)); return g, S, S2, errs
bad = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    # 150 old votes (all = 150^3 bn), now earned 4x as much: a new player would have cbrt(4*150^3e9/4e10)= 69 votes; old ones count 150/3.42 = 44
    g, S, S2, e = panel(b, save(votes=150, life=1.35e16, all=4 * 3.375e15))
    print(f'old save, 150 votes: panel offers +{g} (a new player at these earnings: 69, minus 44 for the old votes = +25) | kept {S[0]} votes, {S[1]} old | after a reload {S2} | cap: {bool(S[2])}', e)
    if not (24 <= g <= 26 and S[0] == 150 and S[1] == 150 and S2 == [150, 150] and not S[2] and not e): bad.append('old')
    # the same numbers on a new save: those votes are far beyond its earnings -> caught
    g, S, S2, e = panel(b, save(voteV=2, votes=150, life=1.35e16, all=4 * 3.375e15, first=1795700000000))
    print(f'same votes on a new save: cap: {bool(S[2])}')
    if not S[2]: bad.append('new save not caught')
    # a new save with honest votes: gain as before
    g, S, S2, e = panel(b, save(voteV=2, votes=20, life=1.35e16, all=4 * 3.375e15, first=1795700000000))
    print(f'new save, 20 votes: panel offers +{g} (69 - 20 = 49) | cap: {bool(S[2])}')
    if not (48 <= g <= 50 and not S[2]): bad.append('new')
assert not bad, bad
print('ALL PASSED')
