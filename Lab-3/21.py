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
        if state[i] ==0:
            return False
    return True

def heuristic(state : list, formula : list) -> int:
    """
    Calculate the heuristic value of a state.
    """
    heuristic_value = 0
    for clause in formula:
        if clauseEval(state, clause):
            heuristic_value += 1
    return heuristic_value


def goalTest(state : list, goal : list) -> bool:
    """
    Test if a state is a goal.
    """
    return heuristic(state, Formula) == len(Formula)

IntialState = [0,0,0]
Formula = []
with open("clauses.txt") as f:
    for line in f:
        Formula.append(line.strip('\n').strip(']').strip('[').split(','))


    
