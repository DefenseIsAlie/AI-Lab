import sys, collections, typing, copy, heapq, time

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
                State.stateHistory.append(newState_1)
            if newState_2.grid != state.grid and not any(newState_2.grid == x.grid for x in State.stateHistory):
                newState_2.parent = state
                # find the heuristic value of the new state
                h = heuristic(newState_2)
                # add the new state to the priority queue
                heapq.heappush(State.stateNeighbours, (h, newState_2))
                State.stateHistory.append(newState_2)

def backTrace(s: State):
    ret = []
    while s.parent != None:
        ret.append(s.grid)
        s = s.parent
    ret.append(s.grid)
    return ret[::-1]

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

def arthmetic_heuristic(s: State):
    correctPositions = 0
    for i in range(len(s.grid)):
        if s.grid[i] == goal.grid[i]:
            correctPositions += i
        else:
            correctPositions -= i
    return -1* correctPositions

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

def L2Norm(s: State):
    g = goal
    ret = 0
    for i in range(3):
        for j in g.grid[i]:
            if j in s.grid[i]:
                ret +=  abs((g.grid[i].index(j) - s.grid[i].index(j)))**2
            else:
                for k in range(3):
                    if j in  s.grid[k]:
                        ret += (abs(i -k)**2 + abs(g.grid[i].index(j)-s.grid[k].index(j))**2)
    return ret

def PositionBased(s: State):
    ret = 0
    for i in range(len(s.grid)):
        for j in range(len(s.grid[i])):
            done = False
            if j != 0:
                for k in range(len(goal.grid)):
                    if s.grid[i][j] in goal.grid[k] and s.grid[i][j-1] == goal.grid[k][goal.grid[k].index(s.grid[i][j])-1]:
                        ret += j+1
                        done = True
                        break
                if done == False:
                    ret -= j+1
            else:
                for k in range(len(goal.grid)):
                    if goal.grid[k] != [] and s.grid[i][j] == goal.grid[k][0]:
                        ret += j+1
                        done = True
                        break
                if done == False:
                    ret -= j+1
    return -1*ret

def HillClimbing(heuristic):
    if goalTest(start):
        return start
    heapq.heappush(State.stateNeighbours,(0,start))
    tmp = heapq.heappop(State.stateNeighbours)
    current = tmp[1]
    max_hueristic = tmp[0]
    proceed = True
    while proceed == True:
        State.stateNeighbours=[]
        if goalTest(current):
            path = backTrace(current)
            return path
        MoveGen(current,heuristic)
        tmp = heapq.heappop(State.stateNeighbours)
        node = tmp[1]
        h1 = tmp[0]
        State.stateHistory.append(node)
        if h1 > max_hueristic:
            current = node
            max_hueristic = h1
        else:
            proceed = False
            path = backTrace(current)
            return path

    

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
start = State([[], ["F","A","B"],["E","G","C"]])
goal = State([["G"],["F","E"],["C","B","A"]])

def goalTest(s: State):
    g = goal
    return s.grid == g.grid


def BestFirstSearch(heuristic):
    #insert start in priorQueue
    #delete elements of priorQ one by one
    #if element is goal exit
    #else traverese neighbours
    State.stateHistory.append(start)
    heapq.heappush(State.stateNeighbours,(heuristic(start),start))
    while State.stateNeighbours != []:
        current = heapq.heappop(State.stateNeighbours)[1]
        if goalTest(current):
            path = backTrace(current)
            return path
        else :
            MoveGen(current,heuristic)
time_start = time.time()
ans = BestFirstSearch(OrdHeuristic)
# ans = BestFirstSearch(L2Norm)
# ans = BestFirstSearch(ManhattanHeuristic)
# ans = BestFirstSearch(PositionBased)
# ans = HillClimbing(ManhattanHeuristic)
end_time = time.time()
print("time taken :",end_time-time_start)
print("state explored: ", len(State.stateHistory))
print("path length: ", len(ans))
for i in range(len(ans)):
    print(ans[i])