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

INP = open("clauses.txt")

CNF = []
for line in INP:
    CNF.append(line.strip('\n').strip(']').strip('[').split(','))

def complement(x: int,n: int):
    ret = 0
    if x <= n:
        ret = n + x
    elif x>n:
        ret = x - N
    elif x<=0 or x>2*n:
        ret = 0
    return ret

N = int(CNF[-1][0])
K = int(CNF[-1][1])

def NeighbourHoodsGen(L: list,N: int):
    a = int(L[0])
    b = int(L[1])
    c = int(L[2])
    ret = []
    for i in range(3):
        if i==0:
            ret.append([a,b,complement(c,N)])
            ret.append([a,complement(b,N),c])
            ret.append([complement(a,N),b,c])
        if i==1:
            ret.append([complement(a,N),complement(b,N),c])
            ret.append([a,complement(b,N),complement(c,N)])
            ret.append([complement(a,N),b,complement(c,N)])
        if i==2:
            ret.append([complement(a,N),complement(b,N),complement(c,N)])
    
    return ret

