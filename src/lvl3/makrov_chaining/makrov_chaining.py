from fractions import gcd, Fraction

'''
Subtracts matrix A with B
'''
def sub(A, B):
    row_a, col_b = len(A), len(B[0])
    # Check fo correct dimensions
    if row_a != len(B) or len(A[0]) != col_b:
        raise Exception("Wrong dimension for subtraction")

    return [[A[i][j] - B[i][j] for j in range(col_b)] for i in range(row_a)]

'''
Returns an identity matrix of dimension dim
'''
def identity(dim):
    return [[1 if i==j else 0 for i in range(dim)] for j in range(dim)]

'''
Matrix multiplication (A * B)
'''
def mul(A, B):
    # Check for correct dimensions
    if len(A[0]) != len(B):
        return -1

    rows, cols, iter = len(A), len(B[0]), len(A[0])
    return [
        [sum([A[r][i]*B[i][c] for i in range(iter)])
                              for c in range(cols)]
                              for r in range(rows)]

'''
Transpose of matrix m
'''
def transpose(m):
    return map(list,zip(*m))

'''
Get minor matrices
'''
def minor(m, i, j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

'''
Calculate the determinant of a nxn matrix
'''
def determinant(m):
    # if dimension is 2x2
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    det = 0
    for col in range(len(m)):
        det += ((-1)**col) * m[0][col] * determinant(minor(m, 0, col))

    return det

'''
Inverts a matrix of fractions
'''
def inv(m):
    det = determinant(m)
    if det == 0:
        raise Exception("Cannot get inverse of matrix with zero determinant")

    N = len(m)
    # 2x2 matrix
    if N == 2:
        return [[m[1][1]/det, (-1)*m[0][1]/det ], [(-1)*m[1][0]/det, m[0][0]/det]]

    cofactor = [
        [((-1)**(r+c))*determinant(minor(m,r,c)) for c in range(N)]
                                                 for r in range(N)]

    # Calculate the adjugate matrix with transpose and divide by determinat
    return [[c / det for c in r] for r in transpose(cofactor)]

'''
Short version of converting matrix of ints into matrix represented with fractions
'''
def into_fractions(m):
    return [r if sum(r) == 0 else [Fraction(c, sum(r)) for c in r] for r in m]

'''
Count terminal states
'''
def transient_count(m):
    return len(m) - len([ i for i in range(len(m)) if sum(m[i]) == 0])

'''
Create Q & R matrices by decomposing the transition matrix
'''
def create_QR(matrix, t):
    return [row[:t] for row in matrix[:t]], [row[t:] for row in matrix[:t]]

'''
Swap column i & j
'''
def swap(arr, i, j):
    rows, cols = len(arr), len(arr[0])
    temp = []
    for r1 in range(rows):
        temp.append(arr[r1][j])
        arr[r1][j] = arr[r1][i]

    for r2 in range(rows):
        arr[r2][i] = temp[r2]

'''
sort transition matrix
'''
def sort(m):
    non_empty, n = [], []
    empty = []
    for num,i in enumerate(m):
        if sum(i) == 0:
            empty.append(i)
        else:
            n.append(i)
            non_empty.append((num,i))

    # Swap columns in the non-empty list
    counter = 0
    for num,row in non_empty:
        if counter != num:
            z = num
            while z != counter:
                swap(n, z-1, z)
                z -= 1

        counter += 1

    return n + empty

'''
compute least common multiple (LCM) for the denominators
'''
def compute_lcm(arr):
    d_arr = [f.denominator for f in arr]
    lcm = d_arr[0]
    for i in d_arr[1:]:
        lcm = (lcm*i)/gcd(lcm,i)
    return lcm

'''
Alter from fractions to ints with LCM last
'''
def format_result(state):
    lcm = compute_lcm(state)
    res = [i[0] * (lcm/i[1]) if i[1] < lcm else i[0] for i in [(f.numerator, f.denominator) for f in state]]
    res.append(lcm)
    return res

def solution(m):
    # if ore zero is terminal
    transient = transient_count(m)
    if sum(m[0]) == 0: # Base case: s0 is terminal
        terminals = [0 for i in range(len(m) - transient - 1)]
        res = [1] + terminals + [1]
        return res
    # Construct fraction matrix from transition matrix
    matrix = into_fractions(sort(m))

    # Get Q & R matrices
    Q, R = create_QR(matrix, transient)

    # Calculate F = (I - Q)^(-1)
    F = inv(sub(identity(transient), Q))

    # Calculate B = F*R
    b = mul(F, R)
    # Take state 0
    return format_result(b[0])

# [7, 6, 8, 21] is the expected solution
print solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])

# [0, 3, 2, 9, 14] is the expected solution
print solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
