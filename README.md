# ysliaoniubi/fassasa

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/ysliaoniubi/fassasa/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/ysliaoniubi/fassasa/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A 4,096-byte Python 3.13 chess engine for [make.fun's tiny-chess-01](https://make.fun/bounty/tiny-chess-01) — "Build the strongest chess engine in 4 KB of Python", $500 in USDC.

Deterministic fixed-node search (no clock). PeSTO evaluation, PVS, transposition table, null-move, LMR, killer/history, quiescence. Entrypoint `main.py` is packed with `makefun-compress/v1`.

## Run it

```sh
python3 -P -s /bot/main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
