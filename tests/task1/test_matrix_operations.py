from project.task1.matrix_operations import add_matrices, multiply_matrices, transpose_matrix

def test_add_matrices():
    m1 = [[1, 2], [3, 4]]
    m2 = [[5, 6], [7, 8]]
    result = add_matrices(m1, m2)
    expected_result = [[6, 8], [10, 12]]
    assert result == expected_result

def test_multiply_matrices():
    m1 = [[1, 2], [3, 4]]
    m2 = [[5, 6], [7, 8]]
    result = multiply_matrices(m1, m2)
    expected_result = [[19, 22], [43, 50]]
    assert result == expected_result

def test_transpose_matrix():
    matrix = [[1, 2, 3], [4, 5, 6]]
    expected_transposed = [[1, 4], [2, 5], [3, 6]]
    actual_transposed = transpose_matrix(matrix)
    assert actual_transposed == expected_transposed