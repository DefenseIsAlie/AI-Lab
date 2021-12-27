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
        return self.grid

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

def moveGen(state):
    neighbors = []
    # find the neighbors of the current state
    for i in range(len(state.grid)):
        if state.grid[i] != []:
            for j in range(len(state.grid[i])):
                pass
    return neighbors
        
def OrdHeuristic(s: State):
    g = goal
    ret = 0
    for i in range(len(s.grid)):
        for j in range(len(s.grid[i])):
            ret += abs(ord(s.grid[i][j])-ord(s.grid[i][j]))
            
    return ret
    
print(f"\n{OrdHeuristic(start)}\n")

listOfStates = moveGen(start)
print(listOfStates)
for i in range(len(listOfStates)):
    print(listOfStates[i].grid)

# = 0
#for line in Input:
#    if j==0 :
#        for i in range(len(line)):
#            start._stackA.append(line[i])
#            j+=1
#    if j==1 :
#        for i in range

