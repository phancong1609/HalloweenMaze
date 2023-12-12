import random
import heapq
from collections import deque
        
def isEscaped(maze, x, y):
    if maze[x-1][y]=="S" or maze[x+1][y]=="S" or maze[x][y-1]=="S" or maze[x][y+1]=="S":
        return True
    return False

def isDead(princess, ghost):
    for g in ghost:
        if princess==g:
            return True
    return False

def isEligibleMove(maze, x, y, new_x, new_y): 
    if new_x < 1 or new_x >= len(maze)-1 or new_y < 1 or new_y >= len(maze)-1:
        return False 
    elif x + 2 == new_x:
        if maze[x+1][y] == "%":
            return False
    elif x - 2 == new_x:
        if maze[x-1][y] == "%":
            return False
    elif y + 2 == new_y:
        if maze[x][y+1] == "%":
            return False
    elif y - 2 == new_y:
        if maze[x][y-1] == "%":
            return False
    return True

def possibleMoves(maze, princess):
    moves = []
    x, y = princess[0], princess[1]
    if isEligibleMove(maze, x, y, x+2, y):
        moves.append((x+2 ,y))
    if isEligibleMove(maze, x, y, x-2, y):
        moves.append((x-2 ,y))
    if isEligibleMove(maze, x, y, x, y+2):
        moves.append((x ,y+2))
    if isEligibleMove(maze, x, y, x, y-2):
        moves.append((x ,y-2))
    if (len(moves)<4):
        moves.append((x,y))
    random.shuffle(moves)
    return moves

def nextGhostMove(maze, princess, ghost):
    if ghost==princess:
        return ghost
    if princess[1]!=ghost[1]:
        if isEligibleMove(maze, ghost[0], ghost[1], ghost[0], ghost[1]+sign(princess[1], ghost[1])*2):
            return (ghost[0], ghost[1] + sign(princess[1], ghost[1]) * 2)
    if isEligibleMove(maze, ghost[0], ghost[1], ghost[0]+sign(princess[0], ghost[0])*2, ghost[1]):
        return (ghost[0] + sign(princess[0], ghost[0]) * 2, ghost[1])
    return ghost
        
def sign(princess, ghost):
    if princess==ghost:
        return 0
    if princess<ghost:
        return -1
    return 1

def BFS(maze, princess, ghost):
    queue = deque([(princess, ghost, [])])
    visited = []
    visualize_node = [princess]
    while queue:
        pr, gh, path = queue.popleft()
        visited.append([pr, gh])
        # if pr not in visualize_node:
        #     visualize_node.append(pr)
        if isEscaped(maze, pr[0], pr[1]):
            return path, visualize_node, len(visited)
        for move in possibleMoves(maze, pr):
            if move not in visualize_node:
                visualize_node.append(move)
            new_gh=[]
            for g in gh:
                g=nextGhostMove(maze, move, g)
                g=nextGhostMove(maze, move, g)
                new_gh.append(g)
            queue_list = [[t[0], t[1]] for t in queue]
            if not isDead(move, list(new_gh)) and [move, new_gh] not in visited+queue_list:
                queue.append((move, new_gh, path + [move]))
    return None
def DFS(maze, princess, ghost):
    stack = [(princess, ghost, [])]
    visited = []
    visualize_node = [princess]
    while stack:
        pr, gh, path = stack.pop()
        visited.append([pr, gh])
        # if pr not in visualize_node:
        #     visualize_node.append(pr)
        if isEscaped(maze, pr[0], pr[1]):
            return path, visualize_node, len(visited)
        for move in possibleMoves(maze, pr):
            if move not in visualize_node:
                visualize_node.append(move)
            new_gh=[]
            for g in gh:
                g=nextGhostMove(maze, move, g)
                g=nextGhostMove(maze, move, g)
                new_gh.append(g)
            stack_list = [[t[0], t[1]] for t in stack]
            if not isDead(move, list(new_gh)) and [move, new_gh] not in visited+stack_list:
                stack.append((move, new_gh, path + [move]))
    return None
