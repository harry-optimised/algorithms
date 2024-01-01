# Integer Partition
# Input: An arrangement S of non-negative numbers s1, s2, s3, ..., sN and a positive integer K.
# Output: Partition S into K or fewer ranges to minimize the maximum sum over all ranges.
# Subproblem: M[n, k] = minimum possible cost over all partitionings of s1, s2, ..., Sn into k ranges, 
#             where the cost of a partition is the maximum sum over all ranges in that partition.
# Solution: We seek M[N, K].
# Intuition: Whenever we place a range boundary, assuming it's the furthest right boundary, then the new minimum
#            cost is the maximum of either the newly created range (to the right of the boundary) or the cost of
#            the set of ranges to the left of the boundary (which is the subproblem M[i, k-1]).
# Recurrence: M[n, k] = min(max(M[i, k-1], sum(S[i+1:n]))) for all i in [0, n-1]
# Efficiency: O(KN^3) time. (O(N^2) for the recurrence, O(K) for the outer loop, O(N) for the inner loop.
# References:
#   - Algorithm Design Manual (Skiena) Section 10.7


import numpy as np

def integer_partition(S: list[int], K: int) -> list[list[int]]:

    N = len(S)
    S = [0] + S # Pad with a zero to make the indices line up. Means we can index from 1.

    M = np.zeros((N+1, K+1), dtype=int)
    dividers = np.zeros((N+1, K+1), dtype=int)

    # Boundary conditions
    M[1, :] = S[1]  # With only one element, the partition is just that element.
    M[:, 1] = np.cumsum(S) # With only one range, the partition is the cumulative sum of the elements. 

    # Populate first row and column with the actual values of S and K, this is for debugging,
    # these values are never used because we index from 1.
    M[:, 0] = S
    M[0, :] = range(0, K+1) 
    dividers[:, 0] = S
    dividers[0, :] = range(0, K+1)

    # Table will look like...
    # First column (with the ?) is cumulative sum of S.
    # M|____K____
    # 1| 1  1  1
    # 2| ?  .  .
    # 3| ?  .  .
    # .| .  .  .
    # N| ?  .  .

    # Evaluation order, left to right, top to bottom:
    # M|____K____
    # 1| 1  1  1
    # 2| ?  -> ->
    # 3| ?  -> ->
    # .| .  -> ->
    # N| ?  -> ->

    # Recurrence
    for n in range(2, N+1):
        for k in range(2, K+1):

            # We want to find the minimum cost of partitioning s1, s2, ..., Sn into k ranges.
            # We can do this by considering all possible locations of the last range boundary.
            # We know that the last range boundary must be at or to the left of n.
            # So we can consider all possible locations i for the last range boundary, and take the minimum.
            # For each i, we can consider the cost of the ranges to the left of i (which is M[i, k-1])
            # and the cost of the range to the right of i (which is the sum of S[i+1:n]).
            # The cost of the partition is the maximum of these two values.
            # We take the minimum of all of these costs.

            costs = []
            for i in range(1, n+1):
                cost = max(M[i, k-1], np.sum(S[i+1:n+1]))
                costs.append(cost)

            M[n, k] = min(costs)
            dividers[n, k] = np.argmin(costs) + 1

    # Solution (traceback)
    partition = []
    n = N
    k = K
    while k > 0:
        i = dividers[n, k]
        partition.append(S[i+1:n+1])
        n = i
        k -= 1
    
    return partition

def run():

    # Input
    S = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    K = 3

    # # Output
    partition = integer_partition(S, K)
    partition = {tuple(p) for p in partition}
    assert partition == {(1, 1, 1), (1, 1, 1), (1, 1, 1)}
    

    # Input
    S = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    K = 3

    # Output
    partition = integer_partition(S, K)
    partition = {tuple(p) for p in partition}
    assert partition == {(1, 2, 3, 4, 5), (6, 7), (8, 9)}

if __name__ == '__main__':
    run()