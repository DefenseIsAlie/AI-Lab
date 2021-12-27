from os import POSIX_FADV_NOREUSE
import sys
import typing
import collections

inp = sys.argv[1]

INPUT = open(inp,"r")

goal_y: int
goal_x: int
SearchType: int = int(INPUT.readline())

INPUT_LIST: list = []

for line in INPUT:
    if '*' in line:
        goal_y = line.index('*')
        goal_x = len(INPUT_LIST)

    INPUT_LIST.append(list(line.strip('\n')))

INPUT.close()

y: int = len(INPUT_LIST[0])
x: int = len(INPUT_LIST)

class Pointer:
    def __init__(self,row: int, col: int) -> None:
        (self._X:int, self._Y:int) = (row,col)

    def __str__(self) -> str:
        return f"row {self._X}, col {self._Y}"

class Node:
    def __init__(self,T: tuple, L: list) -> None:
        self._ID: tuple = T
        self._Data: list = L
        self._next: tuple

class Vertex:
    def __init__(self) -> None:
        pass

class Edge:
    def __init__(self) -> None:
        pass

class Graph:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        pass
