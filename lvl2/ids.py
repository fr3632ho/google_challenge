import sys

def solution(x, y):
    return [(n*(n-1)/2 +1) for n in range(2*max(x, y))][x+y-1]+x-1

print solution(3,2)
print solution(2,3)
print solution(5,10)
