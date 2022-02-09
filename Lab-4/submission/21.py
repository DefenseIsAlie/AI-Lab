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

timedelay = 0

if N >= 250:
    timedelay = 50
else:
    timedelay = 40

Q = 100
alpha = 0.9
beta = 20
rho = 0.3

h = numpy.zeros((N, N))


class Graph:
    solchange = 0
    iterrr = 0
    iterrrprev = 0

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

        if N <= 250:
            if time.time() - Graph.solchange > timedelay:
                self.Phermones = numpy.ones((N, N))
        else:
            if time.time() - Graph.solchange > timedelay and Graph.iterrr < 1:
                Graph.iterrr += 1
                self.Phermones = numpy.ones((N, N))


class ANT:
    deltaPhermone = numpy.zeros((N, N))
    Qu = list(range(N))

    def __init__(self, graph: Graph) -> None:
        self.validCities = list(range(0, N))
        self.currentPath = []
        self.pathCost = numpy.inf
        self.getPath(graph)

    def getPath(self, G: Graph):
        if ANT.Qu == []:
            ANT.Qu = list(range(N))
        initial = ANT.Qu.pop()
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

        self.pathCost = self.getPathCost(G)
        self.validCities = list(range(0, N))

        if self.pathCost < G.bestCost:
            Graph.solchange = time.time()
            Graph.iterrr += 1
            Graph.iterrrprev = Graph.iterrr
            G.bestCost = self.pathCost
            G.bestTour = copy.deepcopy(self.currentPath)
            OUTPUT.write(
                f"The tour found with cost : {G.bestCost} at {time.time() - start} seconds\n"
            )
            OUTPUT.write(" ".join(map(str, G.bestTour)))
            OUTPUT.write("\n \n")
        self.currentPath = []

    def getPathCost(self, G: Graph):
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

while time.time() - start < 298:
    for ant in Ants:
        if time.time() - start > 298:
            break
        ant.getPath(g)

    if time.time() - start > 297:
        break
    g.updatePhermone()
    ANT.deltaPhermone = numpy.zeros((N, N))
    g.updateDeltaProb()
    g.updateProb()

OUTPUT.close()

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

