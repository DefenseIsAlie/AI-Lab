import os

c = []

for i in range (1,10):
    c.append(i/10)
    c.append(i/100)

for i in range(10, 100, 10):
    c.append(i)

for i in range(100,500,100):
    c.append(i)

for i in range(2):
    for case in c:
        os.system(f"python 21.py {case}")


