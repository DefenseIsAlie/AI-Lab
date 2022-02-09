import numpy
import time
import random
import functools
import copy
import sys

INPUT = open(sys.argv[1])

Type = INPUT.readline()
N = int(INPUT.readline())

Inp = INPUT.readlines()

firstN = numpy.array(Inp[:N])
secondN = numpy.array(Inp[N:])

INPUT.close()

OUTPUT = open("output.txt","a")

Q = 1000 
alpha = 5
beta = 35
rho =  0.8


class Graph:
    def __init__(self) -> None:
        self.Vertices = []
        self.probMatrix = [[0 for x in range(N)] for y in range(N)]
        self.epsilon = [[0 for x in range(N)] for y in range(N)]
        self.Phermones = [[1 for x in range(N)] for y in range(N)]
        self.Matrix = [[0 for x in range(N)] for y in range(N)]
        self.delta = [[0 for x in range(N)] for y in range(N)]
        self.bestcost = 696969
        self.bestTour = []
        self.start = time.time()

    def makeGraph(self, AdjList):
        for j in range(N):
            tmp = AdjList[j].strip().split()
            d = 0
            for k in tmp:
                self.Matrix[j][d] = float(k)
                if float(k) != 0:
                    self.epsilon[j][d] = 1/float(k)
                else:
                    self.epsilon[j][d] = 0
                d += 1

        for o in range(N):
            for p in range(N):
                self.probMatrix[o][p] = self.epsilon[o][p]/sum(self.epsilon[o])

    def updateProb(self):
        for o in range(N):
            for p in range(N):
                self.probMatrix[o][p] = (self.Phermones[o][p])**alpha * (self.epsilon[o][p])**beta

    def updatePhermone(self):
        for o in range(N):
            for p in range(N):
                self.Phermones[o][p] = rho * self.Phermones[o][p] + rho * self.delta[o][p]

        self.delta = [[0 for x in range(N)] for y in range(N)]


class ANT:
    def __init__(self, graph: Graph) -> None:
        self.ValidCities = list(range(0, N))
        self.Invalid = []
        self.currentPath = []
        self.pathCost = numpy.inf
        self.getPath(graph)

    def getPath(self, G: Graph) -> None:
        initial = random.randint(0,N-1)
        self.ValidCities.remove(initial)
        self.Invalid.append(initial)
        self.currentPath.append(initial)

        while len(self.currentPath) < N:
            previous = self.currentPath[-1]
            G.updateProb()
            set = [G.probMatrix[previous][x] for x in self.ValidCities]
            next = random.choices(self.ValidCities, weights = set)[0]
            self.currentPath.append(next)
            self.ValidCities.remove(next)
            self.Invalid.append(next)
        
        self.pathCost = self.getPathcost(self.currentPath, G)
        self.ValidCities = list(range(0,N))
        if self.pathCost < G.bestcost:
            G.bestcost = self.pathCost
            G.bestTour = copy.deepcopy(self.currentPath)
        #    OUTPUT.write(f"""
        #    The tour found with cost {G.bestcost} is
        #    {G.bestTour}            
        #    """)

    def getPathcost(self, l: list, G: Graph):
        ret = 0
        for i in range(len(self.currentPath)):
            ret += G.Matrix[self.currentPath[i]][self.currentPath[(i+1) % N]]
        return ret

    def deltaPher(self, l: list, G: Graph):
        for i in range(len(self.currentPath)):
            if G.Matrix[self.currentPath[i]][self.currentPath[(i+1) % N]] != 0:
                G.delta[self.currentPath[i]][self.currentPath[(i+1) % N]] = Q / self.pathCost

g = Graph()
g.makeGraph(secondN)

Ants = []
Que = list(range(0,N))
for i in range(3*N):
    Ants.append(ANT(g))
Que = list(range(0,N))
while time.time() - g.start < 250:
    for ant in Ants:
        ant.getPath(g)
        ant.deltaPher(ant.currentPath,g)
        if time.time() - g.start > 250:
            break
    g.updatePhermone()
    g.updateProb()
    Que = list(range(0,N))

OUTPUT.write(f"""
            The tour found with cost {g.bestcost} is
            {g.bestTour}
            Q = {Q}
            alpha = {alpha}
            beta = {beta}
            rho = {rho}
            pher = {g.Phermones[1]}            
            """)

# Team 21
