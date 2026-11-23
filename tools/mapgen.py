import json,math
from collections import Counter
d=sorted(json.load(open('data/obcine.json')),key=lambda o:o['p'])
def gen(W,ASP=0.48):
    lon0,lon1,lat0,lat1=13.36,16.64,45.40,46.90
    kx=77.0; ky=111.2
    cw=(lon1-lon0)*kx/W; H=round((lat1-lat0)*ky/(cw/ASP)); ch=(lat1-lat0)*ky/H
    pts=[((o['lon']-lon0)*kx,(lat1-o['lat'])*ky,math.sqrt(o['a']/math.pi)) for o in d]
    grid=[[-1]*W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            px=(x+.5)*cw; py=(y+.5)*ch
            ds=[(math.hypot(px-q[0],py-q[1]),i) for i,q in enumerate(pts)]
            if any(dd<max(pts[i][2]*1.4,max(6.0,cw*1.2)) for dd,i in ds):
                grid[y][x]=min(ds,key=lambda t:t[0]/(pts[t[1]][2]**0.5))[1]
    out=set();st=[(0,y) for y in range(H)]+[(W-1,y) for y in range(H)]+[(x,0) for x in range(W)]+[(x,H-1) for x in range(W)]
    while st:
        x,y=st.pop()
        if (x,y) in out or not(0<=x<W and 0<=y<H) or grid[y][x]>=0: continue
        out.add((x,y)); st+=[(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    for y in range(H):
        for x in range(W):
            if grid[y][x]<0 and (x,y) not in out:
                px=(x+.5)*cw; py=(y+.5)*ch
                grid[y][x]=min(range(len(pts)),key=lambda i:math.hypot(px-pts[i][0],py-pts[i][1]))
    for it in range(10):
        cnt=Counter(c for r in grid for c in r if c>=0)
        miss=[i for i in range(len(d)) if i not in cnt]
        if not miss: break
        for i in miss:
            qx,qy,_=pts[i]
            cells=sorted(((x,y) for y in range(H) for x in range(W) if grid[y][x]>=0 and cnt[grid[y][x]]>1),key=lambda c:math.hypot((c[0]+.5)*cw-qx,(c[1]+.5)*ch-qy))
            x,y=cells[0]; cnt[grid[y][x]]-=1; grid[y][x]=i; cnt[i]=1
    seats=[]
    for i,(qx,qy,r) in enumerate(pts):
        cells=[(x,y) for y in range(H) for x in range(W) if grid[y][x]==i]
        seats.append(list(min(cells,key=lambda c:math.hypot((c[0]+.5)*cw-qx,(c[1]+.5)*ch-qy))) if cells else None)
    cnt=Counter(c for r in grid for c in r if c>=0)
    print(W,H,'present',len(cnt),'min',min(cnt.values()))
    # sea mask: outside cells in SW corner below coast
    sea=[[1 if grid[y][x]<0 and x<W*0.09 and y>H*0.8 else 0 for x in range(W)] for y in range(H)]
    rows=[]
    for y in range(H):
        rows.append([grid[y][x] if grid[y][x]>=0 else (-2 if sea[y][x] else -1) for x in range(W)])
    for r in rows: print(''.join('~' if c==-2 else ' ' if c<0 else '#' for c in r))
    return {'W':W,'H':H,'g':rows,'s':seats}
json.dump({'big':gen(84),'small':gen(44)},open('data/maps.json','w'),separators=(',',':'))
