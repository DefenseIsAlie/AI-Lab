import heapq
import math
import time
import random
import copy
import sys

start = time.time()

INPUT = open(sys.argv[1])
Type = INPUT.readline()
N = int(INPUT.readline())
Inp = INPUT.readlines()
INPUT.close()

firstN = Inp[:N]
secondN = Inp[N:]

OUTPUT = open("output.txt", "w")

rrr = 0

if N <= 100:
    rrr = 20
elif N > 100 and N < 300:
    rrr = 12
else:
    rrr = 6


class Graph:
    def __init__(self) -> None:
        self.matrix = [[0 for j in range(N)] for i in range(N)]  # Graph Rep.
        self.edges = []

        self.bestTour = []  # Best tour
        self.bestPath = []
        self.bestCost = math.inf

        self.Dadmatrix = [0 for j in range(N)]  # MST
        self.mst = [[], 0]

        self.mst0 = 0
        self.alphaNearness = [[0 for j in range(N)] for i in range(N)]  # One Heuristic

        self.makeGraph()  # MaketheGraph
        self.Lin_Keringhan()  # Main Algo

    def makeGraph(self):
        for i in range(N):
            tmp = secondN[i].strip().split()
            for j in range(N):
                self.matrix[i][j] = float(tmp[j])
                if i < j:
                    d = {"u": i, "v": j, "w": float(tmp[j])}
                    self.edges.append(d)

        print("fin matrix edges heap")

        self.Prims()

        print("fin prims")

        t = [(self.matrix[0][x], x) for x in range(1, N)]
        t.sort()
        rec = 0
        for j in t:
            if {"u": 0, "v": j[1], "w": j[0]} not in self.mst[0]:
                rec = j[0]
                self.mst0 = self.mst[1] + j[0]
                break

        Beta = [[0 for j in range(N)] for x in range(N)]

        for i in range(1, N):
            Beta[i][i] = -math.inf
            for j in range(i + 1, N):
                Beta[i][j] = max(
                    Beta[i][self.Dadmatrix[j]], self.matrix[j][self.Dadmatrix[j]]
                )

        print("fin mst and mst0")
        for i in range(N):
            self.alphaNearness[i][i] = math.inf
            for j in range(i + 1, N):
                if i == 0:
                    self.alphaNearness[i][j] = -rec + self.matrix[i][j]
                    self.alphaNearness[j][i] = -rec + self.matrix[i][j]
                elif {"u": i, "v": j, "w": self.matrix[i][j]} in self.mst[0]:
                    self.alphaNearness[i][j] = 0
                    self.alphaNearness[j][i] = 0
                else:
                    self.alphaNearness[i][j] = -Beta[i][j] + self.matrix[i][j]
                    self.alphaNearness[j][i] = -Beta[i][j] + self.matrix[i][j]
        fin = time.time()
        print(f"complete alpha nearness in {fin - start}")

    def genRandTour(self):
        validCities = list(range(N))
        path = []
        tour = []
        pathCost = 0
        initial = random.randint(0, N - 1)
        validCities.remove(initial)
        path.append(initial)

        while len(path) < N:
            prev = path[-1]
            setx = [(self.alphaNearness[prev][x], x) for x in validCities]
            setx.sort()
            nextt = setx[0][1]
            path.append(nextt)
            tour.append({"u": prev, "v": nextt, "w": self.matrix[prev][nextt]})
            validCities.remove(nextt)
            pathCost += self.matrix[prev][nextt]

        return [path, pathCost, tour]

    # T = ∅;
    # U = { 1 };
    # while (U ≠ V)
    #    let (u, v) be the lowest cost edge such that u ∈ U and v ∈ V - U;
    #    T = T ∪ {(u, v)}
    #    U = U ∪ {v}
    # Prim's

    def Prims(self):
        U = [[math.inf, _, -1] for _ in range(N)]
        initial = 0
        U[initial][0] = 0
        Q = list(range(N))
        while Q != []:
            u = Q.sort(key=lambda a: U[a][0])
            u = Q[0]
            Q.remove(u)
            for v in range(N):
                if v in Q and v != u and self.matrix[u][v] < U[v][0]:
                    U[v][2] = u
                    self.Dadmatrix[v] = u
                    self.mst[0].append(
                        {"u": min(u, v), "v": max(u, v), "w": self.matrix[u][v]}
                    )
                    self.mst[1] += self.matrix[u][v]
                    U[v][0] = self.matrix[u][v]

    def TourToPath(self, tour):
        path = [random.randint(0, N - 1)]
        Parent = [-1 for _ in range(N)]

        for ed in tour:
            if Parent[ed["v"]] == -1:
                Parent[ed["v"]] = ed["u"]
            else:
                Parent[ed["u"]] = ed["v"]

        while len(path) < N:
            n = path[-1]
            path.append(Parent[n])
        return path

    def isTour(self, tour):
        T = self.TourToPath(tour)
        n = T.count(T[0])
        if n == 1:
            return True
        else:
            return False

    def Lin_Keringhan(self):
        T = [self.genRandTour() for _ in range(rrr)]

        XX = []
        YY = []

        for Tour in T:
            for x in Tour[2]:
                XX = []
                YY = []
                XX.append(x)
                setx = [(self.alphaNearness[x["v"]][_], _) for _ in range(N)]
                setx.sort()
                L = [
                    (self.matrix[x["u"]][x["v"]] - self.matrix[x["v"]][_], _)
                    for _ in setx[:15]
                ]
                L.sort().reverse()

                if L[0][0] <= 0:
                    continue

                bestT = Tour[2]
                bestCost = Tour[1]
                bestPath = Tour[0]

                for y in L:
                    if y[0] <= 0:
                        continue
                    YY.append()

                    i = 1
                    while True:
                        i += 1
                        Tdash = self.Choose_X(i, XX)

                        XX.append(Tdash[0])

                        # if Tdash[]

                        Yi = self.Choose_Y(i, YY)

                        if Yi[0] and Yi[1] and Yi[2]:
                            continue
                        else:
                            break

    def Choose_X(self, i, l):
        pass

    def Choose_Y(self, i, l):
        pass


g = Graph()


print("done")
