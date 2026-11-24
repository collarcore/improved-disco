"""Phone drumming with 2-3 fingers at once (real touch events): never more than 10 paid rings in any second, and
over-limit taps play only a quiet tick, so the speaker isn't flooded."""
import os, json, time
from playwright.sync_api import sync_playwright
bad = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    c = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3, is_mobile=True, has_touch=True)
    pg = c.new_page(); pg.goto('http://localhost:8765/'); pg.wait_for_timeout(800)
    pg.evaluate("document.querySelector('#p-bell .ring').scrollIntoView({block:'center'})"); pg.wait_for_timeout(300)
    bb = pg.locator('#p-bell .ring').bounding_box(); cx, cy = bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2
    cdp = c.new_cdp_session(pg)
    # count every paid ring with its time, from inside the page
    clicks = lambda: (pg.evaluate("dispatchEvent(new Event('pagehide'))"), pg.evaluate("JSON.parse(localStorage.getItem('obcine-v2')).clicks"))[1]
    c0 = clicks(); t0 = time.time(); taps = 0; samples = []
    while time.time() - t0 < 4:
        n = 3 if taps % 2 else 2
        pts = [{'x': cx - 40 + 40 * i, 'y': cy, 'id': i} for i in range(n)]
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': pts})
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
        taps += n
        if taps % 30 < 3: samples.append((time.time() - t0, clicks() - c0))
    el = time.time() - t0; pg.wait_for_timeout(100); paid = clicks() - c0
    print(f'{taps} finger taps in {el:.1f} s ({taps/el:.0f} a second) -> {paid} paid rings ({paid/el:.1f} a second)')
    if paid > 10 * el + 10: bad.append('rate')
    # sliding check: no 1-second window with more than 10 paid
    worst = 0
    for i in range(len(samples)):
        for j in range(i + 1, len(samples)):
            if samples[j][0] - samples[i][0] <= 1.0: worst = max(worst, samples[j][1] - samples[i][1])
    print('most paid rings within any 1 s seen:', worst)
    if worst > 11: bad.append('window')
    print('page zoom after drumming:', pg.evaluate('visualViewport.scale'))
assert not bad, bad
print('ALL PASSED')
