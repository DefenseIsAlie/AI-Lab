import sys, collections, typing, copy, heapq

#t = sys.argv[1]
#Input = open(t)
#SearchType = int(Input.readline())

class State:
    stateHistory = []
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
                # find the heuristic value of the new state
                h = heuristic(newState_1)
                # add the new state to the priority queue
                heapq.heappush(neighbors, (h, newState_1))
            if newState_2.grid != state.grid and not any(newState_2.grid == x.grid for x in State.stateHistory):
                # find the heuristic value of the new state
                h = heuristic(newState_2)
                # add the new state to the priority queue
                heapq.heappush(neighbors, (h, newState_2))
    return

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

def heuristic():
    pass

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
start = State([["A", "E"], ["F"], ["B","D"]])
goal = State([["A","B"],["D","E","F"],[]])

State.stateHistory.append(start)


neighbors = []
MoveGen(start, OrdHeuristic)
for i in range(len(neighbors)):
    print(neighbors[i][1].grid)