def h(maze, princess, gate):
    h_value=abs(princess[0]-gate[0])+abs(princess[1]-gate[1])
    return h_value
def Greedy(maze, princess, ghost, gate):
    stack = [(princess, ghost, [])]
    visited = []
    visualize_node = [princess]
    while stack:
        pr, gh, path = stack.pop()
        visited.append([pr, gh])
        if isEscaped(maze, pr[0], pr[1]):
            return path, visualize_node, len(visited)
        next_move=[]
        for move in possibleMoves(maze, pr):
            if move not in visualize_node:
                visualize_node.append(move)
            new_gh=[]
            for g in gh:
                g=nextGhostMove(maze, move, g)
                g=nextGhostMove(maze, move, g)
                new_gh.append(g)
            stack_list = [[t[0], t[1]] for t in stack]
            if not isDead(move, list(new_gh)) and [move, new_gh] not in visited+stack_list:
                next_move.append((move, new_gh, path + [move], h(maze, move, gate)))
        next_move.sort(key=lambda x: x[3], reverse= True)
        for move in next_move:
            stack.append((move[0],move[1],move[2]))
    return None


def UCS(maze, princess, ghost):
    queue = [(0, princess, ghost, [])]
    v = []
    visualize_node = [princess]
    while queue:
        queue = sorted(queue, key=lambda x: x[0])  
        cost, pr, gh, path = queue.pop(0)  
        v.append([pr, gh])
        if isEscaped(maze, pr[0], pr[1]):
            return path, visualize_node, len(v)
        for move in possibleMoves(maze, pr):
            if move not in visualize_node:
                visualize_node.append(move)
            new_gh = []
            for g in gh:
                g = nextGhostMove(maze, move, g)
                g = nextGhostMove(maze, move, g)
                new_gh.append(g)
            subqueue = [[t[1], t[2]] for t in queue]
            if not isDead(move, list(new_gh)) and not [move, new_gh] in v + subqueue:
                queue.append((cost + 1, move, new_gh, path + [move]))
    return None

def IDS(maze, princess, ghost):
    stack = [(princess, ghost, 0, [])]
    visited = []
    visualize_node = [princess]
    max_depth = 63 
    while stack:
        pr, gh, curdepth, path = stack.pop()
        if (curdepth>max_depth):
            continue
        visited.append([pr, gh])
        if isEscaped(maze, pr[0], pr[1]):
            return path, visualize_node, len(visited)
        for move in possibleMoves(maze, pr):
            if move not in visualize_node:
                visualize_node.append(move)
            new_gh=[]
            for g in gh:
                g=nextGhostMove(maze, move, g)
                g=nextGhostMove(maze, move, g)
                new_gh.append(g)
            stack_list = [[t[0], t[1]] for t in stack]
            if not isDead(move, list(new_gh)) and [move, new_gh] not in visited+stack_list:
                stack.append((move, new_gh, curdepth + 1, path + [move]))


def A_star(maze, princess, ghost, gate):
    v = []
    visualize_node = [princess]
    queue = [(0, 0, princess, ghost, [])]  
    while queue:
        f, cost, pr, gh, path = queue.pop(0)
        v.append([pr, gh])
        if isEscaped(maze, pr[0], pr[1]):
            return path, visualize_node, len(v)
        next_move=[]
        for move in possibleMoves(maze, pr):
            if move not in visualize_node:
                visualize_node.append(move)
            new_gh=[]
            for g in gh:
                g=nextGhostMove(maze, move, g)
                g=nextGhostMove(maze, move, g)
                new_gh.append(g)
            cost += 1
            f = (cost + h(maze, move, gate))
            subqueue = [[t[2], t[3]] for t in queue]
            if not isDead(move, list(new_gh)) and not [move, new_gh] in v+subqueue:
                next_move.append((f, cost, move, new_gh, path + [move]))
        next_move.sort(key=lambda x: x[0])
        for move in next_move:
            queue.append((move))