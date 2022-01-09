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

def stateNeighbors(state : list, bitflips : int, tabuTenureList : list= [], tabuTenure: int = 0) -> list:
    """
    Return the neighbors of a state. which are the possible states after
    flipping a bit.
    """
    neighbors = []
    comb = combinations(range(len(state)), bitflips)
    for i in list(comb):
        neighbor = list(state)
        for j in i:
            if tabuTenure and tabuTenureList[j] == 0:
                neighbor[j] = (neighbor[j]+1)%2
                tabuTenureList[j] = tabuTenure+1
            elif tabuTenure == 0:
                neighbor[j] = (neighbor[j]+1)%2
        neighbors.append(neighbor)
    for i in range(tabuTenure):
        if tabuTenure and tabuTenureList[i] > 0:
            tabuTenure[i] -= 1
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
        current_state = frontier.pop()
        statesExplored.append(current_state)
        if goalTest(current_state, Formula):
            return current_state, statesExplored
        for i in  movegen(current_state, stateNeighbors(current_state, bitflips), Formula, 1):
            if  heuristic(i, Formula) > heuristic(current_state, Formula) and i not in statesExplored and i not in frontier:
                frontier.append(i)
        while frontier == [] and bitflips < len(state)//2+1:
            bitflips += 1
            for i in  movegen(current_state, stateNeighbors(current_state, bitflips), Formula, 1):
                if  heuristic(i, Formula) > heuristic(current_state, Formula) and i not in statesExplored and i not in frontier:
                    frontier.append(i)
    return None

def tabuSearch(state : list, Formula, tabuTenure : int) -> list:
    """
    Tabu search algorithm.
    """
    frontier = [state]
    statesExplored = []
    tabuTenureList = [0]*len(state)
    while frontier:
        current_state = frontier.pop()
        statesExplored.append(current_state)
        if goalTest(current_state, Formula):
            return current_state, statesExplored
        print(movegen(current_state, stateNeighbors(current_state, 1), Formula, 1, tabuTenureList, tabuTenure))
        print(tabuTenureList)
        for i in  movegen(current_state, stateNeighbors(current_state, 1), Formula, 1, tabuTenureList, tabuTenure):
            if  heuristic(i, Formula) > heuristic(current_state, Formula) and i not in statesExplored and i not in frontier:
                frontier.append(i)
    return None, statesExplored
    

IntialState = [0,1,1,1,0]
statesExplored = []
Formula = []
with open("clauses.txt") as f:
    for line in f:
        Formula.append(line.strip('\n').strip(']').strip('[').split(','))

ans = variableNeighbor_descent(IntialState, Formula)
print(ans)