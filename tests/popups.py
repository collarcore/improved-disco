"""Pop-ups: every kind, the longest texts, at many screen sizes and scroll positions.
Each must be fully on screen, the width of its column and aligned with it, clear of the
phone's bell dock, and drawn as an intact box with nothing cut off."""
import os, json
from playwright.sync_api import sync_playwright
st = {"sit": 4e9, "n": 120, "own": [60, 50, 40, 30, 20, 10, 5, 2, 0, 0, 0, 0], "save": 9e15, "sound": 0, "ach": ["o1"]}
KINDS = {
 'sl': [('ach', 'Cela regija: Primorsko-notranjska', 'odkleni vse občine regije. Dohodek +1 %.'),
        ('reg', 'Jugovzhodna Slovenija', 'Vseh 21 občin je tvojih. Dohodek ×1,25.'),
        ('ev', 'Danes: Gasilska veselica', 'vse ×1,1, kurent pogosteje.'),
        ('kur', 'Pustni krof', '+999,99 kvadd SIT (3 minute dohodka).'),
        ('ref', 'Zakon o lokalni samoupravi', 'odklep občin je 20 % cenejši.'),
        ('new', 'ZVONOVI VSEH FAR', 'Tvoj zvon zdaj zveni drugače. Pozvoni!'),
        ('zmaj', 'Ljubljanski zmaj', 'Z Zmajskega mostu pazi na prestolnico. Nanj se lahko zaneseš.'),
        ('galeb', 'Galeb', 'ti je pojedel burek. Na vseh 47 km obale je našel ravno tebe.'),
        ('poldne', 'Poldne', 'Zvonovi vseh far odzvanjajo poldne. Tudi tvoj.')],
 'en': [('ach', 'Region complete: Littoral-Inner Carniola', 'unlock every municipality in the region. Income +1%.'),
        ('reg', 'Littoral-Inner Carniola', 'All 6 municipalities are yours. Income ×1.25.'),
        ('ev', "Today: Firefighters' party", 'everything ×1.1, the Kurent comes more often.'),
        ('kur', 'Carnival doughnut', '+999.99 Oc SIT (3 minutes of income).'),
        ('ref', 'Local Self-Government Act', 'unlocking municipalities costs 20% less.'),
        ('new', 'BELLS OF EVERY PARISH', 'Your bell sounds different now. Ring it!'),
        ('zmaj', 'The Ljubljana dragon', 'From the Dragon Bridge it watches over the capital. You can count on it.'),
        ('galeb', 'A seagull', 'stole your burek. 47 km of coast, and it found you.'),
        ('poldne', 'Noon', 'Every parish rings noon. Yours too.')]}
fails = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    for lang in ('sl', 'en'):
        for w, h in [(320, 568), (360, 640), (390, 844), (600, 900), (768, 1024), (1024, 768), (1280, 800), (1366, 768), (1440, 900), (1920, 1080)]:
            c = b.new_context(viewport={'width': w, 'height': h})
            c.add_init_script("localStorage.setItem('obcine-v2',JSON.stringify(%s))" % json.dumps(dict(st, lang=lang)))
            pg = c.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto('http://localhost:8765/'); pg.wait_for_timeout(700)
            maxy = pg.evaluate("document.documentElement.scrollHeight-innerHeight")
            for sy in (0, maxy // 2, maxy):
                pg.evaluate(f"scrollTo(0,{sy})"); pg.wait_for_timeout(250)
                for kind, ti, tx in KINDS[lang]:
                    pg.evaluate("window.__trunc.length=0")
                    pg.evaluate(f"__dbg.toast({json.dumps(kind)},{json.dumps(ti)},{json.dumps(tx)})"); pg.wait_for_timeout(120)
                    r = pg.evaluate("""()=>{const t=document.getElementById('toast');const b=t.getBoundingClientRect();
                      const three=document.querySelectorAll('#cols .col').length===3;const host=document.querySelectorAll('#cols .col')[three?2:0].getBoundingClientRect();
                      const d=document.getElementById('dock');const db=d.hidden?null:d.getBoundingClientRect();
                      const ls=t.innerText.replace(/\\n$/,'').split('\\n');const pre=[...ls[0]].length;
                      return {l:b.left,r:b.right,t:b.top,bo:b.bottom,hl:host.left,hr:host.right,dock:db&&db.top,lines:ls.map(x=>[...x].length),w0:pre,tr:window.__trunc.length,hidden:t.hidden}}""")
                    problems = []
                    if r['hidden']: problems.append('not shown')
                    if r['l'] < -0.5 or r['r'] > w + 0.5 or r['t'] < -0.5 or r['bo'] > h + 0.5: problems.append(f"off screen {round(r['l'])},{round(r['t'])}-{round(r['r'])},{round(r['bo'])}")
                    if abs(r['l'] - r['hl']) > 1 or abs(r['r'] - r['hr']) > 1: problems.append(f"not on its column ({round(r['l'])}-{round(r['r'])} vs {round(r['hl'])}-{round(r['hr'])})")
                    if r['dock'] is not None and r['bo'] > r['dock'] + 1.5: problems.append(f"overlaps the dock by {round(r['bo']-r['dock'])}px")
                    if len(set(r['lines'])) != 1: problems.append(f"box lines differ {sorted(set(r['lines']))}")
                    if r['tr']: problems.append('text cut off')
                    if problems:
                        fails.append((lang, w, h, sy, kind, problems))
            if errs: fails.append((lang, w, h, 'errors', errs))
            c.close()
    b.close()
for f in fails[:25]: print('FAIL', f)
print(f'{len(fails)} problems' if fails else 'ALL PASSED: 9 kinds x 10 sizes x 3 scroll positions x 2 languages')
