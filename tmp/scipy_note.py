import numpy as np
import scipy

from scipy.spatial.distance import correlation, cosine, pdist, squareform

# Correlation
array_1 = np.array([0, 1, 0])
array_2 = np.array([1, 0, 0])

print(array_1)
print(array_2)

print(correlation(array_1, array_2))

array_3 = np.vstack((array_1, array_2))

print(array_3)

# Cimpute the pairwise distance between all rows
print(pdist(array_3, metric='euclidean'))

# A square matrix with d[i, i] being the Euclidean distance between
# array_3[i, :] and array_3[j, :]
print(squareform(pdist(array_3, metric='euclidean')))
