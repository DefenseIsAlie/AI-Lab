import sys, collections, typing, copy, heapq

#t = sys.argv[1]
#Input = open(t)
#SearchType = int(Input.readline())

class State:
    stateHistory = []  # closed list
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
    max_h = heuristic(state)
    max_node = state
    for i in range(len(state.grid)):
        if state.grid[i] != []:
            newState_1 = State(copy.deepcopy(state.grid))
            newState_2 = State(copy.deepcopy(state.grid))
            upperBlock = newState_1.grid[i].pop()
            newState_2.grid[i].pop()
            newState_1.grid[(i+1)%3].append(upperBlock)
            newState_2.grid[(i+2)%3].append(upperBlock)
            if newState_1.grid != state.grid and not any(newState_1.grid == x.grid for x in State.stateHistory):
                # add to the closed list
                State.stateHistory.append(newState_1)
                # find the maximum heuristic value of the neighbors
                h1 = heuristic(newState_1)
                if h1 > max_h:
                    max_h = h1
                    max_node = newState_1
                    newState_1.parent = state
            if newState_2.grid != state.grid and not any(newState_2.grid == x.grid for x in State.stateHistory):
                # add to the closed list
                State.stateHistory.append(newState_2)
                # find the maximum heuristic value of the neighbors
                h2 = heuristic(newState_2)
                if h2 > max_h:
                    max_h = h2
                    max_node = newState_2
                    newState_2.parent = state
    return max_node

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
    return -1 * ret

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
    return -1 * ret

def PositionBased(s: State):
    pass

def HillClimbing(heuristic):
    current = start
    proceed = True
    while proceed == True:
        if goalTest(current):
            path = backTrace(current)
            return path
        node = MoveGen(current,heuristic)
        if node and heuristic(node) > heuristic(current):
            current = node
        else:
            proceed = False
            return backTrace(current)

    

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
start = State([[], ["C","B","A"], ["E","D"]])
goal = State([["C","B","D","A"],["E"],[]])

def goalTest(s: State):
    g = goal
    return s.grid == g.grid

ans = HillClimbing(ManhattanHeuristic)

# for l in State.stateHistory:
#     print(l.grid)

for i in range(len(ans)):
    print(ans[i])