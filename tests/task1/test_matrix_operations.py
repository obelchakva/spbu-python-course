import pytest

from project.task1.matrix_operations import (
    add_matrices,
    multiply_matrices,
    transpose_matrix,
)


# Tests for matrix operations


def test_add_matrices(): # The names of the variables have been replaced
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    assert add_matrices(a, b) == [[6, 8], [10, 12]]

    # Test for incorrect matrix sizes
    with pytest.raises(ValueError):
        add_matrices([[1]], [[1, 2]])

    # Test with zero elements
    a = [[0, 0], [0, 0]]
    b = [[1, 2], [3, 4]]
    assert add_matrices(a, b) == [[1, 2], [3, 4]]


def test_multiply_matrices(): # The names of the variables have been replaced
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    assert multiply_matrices(a, b) == [[19, 22], [43, 50]]

    # Test for incorrect matrix sizes
    with pytest.raises(ValueError):
        multiply_matrices([[1, 2]], [[1], [2], [3]])

    # Multiplication by a identity matrix
    a = [[1, 2], [3, 4]]
    E = [[1, 0], [0, 1]]
    assert multiply_matrices(a, E) == a

    # Test with zero elements
    a = [[0, 0], [0, 0]]
    b = [[1, 2], [3, 4]]
    assert multiply_matrices(a, b) == [[0, 0], [0, 0]]

    # Multiplication of 3x2 and 2x3 matrices
    a = [[1, 2], [3, 4], [5, 6]]
    b = [[7, 8, 9], [10, 11, 12]]
    assert multiply_matrices(a, b) == [[27, 30, 33], [61, 68, 75], [95, 106, 117]]

    # Test for multiplying a 1x2 matrix by 2x1
    a = [[1, 2]]
    b = [[3], [4]]
    assert multiply_matrices(a, b) == [[11]]


def test_transpose_matrix(): # The names of the variables have been replaced
    a = [[1, 2, 3], [4, 5, 6]]
    assert transpose_matrix(a) == [[1, 4], [2, 5], [3, 6]]

    # The Square matrix test
    b = [[1, 2], [3, 4]]
    assert transpose_matrix(b) == [[1, 3], [2, 4]]
