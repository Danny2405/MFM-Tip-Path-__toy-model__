# MFM Tip Path — Toy Model

Small, reproducible Python toy model to simulate an AFM tip moving on a 10×10 grid with obstacles.

## Context & Goals
- Discrete grid (10×10), 15 obstacles.
- Compare strategies (Random Walk vs deterministic DRLU).
- Report simple metrics: steps, collisions, coverage, Manhattan efficiency.
- Reproducibility first (fixed seeds).

## Reproducibility
- Obstacles seed: `123`
- Random Walk seed: `124`
- Start/Target: `S=(0,0)`, `T=(9,9)`
- Collision-free route example: `DDDDDDDDRRRRRRRRRD` (18 steps, 0 collisions)

## Quick start
```bash
# clone
git clone https://github.com/<you>/mfm-tip-path-toy-model.git
cd mfm-tip-path-toy-model

Initial map (ASCII)
S . . . . # . # . .
. . # . # . . . # .
. # . . . . . . . .
. . # . . # . . . .
. . . # # . . . . #
. . . # . . . . . .
. . . . . . . . . #
. . # . . . . . . .
. . . . . . . . . .
# . . . . . . . . T


After (trace *)
S . . . . # . # . .
* . # . # . . . # .
* # . . . . . . . .
* . # . . # . . . .
* . . # # . . . . #
* . . # . . . . . .
* . . . . . . . . #
* . # . . . . . . .
* * * * * * * * * *
# . . . . . . . . T




# run (ASCII-only baseline)
python main.py
