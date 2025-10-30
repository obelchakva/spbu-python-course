import pytest
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from project.task3.un_curry import curry_explicit, uncurry_explicit


def test_curry_explicit_single_argument_only():
    """Тестирует, что каррированная функция принимает только по одному аргументу за раз"""
    f = curry_explicit(lambda x, y, z: x + y + z, 3)

    #  CORRECTIONS: Корректное использование - по одному аргументу
    result = f(1)(2)(3)
    assert result == 6

    # CORRECTIONS: Проверяем, что НЕЛЬЗЯ передать несколько аргументов за раз
    with pytest.raises((TypeError, AttributeError)):
        f(1, 2)  # Пытаемся передать 2 аргумента сразу

    # CORRECTIONS: Проверяем, что на каждом шаге возвращается функция (кроме последнего)
    step1 = f(1)
    assert callable(step1)

    step2 = step1(2)
    assert callable(step2)

    final = step2(3)
    assert not callable(final)
    assert final == 6


@pytest.mark.parametrize(
    "args, expected",
    [
        ((1, 2, 3), "<1, 2, 3>"),
        ((10, 20, 30), "<10, 20, 30>"),
        ((5, 5, 5), "<5, 5, 5>"),
    ],
)
def test_curry_explicit_valid_cases(args, expected):
    f = curry_explicit(lambda x, y, z: f"<{x}, {y}, {z}>", 3)
    # CORRECTIONS: Call with one argument at a time
    result = f(args[0])(args[1])(args[2])
    assert result == expected


def test_curry_explicit_arity_zero():
    f = curry_explicit(lambda: "No args", 0)
    assert f() == "No args"


def test_curry_explicit_arity_one():
    f = curry_explicit(lambda x: x * 2, 1)
    assert f(5) == 10


@pytest.mark.parametrize("args", [(1, 2, 3), (1, 2, 3, 4)])
def test_curry_explicit_too_many_arguments(args):
    f = curry_explicit(lambda x, y: x + y, 2)
    with pytest.raises(TypeError):
        f(*args)


@pytest.mark.parametrize("arity", [-1, "a"])
def test_curry_explicit_invalid_arity(arity):
    with pytest.raises(ValueError):
        curry_explicit(lambda x: x, arity)


# CORRECTIONS: Check that print was called with correct arguments
# CORRECTIONS: Check that return value is None (print returns None)
def test_curry_explicit_function_with_arbitrary_args():
    """Tests currying with the built-in print function"""
    with patch("builtins.print") as mock_print:
        # Setting the return value to None to simulate a real print
        mock_print.return_value = None

        f = curry_explicit(print, 2)
        result = f(1)(2)

        # We check that print was called with the correct arguments.
        mock_print.assert_called_once_with(1, 2)
        # We check that the return value is None
        assert result is None


# Tests for uncurry_explicit
@pytest.mark.parametrize(
    "args, expected",
    [
        ((1, 2, 3), "<1, 2, 3>"),
        ((4, 5, 6), "<4, 5, 6>"),
    ],
)
def test_uncurry_explicit_valid_cases(args, expected):
    f = curry_explicit(lambda x, y, z: f"<{x}, {y}, {z}>", 3)
    g = uncurry_explicit(f, 3)
    assert g(*args) == expected


@pytest.mark.parametrize(
    "args",
    [
        (1,),
        (1, 2, 3),
    ],
)
def test_uncurry_explicit_wrong_argument_count(args):
    f = curry_explicit(lambda x, y: x + y, 2)
    g = uncurry_explicit(f, 2)
    with pytest.raises(TypeError):
        g(*args)


@pytest.mark.parametrize("arity", [-1, "a"])
def test_uncurry_explicit_invalid_arity(arity):
    f = curry_explicit(lambda x: x, 1)
    with pytest.raises(ValueError):
        uncurry_explicit(f, arity)
