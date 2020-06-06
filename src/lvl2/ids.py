import sys

def solution(x, y):
    N = max(x,y)
    x_list = [ (n*(n+1)/2) for n in range(2*N)]
    y_list = [ (n*(n-1)/2 +1) for n in range(2*N)]

    indx = x+y-1

    return y_list[indx]+x-1


solution(3,2)
solution(2,3)
solution(5,10)
