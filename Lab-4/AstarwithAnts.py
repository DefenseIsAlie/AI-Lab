import heapq
import numpy
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

firstN = numpy.array(Inp[:N])
secondN = numpy.array(Inp[N:])

OUTPUT = open("output.txt", "w")

Q = 100
alpha = 0.9
beta = 20
rho = 0.3

h = numpy.zeros((N, N))


class Graph:
    def __init__(self, adj) -> None:
        self.matrix = numpy.zeros((N, N))
        self.Phermones = numpy.zeros((N, N))
        self.deltaProb = numpy.zeros((N, N))
        self.epsilon = numpy.zeros((N, N))
        self.probMatrix = numpy.zeros((N, N))
        self.bestCost = numpy.inf
        self.bestTour = []
        self.makeGraph(adj)

    def makeGraph(self, AdjList):
        for j in range(N):
            tmp = AdjList[j].strip().split()
            d = 0
            for k in tmp:
                self.matrix[j][d] = float(k)
                if float(k) != 0:
                    self.epsilon[j][d] = 1 / float(k)
                else:
                    self.epsilon[j][d] = 0
                d += 1

        for o in range(N):
            for p in range(N):
                self.probMatrix[o][p] = self.epsilon[o][p] / self.epsilon[o].sum()

    def updateProb(self):
        for o in range(N):
            for p in range(N):
                self.probMatrix[o][p] = self.deltaProb[o][p] / self.deltaProb[o].sum()

    def updateDeltaProb(self):
        for o in range(N):
            for p in range(N):
                self.deltaProb[o][p] = (
                    self.Phermones[o][p] ** alpha * self.epsilon[o][p] ** beta
                )

    def updatePhermone(self):
        for o in range(N):
            for p in range(N):
                self.Phermones[o][p] = (
                    rho * self.Phermones[o][p] + ANT.deltaPhermone[o][p]
                )


class ANT:
    deltaPhermone = numpy.zeros((N, N))
    Q = list(range(N))

    def __init__(self, graph: Graph) -> None:
        self.validCities = list(range(0, N))
        self.currentPath = []
        self.pathCost = numpy.inf
        self.getPath(graph)

    def getPath(self, G: Graph):
        if ANT.Q == []:
            ANT.Q = list(range(N))
        initial = ANT.Q.pop()
        # initial = random.randint(0, N - 1)
        self.validCities.remove(initial)
        self.currentPath.append(initial)

        while len(self.currentPath) < N:
            previous = self.currentPath[-1]
            set = [
                float(G.probMatrix[previous][x]) + 0.000000000000000000000001
                for x in self.validCities
            ]
            # print(set)
            next = random.choices(self.validCities, weights=set)[0]
            h[previous][next] += 0.5
            self.currentPath.append(next)
            self.validCities.remove(next)
            if G.matrix[previous][next] != 0:
                ANT.deltaPhermone[previous][next] += Q / G.matrix[previous][next]
            else:
                ANT.deltaPhermone[previous][next] += 0

        self.pathCost = self.getPathCost(self.currentPath, G)
        self.validCities = list(range(0, N))

        if self.pathCost < G.bestCost:
            G.bestCost = self.pathCost
            G.bestTour = copy.deepcopy(self.currentPath)
            OUTPUT.write(
                f"The tour found with cost : {G.bestCost} at {time.time() - start} seconds\n"
            )
            OUTPUT.write(" ".join(map(str, G.bestTour)))
            OUTPUT.write("\n \n")
        self.currentPath = []

    def getPathCost(self, l: list, G: Graph):
        ret = 0
        for i in range(len(self.currentPath)):
            ret += G.matrix[self.currentPath[i]][self.currentPath[(i + 1) % N]]
        return ret


g = Graph(secondN)

Ants = []
for i in range(N):
    Ants.append(ANT(g))


def colonize():
    for ant in Ants:
        ant.getPath(g)

    g.updatePhermone()
    ANT.deltaPhermone = numpy.zeros((N, N))
    g.updateDeltaProb()
    g.updateProb()


ti = time.time()
colonize()
til = time.time() - ti
print(f"Colonized in {til}")

for _ in range(int(40 / til)):
    for ant in Ants:
        ant.getPath(g)

    g.updatePhermone()
    ANT.deltaPhermone = numpy.zeros((N, N))
    g.updateDeltaProb()
    g.updateProb()

""" H = numpy.zeros((N, N))

for i in range(N):
    for j in range(N):
        if h[i][j] > 1:
            H[i][j] = 1 / h[i][j] * g.matrix[i][j]
        elif h[i][j] == 0:
            H[i][j] = g.matrix[i][j]
        elif h[i][j] == 0.5:
            H[i][j] = 0.9 * g.matrix[i][j]
        elif h[i][j] == 1:
            H[i][j] = 0.95 * g.matrix[i][j]

OUTPUT.close()


class Solution:
    upperBound = g.bestCost

    def __init__(self, n: int) -> None:
        self.F = 0
        self.G = 0
        self.Path = [n]
        self.pathCost = 0

    def getPathCost(self, l: list):
        ret = 0
        k = len(l)
        for i in range(k):
            ret += g.matrix[l[i]][l[(i + 1) % k]]
        return ret

    def MoveGen(self):
        ret = []
        l = [x for x in list(range(N)) if x not in self.Path]
        l.sort(key=lambda a: H[self.Path[0]][a])
        for x in l:
            tmp = Solution(x)
            tmp.Path = copy.deepcopy(self.Path)
            tmp.Path.append(x)
            tmp.pathCost = self.pathCost + g.matrix[self.Path[0]][x]
            tmp.G = self.G + g.matrix[self.Path[-1]][x]
            tmp.F = tmp.G + H[self.Path[-1]][x]
            ret.append(tmp)

        return ret


def A_Star():
    Open = []
    heapq.heapify(Open)
    tmp = Solution(random.randint(0, N - 1))
    tmp.Path = copy.deepcopy(g.bestTour[: N // 2])
    tmp.G = tmp.getPathCost(tmp.Path) - g.matrix[tmp.Path[-1]][tmp.Path[0]]
    tmp.F = tmp.G
    heapq.heappush(Open, (tmp.F, tmp))

    while Open != []:
        n = heapq.heappop(Open)[1]
        if len(n.Path) == N:
            return n
        Neighbours = n.MoveGen()
        for soln in Neighbours:
            if soln.pathCost > Solution.upperBound:
                continue
            heapq.heappush(Open, (soln.F, soln))

    return "fail"
 """


def Lin_Keringhan():
    pass


print(f"Executed in {time.time()-start}")
