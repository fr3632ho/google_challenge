import sys
from collections import deque

def get_slope(dx, dy):
    '''
    Calculate the slope between two points
    '''
    if dx == dy == 0:
        return 0
    tx, ty = abs(dx), abs(dy)
    while ty:
        tx, ty = ty, tx % ty
    return (dx // tx, dy // tx)

def get_distance(p1, p2):
    '''
    Squared distance between two given points
    '''
    return pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2)

def solution(dimensions, captain, guard, distance):


    if captain == guard:
        return 0

    def get_reflections(p): # (2n +- a, 2m +- b)
        '''
        Make sure to only add reflections that are outside of dimensions
        '''
        return [(p[0], 2*dimensions[1] - p[1]), (p[0], -p[1]),
                (-p[0], p[1]), (2*dimensions[0] - p[0], p[1])]


    distance = pow(distance, 2)
    def get_all_reflections(point):
        targets = set([(point[0], point[1])])
        queue = deque([point])
        while True:
            new_targets = set([])
            while queue:
                p = queue.pop()
                reflections = [ref for ref in get_reflections(p)
                               if (get_distance(captain, ref) <= distance)]

                # Union new_targets with new reflections
                new_targets |= set(reflections) - targets

            # No more reflections
            if not new_targets:
                break

            # Append to queue
            for i in new_targets:
                queue.appendleft(i)
                targets.add(i)

        return targets

    # Get the two sets of reflections
    friendlies = get_all_reflections(captain)
    targets = get_all_reflections(guard)


    # With the slope function, assign each slope a distance value
    c_x, c_y = captain
    slope_values = {}
    for x, y in friendlies: # Setup inital slope values with friendlies
        dx, dy = c_x - x, c_y - y
        slope = get_slope(dx, dy)
        dist = get_distance(captain, (x, y))
        if dist <= slope_values.get(slope, distance):
            slope_values[slope] = dist

    answer = set()
    for x, y in targets:
        dx, dy = c_x - x, c_y - y
        slope = get_slope(dx, dy)
        dist = get_distance(captain, (x, y))
        if dist <= slope_values.get(slope, distance):
            answer.add(slope)

    return len(answer)


### TEST CASES
print(solution([3,2], [1,1], [2,1], 4)) # Output := 7

print(solution([300,275], [150,150], [185,100], 500)) # Output := 9
