import numpy as np
from numpy.core.fromnumeric import shape 

# Implementation of simplex algorithm
#
#  maximize z = c'[x, 1]
#  subject to 
#         Ax <= b
#         x >= 0
#  return INF if unbounded, 'infeasible' if infeasible, 'optimal', z* and x* if feasible.

#
# B = {basic} , N = {Non-basic} 
# B + N = {x1, x2, ..., xn, xn+1,..., xn+m} 
# m: # of equality constraints
# n: # of variables
# 
#maximize c1 * N1 + ... + cn * Nn + cn+1 * 1
#----------------------------
#|       N1   N2 ...  Nn   1|
#|B1 =  a11  a12 ... a1n  b1|
#|B2 =  a21  a22 ... a2n  b2|
#|...                       |
#|Bm =  am1  am2 ... amn  bm|
#----------------------------
# 

# the last column of A is extended constance
# it assumes the constance is already an initial solution
def pivot (B: list, N: list, A: np.array, c: np.array) -> str:
    assert (np.min(A[:, -1]) >= 0)
    info = ""
    while True:
        col = -1
        for i in range(len(N)):
            # try to increment
            if c[i] > 0:
                col = i 
                break 
        if col == -1:
            # no more variable could be incremented
            info = "optimal"
            break
        # find the tightest constraint
        min_relax, index = 1e18, -1
        for i in range(len(B)):
            if A[i, col] < 0:
                relax = - A[i, -1] / A[i, col] 
                if relax < min_relax:
                    min_relax = relax
                    index = i 
        if index == -1:
            # unbouned
            info = "unbounded"
            break 
        else:
            row = index
        # print(row, col)
        # pivot move
        B[row], N[col] = N[col], B[row]
        k = - A[row, col]
        A[row, col] = -1
        tmp = A[row, :] / k
        # make substitution
        for i in range(len(B)):
            if i == row:
                A[i, :] = tmp 
            else:
                k = A[i, col]
                A[i, col] = 0
                A[i, :] += k * tmp
        
        # substitution for c
        k = c[col]
        c[col] = 0
        c += k * tmp

    return info

# 
# introduce slack variable x0, solve the slack version to check if original inequalities make a non-empty set
def find_basic(B: list, N: list, A: np.array, c: np.array) -> tuple([str, list, list, np.array]):
    b_min = np.min(A[:, -1])
    n_min = np.argmin(A[:, -1])

    if b_min < 0:
        tmp = -A[n_min, :]
        tmp[0] = 1
        for i in range(len(B)):
            if i == n_min:
                A[i, :] = tmp 
            else: 
                k = A[i, 0]
                A[i, 0] = 0
                A[i, :] += k * tmp
        B[n_min], N[0] = N[0], B[n_min]
        c = - tmp
    # ready for pivot 
    info = pivot(B, N, A, c)
    # print(B)
    # print(N)
    # print(A)
    # print(c)
    # print("--------")
    if np.abs(c[-1]) > 1e-12:
        return "infeasible", None, None, None
    elif info == "unbounded":
        return "unbounded", None, None, None
    else:
        # find the position of 0
        pos = -1
        for i in range(len(N)):
            if N[i] == 0:
                pos = i 
                break
        assert pos != -1, "x0 is in basic variables!"
        # replace x0 with 0 and eliminate the columns
        A[:, pos:-1] = A[:, pos+1:]
        A = A[:, :-1]
        N[pos: -1] = N[pos + 1:]
        N = N[:-1]
        return info, B, N, A
    

def simplex (c: np.array, A: np.array, b: np.array):
    # -> tuple([str, float, np.array])
    # Step 1: introduce slack variable x0 as well as test for feasibility
    n_const, n_var = np.shape(A)
    assert c.shape[0] == n_var + 1, "the last term of c is constance! please fill with 0"

    N = [i for i in range(n_var + 1)]
    B = [i for i in range(n_var + 1, n_var + n_const + 1)]

    # x0, x1, ..., xn, b in columns
    piv_A = np.zeros((n_const, n_var + 2))  
    piv_A[:, 0] = 1
    piv_A[:, 1:-1] = -A
    piv_A[:, -1] = b 

    piv_c = np.zeros((n_var + 2, 1))
    piv_c[0,0] = -1

    info, B, N, A = find_basic(B, N, piv_A, piv_c)
    # print(B)
    # print(N)
    # print(A)
    # print(info)
    # print("------")
    if info != "optimal":
        return info, None, None
    else:
        # make a new target function
        # if orgininal variable is in basic variables, replace with right-hand side in c
        # otherwise, add them without change
        new_c = np.zeros_like(c, dtype='float64')
        for idx, val in enumerate(B):
            if val <= n_var:
                new_c += c[val-1] * A[idx, :]
        for idx, val in enumerate(N):
            if val <= n_var:
                new_c[idx] += c[idx]
        # don't forget the constance
        new_c[-1] += c[-1]      

        info = pivot(B, N, A, new_c)
        if info != "optimal":
            return info, None, None
        else:
            # collect the results by assuming non-basic variables all zero
            result = [ i for i in range(n_var + n_const)]
            for x in N:
                result[x-1] = 0

            for idx, x in enumerate(B):
                result[x-1] = A[idx, -1]
            x = np.array(result[:n_var])
            val = new_c[-1]

            #return only the original variables
            return info, val, x

if __name__ == '__main__':
    A = np.array([ [1, 1, 3], [2, 2, 5], [4, 1, 2]])
    b = np.array([30, 24, 36])
    c = np.array([3, 1, 2, 0])

    # A = np.array([[2, -1], [1, -5]])
    # b = np.array([2, -4])
    # c = np.array([2, -1, 0])

    # A = np.array([[1, -1], [-1, -1], [-1, 4] ])
    # b = np.array([8, -3 ,2])
    # c = np.array([1, 3, 0])

    # A = np.array([[1, 2], [-2, -6], [0, 1] ])
    # b = np.array([4, -12 ,1])
    # c = np.array([1, -2, 0])

    # A = np.array([[-1, 1], [-1, -1], [-1, 4] ])
    # b = np.array([-1, -3 ,2])
    # c = np.array([1, 3, 0])

    info, val, x = simplex(c, A, b)
    print(info)
    print(val, x)
