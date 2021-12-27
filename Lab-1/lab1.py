import sys

def markMazepath(maze, path):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
                if (i, j) in path:
                    maze[i][j] = '0'
    # print maze as a matrix
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            print(maze[i][j], end = "")
        print()

def BFS(maze, finalDestination_x, finalDestination_y):
    statesExplored = 0
    visited = [[False for i in range(len(maze[0]))] for j in range(len(maze))]
    # is free is to find whether the current position is space or not in maze
    is_free = [[True if maze[j][i] == " " else False for i in range(len(maze[0]))] for j in range(len(maze))]
    backtrack = [[False for i in range(len(maze[0]))] for j in range(len(maze))]
    is_free[finalDestination_x][finalDestination_y] = True

    queue = []
    queue.append((0, 0))
    visited[0][0] = True
    path = []

    while queue:
        current = queue.pop(0)
        if maze[current[0]][current[1]] == "*":
            break
        # find the nieghbors of the current node
        if current[0] + 1 < len(maze) and is_free[current[0] + 1][current[1]] and not visited[current[0] + 1][current[1]]:
            statesExplored += 1
            queue.append((current[0] + 1, current[1]))
            visited[current[0] + 1][current[1]] = True
            backtrack[current[0] + 1][current[1]] = (current[0], current[1])
        if current[0] - 1 >= 0 and is_free[current[0] - 1][current[1]] and not visited[current[0] - 1][current[1]]:
            statesExplored += 1
            queue.append((current[0] - 1, current[1]))
            visited[current[0] - 1][current[1]] = True
            backtrack[current[0] - 1][current[1]] = (current[0], current[1])
        if current[1] + 1 < len(maze[0]) and is_free[current[0]][current[1] + 1] and not visited[current[0]][current[1] + 1]:
            statesExplored += 1
            queue.append((current[0], current[1] + 1))
            visited[current[0]][current[1] + 1] = True
            backtrack[current[0]][current[1] + 1] = (current[0], current[1])
        if current[1] - 1 >= 0 and is_free[current[0]][current[1] - 1] and not visited[current[0]][current[1] - 1]:
            statesExplored += 1
            queue.append((current[0], current[1] - 1))
            visited[current[0]][current[1] - 1] = True
            backtrack[current[0]][current[1] - 1] = (current[0], current[1])
    # find the path using backtrack
    path.append((current[0], current[1]))
    while backtrack[current[0]][current[1]]:
        path.append(backtrack[current[0]][current[1]])
        current = backtrack[current[0]][current[1]] 
    path = path[::-1]
    print(statesExplored)
    print(len(path))
    markMazepath(maze, path)


def DFS(maze, finalDestination_x, finalDestination_y):
    statesexplored = 0
    visited = [[False for i in range(len(maze[0]))] for j in range(len(maze))]
    is_free = [[True if maze[j][i] == " " else False for i in range(len(maze[0]))] for j in range(len(maze))]
    backtrack = [[False for i in range(len(maze[0]))] for j in range(len(maze))]
    is_free[finalDestination_x][finalDestination_y] = True
    stack = []
    stack.append((0, 0))
    visited[0][0] = True
    path = []
    while stack:
        statesexplored += 1
        current = stack.pop()
        if maze[current[0]][current[1]] == "*":
            break
        if current[0] + 1 < len(maze) and is_free[current[0] + 1][current[1]] and not visited[current[0] + 1][current[1]]:
            stack.append((current[0] + 1, current[1]))
            visited[current[0] + 1][current[1]] = True
            backtrack[current[0] + 1][current[1]] = (current[0], current[1])
        if current[0] - 1 >= 0 and is_free[current[0] - 1][current[1]] and not visited[current[0] - 1][current[1]]:
            stack.append((current[0] - 1, current[1]))
            visited[current[0] - 1][current[1]] = True
            backtrack[current[0] - 1][current[1]] = (current[0], current[1])
        if current[1] + 1 < len(maze[0]) and is_free[current[0]][current[1] + 1] and not visited[current[0]][current[1] + 1]:
            stack.append((current[0], current[1] + 1))
            visited[current[0]][current[1] + 1] = True
            backtrack[current[0]][current[1] + 1] = (current[0], current[1])
        if current[1] - 1 >= 0 and is_free[current[0]][current[1] - 1] and not visited[current[0]][current[1] - 1]:
            stack.append((current[0], current[1] - 1))
            visited[current[0]][current[1] - 1] = True
            backtrack[current[0]][current[1] - 1] = (current[0], current[1])
    # find the path
    path.append((current[0], current[1]))
    while backtrack[current[0]][current[1]]:
        path.append(backtrack[current[0]][current[1]])
        current = backtrack[current[0]][current[1]]
    path = path[::-1]
    print(statesexplored)
    print(len(path))
    markMazepath(maze, path)



