from typing import List

# Matrix operations


def add_matrices(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    """
    Add two matrices

    Parameters:

    A : List[List[float]] (first input matrix)
    B : List[List[float]] (second input matrix)

    Returns:

    List[List[float]]: resulting matrix from the addition

    Raises:

    ValueError: if the dimensions of the input matrices do not match
    """
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError("Error: matrices of different dimensions.")

    result_m = [[0.0] * len(A[0]) for i in range(len(A))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            result_m[i][j] = A[i][j] + B[i][j]
    return result_m


def multiply_matrices(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    """
    Multiply two matrices

    Parameters:

    A : List[List[float]] (first input matrix)
    B : List[List[float]] (second input matrix)

    Returns:

    List[List[float]]: resulting matrix from the multiplication

    Raises:

    ValueError: if the number of columns in the first matrix does not match the number of rows in the second matrix

    Examples:

    >>> matrix_multiplication([[1, 2], [3, 4]], [[5, 6], [7, 8]])
    [[19, 22], [43, 50]]
    """
    if len(A[0]) != len(B):
        raise ValueError(
            "Error: number of rows of first matrix and number of columns of second matrix are different."
        )

    result_m = [[0.0] * len(B[0]) for i in range(len(A))]

    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result_m[i][j] += A[i][k] * B[k][j]

    return result_m


def transpose_matrix(A: List[List[float]]) -> List[List[float]]:
    """
    Transpose a matrix

    Parameters:

    A : List[List[float]] (input matrix to be transposed)

    Returns:

    List[List[float]]: transposed matrix
    """

    result_m = [[0.0] * len(A) for i in range(len(A[0]))]

    for i in range(len(A[0])):
        for j in range(len(A)):
            result_m[i][j] = A[j][i]
    return result_m
