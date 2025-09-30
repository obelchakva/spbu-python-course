from project.task1.vector_operations import (
    dot_product,
    magnitude,
    angle_between_vectors,
)


def test_dot_product():
    assert dot_product([1, 2], [3, 4]) == 11


def test_magnitude():
    assert round(magnitude([3, 4]), 2) == 5.0


def test_angle_between_vectors():
    vec1 = [1, 0]
    vec2 = [0, 1]
    expected_angle = 90.0
    calculated_angle = round(angle_between_vectors(vec1, vec2), 2)
    assert abs(expected_angle - calculated_angle) <= 0.01
