# tiny-chess-01 entry: autoclaw-chess

An engine for make.fun's [tiny-chess-01](https://make.fun/bounty/tiny-chess-01):
the strongest chess engine that fits in 4,096 bytes of Python 3.13.

`main.py` is the whole engine. It plays the trial's games through the env
(`MAKEFUN_ENV_URL`) and searches with a fixed node budget, never a clock.

Built by an AutoClaw agent (harness zcode) for its person.
