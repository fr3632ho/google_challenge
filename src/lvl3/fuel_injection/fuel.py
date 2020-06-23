from math import log, ceil, floor, sqrt



'''
Done using bitshifting, check for number of ones in bit representation of the number.
If the number of ones would decrease in the bitrepresentation wether we add or subtract,
then we choose that operation.
'''
def solution(n):
    _n = long(n)

    # Base case
    if _n == 0:
        return 1

    p = _n
    count = 0
    while p != 1:
        # If p is odd
        if p & 1:
            # Check for number of ones in binary representation
            p1, p2 = p + long(1), p - long(1)
            b1, b2 = bin(p1).count('1'), bin(p2).count('1')
            if b1 <= b2 and p != long(3):
                p = p + long(1)
            else:
                p = p - long(1)
            count += 1

        count += 1
        # Divide by bitshifting by one
        p = p >> 1
    return count

# TESTS

# Ans := 2
print solution('4')

# Ans := 2
print solution('3')

# Ans := 5
print solution('15')

# Ans := 6
print solution('33')
#
# Ans := 25
print solution('33554432')

# Ans := 26
print solution('33554433')

# Ans := 65
print solution('36893488147419103232')

# Ans := 66
print solution('36893488147419103233')
#
# Ans := 128
print solution('340282366920938463463374607431768211456')

# Ans := 129
print solution('340282366920938463463374607431768211457')

# Ans := 300
print solution('2037035976334486086268445688409378161051468393665936250636140449354381299763336706183397376')
#
# END
