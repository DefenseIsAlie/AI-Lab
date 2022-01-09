from itertools import combinations
import numpy as np



def logic(state: list) -> list:
    """
    Solve the logic problem.
    """
    ans = state.copy()
    for i in range(len(state)):
        ans.append((state[i]+1)%2)
    return ans


def clauseEval(state : list, clause: list) -> bool:
    """
    Evaluate a clause of the goal.
    """
    for i in clause:
        if state[int(i)-1] == 1:
            return True
    return False

def heuristic(state : list, formula : list) -> int:
    """
    Calculate the heuristic value of a state.
    """
    state = logic(state)
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

def movegen(state : list, stateList : list, Formula, number: int) -> list:
    """
    gives max heuristic value of the state in list.
    """
    state_list = []
    heuristic_list = []
    for i in stateList:
        heuristic_list.append(heuristic(i, Formula))
    # argsort the heuristic list for states with max heuristic value
    max_heuristic_list = np.argsort(heuristic_list)
    for i in max_heuristic_list:    
        state_list.append(stateList[i])
    return state_list[-number:]

def goalTest(state : list, Formula) -> bool:
    """
    Test if a state is a goal.
    """
    return heuristic(state, Formula) == len(Formula)


def BeamSearch(state : list, beam_size : int, Formula) -> list:
    """
    Beam search algorithm.
    """
    frontier = [state]
    statesExplored = []
    while frontier:
        current_state = frontier.pop()
        statesExplored.append(current_state)
        if goalTest(current_state, Formula):
            return current_state, statesExplored
        print(movegen(current_state, stateNeighbors(current_state, 1), Formula, beam_size))
        for i in  movegen(current_state, stateNeighbors(current_state, 1), Formula, beam_size):
            if  heuristic(i, Formula) > heuristic(current_state, Formula) and i not in statesExplored and i not in frontier:
                frontier.append(i)
    return None, statesExplored

def variableNeighbor_descent(state : list, Formula) -> list:
    """
    Variable neighbor descent algorithm.
    """
    bitflips = 1
    frontier = [state]
    statesExplored = []
    while frontier:
        neighbor = stateNeighbors(frontier[0], bitflips)
        if neighbor not in statesExplored:
            if goalTest(neighbor):
                return neighbor
            else:
                if heuristic(neighbor, Formula) < heuristic(frontier[0], Formula):
                    frontier = [neighbor]
                else:
                    frontier.append(neighbor)
        frontier.pop(0)
            
    return None

IntialState = [0,1,1,1,0]
statesExplored = []
Formula = []
with open("clauses.txt") as f:
    for line in f:
        Formula.append(line.strip('\n').strip(']').strip('[').split(','))

ans = BeamSearch(IntialState, 2, Formula)
print(ans[0])
print(ans[1])
# ans = movegen([1,1,1,0,1], stateNeighbors([1,1,1,0,1], 1), Formula, 2)
# print(ans)
