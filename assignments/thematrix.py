#### creating a matrix in Python and multiplying matrices #####

import numpy as np


### easy way to create and invert matrices ####
"""
A = np.mat("0,1,4;2,6,7;0,4,5")
print("Matrix A: \n", A)

inverseA = np.linalg.inv(A)
print("inverse of Matrix A: \n", inverseA)
"""



###### example code from stackoverflow ####
"""
A = matrix( [[1,2,3],[11,12,13],[21,22,23]]) # Creates a matrix.
x = matrix( [[1],[2],[3]] )                  # Creates a matrix (like a column vector).
y = matrix( [[1,2,3]] )                      # Creates a matrix (like a row vector).
print A.T                                    # Transpose of A.
print A*x                                    # Matrix multiplication of A and x.
print A.I                                    # Inverse of A.
print linalg.solve(A, x)     # Solve the linear equation system.
"""



#### let's try without the matrix function ####

def sum (matrA, matrB):
    if(matrA.shape == matrB.shape):
        print(matrA+matrB)
    else:
        print("Error: These matrices don't have the same size")

def product (matrA, matrB):
    print(matrA*matrB)

A = np.zeros((3,3))
A = np.array([
    [0, 1, 5],
    [2, 5, 6],
    [4, 6, 3]
    ])

print ("\nMatrix A: \n", A)

B = np.zeros((3,3))
B = np.array([
    [4, 5, 6],
    [3, 2, 4],
    [3, 5, 1]
    ])

print ("\nMatrix B: \n", B)

print("\n The sum of matrix A and B ")
sum(A,B)

print("\n The product of matrix A and B ")
product(A,B)




# okay, so up 'n til now it seems like the basic calculations can be done with the matrixarrays, should they have the same size
# what happens when I use different size matrices?

C = np.zeros((1,3))
C = np.array([
    [2, 4, 5]
    ])

print("\n Matrix C: \n", C)

print("\n The sum of matrix A and C ")
sum(A,C)


"""
difadd = A+C
print ("\n Matrix A+C \n", difadd)

#it seems like it will add Matrix C to all rows of the A matrix, which isn't correct according to linalg rules

"""
