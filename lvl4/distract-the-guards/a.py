# b <= 2^30-1
from fractions import Fraction
from collections import defaultdict

mem = set()
def to_fraction(a, b):
    if a > b:
        a, b = b, a
    frac = Fraction(a, b)
    return frac.numerator, frac.denominator

def loops(a ,b):
    n, m = to_fraction(a, b)
    return bool(pow(2, m, n+m)) # If zero, does not loop

def remove(guards, ref):
    for i in range(len(guards)):
        j = 0
        while j < len(guards[i]):
            if(guards[i][j]==ref):
                guards[i].pop(j)
            j+=1
    guards[ref]= [-1]

def solution(banana_list):
    n = len(banana_list)
    G = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if loops(banana_list[i], banana_list[j]):
                G[i].append(j)
                G[j].append(i)
    bad = 0
    to_process=len(banana_list)
    while(to_process>0):

        min_num=0
        for i in range(len(G)):
            if(i!=0 and (len(G[i])<len(G[min_num]) or G[min_num] == [-1]) and G[i]!=[-1]):
                min_num=i

        if((len(G[min_num])) == 0 or (len(G[min_num])==1 and G[min_num][0] == G[min_num]) and G[min_num] != [-1]):
            remove(G, min_num)
            to_process-=1
            bad+=1
        else:
            min_node=G[min_num][0]
            for i in range(len(G[min_num])):
                if(i!=0 and G[min_num][i]!=min_num and len(G[G[min_num][i]])<len(G[min_node])):
                    min_node=G[min_num][i]
            if(G[min_node]!=[-1]):
                remove(G, min_num)
                remove(G, min_node)
                to_process-=2
    return bad



# TESTS
# print cycle(1, 1)
# print cycle(1, 4)
# print cycle(4, 1)
# print cycle(1, 21)
print solution([1,1]) # out => 2
print solution([1, 7, 3, 21, 13, 19]) # out => 0
print solution([1, 2, 1, 7, 3, 21, 13, 19]) # out => 0
