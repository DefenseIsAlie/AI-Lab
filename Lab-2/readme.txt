# How to run the program:

python3 21.py input.txt

where input.txt is the input file with the input start state and goal state.

# input.txt example:
First three lines of input is for start state and left to right is bottom to top. Later part is for goal state. 
```
E B F
A D
C
A D B
E F C

```
This snippet implies:
start state -
F
B   D
E   A   C
-----------

goal state -
B   C
D   F 
A   E
-----------
# Selecting Algorithm:

When prompted you can select the algorithm you want to execute either BFS or HC. Also the heuristic can be selected among the following:
OrdHeuristic, ManhattanHeuristic, L2Norm, PositionBased

# Output:

Output will be printed to the console.
example:
```
goal state achieved : False
time taken : 0.0014317035675048828
states explored:  9
path length:  2

<PATH TO GOAL>
```
where <PATH TO GOAL> is the path to the goal state one line each.
