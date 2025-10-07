import pytest

from project.task1.vector_operations import (
    dot_product,
    magnitude,
    angle_between_vectors,
)

# Tests for vector operations


def test_dot_product():
    assert dot_product([1, 2, 3], [4, 5, 6]) == 32.0

    # Zero Vector test
    assert dot_product([0, 0, 0], [1, 1, 1]) == 0.0

    # Vectors with negative numbers
    assert dot_product([1, -2, 3], [-4, 5, -6]) == -32.0

    # Vector size mismatch
    with pytest.raises(ValueError):
        dot_product([1, 2], [1])


def test_magnitude():
    assert magnitude([3, 4]) == pytest.approx(5.0)
    assert magnitude([1, 0, 0]) == 1.0
    assert magnitude([0, 0, 0]) == 0.0

    # Vector with negative components
    assert magnitude([-3, -4]) == pytest.approx(5.0)


def test_angle_between_vectors():
    # Orthogonal vectors
    assert pytest.approx(angle_between_vectors([1, 0], [0, 1]), 0.1) == 90.0
    assert pytest.approx(angle_between_vectors([0, 1], [1, 0]), 0.1) == 90.0
    assert pytest.approx(angle_between_vectors([0, 10], [10, 0]), 0.1) == 90.0

    # Parallel vectors
    assert pytest.approx(angle_between_vectors([1, 0], [1, 0]), 0.1) == 0.0
    assert pytest.approx(angle_between_vectors([1, 0], [-1, 0]), 0.1) == 180.0
