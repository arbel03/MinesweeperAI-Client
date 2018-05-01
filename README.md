Python & MATLAB Minesweeper AI
===========================
Rewriting this Minesweeper game, written in python, to export useful data.
This data will later be used to create a Minesweeper AI in MATLAB.

Example data recording:
```
[[[-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]], 1]
[[[-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]], 1]
[[[-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]], 1]
[[[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, -1, 1, 0], [0, 1, -2, 1, 0], [0, 1, 1, 1, 0]], 1]
[[[0, 0, 3, -2, 4], [1, 1, 3, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]], 1]
[[[0, 0, 0, 0, 3], [1, 1, 1, 1, 3], [-1, -1, -1, -2, 2], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]], 1]
[[[1, 1, 1, 1, 3], [-1, -1, 1, -2, 2], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]], 1]
```

-1 is a covered tile
-2 is a flag
0 to 8 are numbers that appear on each tile
0 or 1 at the second index in each row is a good/bad decision

good=no bombs
bad=bomb exploded :(
