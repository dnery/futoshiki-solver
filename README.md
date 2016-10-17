# Futoshiki Solver

Implementation of a futoshiki game solver, with some (hopefully good)
constraint satisfaction heuristics.

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

# Perf-eval Status
  -> cpython: 19:35m
  -> pypy (pypy2): 1:28m
