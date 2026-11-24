import os, json
from playwright.sync_api import sync_playwright
st={"sit":1e6,"n":45,"own":[40,30,20,12,8,0,0,0,0,0,0,0],"ups":["k1","k2"],"clicks":800,"save":9e15,"sound":0,"lang":"sl"}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ.get('CHROME') or None)
    for w,h,touch in [(1600,1000,False),(390,844,True)]:
        c=b.new_context(viewport={'width':w,'height':h},has_touch=touch,is_mobile=touch)
        c.add_init_script("localStorage.setItem('obcine-v2',JSON.stringify(%s))"%json.dumps(st))
        pg=c.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)));pg.goto('http://localhost:8765/');pg.wait_for_timeout(900)
        sel='#p-bell .ring'
        if touch: pg.evaluate("document.querySelector('#p-bell .ring').scrollIntoView({block:'center'})");pg.wait_for_timeout(400);sel='#p-bell .ring'
        pg.evaluate(f"window.__btn=document.querySelector('{sel}')")
        bb=pg.locator(sel).bounding_box();x,y=bb['x']+bb['width']/2,bb['y']+bb['height']/2
        pg.mouse.move(x,y);bgs=[];same=True
        for i in range(40):
            if touch: pg.touchscreen.tap(x,y)
            else: pg.mouse.down();pg.mouse.up()
            pg.wait_for_timeout(110)  # under the 10 paid rings a second
            same=same and pg.evaluate(f"document.querySelector('{sel}')===window.__btn")
            if i>2: bgs.append(pg.evaluate(f"getComputedStyle(document.querySelector('{sel}')).backgroundColor"))
        print(f'[{w}] ring button kept the same element: {same}; distinct backgrounds while spamming: {sorted(set(bgs))}; clicks counted: ',end='')
        pg.evaluate("dispatchEvent(new Event('pagehide'))");print(pg.evaluate("JSON.parse(localStorage.getItem('obcine-v2')).clicks")-800, errs)
        c.close()
    b.close()
