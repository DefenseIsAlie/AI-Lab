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
rho = 0.2

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
        # initial = random.randint(0, N-1)
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
            OUTPUT.write(f"The tour found with cost {G.bestCost} is: \n")
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

for _ in range(int(290 / til)):
    for ant in Ants:
        ant.getPath(g)

    g.updatePhermone()
    ANT.deltaPhermone = numpy.zeros((N, N))
    g.updateDeltaProb()
    g.updateProb()

H = numpy.zeros((N, N))
F = numpy.zeros(N)
Parent = numpy.zeros(N)

for i in range(N):
    for j in range(N):
        if h[i][j] != 0:
            H[i][j] = 1 / h[i][j] * g.matrix[i][j]
        else:
            H[i][j] = numpy.inf


def GoalTest(n):
    ret = []
    curr = n
    ret.append(curr)
    while curr != -1:
        curr = Parent[curr]
        ret.append(curr)
    ret.remove(-1)
    if len(ret) == N:
        return True
    else:
        return False


def Path(n):
    ret = []
    curr = n
    ret.append(curr)
    while curr != -1:
        curr = Parent[curr]
        ret.append(curr)
    ret.remove(-1)
    return ret


def MoveGen(n):
    path = []
    curr = n
    path.append(curr)
    while curr != -1:
        curr = Parent[curr]
        path.append(curr)
    path.remove(-1)
    ret = [x for x in range(0, N)]
    ret.sort(key=lambda a: H[n][a])
    ti = ret[: N // 2]
    tmp = [x for x in ti if x not in path]
    if tmp == []:
        return [x for x in ret[N // 2 :] if x not in path]
    else:
        return tmp


def A_Star():
    a = random.randint(0, N - 1)
    Open = []
    heapq.heapify(Open)
    F[a] = H[a][0]
    heapq.heappush(Open, (F[a], a))
    Parent[a] = -1
    Closed = []
    while Open != []:
        n = heapq.heappop(Open)[1]
        Closed.append(n)
        if GoalTest(n):
            return Path(n)

        Neighbour = MoveGen(n)
        for node in Neighbour:
            if (F[node], node) not in Open and node not in Closed:
                heapq.heappush(Open, (F[node], node))

            if (F[node], node) in Open:
                pass
            if node in Closed:
                pass

    return "failure"


print(f"Executed in {time.time()-start}")
OUTPUT.close()
