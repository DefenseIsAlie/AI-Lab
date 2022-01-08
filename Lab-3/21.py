from itertools import combinations

def logic(state: list) -> list:
    """
    Solve the logic problem.
    """
    ans = state
    for i in range(len(state)):
        ans.append((state[i]+1)%2)
    return ans


def clauseEval(state : list, clause: list) -> bool:
    """
    Evaluate a clause of the goal.
    """
    for i in clause:
        if state[i] == 1:
            return True
    return False

def heuristic(state : list, formula : list) -> int:
    """
    Calculate the heuristic value of a state.
    """
    heuristic_value = 0
    for clause in formula:
        if clauseEval(state, clause):
            heuristic_value += 1
    return heuristic_value

def stateNeighbors(state : list, bitflips : int) -> list:
    """
    Return the neighbors of a state. which are the possible states after
    flipping a bit.
    """
    neighbors = []
    comb = combinations(range(len(state)), bitflips)
    for i in list(comb):
        neighbor = list(state)
        for j in i:
            neighbor[j] = (neighbor[j]+1)%2
        neighbors.append(neighbor)
    return neighbors


def goalTest(state : list, goal : list) -> bool:
    """
    Test if a state is a goal.
    """
    return heuristic(state, Formula) == len(Formula)


def BeamSearch(state : list, goal : list, beam_size : int) -> list:
    """
    Beam search algorithm.
    """
    frontier = [state]
    statesExplored = []
    while frontier:
        for _ in range(beam_size):
            if goalTest(frontier[0], goal):
                return frontier[0]
            else:
                statesExplored.append(frontier[0])
                for neighbor in stateNeighbors(frontier[0],1):
                    if neighbor not in statesExplored:
                        frontier.append(neighbor)
        frontier.pop(0)
    return None

def variableNeighbor_descent(state : list, goal : list, Formula) -> list:
    """
    Variable neighbor descent algorithm.
    """
    bitflips = 1
    frontier = [state]
    statesExplored = []
    while frontier:
        neighbor = stateNeighbors(frontier[0], bitflips)
        if neighbor not in statesExplored:
            if goalTest(neighbor, goal):
                return neighbor
            else:
                if heuristic(neighbor, Formula) < heuristic(frontier[0], Formula):
                    frontier = [neighbor]
                else:
                    
        frontier.pop(0)
            
    return None

IntialState = [0,0,0]
statesExplored = []
Formula = []
with open("clauses.txt") as f:
    for line in f:
        Formula.append(line.strip('\n').strip(']').strip('[').split(','))
    
