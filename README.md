# Futoshiki Solver

Implementation of a futoshiki game solver, with some (hopefully good)
constraint satisfaction heuristics.

### Usage:
```
pypy <mode> solve-a-shiki.py [p] [<experiment file>]
```
where `<mode>` is one of:
- `a`: No backtracking heuristics applied
- `b`: Use forward checking for faster cutoff, when backtracking
- `c`: in addition to forward checking, use a 'least remaining values' policy to
choose the next branch target position

The optional `p` flag activates profiling mode; perf-eval dumps are generated
(with a much higher overhead). Also, if no `<experiment file>` is provided, the
standard input is used (for manual input).

[![Floobits Status](https://floobits.com/dnery/futoshiki-solver.svg)](https://floobits.com/dnery/futoshiki-solver/redirect)

# What is Futoshiki?
From Wikipedia

| Futoshiki (不等式 futōshiki?), or More or Less, is a logic puzzle game from
| Japan. Its name means "inequality". It is also spelled hutosiki (using
| Kunrei-shiki romanization).

Example of a 5x5 Futoshiki puzzle...

![pre-sol](https://upload.wikimedia.org/wikipedia/commons/0/00/Futoshiki1.png)

...And it's solution

![pos-sol](https://upload.wikimedia.org/wikipedia/commons/3/37/Futoshiki2.png)
