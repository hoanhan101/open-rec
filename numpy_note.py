import numpy as np
import scipy

# 1D array
array_1D = np.array([1, 2, 3, 4, 5])
print(array_1D)

# 2D array
array_2D = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])
print(array_2D)

# Get a tuple with number of row and column
print(array_1D.shape)
print(array_2D.shape)

# Access array by index
print(array_2D[1, 2])

# Access [1, 2] and [0, 1] at the same time
print(array_2D[[1, 0], [2, 1]])

# Return an array with the same size and shape but each element will be a
# boolean which says whether the corresponding element of the original array
# satisfies the condition
print(array_2D > 5)
print(array_2D[array_2D > 5])

# Create an array with specified row and column, filled with 0
# dtype is optional, default is float64
array_zeros = np.zeros((5, 2), dtype='int64')
print(array_zeros)

# Create an array filled with 1
array_ones = np.ones((5, 2))
print(array_ones)

# Create an array of size 5, filled with 2
array_full = np.full(5, 2)
print(array_full)

# Create a 2x2 array with random value from 0 to 1
array_random = np.random.random((2, 2))
print(array_random)

# Create a 2x2 indentity matrix
identity_matrix = np.eye(2)
print(identity_matrix)
