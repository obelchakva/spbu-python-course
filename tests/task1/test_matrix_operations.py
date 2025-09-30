import pytest

from project.task1.matrix_operations import (
    add_matrices,
    multiply_matrices,
    transpose_matrix,
)


# Tests for matrix operations


def test_add_matrices():
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    assert add_matrices(A, B) == [[6, 8], [10, 12]]

    # Test for incorrect matrix sizes
    with pytest.raises(ValueError):
        add_matrices([[1]], [[1, 2]])

    # Test with zero elements
    A = [[0, 0], [0, 0]]
    B = [[1, 2], [3, 4]]
    assert add_matrices(A, B) == [[1, 2], [3, 4]]


def test_multiply_matrices():
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    assert multiply_matrices(A, B) == [[19, 22], [43, 50]]

    # Test for incorrect matrix sizes
    with pytest.raises(ValueError):
        multiply_matrices([[1, 2]], [[1], [2], [3]])

    # Multiplication by a identity matrix
    A = [[1, 2], [3, 4]]
    E = [[1, 0], [0, 1]]
    assert multiply_matrices(A, E) == A

    # Test with zero elements
    A = [[0, 0], [0, 0]]
    B = [[1, 2], [3, 4]]
    assert multiply_matrices(A, B) == [[0, 0], [0, 0]]

    # Multiplication of 3x2 and 2x3 matrices
    A = [[1, 2], [3, 4], [5, 6]]
    B = [[7, 8, 9], [10, 11, 12]]
    assert multiply_matrices(A, B) == [[27, 30, 33], [61, 68, 75], [95, 106, 117]]

    # Test for multiplying a 1x2 matrix by 2x1
    A = [[1, 2]]
    B = [[3], [4]]
    assert multiply_matrices(A, B) == [[11]]


def test_transpose_matrix():
    A = [[1, 2, 3], [4, 5, 6]]
    assert transpose_matrix(A) == [[1, 4], [2, 5], [3, 6]]

    # The Square matrix test
    B = [[1, 2], [3, 4]]
    assert transpose_matrix(B) == [[1, 3], [2, 4]]