import sys, collections, typing

#t = sys.argv[1]
#Input = open(t)
#SearchType = int(Input.readline())

class State:
    stateHistory = []
    # grid is an 2-d array.
    def __init__(self, grid):
        self.grid = grid

    def __str__(self) -> str:
        return f"{self.grid}"

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()
    inputLine = []
    for line in lines:
        line = line.strip().split()
        if line:
            inputLine.append(line)
    startState = inputLine[:3]
    print(startState)
    goalState = inputLine[-3:]
    print(goalState)
    del inputLine

start = State([["A", "E"], ["F"], ["B","D"]])
goal = State([["A","B"],["D","E","F"],[]])

State.stateHistory.append(start)

def MoveGen(state):
    neighbors = []
    # find the neighbors of the current state
    for i in range(len(state.grid)):
        if state.grid[i] != []:
            Si = State(state.grid)
            Sii = State(state.grid) 
            a = Si.grid[i].pop()
            b = Sii.grid[i].pop()
            Si.grid[(i+1)%3].append(a)
            Sii.grid[(i+2)%3].append(b)
            neighbors.append(Si)
            neighbors.append(Sii)
    return neighbors
        
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

print(f"\n{OrdHeuristic(start)}\n")

listOfStates = MoveGen(start)

for _D in listOfStates:
    print(_D)


# = 0
#for line in Input:
#    if j==0 :
#        for i in range(len(line)):
#            start._stackA.append(line[i])
#            j+=1
#    if j==1 :
#        for i in range

