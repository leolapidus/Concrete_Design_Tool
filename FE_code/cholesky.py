from math import sqrt
import numpy as np

def _cholesky(A):
    n = len(A)

    L = np.zeros((n, n), dtype=object)

    for i in range(n):
        for k in range(i + 1):
            tmp_sum = sum(L[i, j] * L[k, j] for j in range(k))
            
            if i == k:
                L[i, k] = np.sqrt(A[i, i] - tmp_sum)
            else:
                L[i, k] = 1.0 / L[k, k] * (A[i, k] - tmp_sum)
    return L

def _foreward(L, b):
    n = b.size
    y = np.zeros(n, dtype=object)
    y[0] = b[0] / L[0,0]
    for i in range(1, n):
        s = 0.0
        for j in range(i):
            s = s + L[i, j] * y[j]
        y[i] = (b[i] - s) / L[i,i]
    return y

def _backward(R, y):
    n = y.size
    x = np.zeros(n, dtype=object)
    x[-1] = y[-1] / R[-1,-1]
    for i in range(n-2, -1, -1):
        s = 0.0
        for j in range(i+1, n):
            s = s + R[i, j] * x[j]
        x[i] = (y[i] - s) / R[i,i]
    return x

def solve(A, b):
    L = _cholesky(A)
    y = _foreward(L, b)
    x = _backward(L.T, y)
    return x
