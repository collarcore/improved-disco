"""How long does a *casual* player take? Calendar days, not hours of play.

The player opens the game a few times a day for a short session, clicks a bit,
buys greedily (same rule as tools/sim_prestige.py) and closes the tab. While
closed the game pays offline income: 50 % for up to 8 h. Past 150 občine the
player calls a referendum at the end of a session whenever it would at least
double the votes (use_refs=False never calls one). Amendments,
the Kurent, achievements and seasonal events are left out, so real players
with those bonuses will be somewhat faster.

    python3 tools/sim_casual.py
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from econ import d, IDX, GEN, TIERS, LM, regs  # noqa: E402
from sim_prestige import ocost, PDIV, VOTE_DIV, VOTE_PCT  # noqa: E402

LATE = 0.12


class Game:
    def __init__(self, votes=0, life=0.0):
        self.votes = votes; self.life = life
        self.sit = 15.0; self.n = 0; self.own = [0] * len(GEN); self.gm = [1.0] * len(GEN)
        self.glob = 1.0; self.pct = 0.0; self.P = 0; self.rc = {}; self.rdone = 0
        self.tiers = set(); self.lms = set()

    def mult(self):
        return self.glob * (1 + self.P / PDIV) * 1.25 ** self.rdone * (1 + VOTE_PCT * self.votes)

    def ips(self, P=None, rdone=None):
        P = self.P if P is None else P; rdone = self.rdone if rdone is None else rdone
        base = sum(self.own[k] * GEN[k][2] * self.gm[k] for k in range(len(GEN)))
        return base * self.glob * (1 + P / PDIV) * 1.25 ** rdone * (1 + VOTE_PCT * self.votes)

    def earn(self, x):
        self.sit += x; self.life += x

    def buy_best(self, cps):
        """one greedy purchase if affordable; returns True if something was bought"""
        ips = self.ips(); m = self.mult(); cands = []
        for k, g in enumerate(GEN):
            if self.n >= g[3]:
                c = g[1] * 1.15 ** self.own[k]
                cands.append((c / (g[2] * self.gm[k] * m), c, ('g', k)))
            for ti, (cnt, mul, *_r) in enumerate(TIERS):
                if self.own[k] >= cnt and (k, ti) not in self.tiers:
                    c = g[1] * mul
                    cands.append((c / max(self.own[k] * g[2] * self.gm[k] * m, 1e-9), c, ('t', k, ti)))
        for li, l in enumerate(LM):
            if li not in self.lms and IDX[l[0]] < self.n:
                c = ocost(IDX[l[0]], LATE) * 3
                if l[1] == 'gen': dl = self.own[l[2]] * GEN[l[2]][2] * self.gm[l[2]] * (l[3] - 1) * m
                elif l[1] == 'glob': dl = ips * (l[3] - 1)
                elif l[1] == 'pct': dl = cps * l[3] * ips
                else: dl = ips * 0.05
                cands.append((c / max(dl, 1e-9), c, ('l', li)))
        if self.n < len(d):
            c = ocost(self.n, LATE)
            rd2 = self.rdone + (1 if self.rc.get(d[self.n]['r'], 0) + 1 == regs[d[self.n]['r']] else 0)
            dl = self.ips(self.P + d[self.n]['p'], rd2) - ips
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

    def session(self, minutes, cps):
        for _ in range(int(minutes * 60)):
            self.earn(self.ips() + cps * (1 + self.pct * self.ips()))
            for _ in range(50):          # catch up on everything affordable
                if not self.buy_best(cps): break

    def away(self, hours, tab_open):
        secs = hours * 3600
        self.earn(self.ips() * (secs if tab_open else min(secs, 8 * 3600) * 0.5))


def player(sessions, minutes, cps, tab_open=False, max_days=120, use_refs=True):
    """sessions: hours of the day at which the player looks in"""
    g = Game(); day = 0; marks = {}; refs = 0
    while day < max_days:
        for i, h in enumerate(sessions):
            g.session(minutes, cps)
            for m in (50, 100, 150, 200, 212):
                if g.n >= m and m not in marks:
                    marks[m] = round(day + h / 24, 1)
            if g.n == len(d):
                return marks, refs
            nxt = sessions[i + 1] if i + 1 < len(sessions) else sessions[0] + 24
            # late in a run, call a referendum once it would at least double the votes
            gain = int(math.cbrt(g.life / VOTE_DIV)) - g.votes
            if use_refs and g.n >= 150 and gain >= max(10, g.votes):
                g = Game(g.votes + gain, g.life); refs += 1
            g.away(nxt - h - minutes / 60, tab_open)
        day += 1
    return marks, refs


if __name__ == '__main__':
    profiles = [
        ('3 visits a day (10 min), uses referendums', [8, 13, 21], 10, 3, False, True),
        ('3 visits a day (10 min), never a referendum', [8, 13, 21], 10, 3, False, False),
    ]
    for name, sess, mins, cps, tab, refs_on in profiles:
        marks, refs = player(sess, mins, cps, tab, use_refs=refs_on)
        print(f'{name:50s} days to 50/100/150/200/212: {marks}  referendums: {refs}')