"""
class LKH:
    def __init__(self) -> None:
        self.Tour = set()
        self.tour = []
        self.TourCost = 0
        self.X = set()
        self.xx = []
        self.Y = set()
        self.yy = []
        self.G = 0
        self.Path = []
        self.randTour()
        self.PathToTour()

    def randTour(self):
        validCities = list(range(0, N))
        path = []
        pathCost = 0
        initial = random.randint(0, N - 1)
        validCities.remove(initial)
        path.append(initial)

        while len(path) < N:
            prev = path[-1]
            setx = [g.matrix[prev][x] for x in validCities]
            next = random.choices(validCities, weights=setx)[0]
            path.append(next)
            validCities.remove(next)
            pathCost += g.matrix[prev][next]

        self.TourCost = pathCost
        print(pathCost)
        self.Path = path

    def PathToTour(self):
        i = 0
        for x in self.Path:
            i += 1
            self.tour.append((x, self.Path[i % N]))
            self.Tour.add(frozenset({x, self.Path[i % N]}))

    def TourToPath(self):
        Parent = numpy.zeros(N)
        for tup in self.tour:
            Parent[tup[1]] = int(tup[0])
        path = []
        curr = 0

        while len(path) < N:
            path.append(int(Parent[curr]))
            curr = int(Parent[curr])

        return path

    def Lkmove(self, r: int):
        T = copy.deepcopy(self.Tour)
        t = copy.deepcopy(self.tour)
        Closed = set()
        for tup in t:
            self.r = r
            self.G = 0
            self.X = set()
            self.xx = []
            self.yy = []
            self.Y = set()
            if frozenset(set(tup)) in Closed:
                continue
            Closed.add(frozenset(set(tup)))
            self.X.add(frozenset(set(tup)))
            self.xx.append(tup)
            setx = list(range(N))
            setx.remove(tup[1])
            setx.sort(key=lambda a: h[tup[1]][a])
            temppp = setx[:30]
            gi = [(g.matrix[tup[0]][tup[1]] - g.matrix[tup[1]][x], x) for x in temppp]
            for x in gi:
                if frozenset({tup[1], x[1]}) in T:
                    gi.remove(x)
            gi.sort()
            if gi == [] or gi[-1][0] <= 0:
                continue
            y1 = (tup[1], gi[-1][1])
            if frozenset(y1) not in T and frozenset(y1) not in self.X:
                self.G += gi[-1][0]
                self.Y.add(frozenset(y1))
                self.yy.append(y1)
                Closed.add(frozenset(y1))
            else:
                continue

            broke = True
            for i in range(self.r - 1):
                print(i)
                tempp = -1
                x1 = (self.yy[-1][1], self.Path[self.Path.index(self.yy[-1][1]) - 1])
                x2 = (
                    self.yy[-1][1],
                    self.Path[(self.Path.index(self.yy[-1][1]) + 1) % N],
                )
                tt = [x1, x2]
                for x in tt:
                    if frozenset(x) in self.Y:
                        continue
                    Tdash = copy.deepcopy(T)
                    y2 = (x[1], self.xx[0][0])
                    if frozenset(x) in Tdash:
                        Tdash.remove(frozenset(x))
                    if frozenset(self.xx[0]) in Tdash:
                        Tdash.remove(frozenset(self.xx[0]))
                    Tdash.add(frozenset(y1))
                    Tdash.add(frozenset(y2))
                    if self.isTour(Tdash):
                        tempp = x
                        break
                if tempp == -1:
                    broke = False
                    break
                if frozenset(tempp) in self.Y:
                    broke = False
                    break
                self.X.add(frozenset(tempp))
                self.xx.append(tempp)
                Closed.add(frozenset(tempp))

                setx = list(range(N))
                setx.remove(tempp[1])
                hello = tempp[1]
                setx.sort(key=lambda a: h[hello][a])
                l = setx[:30]
                gi = [
                    (g.matrix[tempp[0]][tempp[1]] - g.matrix[tempp[1]][x], x) for x in l
                ]
                for x in gi:
                    if frozenset({tempp[1], x[1]}) in T:
                        gi.remove(x)
                gi.sort()
                if gi == [] or gi[-1][0] + self.G <= 0:
                    self.Y.add(frozenset({tempp[1], self.X[-1][0]}))
                    self.yy.append((tempp[1], self.X[-1][0]))
                    break
                gi.reverse()
                for x in gi:
                    yi = frozenset({tup[1], x[1]})
                    if yi not in T and self.G + x[0] > 0 and yi not in self.X:
                        self.G += x[0]
                        self.Y.add(yi)
                        self.yy.append(tuple(yi))
                        Closed.add(yi)
                        break

            if self.G > 0 and broke:
                for x in self.X:
                    if x in T:
                        T.remove(x)
                for y in self.Y:
                    T.add(y)
                self.Tour = copy.deepcopy(T)
                self.TourCost -= self.G
                self.Tourtotour()
                self.Path = self.TourToPath()

    def TourCost(self, l: list):
        ret = 0
        for tup in l:
            ret += g.matrix[tup[0]][tup[1]]
        return ret

    def Tourtotour(self):
        grap = [[-1, -1] for x in range(N)]
        tor = []
        for x in self.Tour:
            f = tuple(x)
            if grap[f[0]][0] == -1:
                grap[f[0]][0] = f[1]
                grap[f[1]][1] = f[0]
            else:
                grap[f[0]][1] = f[1]
                grap[f[1]][0] = f[0]
        cuur = 0

        while len(tor) < N:
            tor.append((cuur, grap[cuur][0]))
            cuur = grap[cuur][0]

        self.tour = copy.deepcopy(tor)

    def isTour(self, l: set):
        ret = True
        count = [0 for x in range(N)]
        for tup in l:
            t = tuple(tup)
            try:
                count[t[0]] += 1
                count[t[1]] += 1
            except:
                continue

        for i in count:
            if i != 2:
                ret = False

        return ret


lk = LKH()
for i in range(5, N, 2):
    lk.Lkmove(i)

print(lk.TourCost)
print(lk.Path)
"""

print(f"Executed in {time.time()-start}")
