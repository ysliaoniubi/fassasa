# autoclaw-chess v0.1 -- make.fun tiny-chess-01 entry (MIT, see LICENSE)
# Deterministic greedy-capture baseline; search arrives in later versions.
import json, os, urllib.request
N8 = (-21, -19, -12, -8, 8, 12, 19, 21)
K8 = (-11, -10, -9, -1, 1, 9, 10, 11)
R4 = (-10, -1, 1, 10)
B4 = (-11, -9, 9, 11)
VAL = {'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000}

def board(fen):
    b = ['x'] * 120
    for r in range(8):
        for f in range(8):
            b[21 + 10 * r + f] = '.'
    p = fen.split()
    for r, row in enumerate(p[0].split('/')):
        f = 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                b[21 + 10 * r + f] = ch
                f += 1
    st = (p[1] == 'w', p[2] if len(p) > 2 else '-', None if len(p) < 4 or p[3] == '-' else (10 - int(p[3][1])) * 10 + 1 + "abcdefgh".index(p[3][0]))
    return b, st

def w_of(p):
    return p.isupper()

def attacked(b, sq, by_white):
    for d in ((9, 11) if by_white else (-9, -11)):
        if b[sq + d] == ('P' if by_white else 'p'):
            return True
    for d in N8:
        if b[sq + d] == ('N' if by_white else 'n'):
            return True
    for d in K8:
        if b[sq + d] == ('K' if by_white else 'k'):
            return True
    for dirs, ray in ((R4, ('R', 'Q')), (B4, ('B', 'Q'))):
        for d in dirs:
            s = sq + d
            while b[s] == '.':
                s += d
            if b[s] != '.' and b[s] in (ray if by_white else tuple(x.lower() for x in ray)):
                return True
    return False

def enemy(b, t, white):
    q = b[t]
    return q in ("pnbrqk" if white else "PNBRQK")

def gen(b, white, ep, rights):
    out = []
    own = "PNBRQK" if white else "pnbrqk"
    for s in range(21, 99):
        p = b[s]
        if p == '.' or p not in own:
            continue
        u = p.upper()
        if u == 'P':
            d = -10 if white else 10
            t = s + d
            if b[t] == '.':
                if 31 <= t <= 88:
                    out.append((s, t, '', ''))
                else:
                    for pr in 'qrbn':
                        out.append((s, t, pr, ''))
                if ((81 <= s <= 88) if white else (31 <= s <= 38)) and b[t + d] == '.':
                    out.append((s, t + d, '', '2'))
            for dd in (d - 1, d + 1):
                t = s + dd
                if enemy(b, t, white):
                    if 31 <= t <= 88:
                        out.append((s, t, '', ''))
                    else:
                        for pr in 'qrbn':
                            out.append((s, t, pr, ''))
                if ep is not None and t == ep:
                    out.append((s, t, '', 'e'))
        elif u == 'N' or u == 'K':
            for d in (N8 if u == 'N' else K8):
                t = s + d
                if b[t] == '.' or enemy(b, t, white):
                    out.append((s, t, '', ''))
            if u == 'K' and rights != '-':
                home = 95 if white else 25
                rr = rights if white else rights.lower()
                kr, qr = ('K', 'Q') if white else ('k', 'q')
                if kr in rr and b[home + 1] == '.' and b[home + 2] == '.' and b[home] == p and b[home + 3] == ('R' if white else 'r'):
                    if not attacked(b, home, not white) and not attacked(b, home + 1, not white):
                        out.append((s, home + 2, '', 'O'))
                if qr in rr and b[home - 1] == '.' and b[home - 2] == '.' and b[home - 3] == '.' and b[home] == p and b[home - 4] == ('R' if white else 'r'):
                    if not attacked(b, home, not white) and not attacked(b, home - 1, not white):
                        out.append((s, home - 2, '', 'O'))
        else:
            for D in (R4 if u == 'R' else B4 if u == 'B' else K8):
                t = s + D
                while b[t] == '.':
                    out.append((s, t, '', ''))
                    t += D
                if enemy(b, t, white):
                    out.append((s, t, '', ''))
    return out

def do(b, white, mv):
    s, t, pr, fl = mv
    p = b[s]
    cap = b[t]
    b[t] = (pr.upper() if white else pr) if pr else p
    b[s] = '.'
    nep = None
    if fl == '2':
        nep = (s + t) // 2
    elif fl == 'e':
        b[t + (10 if white else -10)] = '.'
    elif fl == 'O':
        if t > s:
            b[t + 1] = '.'; b[t - 1] = 'R' if white else 'r'
        else:
            b[t - 2] = '.'; b[t + 1] = 'R' if white else 'r'
    return cap, nep

def undo(b, white, mv, cap):
    s, t, pr, fl = mv
    p = b[t] if not pr else ('P' if white else 'p')
    b[s] = p
    b[t] = cap
    if fl == 'e':
        b[t + (10 if white else -10)] = 'p' if white else 'P'
    elif fl == 'O':
        if t > s:
            b[t + 1] = 'R' if white else 'r'; b[t - 1] = '.'
        else:
            b[t - 2] = 'R' if white else 'r'; b[t + 1] = '.'

def ksq(b, white):
    k = 'K' if white else 'k'
    for s in range(21, 99):
        if b[s] == k:
            return s
    return -1

def legal(b, white, ep, rights):
    out = []
    for mv in gen(b, white, ep, rights):
        cap, nep = do(b, white, mv)
        if not attacked(b, ksq(b, white), not white):
            out.append(mv)
        undo(b, white, mv, cap)
    return out

def uci(mv):
    s, t, pr, fl = mv
    nm = lambda q: "abcdefgh"[q % 10 - 1] + str(10 - q // 10) if q < 100 else '?'
    return nm(s) + nm(t) + pr

def main():
    url = os.environ["MAKEFUN_ENV_URL"]
    def send(path, obj):
        r = urllib.request.Request(url + path, json.dumps(obj or {}).encode(), {"Content-Type": "application/json"})
        return json.loads(urllib.request.urlopen(r, timeout=60).read())
    g = send("/game", {})
    while g.get("status") != "done":
        if g.get("status") != "your_move":
            g = send("/game", {})
            continue
        b, st = board(g["fen"])
        white, rights, ep = st
        ms = legal(b, white, ep, rights)
        allowed = g.get("legal_moves") or []
        pick, bk = allowed[0] if allowed else None, (-1, -1, -1)
        mv_by_uci = {uci(m): m for m in ms}
        for u in allowed:
            m = mv_by_uci.get(u)
            if not m:
                continue
            q = b[m[1]]
            gain = VAL.get(q.upper(), 0)
            cost = VAL.get(b[m[0]].upper(), 0)
            k = (gain, 1 if m[2] else 0, -cost)
            if k > bk:
                bk, pick = k, u
        g = send("/move", {"game": g["game"], "move": pick})

if __name__ == "__main__":
    main()
