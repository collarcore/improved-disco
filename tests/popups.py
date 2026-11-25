"""Pop-ups: every kind, the longest texts, at many screen sizes and scroll positions.
Each must be the same height (10 lines), fully on screen, the width of its column and aligned with it, and drawn as an intact box with nothing cut off."""
import os, json
from playwright.sync_api import sync_playwright
st = {"sit": 4e9, "n": 120, "own": [60, 50, 40, 30, 20, 10, 5, 2, 0, 0, 0, 0], "save": 9e15, "sound": 0, "ach": ["o1"]}
KINDS = {
 'sl': [
        ('hi', 'Dobrodošel v Občinah', 'Klikaj zvon ali preslednico. S tolarji kupuj proizvodnjo in odklepaj občine.'),
        ('upd', 'Nova različica', 'Igra je posodobljena. Tapni tukaj za osvežitev; napredek ostane.'),
        ('osel', 'Ponarejeni tolarji', 'Teh tolarjev nisi prizvonil. Zvonik bo zdaj za vedno nosil oslovsko kapo.'),
        ('ev', 'Prešernov dan', 'klik ×3.'),
        ('ev', 'Dan državnosti', 'vse ×1,25.'),
        ('new', 'VELIKI ZVON', 'Tvoj zvon zdaj zveni drugače. Pozvoni!'),
        ('new', 'ZVONOVI VSEH FAR', 'Tvoj zvon zdaj zveni drugače. Pozvoni! '),
        ('piran', 'Zahod v Piranu', 'Sonce tone v morje za Tartinijevim trgom. Lepšega zahoda ni. Dosežek:\u00a0+1 %.'),
        ('grb', '25. junij 1991', '1991 zvonov za samostojno Slovenijo. Vsi so zvonili s teboj. Dosežek:\u00a0+1 %.'),
        ('win', 'Vsa Slovenija je tvoja', 'Vseh 212 občin. Tvoja listina je v panelu Naslednja občina.'),
        ('ach', 'Cela regija: Primorsko-notranjska', 'odkleni vse občine regije. Dohodek +1 %.'),
        ('reg', 'Jugovzhodna Slovenija', 'Vseh 21 občin je tvojih. Dohodek ×1,25.'),
        ('ev', 'Danes: Gasilska veselica', 'vse ×1,1, kurent pogosteje.'),
        ('kur', 'Pustni krof', '+999,99 kvadd SIT (3 minute dohodka).'),
        ('ref', 'Zakon o lokalni samoupravi', 'odklep občin je 20 % cenejši.'),
        ('new', 'ZVONOVI VSEH FAR', 'Tvoj zvon zdaj zveni drugače. Pozvoni!'),
        ('zmaj', 'Ljubljanski zmaj', 'Z Zmajskega mostu pazi na prestolnico. Nanj se lahko zaneseš.'),
        ('galeb', 'Galeb in burek', 'Galeb ti je pojedel burek. Na vseh 47 km obale je našel ravno tebe.'),
        ('poldne', 'Poldne', 'Zvonovi vseh far odzvanjajo poldne. Tudi tvoj.'),
        ('triglav', 'Na vrhu', 'Triglav, 2864 m. Vsak Slovenec mora vsaj enkrat gor. Dosežek: +1 %.'),
        ('hacek', 'Strešica', 'Strešica je padla s črke Č. Zdaj so Občine samo Obcine. Klikni jo, da jo vrneš. Dosežek: +1 %.')],
 'en': [
        ('hi', 'Welcome to Občine', 'Click the bell or press space. Spend tolars on production and unlock municipalities.'),
        ('upd', 'New version', 'The game has been updated. Tap here to reload; your progress stays.'),
        ('osel', 'Counterfeit tolars', 'You did not ring up these tolars. From now on the belfry wears a dunce cap.'),
        ('ev', 'Prešeren Day', 'clicks ×3.'),
        ('ev', 'Statehood Day', 'everything ×1.25.'),
        ('new', 'GREAT BELL', 'Your bell sounds different now. Ring it!'),
        ('new', 'BELLS OF EVERY PARISH', 'Your bell sounds different now. Ring it! '),
        ('piran', 'Sunset in Piran', 'The sun sinks into the sea behind Tartini Square. No finer sunset. Achievement:\u00a0+1%.'),
        ('grb', '25 June 1991', '1991 rings for an independent Slovenia. Every bell rang with you. Achievement:\u00a0+1%.'),
        ('win', 'All of Slovenia is yours', 'All 212 municipalities. Your certificate is in the Next municipality panel.'),
        ('ach', 'Region complete: Littoral-Inner Carniola', 'unlock every municipality in the region. Income +1%.'),
        ('reg', 'Littoral-Inner Carniola', 'All 6 municipalities are yours. Income ×1.25.'),
        ('ev', "Today: Firefighters' party", 'everything ×1.1, the Kurent comes more often.'),
        ('kur', 'Carnival doughnut', '+999.99 Oc SIT (3 minutes of income).'),
        ('ref', 'Local Self-Government Act', 'unlocking municipalities costs 20% less.'),
        ('new', 'BELLS OF EVERY PARISH', 'Your bell sounds different now. Ring it!'),
        ('zmaj', 'The Ljubljana dragon', 'From the Dragon Bridge it watches over the capital. You can count on it.'),
        ('galeb', 'A seagull', 'stole your burek. 47 km of coast, and it found you.'),
        ('poldne', 'Noon', 'Every parish rings noon. Yours too.'),
        ('triglav', 'On top', 'Triglav, 2,864 m. Every Slovene has to climb it at least once. Achievement: +1%.'),
        ('hacek', 'The háček', 'The háček fell off the Č: Občine is now Obcine. Click it to put it back. Achievement: +1%.')]}
