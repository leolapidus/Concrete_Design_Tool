import numpy as np
import hyperjet as hj

b = hj.HyperJet(1, [1])

m = np.zeros((2))

print(m)
print(b)

m[0] = b

print(m)
print(b)
