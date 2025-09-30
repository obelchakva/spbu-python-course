def add_matrices(m1, m2):
    """Складывает две матрицы."""
    result = []
    for i in range(len(m1)):
        row = []
        for j in range(len(m1[i])):
            row.append(m1[i][j] + m2[i][j])
        result.append(row)
    return result


def multiply_matrices(m1, m2):
    """Умножает две матрицы."""
    rows_A = len(m1)
    cols_A = len(m1[0])
    rows_B = len(m2)
    cols_B = len(m2[0])

    # Проверяем совместимость размеров матриц
    if cols_A != rows_B:
        raise ValueError("Невозможно перемножить матрицы: размеры несовместимы")

    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += m1[i][k] * m2[k][j]

    return result


def transpose_matrix(matrix):
    """Транспонирует матрицу."""
    transposed = [
        [matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))
    ]
    return transposed
