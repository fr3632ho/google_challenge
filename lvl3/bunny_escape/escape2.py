import sys
from collections import deque
from copy import deepcopy

def get_neighbours(m, u, w, h):
    n = []
    y, x = u[0], u[1]

    if x > 0:
        if not m[y][x - 1] == 1:
            n.append((y, x - 1))

    if x < w - 1:
        if not m[y][x + 1] == 1:
            n.append((y, x + 1))

    if y > 0:
        if not m[y - 1][x] == 1:
            n.append((y - 1, x))

    if y < h - 1:
        if not m[y + 1][x] == 1:
            n.append((y + 1, x))

    return n

def get_shortest_path(map):
    source = (0, 0)
    w, h = len(map[0]), len(map)
    finish = (h - 1,w - 1)
    queue = deque([source])
    dist = {source: 1}

    while queue:

        u = queue.pop()

        if u[0] == finish[0] and u[1] == finish[1]:
            return dist[u]

        for n in get_neighbours(map, u, w, h):
            if n not in dist:
                dist[n] = dist[u] + 1
                queue.appendleft(n)

    return float('inf')

'''
Starting at index (0, 0) and want to end at index (w-1, h-1)
where w := len(m[0]) and h := len(m)

Used BFS instead of bellman ford as intended
'''
def solution(map):
    w, h = len(map[0]), len(map)
    ones = [(x,y) for x in range(w) for y in range(h) if map[y][x] == 1]
    current_min = float('inf')
    for x, y in ones:
        new_grid = deepcopy(map)

        new_grid[y][x] = 0
        current_min = min(current_min, get_shortest_path(new_grid))

    return current_min
