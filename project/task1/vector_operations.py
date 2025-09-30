import math


def dot_product(v1, v2):
    """Вычисляет скалярное произведение двух векторов."""
    return sum(x * y for x, y in zip(v1, v2))


def magnitude(v):
    """Вычисляет длину (норму) вектора."""
    return math.sqrt(sum(x**2 for x in v))


def angle_between_vectors(v1, v2):
    """Вычисляет угол между двумя векторами в градусах."""
    dp = dot_product(v1, v2)
    mag_v1 = magnitude(v1)
    mag_v2 = magnitude(v2)

    if mag_v1 == 0 or mag_v2 == 0:
        raise ValueError("Длина хотя бы одного из векторов равна нулю.")

    cos_theta = dp / (mag_v1 * mag_v2)
    theta_rad = math.acos(cos_theta)
    return math.degrees(theta_rad)
