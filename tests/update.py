"""A tab running an older version notices the new one: a playing tab gets a notice that stays until tapped and then
reloads (progress kept); a background tab reloads by itself; no reload loop if the server still sends the old page."""
import os, json, shutil
from playwright.sync_api import sync_playwright
bad = []
V = 'version.json'; real = open(V).read()
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
        c = b.new_context(viewport={'width': 1600, 'height': 900}); pg = c.new_page(); pg.goto('http://localhost:8765/'); pg.wait_for_timeout(700)
        for i in range(5): pg.keyboard.press('Space'); pg.wait_for_timeout(120)
        open(V, 'w').write(json.dumps({'build': 'newer12345'}))
        pg.evaluate("document.dispatchEvent(new Event('visibilitychange'))")
        t = ''
        for _ in range(40):  # it waits behind pop-ups already queued
            t = pg.evaluate("document.getElementById('toast').hidden?'':document.getElementById('toast').innerText")
            if 'POSODOBITEV' in t: break
            pg.wait_for_timeout(500)
        print('notice shown:', 'POSODOBITEV' in t)
        if 'POSODOBITEV' not in t: bad.append('notice')
        pg.wait_for_timeout(14000)
        t = pg.evaluate("document.getElementById('toast').hidden?'':document.getElementById('toast').innerText")
        print('still there 14 s later:', 'POSODOBITEV' in t)
        if 'POSODOBITEV' not in t: bad.append('sticky')
        before = pg.evaluate("performance.timeOrigin")
        tb = pg.locator('#toast').bounding_box()
        with pg.expect_navigation(timeout=5000): pg.mouse.click(tb['x'] + 60, tb['y'] + 60)
        pg.wait_for_timeout(1500)
        reloaded = pg.evaluate("performance.timeOrigin") != before
        clicks = (pg.evaluate("dispatchEvent(new Event('pagehide'))"), pg.evaluate("JSON.parse(localStorage.getItem('obcine-v2')).clicks"))[1]
        print('tap reloads:', reloaded, '| rings kept:', clicks)
        if not reloaded or clicks < 5: bad.append('reload')
        # the server still has the old page (version.json says newer): no second notice, no loop
        pg.evaluate("document.dispatchEvent(new Event('visibilitychange'))"); pg.wait_for_timeout(800)
        t = pg.evaluate("document.getElementById('toast').hidden?'':document.getElementById('toast').innerText")
        print('no loop when the server is still behind:', 'POSODOBITEV' not in t)
        if 'POSODOBITEV' in t: bad.append('loop')
        c.close()
        # a tab in the background reloads by itself
        c = b.new_context(); pg = c.new_page(); open(V, 'w').write(real); pg.goto('http://localhost:8765/'); pg.wait_for_timeout(600)
        open(V, 'w').write(json.dumps({'build': 'newer67890'}))
        before = pg.evaluate("performance.timeOrigin")
        pg.evaluate("Object.defineProperty(document,'hidden',{get:()=>true,configurable:true});document.dispatchEvent(new Event('visibilitychange'))")
        pg.wait_for_timeout(300)
        pg.evaluate("Object.defineProperty(document,'hidden',{get:()=>false,configurable:true});document.dispatchEvent(new Event('visibilitychange'))")  # check
        pg.wait_for_timeout(600)
        pg.evaluate("Object.defineProperty(document,'hidden',{get:()=>true,configurable:true});document.dispatchEvent(new Event('visibilitychange'))")
        pg.wait_for_timeout(1500)
        r = pg.evaluate("performance.timeOrigin") != before
        print('background tab reloads by itself:', r)
        if not r: bad.append('background')
finally:
    open(V, 'w').write(real)
assert not bad, bad
print('ALL PASSED')
