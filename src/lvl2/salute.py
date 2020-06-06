import sys

def solution(s):
    count = 0
    handshakes = 0

    for char in s:
        if char == '>':
            count += 1
        elif char == '<':
            if count != 0:
                handshakes += 2*count
    return handshakes

print(solution("<<>><"))
print(solution(">----<"))
