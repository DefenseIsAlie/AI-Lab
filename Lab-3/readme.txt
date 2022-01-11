# How to run the script:

python 21.py 

# Generation of random cnf file:

cnf circuit formula with n = 4 variables and k = 10 clauses written to file clauses.txt

1 to n variables are normal variables
n+1 to 2n variables are negated variables

each line of the file contains a clause
each clause is a list of variables

# Program selection:

1 for Beam search
2 for Variable neighbourhood descent 
3 for Tabu search
4 for exit

for each program:
    solution is printed(if satisifable)
    time taken is printed

