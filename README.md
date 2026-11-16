# tiny-chess-01

A chess engine for make.fun bounty tiny-chess-01: "Build the strongest chess engine in 4 KB of Python."

## Entry

- `main.py` — 4072 bytes, Python 3.13 stdlib only
- Alpha-beta search at fixed depth 3 with a 15,000 node limit
- MVV-LVA move ordering
- Material evaluation (p=1, n=3, b=3, r=5, q=9, k=100) plus piece-square bonuses for knights and bishops on center squares

## Run

```bash
MAKEFUN_ENV_URL=<url> python3 main.py
```

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/BaneWong/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/BaneWong/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
