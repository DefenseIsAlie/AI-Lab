def VariableNeighbourHoodDescent(Neighbourhoods: list):
    x = [0,0,0]
    l = 0
    while(l!=len(Neighbourhoods)):
        x_1 = BestofNeighbourHood(Neighbourhoods[l])
        if heuristic(x_1) > heuristic(x):
            x = x_1
        else:
            l+=1
    return x

def heuristic(s):
    return s[0]+s[1]+s[2]

def BestofNeighbourHood(Neighbourhood: list):
    x = [0,0,0]
    k = 0
    for x_1 in Neighbourhood:
        if heuristic(x_1) > heuristic(x):
            x = x_1
        else:
            continue
    return x

test = [[[1,1,1],[1,0,1]],[[0,0,1],[0,1,0]]]

print(heuristic(test[0][0]))

print(BestofNeighbourHood(test[0]))

print(VariableNeighbourHoodDescent(test))

    