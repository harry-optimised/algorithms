# Subset Sum (or Knapsack)
# Input: A set of positive integers S1, S2, ..., SN and a target sum of integers K
# Output: A subset of S that adds up to K, or None if no such subset exists.
# Subproblem: Let M[n, k] be a boolean indicating whether there is a subset of S1, S2, ..., Sn that adds up to k.
# Solution: We seek M[N, K].
# Recurrence: M[n, k] = M[n-1, k] or M[n-1, k-Sn]
# Efficiency: O(nk) time.
# References:
#   - Algorithm Design Manual (Skiena) Section 10.5

import numpy as np

def subset_sum(S: list[int], K: int) -> list[int]:

    N = len(S)

    # Table will look like:

    #     0 1 2 3 4 5 ... k  
    #  {} T F F F F F ... F
    #  S1 T . . . . . ... .
    #  S2 T . . . . . ... .
    #  S3 T . . . . . ... .
    #  S4 T . . . . . ... .
    #  .. T . . . . . ... .
    #  Sn T . . . . . ... .
    
    M = np.zeros((N+1, K+1), dtype=bool)

    # This allows us to reconstruct the subset.
    traceback = np.zeros((N+1, K+1), dtype=int)

    # Boundary conditions 
    M[0, 0] = True  # (we can always make 0 with no elements)
    M[1:, 0] = True # (we can always make 0 by taking no elements)
    M[0, 1:] = False # (we can never make a positive number with no elements)

    # Recurrence
    for n in range(1, N+1):
        for k in range(1, K+1):

            M[n, k] = M[n-1, k]

            if k >= S[n-1] and M[n-1, k-S[n-1]]:

                M[n, k] = True
                traceback[n, k] = S[n-1]

    # Solution (traceback)
    if not M[N, K]:
        return None
    
    subset = []
    k = K
    for n in range(N, 0, -1):
        if traceback[n, k] > 0:
            subset.append(traceback[n, k])
            k -= traceback[n, k]

    return subset


def run():

    # Input
    S: list[int] = [1, 2, 4, 8]
    K: int = 11

    # Output
    subset = subset_sum(S, K)
    assert set(subset) == {1, 2, 8}

if __name__ == '__main__':
    run()