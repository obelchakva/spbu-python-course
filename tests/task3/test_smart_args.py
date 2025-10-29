import pytest
from itertools import count
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from project.task3.smart_args import smart_args, Isolated, Evaluated

# Function to simulate unique values
counter = count()


def get_unique_value():
    return next(counter)


@pytest.mark.parametrize(
    "initial_dict, expected_dict, expected_original",
    [
        ({"a": 10}, {"a": 0}, {"a": 10}),
        ({"b": 5}, {"b": 5, "a": 0}, {"b": 5}),
    ],
)
def test_isolated(initial_dict, expected_dict, expected_original):
    """
    Test that Isolated prevents mutations across invocations.
    """

    @smart_args
    def check_isolation(*, d=Isolated()):
        d["a"] = 0
        return d

    result = check_isolation(d=initial_dict)

    assert result == expected_dict
    assert initial_dict == expected_original


@pytest.mark.parametrize(
    "override_y, expected_y_different",  # CORRECTIONS: removed expected_x_differs
    [
        (None, True),
        (150, False),
    ],
)
def test_evaluated(
    override_y, expected_y_different
):  # CORRECTIONS: removed expected_x_differs
    @smart_args
    def check_evaluation(*, x=get_unique_value(), y=Evaluated(get_unique_value)):
        return x, y

    result1 = check_evaluation()
    result2 = check_evaluation()

    if override_y is not None:
        result3 = check_evaluation(y=override_y)
        assert result3[1] == override_y

    assert result1[0] == result2[0]

    if expected_y_different:
        assert result1[1] != result2[1]


@pytest.mark.parametrize(
    "decorator_combo, expected_exception",
    [
        (lambda: Evaluated(Isolated()), TypeError),
        (lambda: Isolated(Evaluated(get_unique_value)), TypeError),
    ],
)
def test_invalid_combinations(decorator_combo, expected_exception):
    """
    Test that invalid combinations of Isolated and Evaluated raise proper exceptions.
    """

    with pytest.raises(expected_exception):

        @smart_args
        def invalid_decorator_combo(*, arg=decorator_combo()):
            return arg


@pytest.mark.parametrize(
    "arg, expected_result, raises_exception",
    [
        ({"a": 10}, {"a": 0}, False),
        (5, None, True),
    ],
)
def test_isolated_with_positional(arg, expected_result, raises_exception):
    """
    Test that Isolated works with positional arguments passed by key and raises TypeError otherwise.
    """

    @smart_args
    def check_isolated_positional(d=Isolated()):
        d["a"] = 0
        return d

    if raises_exception:
        with pytest.raises(TypeError):
            check_isolated_positional(arg)
    else:
        result = check_isolated_positional(d=arg)
        assert result == expected_result


@pytest.mark.parametrize(
    "override_value, expect_override",
    [
        (None, False),
        (10, True),
    ],
)
def test_evaluated_with_positional(override_value, expect_override):
    """
    Test that Evaluated works with positional arguments passed by key.
    """

    @smart_args
    def check_evaluated_positional(b=Evaluated(get_unique_value)):
        return b

    if expect_override:
        result = check_evaluated_positional(b=override_value)
        assert result == override_value
    else:
        result1 = check_evaluated_positional()
        result2 = check_evaluated_positional()
        assert result1 != result2
