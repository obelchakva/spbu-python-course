import pytest
from project.task3.un_curry import curry_explicit, uncurry_explicit

# Tests for curry_explicit
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
    assert f(*args) == expected


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


def test_curry_explicit_function_with_arbitrary_args():
    f = curry_explicit(print, 2)
    assert f(1)(2) is None


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
