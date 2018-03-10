import numpy as np

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

# Tranpose an array/matrix
array_transpose = np.transpose(array_2D)
print(array_2D.shape)
print(array_transpose.shape)
print(array_2D.T)

# Reshape array into any shape as long as the total number of elements remains
# the same
array_reshape = np.reshape(array_2D, (10, 1))
print(array_2D)
print(array_reshape)

# Normal operations in same dimensions
array_normal_1 = np.array([[1, 2, 3], [4, 5, 6]])
array_normal_2 = np.array([[7, 8, 9], [10, 11, 12]])
print(array_normal_1 + array_normal_2)
print(array_normal_1 - array_normal_2)
print(array_normal_1 * array_normal_2)
print(array_normal_1 / array_normal_2)

# Can also do
print(np.add(array_normal_1, array_normal_2))
print(np.subtract(array_normal_1, array_normal_2))
print(np.multiply(array_normal_1, array_normal_2))
print(np.divide(array_normal_1, array_normal_2))

# Broadcasting is a way in which you can add matrices or arrays of different
# dimensions
# For the example below, adding 1D array and 2D array
# It basically add 1D array to each row of 2D array
# The rule of thumb is that the arrays need to be able to allign along at least
# 1 dimension.
print(array_1D)
print(array_2D)
print(array_1D + array_2D)

# Dot product
array_dot_1 = np.array([[1, 2, 3], [4, 5, 6]])
array_dot_2 = np.array([[7, 8], [9, 10], [11, 12]])
print(array_dot_1)
print(array_dot_2)
print(np.dot(array_dot_1, array_dot_2))

# Sum of all element in a row
print(array_1D)
print(np.sum(array_1D, axis=0))

# Stack array together in order
# Verically
array_vstack_1 = np.array([1, 2, 3, 4, 5])
array_vstack_2 = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])

print(array_vstack_1)
print(array_vstack_2)

# Stack array 1 on top of 2
print(np.vstack((array_vstack_1, array_vstack_2)))
# Stack array 2 on top of 1
print(np.vstack((array_vstack_2, array_vstack_1)))

# Horizontally
array_hstack_1 = np.array([[1, 2], [3, 4]])
array_hstack_2 = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])

print(array_hstack_1)
print(array_hstack_2)

# Stack array 1 on the left, the array 2
print(np.hstack((array_hstack_1, array_hstack_2)))

# Stack array 2 on the left, the array 1
print(np.hstack((array_hstack_2, array_hstack_1)))
