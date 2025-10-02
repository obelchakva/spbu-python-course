from typing import List

# Matrix operations


def add_matrices(a: List[List[float]], b: List[List[float]]) -> List[List[float]]: # The names of the variables have been replaced
    """
    add two matrices

    Parameters:

    a : List[List[float]] (first input matrix)
    b : List[List[float]] (second input matrix)

    Returns:

    List[List[float]]: resulting matrix from the addition

    Raises:

    ValueError: if the dimensions of the input matrices do not match
    """
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        raise ValueError("Error: matrices of different dimensions.")

    result_m = [[0.0] * len(a[0]) for i in range(len(a))]
    for i in range(len(a)):
        for j in range(len(a[0])):
            result_m[i][j] = a[i][j] + b[i][j]
    return result_m


def multiply_matrices(a: List[List[float]], b: List[List[float]]) -> List[List[float]]: # The names of the variables have been replaced
    """
    Multiply two matrices

    Parameters:

    a : List[List[float]] (first input matrix)
    b : List[List[float]] (second input matrix)

    Returns:

    List[List[float]]: resulting matrix from the multiplication

    Raises:

    ValueError: if the number of columns in the first matrix does not match the number of rows in the second matrix

    Examples:

    >>> matrix_multiplication([[1, 2], [3, 4]], [[5, 6], [7, 8]])
    [[19, 22], [43, 50]]
    """
    if len(a[0]) != len(b):
        raise ValueError(
            "Error: number of rows of first matrix and number of columns of second matrix are different."
        )

    result_m = [[0.0] * len(b[0]) for i in range(len(a))]

    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                result_m[i][j] += a[i][k] * b[k][j]

    return result_m


def transpose_matrix(a: List[List[float]]) -> List[List[float]]: # The names of the variables have been replaced
    """
    Transpose a matrix

    Parameters:

    a : List[List[float]] (input matrix to be transposed)

    Returns:

    List[List[float]]: transposed matrix
    """

    result_m = [[0.0] * len(a) for i in range(len(a[0]))]

    for i in range(len(a[0])):
        for j in range(len(a)):
            result_m[i][j] = a[j][i]
    return result_m
