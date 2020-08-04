from copy import deepcopy
from collections import deque

def get_edges(w, h):
    edge_list = []

    # Construct edge list
    for i in range(w*h):
        if i - w > 0:
            edge_list.append((i, i - w))

        if i + w < w*h:
            edge_list.append((i, i + w))

        if i%w - 1 >= 0:
            edge_list.append((i, i - 1))

        if i%w + 1 < w:
            edge_list.append((i, i +  1))

    return edge_list

def bellman_ford(G, edges, w, h, source):
    target = w*h-1
    predecessor = [None for _ in range(target + 1)]
    distance = [float('inf') for _ in range(target + 1)]
    distance[source] = 1 # first is weight and second is saldo

    for i in range(target):
        for u, v in edges:
            if distance[u] + 1 < distance[v] and not G[v]:
                distance[v] = distance[u] + 1
                predecessor[v] = u

    return distance[target]

'''
Starting at index (0, 0) and want to end at index (w-1, h-1)
where w := len(m[0]) and h := len(m)

End node on flatmap := w*h - 1
'''
def solution(map):
    # width and height
    w, h = len(map[0]), len(map)
    # Flattened labyrinth
    m_flat = [val for sublist in map for val in sublist]
    ones = [i for i in range(w*h) if m_flat[i] == 1]

    cur_min = float('inf')
    for i in ones:
        new_grid = deepcopy(m_flat)
        new_grid[i] = 0

        edge_list = get_edges(w, h)
        cur_min = min(cur_min, bellman_ford(new_grid, edge_list, w, h, 0))

    return cur_min
