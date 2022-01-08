INP = open("clauses.txt")

CNF = []
for line in INP:
    CNF.append(line.strip('\n').strip(']').strip('[').split(','))

