"""Balance simulation with referendums (prestige).

A greedy bot plays: every 2 s it buys whatever pays back fastest
(producer, tier upgrade, landmark or the next občina). It calls a referendum
when it has stalled for STALL minutes and the referendum would at least
double its votes. Prints a timeline per run.

    python3 tools/sim_prestige.py
"""
import math, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from econ import d, IDX, GEN, TIERS, LM, regs  # noqa: E402

PDIV = 20000
VOTE_DIV = 1e9      # votes = cbrt(lifetime / VOTE_DIV)
VOTE_PCT = 0.02     # each vote: +2 % income


def ocost(i, late=0.0):
    base = 30 * 1.15 ** i * math.exp(.08 * i * (211 - i) / 211) + 8 * (i + 1) ** 3
    return base * math.exp(late * max(0, i - 140))


def play(votes, life_all, cps, late, stall_min, tmax):
    sit = 15.0; n = 0; own = [0] * len(GEN); gm = [1.0] * len(GEN); glob = 1.0; pct = 0.0
    P = 0; rc = {}; rdone = 0; tiers = set(); lms = set(); t = 0; last_unlock = 0; marks = {}
    vm = 1 + VOTE_PCT * votes
    def ips_of(own, gm, glob, P, rdone):
        return sum(own[k] * GEN[k][2] * gm[k] for k in range(len(GEN))) * glob * (1 + P / PDIV) * 1.25 ** rdone * vm
    while t < tmax:
        ips = ips_of(own, gm, glob, P, rdone)
        g = ips + cps * (1 + pct * ips); sit += g; life_all += g; t += 1
        if n == len(d):
            break
        gain = int(math.cbrt(life_all / VOTE_DIV)) - votes
        if t - last_unlock > stall_min * 60 and gain >= max(1, votes):
            break
        if t % 2: continue
        mult = glob * (1 + P / PDIV) * 1.25 ** rdone * vm
        cands = []
        for k, gg in enumerate(GEN):
            if n >= gg[3]:
                c = gg[1] * 1.15 ** own[k]
                cands.append((c / (gg[2] * gm[k] * mult), c, ('g', k)))
            for ti, (cnt, mul, *_r) in enumerate(TIERS):
                if own[k] >= cnt and (k, ti) not in tiers:
                    c = gg[1] * mul
                    cands.append((c / max(own[k] * gg[2] * gm[k] * mult, 1e-9), c, ('t', k, ti)))
        for li, l in enumerate(LM):
            if li not in lms and IDX[l[0]] < n:
                c = ocost(IDX[l[0]], late) * 3
                if l[1] == 'gen': dl = own[l[2]] * GEN[l[2]][2] * gm[l[2]] * (l[3] - 1) * mult
                elif l[1] == 'glob': dl = ips * (l[3] - 1)
                elif l[1] == 'pct': dl = cps * l[3] * ips
                else: dl = ips * 0.05
                cands.append((c / max(dl, 1e-9), c, ('l', li)))
        c = ocost(n, late)
        rd2 = rdone + (1 if rc.get(d[n]['r'], 0) + 1 == regs[d[n]['r']] else 0)
        dl = ips_of(own, gm, glob, P + d[n]['p'], rd2) - ips
        opens = any(gg[3] == n + 1 for gg in GEN)
        cands.append((c / max(dl, 1e-9) * (0.3 if opens else 1), c, ('o',)))
        best = min(cands)
        if sit >= best[1]:
            sit -= best[1]; a = best[2]
            if a[0] == 'g': own[a[1]] += 1
            elif a[0] == 't': tiers.add((a[1], a[2])); gm[a[1]] *= 2
            elif a[0] == 'l':
                lms.add(a[1]); l = LM[a[1]]
                if l[1] == 'gen': gm[l[2]] *= l[3]
                elif l[1] == 'glob': glob *= l[3]
                elif l[1] == 'pct': pct += l[3]
            else:
                P += d[n]['p']; rc[d[n]['r']] = rc.get(d[n]['r'], 0) + 1
                if rc[d[n]['r']] == regs[d[n]['r']]: rdone += 1
                n += 1; last_unlock = t
                if n in (25, 50, 100, 150, 175, 200, 212): marks[n] = round(t / 3600, 1)
    return t, n, life_all, marks


def campaign(cps=5, late=0.0, stall_min=45, tmax_total=80 * 3600, quiet=False):
    votes = 0; life = 0.0; total = 0; run = 0
    while total < tmax_total:
        run += 1
        t, n, life, marks = play(votes, life, cps, late, stall_min, tmax_total - total)
        total += t
        if not quiet:
            print(f'  run {run}: {t/3600:5.1f} h, reached {n:3d}, votes before {votes:4d}, milestones {marks}')
        if n == len(d):
            return total / 3600, run
        votes = int(math.cbrt(life / VOTE_DIV))
    return None, run


if __name__ == '__main__':
    late = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
    h, runs = campaign(late=late)
    print(f'late={late}: all 212 after {h} h of play over {runs} runs')
