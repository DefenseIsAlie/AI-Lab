import sys, collections, typing, copy, heapq, time

class State:
    stateHistory = []  # closed list
    stateNeighbours = [] # open list
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

def goalTest(s: State):
    g = goal
    return s.grid == g.grid

def backTrace(s: State):
    ret = []
    while s.parent != None:
        ret.append(s.grid)
        s = s.parent
    ret.append(s.grid)
    return ret[::-1]

######################### Heuristics #########################
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



######################### Algorithms #########################
def HillClimbing(heuristic):
    if goalTest(start):
        return [start]
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
        [h1,node] = heapq.heappop(State.stateNeighbours)
        if h1 <= heuristic(current):
            current = node
        else:
            proceed = False
            path = backTrace(current)
            return path


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

######################### Main #########################
algos = [BestFirstSearch,HillClimbing]
heuristic_algos = [OrdHeuristic,ManhattanHeuristic,L2Norm,PositionBased]
with open(sys.argv[1], 'r') as f:
    lines = f.readlines()
    inputLine = []
    for line in lines:
        if line != '\n':
            inputLine.append(line.strip().split(' '))
        else:
            inputLine.append([])
    startState = inputLine[:3]
    goalState = inputLine[3:]
    if len(goalState) != 3:
        for i in range(3-len(goalState)):
            goalState.append([])
    del inputLine
print("Intial State:")
print(startState)
print("Goal State:")
print(goalState)
start = State(startState)
goal = State(goalState)

# take input from user for BFS or HillClimbing and heuristic
print("Enter 0 for BFS or 1 for HillClimbing")
a = int(input())
print("Enter 0 for OrdHeuristic or 1 for ManhattanHeuristic or 2 for L2Norm or 3 for PositionBased")
b = int(input())
time_start = time.time()
# ans = BestFirstSearch(OrdHeuristic)
# ans = BestFirstSearch(L2Norm)
# ans = BestFirstSearch(ManhattanHeuristic)
# ans = BestFirstSearch(PositionBased)
# ans = HillClimbing(PositionBased)
# ans = HillClimbing(ManhattanHeuristic)
# ans = HillClimbing(L2Norm)
# ans = HillClimbing(OrdHeuristic)
ans = algos[a](heuristic_algos[b])
end_time = time.time()
print("goal state achieved :", ans[-1] == goal.grid)
print("time taken :",end_time-time_start)
print("states explored: ", len(State.stateHistory))
print("path length: ", len(ans))
print("\npath :")
for i in range(len(ans)):
    print(ans[i])