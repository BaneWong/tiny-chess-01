# tiny-chess-01

A chess engine for make.fun bounty tiny-chess-01: "Build the strongest chess engine in 4 KB of Python."

## Entry

- `main.py` — 4072 bytes, Python 3.13 stdlib only
- Alpha-beta search at fixed depth 3 with a 15,000 node limit
- MVV-LVA move ordering
- Material evaluation (p=1, n=3, b=3, r=5, q=9, k=100) plus piece-square bonuses for knights and bishops on center squares

## License

MIT
