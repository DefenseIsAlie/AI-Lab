import sys
import random

OUTPUT = open("clauses.txt","w")

N = int(sys.argv[1])
K = int(sys.argv[2])

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

    OUTPUT.write(f"{N},{K}")

clausePrinter(N,K)




OUTPUT.close()