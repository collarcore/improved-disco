"""Balance simulator for Občine.

Models what drives the economy: producers and their tier upgrades, landmarks,
population and region multipliers, bell upgrades and the ringing meter, the
weekly cycle, referendums (votes) and offline income. Leaves out the Kurent,
achievements, amendments and holidays, so real players are somewhat faster.

Two kinds of player:
  active  - plays nonstop, rings CPS times a second, buys greedily every 2 s
  casual  - opens the game at fixed hours for a short session, then closes it
Both call a referendum once past REF_FROM občine when it would at least double
their votes.

    python3 tools/balance.py            # both players, current prices
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from econ import d, IDX, GEN, TIERS, LM, regs  # noqa: E402

# ---- the game's numbers (keep in step with src/game.js) ----
PRICE = dict(A=30, B=.12, E=200, P=4, C=.18)        # unlock price curve
PDIV = 20000                                        # residents per +100 %
VOTE_DIV, VOTE_PCT = 1e9, .05                       # votes = cbrt(lifetime/1e9), +5 % each
OFFLINE_RATE, OFFLINE_CAP_H = .5, 8
CLK = [(50, 200), (500, 2e4), (2000, 2e7), (6000, 2e10), (15000, 2e13)]   # (rings needed, cost)
CLK_MULT = [2, 2, 2, 2, 2]; CLK_PCT = [0, .01, .01, .02, .02]
METER_CAP = [1.5, 2, 2.5, 3, 4, 5]                  # by bell tier
METER_AVG = .8                                      # how full a ringing player keeps the meter
REF_FROM = 140
# weekday bonuses by producer index (Mon..Sun); Sunday's bonus is on the meter/clicks
WEEK = [{0: 3, 1: 3, 2: 3}, {5: 2, 6: 2}, {9: 2, 10: 2, 11: 2}, {7: 2, 8: 2}, {3: 2, 4: 2}, {'all': 1.1}, {'click': 3}]


def ocost(i, p=None):
    p = p or PRICE
    base = p['A'] * 1.15 ** i * math.exp(p['B'] * i * (211 - i) / 211) + p['E'] * (i + 1) ** p['P']
    return base * math.exp(p['C'] * max(0, i - 140))


class Game:
    def __init__(self, price, votes=0, life=0.0, clicks=0):
        self.p = price; self.votes = votes; self.life = life; self.clicks = clicks
        self.sit = 0.0; self.n = 0; self.own = [0] * len(GEN); self.gm = [1.0] * len(GEN)
        self.glob = 1.0; self.pct = 0.0; self.P = 0; self.rc = {}; self.rdone = 0
        self.tiers = set(); self.lms = set(); self.bell = 0; self.day = 0

    def week(self, k=None):
        w = WEEK[self.day % 7]
        if k is None: return w.get('all', 1)
        return w.get(k, 1)

    def base(self, P=None, rdone=None):
        P = self.P if P is None else P; rdone = self.rdone if rdone is None else rdone
        s = sum(self.own[k] * GEN[k][2] * self.gm[k] * self.week(k) for k in range(len(GEN)))
        return s * self.glob * (1 + P / PDIV) * 1.25 ** rdone * (1 + VOTE_PCT * self.votes) * self.week()

    def meter(self, ringing):
        return 1 + METER_AVG * (METER_CAP[self.bell] - 1) if ringing else 1

    def click_val(self):
        cm = 1
        for t in range(self.bell): cm *= CLK_MULT[t]
        return (cm * self.week('click') + self.pct * self.base())

    def second(self, cps):
        m = self.meter(cps > 0)
        g = (self.base() + cps * self.click_val()) * m
        self.sit += g; self.life += g; self.clicks += cps

    def buy_best(self, cps):
        ips = self.base(); mult = self.glob * (1 + self.P / PDIV) * 1.25 ** self.rdone * (1 + VOTE_PCT * self.votes) * self.week()
        cands = []
        if self.bell < len(CLK) and self.clicks >= CLK[self.bell][0] and self.sit >= CLK[self.bell][1]:
            self.sit -= CLK[self.bell][1]; self.bell += 1; self.pct += CLK_PCT[self.bell - 1]   # bells first: cheap for what they give
            return True
        for k, g in enumerate(GEN):
            if self.n >= g[3]:
                c = g[1] * 1.15 ** self.own[k]
                cands.append((c / (g[2] * self.gm[k] * self.week(k) * mult + 1e-12), c, ('g', k)))
            for ti, (cnt, mul, *_r) in enumerate(TIERS):
                if self.own[k] >= cnt and (k, ti) not in self.tiers:
                    c = g[1] * mul
                    cands.append((c / max(self.own[k] * g[2] * self.gm[k] * mult, 1e-9), c, ('t', k, ti)))
        for li, l in enumerate(LM):
            if li not in self.lms and IDX[l[0]] < self.n:
                c = ocost(IDX[l[0]], self.p) * 3
                if l[1] == 'gen': dl = self.own[l[2]] * GEN[l[2]][2] * self.gm[l[2]] * (l[3] - 1) * mult
                elif l[1] == 'glob': dl = ips * (l[3] - 1)
                elif l[1] == 'pct': dl = cps * l[3] * ips
                else: dl = ips * 0.05
                cands.append((c / max(dl, 1e-9), c, ('l', li)))
        if self.n < len(d):
            c = ocost(self.n, self.p)
            rd2 = self.rdone + (1 if self.rc.get(d[self.n]['r'], 0) + 1 == regs[d[self.n]['r']] else 0)
            dl = self.base(self.P + d[self.n]['p'], rd2) - ips
            opens = any(g[3] == self.n + 1 for g in GEN)
            cands.append((c / max(dl, 1e-9) * (0.3 if opens else 1), c, ('o',)))
        best = min(cands)
        if self.sit < best[1]:
            return False
        self.sit -= best[1]; a = best[2]
        if a[0] == 'g': self.own[a[1]] += 1
        elif a[0] == 't': self.tiers.add((a[1], a[2])); self.gm[a[1]] *= 2
        elif a[0] == 'l':
            self.lms.add(a[1]); l = LM[a[1]]
            if l[1] == 'gen': self.gm[l[2]] *= l[3]
            elif l[1] == 'glob': self.glob *= l[3]
            elif l[1] == 'pct': self.pct += l[3]
        else:
            self.P += d[self.n]['p']; r = d[self.n]['r']; self.rc[r] = self.rc.get(r, 0) + 1
            if self.rc[r] == regs[r]: self.rdone += 1
            self.n += 1
        return True

    def gain(self):
        return int(math.cbrt(self.life / VOTE_DIV)) - self.votes


def referendum_due(g):
    return g.n >= REF_FROM and g.gain() >= max(10, g.votes)


def active(price, cps=5, max_h=200):
    """hours of play to milestones, nonstop"""
    g = Game(price); t = 0; marks = {}; refs = 0
    while t < max_h * 3600:
        g.day = int(t // 86400); g.second(cps); t += 1
        if t % 2 == 0:
            while g.buy_best(cps): pass
        for m in (10, 25, 50, 100, 150, 212):
            if g.n >= m and m not in marks: marks[m] = round(t / 3600, 1)
        if g.n == len(d): return marks, refs
        if t % 600 == 0 and referendum_due(g):
            g = Game(price, g.votes + g.gain(), g.life, g.clicks); refs += 1
    return marks, refs


def casual(price, sessions=(8, 13, 21), minutes=10, cps=3, use_refs=True, max_days=60):
    """calendar days to milestones for someone who looks in a few times a day"""
    g = Game(price); marks = {}; refs = 0
    for day in range(max_days):
        for i, h in enumerate(sessions):
            g.day = day
            for s in range(minutes * 60):
                g.second(cps)
                if s % 2 == 0:
                    while g.buy_best(cps): pass
            for m in (10, 25, 50, 100, 150, 212):
                if g.n >= m and m not in marks: marks[m] = round(day + h / 24, 1)
            if g.n == len(d): return marks, refs
            if use_refs and referendum_due(g):
                g = Game(price, g.votes + g.gain(), g.life, g.clicks); g.day = day; refs += 1
            nxt = sessions[i + 1] if i + 1 < len(sessions) else sessions[0] + 24
            away = (nxt - h) * 3600 - minutes * 60
            g.sit += g.base() * min(away, OFFLINE_CAP_H * 3600) * OFFLINE_RATE
            g.life += g.base() * min(away, OFFLINE_CAP_H * 3600) * OFFLINE_RATE
    return marks, refs


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if which in ('all', 'active'):
        print('active, 5 rings/s, hours of play:', active(PRICE), flush=True)
    if which in ('all', 'casual'):
        print('casual, 3×10 min a day, days:', casual(PRICE), flush=True)
    if which in ('all', 'noref'):
        print('casual, never a referendum, days:', casual(PRICE, use_refs=False), flush=True)
