import sys,math
from econ import *
import math
OCOST=lambda i:30*1.15**i*math.exp(.08*i*(211-i)/211)+8*(i+1)**3
def run(ocost=OCOST,PDIV=20000,cps=5,tmax=40*3600):
    sit=0;n=0;own=[0]*len(GEN);gm=[1]*len(GEN);glob=1;pct=0;cm=1;P=0;rc={};rdone=0
    tiers=set();lms=set();t=0;marks={}
    def ips_of(own,gm,glob,P,rdone):
        base=sum(own[k]*GEN[k][2]*gm[k] for k in range(len(GEN)))
        return base*glob*(1+P/PDIV)*1.25**rdone
    while n<len(d) and t<tmax:
        ips=ips_of(own,gm,glob,P,rdone)
        sit+=ips+cps*(cm+pct*ips); t+=1
        if t%2: continue
        # candidates
        cands=[]
        for k,g in enumerate(GEN):
            if n>=g[3]:
                c=g[1]*1.15**own[k]; dl=g[2]*gm[k]*glob*(1+P/PDIV)*1.25**rdone
                cands.append((c/dl+c/max(ips,1e-9)*0,c,('g',k)))
            for ti,(cnt,mul) in enumerate(TIERS):
                if own[k]>=cnt and (k,ti) not in tiers:
                    c=g[1]*mul; dl=own[k]*g[2]*gm[k]*glob*(1+P/PDIV)*1.25**rdone
                    cands.append((c/max(dl,1e-9),c,('t',k,ti)))
        for li,l in enumerate(LM):
            if li not in lms and IDX[l[0]]<n:
                c=ocost(IDX[l[0]])*3
                if l[1]=='gen': dl=own[l[2]]*GEN[l[2]][2]*gm[l[2]]*(l[3]-1)*glob*(1+P/PDIV)*1.25**rdone
                elif l[1]=='glob': dl=ips*(l[3]-1)
                elif l[1]=='pct': dl=cps*l[3]*ips
                elif l[1]=='click': dl=cps*cm
                else: dl=ips*0.05
                cands.append((c/max(dl,1e-9),c,('l',li)))
        if n<len(d):
            c=ocost(n);p=d[n]['p']
            rd2=rdone+(1 if rc.get(d[n]['r'],0)+1==regs[d[n]['r']] else 0)
            dl=ips_of(own,gm,glob,P+p,rd2)-ips
            # gating value: unlocking may open generator
            bonus=any(g[3]==n+1 for g in GEN)
            cands.append((c/max(dl,1e-9)*(0.3 if bonus else 1),c,('o',)))
        best=min(cands)
        if sit>=best[1]:
            sit-=best[1];a=best[2]
            if a[0]=='g': own[a[1]]+=1
            elif a[0]=='t': tiers.add((a[1],a[2]));gm[a[1]]*=2
            elif a[0]=='l':
                lms.add(a[1]);l=LM[a[1]]
                if l[1]=='gen': gm[l[2]]*=l[3]
                elif l[1]=='glob': glob*=l[3]
                elif l[1]=='pct': pct+=l[3]
                elif l[1]=='click': cm*=l[3]
            else:
                P+=d[n]['p'];rc[d[n]['r']]=rc.get(d[n]['r'],0)+1
                if rc[d[n]['r']]==regs[d[n]['r']]: rdone+=1
                n+=1
                if n in (10,25,50,100,125,150,175,200,212): marks[n]=round(t/3600,2)
    return round(t/3600,2),n,marks,f"{ips:.3g}"
if __name__=='__main__':
    print(run())  # (hours, občine, {milestone: hours}, final income)
