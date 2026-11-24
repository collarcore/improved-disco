"""Honeypots: flipping `razvijalec` or calling `odkleniVse()` from a paused debugger, or a save with `dev` set, earns the
cap with its own 'Past' (trap) pop-up; honest play never does; the console greets whoever opens it."""
import os, json, time
from playwright.sync_api import sync_playwright
URL = 'http://127.0.0.2:8765/'
bad = []
def cap(pg): return '/O\\' in pg.evaluate("document.getElementById('p-bell').innerText")
def toast(pg): return pg.evaluate("document.getElementById('toast').hidden?'':document.getElementById('toast').innerText")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    for expr in ('razvijalec=true', 'odkleniVse()'):
        c = b.new_context(viewport={'width': 1600, 'height': 900}); pg = c.new_page(); logs = []
        pg.on('console', lambda m: logs.append(m.text))
        pg.goto(URL); pg.wait_for_timeout(800)
        cdp = c.new_cdp_session(pg); paused = []
        cdp.on('Debugger.paused', lambda e: paused.append(e))
        cdp.send('Debugger.enable'); done = False
        # pause until it stops inside the game's code, then run the 'cheat' there, as one would in the debugger console
        for attempt in range(20):
            paused.clear(); cdp.send('Debugger.pause')
            for _ in range(40):
                if paused: break
                pg.wait_for_timeout(50)
            for f in (paused[0]['callFrames'] if paused else []):
                r = cdp.send('Debugger.evaluateOnCallFrame', {'callFrameId': f['callFrameId'], 'expression': f'typeof razvijalec!=="undefined"&&({expr},1)'})
                if r.get('result', {}).get('value') == 1: done = True; break
            if paused: cdp.send('Debugger.resume')
            if done: break
            pg.wait_for_timeout(120)
        pg.wait_for_timeout(900)
        got = cap(pg); t = toast(pg)
        print(f'debugger: {expr:16s} ran in game scope={done} cap={got} trap pop-up={"Past" in t}')
        if not (done and got and 'Past' in t): bad.append(expr)
        if not any('Živjo, goljuf' in l for l in logs): bad.append('greeting'); print('no console greeting', logs[:3])
        c.close()
    # a save with the dev flag set (what a 'turn every flag on' script does)
    c = b.new_context(viewport={'width': 1600, 'height': 900})
    c.add_init_script("if(!sessionStorage.x){sessionStorage.x=1;localStorage.setItem('obcine-v2',JSON.stringify({v:5,runV:5,sit:10,life:20,all:20,n:0,own:[0,0,0,0,0,0,0,0,0,0,0,0],sound:0,dev:1}))}")
    pg = c.new_page(); pg.goto(URL); pg.wait_for_timeout(1000); got = cap(pg); t = toast(pg)
    print(f'save with dev=1: cap={got} trap pop-up={"Past" in t}')
    if not (got and 'Past' in t): bad.append('dev')
    c.close()
    # honest play for a while: no cap
    c = b.new_context(viewport={'width': 1600, 'height': 900}); pg = c.new_page(); pg.goto(URL); pg.wait_for_timeout(600)
    for i in range(40): pg.keyboard.press('Space'); pg.wait_for_timeout(110)
    pg.wait_for_timeout(5500); got = cap(pg); print('honest play: cap =', got)
    if got: bad.append('honest')
assert not bad, bad
print('ALL PASSED')
