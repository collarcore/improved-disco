"""In a background tab, the Kurent, the dragon and the boat still arrive on their own and play their arrival sounds.
A tab whose sound is working is not reloaded behind your back when a new version comes out (a reload would mute it
until the next click); it shows the update notice when you come back."""
import os, json, re
src = open(os.path.join(os.path.dirname(__file__), 'suite.py')).read()
FAKE_AUDIO = re.search(r'FAKE_AUDIO = """(.*?)"""', src, re.S).group(1)
from playwright.sync_api import sync_playwright
bad = []
st = {"v": 5, "runV": 5, "sit": 5000, "life": 1e5, "all": 1e5, "n": 10, "own": [5] + [0] * 11, "clicks": 50, "sound": 1, "lang": "sl", "ach": ["o1"]}
V = 'version.json'; real = open(V).read()
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
        c = b.new_context(viewport={'width': 1600, 'height': 900})
        c.add_init_script(FAKE_AUDIO); c.add_init_script("localStorage.setItem('obcine-v2',%s);localStorage.setItem('obcine-hi','1')" % json.dumps(json.dumps(st)))
        game = c.new_page(); game.goto('http://localhost:8765/'); game.wait_for_timeout(600)
        game.mouse.click(5, 5); game.wait_for_timeout(200)          # the player has clicked once: sound is unlocked
        game.evaluate("window.__osc.length=0;__dbg.soon()")
        other = c.new_page(); other.goto('about:blank'); other.bring_to_front(); game.wait_for_timeout(300)
        # headless Chrome doesn't report background tabs as hidden, so the test does what a real browser would
        HIDE = "Object.defineProperty(document,'hidden',{get:()=>%s,configurable:true});Object.defineProperty(document,'visibilityState',{get:()=>'%s',configurable:true});document.dispatchEvent(new Event('visibilitychange'));0"
        game.evaluate(HIDE % ('true', 'hidden')); hidden = game.evaluate("document.hidden")
        open(V, 'w').write(json.dumps({'build': 'newerABC'}))       # and a new version appears meanwhile
        other.wait_for_timeout(6000)
        osc = game.evaluate("window.__osc.slice()")
        cow = sum(1 for f in osc if 560 <= f <= 980); low = sum(1 for f in osc if f < 160)
        out = game.evaluate("[__dbg.zmaj,__dbg.boatOut]")
        print(f'game tab hidden={hidden} | Kurent cowbells={cow} | dragon/boat low sounds={low} | dragon out={out[0]} boat out={out[1]}')
        if not (hidden and cow >= 8 and low >= 4): bad.append('sounds')
        before = game.evaluate("performance.timeOrigin")
        game.evaluate("document.dispatchEvent(new Event('visibilitychange'));0"); other.wait_for_timeout(1500)
        same = game.evaluate("performance.timeOrigin") == before
        print('tab with working sound was not reloaded in the background:', same)
        if not same: bad.append('reloaded')
        game.bring_to_front(); game.evaluate(HIDE % ('false', 'visible'))
        seen = False
        for _ in range(60):
            t = game.evaluate("document.getElementById('toast').hidden?'':document.getElementById('toast').innerText")
            if 'POSODOBITEV' in t: seen = True; break
            game.evaluate("(()=>{const t=document.getElementById('toast');if(!t.hidden&&!t.innerText.includes('POSODOBITEV'))t.dispatchEvent(new PointerEvent('pointerup',{button:0,pointerType:'mouse'}))})()"); game.wait_for_timeout(300)
        print('coming back shows the update notice:', seen)
        if not seen: bad.append('notice')
finally:
    open(V, 'w').write(real)
assert not bad, bad
print('ALL PASSED')
