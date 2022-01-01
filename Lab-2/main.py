import sys, collections, typing, copy, heapq

#t = sys.argv[1]
#Input = open(t)
#SearchType = int(Input.readline())

class State:
    stateHistory = []  # closed list
    stateNeighbours = [] # open list
    statesExplored = 0
    # grid is an 2-d array.
    def __init__(self, grid):
        # store copy of grid
        self.grid = grid
        self.parent = None

    def __str__(self) -> str:
        return f"{self.grid}"
    
    def __lt__(self, other):
        return self.grid < other.grid

    def __le__(self,other):
        return self.grid <= other.grid


def MoveGen(state, heuristic):
    # find the neighbors of the current state
    for i in range(len(state.grid)):
        if state.grid[i] != []:
            newState_1 = State(copy.deepcopy(state.grid))
            newState_2 = State(copy.deepcopy(state.grid))
            upperBlock = newState_1.grid[i].pop()
            newState_2.grid[i].pop()
            newState_1.grid[(i+1)%3].append(upperBlock)
            newState_2.grid[(i+2)%3].append(upperBlock)
            if newState_1.grid != state.grid and not any(newState_1.grid == x.grid for x in State.stateHistory):
                newState_1.parent = state
                # find the heuristic value of the new state
                h = heuristic(newState_1)
                # add the new state to the priority queue
                heapq.heappush(State.stateNeighbours, (h, newState_1))
            if newState_2.grid != state.grid and not any(newState_2.grid == x.grid for x in State.stateHistory):
                newState_2.parent = state
                # find the heuristic value of the new state
                h = heuristic(newState_2)
                # add the new state to the priority queue
                heapq.heappush(State.stateNeighbours, (h, newState_2))

def backTrace(s: State):
    ret = []
    while s.parent != None:
        ret.append(s.grid)
        s = s.parent
    return ret

def OrdHeuristic(s: State):
    g = goal
    ret = 0
    for i in range(len(s.grid)):
        for j in s.grid[i]:
            if j in g.grid[i]:
                ret += abs(ord(j)-ord(g.grid[i][g.grid[i].index(j)]))
            else:
                ret += abs(ord(j))
    return ret

def ManhattanHeuristic(s: State):
    g = goal
    ret = 0
    for i in range(3):
        for j in g.grid[i]:
            if j in s.grid[i]:
                ret +=  abs((g.grid[i].index(j) - s.grid[i].index(j)))
            else:
                for k in range(3):
                    if j in  s.grid[k]:
                        ret += abs(i -k) + abs(g.grid[i].index(j)-s.grid[k].index(j))
    return ret

def Heuristic2(s: State):
    pass

def Heuristic3(s: State):
    pass

def HillClimbing(heuristic):
    if goalTest(start):
        return start
    heapq.heappush(State.stateNeighbours,(0,start))
    current = heapq.heappop(State.stateNeighbours)[1]
    State.stateHistory.append(current)
    while State.stateNeighbours !=[]:
        if goalTest(current):
            return current
        MoveGen(current)
        tmp = heapq.heappop(State.stateNeighbours)[1]
        State.stateHistory.append(tmp)
        if heuristic(tmp) > heuristic(current):
            current = tmp


    

#def heuristic():
#    pass

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()
    inputLine = []
    for line in lines:
        line = line.strip().split()
        if line:
            inputLine.append(line)
    startState = inputLine[:3]
    goalState = inputLine[-3:]
    del inputLine
start = State([[], ["B","A"], ["C"]])
goal = State([[],[],["C","B","A"]])

def goalTest(s: State):
    g = goal
    return s.grid == g.grid

#MoveGen(start, OrdHeuristic)

#for i in range(len(State.stateNeighbours)):
#    print(State.stateNeighbours[i][1].grid)

def BestFirstSearch(heuristic):
    #insert start in priorQueue
    #delete elements of priorQ one by one
    #if element is goal exit
    #else traverese neighbours
    heapq.heappush(State.stateNeighbours,(0,start))
    while State.stateNeighbours != []:
        current = heapq.heappop(State.stateNeighbours)[1]
        State.stateHistory.append(current)
        if goalTest(current):
            return current
        else :
            MoveGen(current,heuristic)

ans = BestFirstSearch(ManhattanHeuristic)
#ans = HillClimbing(OrdHeuristic)

ans = backTrace(ans)
for i in range(len(ans)-1,-1,-1):
    print(ans[i])