from itertools import combinations
import numpy as np
import random

def logic(state: list) -> list:
    """
    convert the state to logic i.e adds complementary values for each bit.
    """
    ans = state.copy()
    for i in range(len(state)):
        ans.append((state[i]+1)%2)
    return ans


def clauseEval(state : list, clause: list) -> bool:
    """
    Evaluate a clause of the goal.
    state : state with complementary values.(logic state)
    clause : A clause in formulae.(list of numbers i.e literals)
    """
    for i in clause:
        if state[int(i)-1] == 1:
            return True
    return False

def heuristic(state : list, formula : list) -> int:
    """
    Calculate the heuristic value of a state.
    Number of clauses satisfied.
    """
    if type(state) == tuple:
        (state, tabuTenureList) = state
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
    bitflips : number of bitflips to be made.
    """
    neighbors = []
    comb = combinations(range(len(state)), bitflips)
    for i in list(comb):
        neighbor = list(state)
        for j in i:
            neighbor[j] = (neighbor[j]+1)%2
        neighbors.append(neighbor)
    return neighbors

def tabuStateNeighbors(state : tuple, tabuTenure : int) -> list:
    """
    Return the neighbors of a state. which are the possible states after
    flipping a bit according to tabuTenure.
    bitflips : number of bitflips to be made.
    """
    (bitState, tabuTenureList) = state
    neighbors = []
    for i in range(len(bitState)):
        if tabuTenureList[i] == 0:
            neighbor = (list(bitState), list(tabuTenureList))
            neighbor[0][i] = (neighbor[0][i]+1)%2
            neighbor[1][i] = tabuTenure + 1
            neighbors.append(neighbor)
            for i in range(len(neighbor[1])):
                if neighbor[1][i] > 0:
                    neighbor[1][i] -= 1

    return neighbors

def movegen(stateList : list, Formula :list, number: int) -> list:
    """
    gives max heuristic value of the state in list.
    stateList : list of states to be evaluated generally stateNeighbors or tabuStateNeighbors
    """
    # if tabu
    tabu =  type(stateList) == tuple
    if tabu:
        (stateList, tabuTenureList) = stateList
    state_list = []
    tabu_list = []
    heuristic_list = []
    for i in stateList:
        heuristic_list.append(heuristic(i, Formula))
    # argsort the heuristic list for states with max heuristic value
    max_heuristic_list = np.argsort(heuristic_list)
    
    for i in max_heuristic_list:    
        state_list.append(stateList[i])
        if tabu:
            tabu_list.append(tabuTenureList[i])
    if tabu:
        return state_list[-number:] , tabu_list[-number:]
    return state_list[-number:]

def goalTest(state : list, Formula) -> bool:
    """
    Test if a state is a goal.
    all clauses are satisfied.
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
        for i in  movegen(stateNeighbors(current_state, 1), Formula, beam_size):
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
        for i in  movegen(stateNeighbors(current_state, bitflips), Formula, 1):
            if  heuristic(i, Formula) > heuristic(current_state, Formula) and i not in statesExplored and i not in frontier:
                frontier.append(i)
        while frontier == [] and bitflips < len(state)//2+1:
            bitflips += 1
            for i in  movegen(stateNeighbors(current_state, bitflips), Formula, 1):
                if  heuristic(i, Formula) > heuristic(current_state, Formula) and i not in statesExplored and i not in frontier:
                    frontier.append(i)
    return None

def tabuSearch(state : list, Formula, tabuTenure : int) -> list:
    """
    Tabu search algorithm.
    """
    frontier = [state]
    statesExplored = []
    while frontier:
        current_state = frontier.pop()
        statesExplored.append(current_state)
        if goalTest(current_state[0], Formula):
            return current_state, statesExplored
        print(movegen( tabuStateNeighbors(current_state, 1), Formula, 1))
        for i in  movegen( tabuStateNeighbors(current_state, 1), Formula, 1):
            if  heuristic(i[0], Formula) > heuristic(current_state[0], Formula) and i not in statesExplored and i not in frontier:
                frontier.append(i)
    return None, statesExplored
    
########################### writing clauses to file #############################
OUTPUT = open("clauses.txt","w")

N = 4
K = 10

def generateLiterals(n: int):
    ret = []
    ret.append(random.randrange(1,2*n+1))
    ret.append(random.randrange(1,2*n+1))
    ret.append(random.randrange(1,2*n+1))
    return ret

def checkedLiterals(n: int):
    ret = []
    checkpass = True
    while checkpass:
        ret = generateLiterals(n)
        for x in ret:
            if ret.count(x) != 1:
                checkpass = True
            elif complement(x,n) in ret:
                checkpass = True
            else:
                checkpass = False
            if checkpass:
                break
    return ret

def complement(x: int,n: int):
    ret = 0
    if x <= n:
        ret = n + x
    elif x>n:
        ret = x - N
    elif x<=0 or x>2*n:
        ret = 0
    return ret

def clausePrinter(n: int, k: int):
    for _ in range(k):
        OUTPUT.write(str(checkedLiterals(n))+"\n")
clausePrinter(N,K)
OUTPUT.close()

########################### reading clauses from file #############################
IntialState = [0]*N
statesExplored = []
Formula = []
with open("clauses.txt") as f:
    for line in f:
        Formula.append(line.strip('\n').strip(']').strip('[').split(','))
TabuIntialState = (IntialState, [0]*N)

print("CNF circuit :", Formula)
print("1 to 4 : normal variable, 5 to 8 : negated variable\n\n")
print("Input State: ", IntialState)
########################### running algorithms #############################

while True:
    print("Enter 1 for Beam Search")
    print("Enter 2 for Variable Neighbor Descent")
    print("Enter 3 for Tabu Search")
    print("Enter 4 for Exit")
    choice = int(input("Enter your choice : "))
    if choice == 1:
        ans = BeamSearch(IntialState, 10, Formula)
        if ans[0] != None:
            print("\n\nSolution :", ans[0])
            print("States Explored :", ans[1])
            print("\n\n")
        else:
            print("No solution found")
            print("States Explored :", ans[1])
            print("\n\n")
    elif choice == 2:
        ans = variableNeighbor_descent(IntialState, Formula)
        if ans[0] != None:
            print("\n\nSolution :", ans[0])
            print("States Explored :", ans[1])
            print("\n\n")
        else:
            print("No solution found")
            print("States Explored :", ans[1])
            print("\n\n")
    elif choice == 3:
        ans = tabuSearch(TabuIntialState, Formula, 10)
        if ans[0] != None:
            print("\n\nSolution :", ans[0])
            print("States Explored :", ans[1])
            print("\n\n")
        else:
            print("No solution found")
            print("States Explored :", ans[1])
            print("\n\n")
    elif choice == 4:
        break
    else:
        print("Invalid Choice")
        continue
    