def DFID(maze, finalDestination_x, finalDestination_y):
    statesexplored = 0
    is_free = [[True if maze[j][i] == " " else False for i in range(len(maze[0]))] for j in range(len(maze))]
    backtrack = [[False for i in range(len(maze[0]))] for j in range(len(maze))]
    is_free[finalDestination_x][finalDestination_y] = True
    iteration = 0
    found = False
    depthLevel = [[ 0 for _ in range(len(maze[0]))] for _ in range(len(maze))]
    while not found:
        depthLevel = [[ 0 for _ in range(len(maze[0]))] for _ in range(len(maze))]
        visited = [[False for i in range(len(maze[0]))] for j in range(len(maze))]
        stack = []
        stack.append((0, 0))
        visited[0][0] = True
        path = []
        while stack:
            statesexplored += 1
            current = stack.pop()
            if maze[current[0]][current[1]] == "*":
                found = True
                break
            if depthLevel[current[0]][current[1]] >= iteration:
                continue
            if current[0] + 1 < len(maze) and is_free[current[0] + 1][current[1]] and not visited[current[0] + 1][current[1]]:
                stack.append((current[0] + 1, current[1]))
                visited[current[0] + 1][current[1]] = True
                backtrack[current[0] + 1][current[1]] = (current[0], current[1])
                depthLevel[current[0] + 1][current[1]] = depthLevel[current[0]][current[1]] + 1
            if current[0] - 1 >= 0 and is_free[current[0] - 1][current[1]] and not visited[current[0] - 1][current[1]]:
                stack.append((current[0] - 1, current[1]))
                visited[current[0] - 1][current[1]] = True
                backtrack[current[0] - 1][current[1]] = (current[0], current[1])
                depthLevel[current[0] - 1][current[1]] = depthLevel[current[0]][current[1]] + 1
            if current[1] + 1 < len(maze[0]) and is_free[current[0]][current[1] + 1] and not visited[current[0]][current[1] + 1]:
                stack.append((current[0], current[1] + 1))
                visited[current[0]][current[1] + 1] = True
                backtrack[current[0]][current[1] + 1] = (current[0], current[1])
                depthLevel[current[0]][current[1] + 1] = depthLevel[current[0]][current[1]] + 1
            if current[1] - 1 >= 0 and is_free[current[0]][current[1] - 1] and not visited[current[0]][current[1] - 1]:
                stack.append((current[0], current[1] - 1))
                visited[current[0]][current[1] - 1] = True
                backtrack[current[0]][current[1] - 1] = (current[0], current[1])
                depthLevel[current[0]][current[1] - 1] = depthLevel[current[0]][current[1]] + 1
        # find the path
        if found:
            path.append((current[0], current[1]))
            while backtrack[current[0]][current[1]]:
                path.append(backtrack[current[0]][current[1]])
                current = backtrack[current[0]][current[1]]
            path = path[::-1]
            print(statesexplored)
            print(len(path))
            markMazepath(maze, path)
            break
        iteration += 1





# Main
# read Input file from command line
finalDestination_x = 0
finalDestination_y = 0
t = sys.argv[1]
inputFile = open(t, 'r')
algorithm = int(inputFile.readline())
# make a 2-d list for the maze from input file
maze = []
for line in inputFile:
    # find final destination which is *
    if '*' in line:
        finalDestination_y = line.index('*')
        finalDestination_x = len(maze)
    maze.append(list(line.strip('\n')))
inputFile.close()

# if algorithm is 0 then BFS
if algorithm == 0:
    BFS(maze, finalDestination_x, finalDestination_y)
# if algorithm is 1 then DFS
elif algorithm == 1:
    DFS(maze, finalDestination_x, finalDestination_y)
# if algorithm is 2 then DFID
elif algorithm == 2:
    DFID(maze, finalDestination_x, finalDestination_y)