ART = {('sl','hi','Dobrodošel v Občinah'):'b2',('en','hi','Welcome to Občine'):'b2',('sl','ev','Prešernov dan'):'kultura',('sl','ev','Dan državnosti'):'drzava',('sl','new','VELIKI ZVON'):'b4',('sl','new','ZVONOVI VSEH FAR'):'b5',
       ('en','ev','Prešeren Day'):'kultura',('en','ev','Statehood Day'):'drzava',('en','new','GREAT BELL'):'b4',('en','new','BELLS OF EVERY PARISH'):'b5'}
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
                    pg.evaluate("([k,ti,tx,a])=>__dbg.toast(k,ti,tx,a?(a[0]==='b'?__dbg.art.BELLART[+a.slice(1)]:__dbg.art.EVART[a]):undefined)",[kind,ti,tx,ART.get((lang,kind,ti))]); pg.wait_for_timeout(120)
                    r = pg.evaluate("""()=>{const t=document.getElementById('toast');const b=t.getBoundingClientRect();
                      const three=document.querySelectorAll('#cols .col').length===3;const host=document.querySelectorAll('#cols .col')[three?2:0].getBoundingClientRect();
                      const db=null;
                      const ls=t.innerText.replace(/\\n$/,'').split('\\n');const pre=[...ls[0]].length;
                      return {l:b.left,r:b.right,t:b.top,bo:b.bottom,hl:host.left,hr:host.right,dock:db&&db.top,lines:ls.map(x=>[...x].length),w0:pre,tr:window.__trunc.length,hidden:t.hidden}}""")
                    problems = []
                    if r['hidden']: problems.append('not shown')
                    if r['l'] < -0.5 or r['r'] > w + 0.5 or r['t'] < -0.5 or r['bo'] > h + 0.5: problems.append(f"off screen {round(r['l'])},{round(r['t'])}-{round(r['r'])},{round(r['bo'])}")
                    if abs(r['l'] - r['hl']) > 1 or abs(r['r'] - r['hr']) > 1: problems.append(f"not on its column ({round(r['l'])}-{round(r['r'])} vs {round(r['hl'])}-{round(r['hr'])})")
                    if len(set(r['lines'])) != 1: problems.append(f"box lines differ {sorted(set(r['lines']))}")
                    if r['tr']: problems.append('text cut off')
                    if len(r['lines']) != 10: problems.append(f"{len(r['lines'])} lines tall, not 10")
                    if problems:
                        fails.append((lang, w, h, sy, kind, problems))
            if errs: fails.append((lang, w, h, 'errors', errs))
            c.close()
    b.close()
for f in fails[:25]: print('FAIL', f)
print(f'{len(fails)} problems' if fails else 'ALL PASSED: 21 kinds x 10 sizes x 3 scroll positions x 2 languages')
