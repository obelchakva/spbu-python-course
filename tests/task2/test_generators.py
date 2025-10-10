import pytest
from typing import List, Tuple
from itertools import chain
from functools import reduce
from project.task2.generators import *


# Tests for the data_generator function
class TestDataGenerator:
    """Tests for the data_generator function"""

    @pytest.mark.parametrize(
        "input_data, expected",
        [
            ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
            (range(1, 6), [1, 2, 3, 4, 5]),
            ([], []),
            ([42], [42]),
            (["a", "b", "c"], ["a", "b", "c"]),
            ((1, 2, 3, 4, 5), [1, 2, 3, 4, 5]),
        ],
    )
    def test_data_generator_with_iterables(self, input_data, expected):
        """Test for working with different kinds of iterable objects"""
        result = list(make_data_generator(input_data))
        assert result == expected

    def test_data_generator_with_generator(self):
        """Test for working with custom generator"""

        def custom_gen():
            yield 1
            yield 2
            yield 3

        result = list(make_data_generator(custom_gen()))
        assert result == [1, 2, 3]


# Tests for the compose_steps function
class TestComposeSteps:
    """Tests for the compose_steps function"""

    @pytest.mark.parametrize(
        "input_data, transformations, expected",
        [
            (
                [1, 2, 3, 4, 5],
                [apply_map(lambda x: x * 2)],
                [2, 4, 6, 8, 10],
            ),
            (
                [1, 2, 3, 4, 5],
                [apply_filter(lambda x: x % 2 == 0)],
                [2, 4],
            ),
            (
                [1, 2, 3, 4, 5],
                [apply_map(lambda x: x * 2), apply_filter(lambda x: x > 5)],
                [6, 8, 10],
            ),
            (
                [1, 2, 3, 4, 5],
                [apply_reduce(lambda acc, x: acc + x, 0)],
                15,
            ),
        ],
    )
    def test_compose_steps_with_transformations(
        self, input_data, transformations, expected
    ):
        """Test sequential composition of transformations"""
        data_gen = make_data_generator(input_data)
        composed = compose_steps(data_gen, transformations)
        last_operation = transformations[-1]
        if "apply_reduce" in getattr(last_operation, "__qualname__", ""):
            result = composed
        else:
            result = list(composed)
        assert result == expected


# Tests for the aggregate_results function
class TestAggregateResults:
    """Tests for the aggregate_results function"""

    @pytest.mark.parametrize(
        "generator, collector, expected",
        [
            (
                make_data_generator([1, 2, 3, 4, 5]),
                list,
                [1, 2, 3, 4, 5],
            ),
            (
                make_data_generator([1, 2, 3, 4, 5]),
                set,
                {1, 2, 3, 4, 5},
            ),
            (
                make_data_generator([1, 2, 3, 4, 5]),
                tuple,
                (1, 2, 3, 4, 5),
            ),
            (
                make_data_generator(["a", "b", "c"]),
                list,
                ["a", "b", "c"],
            ),
            (
                make_data_generator([(1, 2), (3, 4), (5, 6)]),
                dict,
                {1: 2, 3: 4, 5: 6},
            ),
        ],
    )
    def test_aggregate_results_with_collectors(self, generator, collector, expected):
        """Test collecting results with different methods"""
        result = aggregate_results(generator, collector)
        assert result == expected


# CORRECTIONS:


class TestBuiltinsAndCustomFunctions:
    """Tests that check built-in map/filter/zip and custom user functions are supported"""

    def test_compose_with_builtin_map_and_filter(self):
        data_gen = make_data_generator([1, 2, 3, 4, 5])
        transformations = [
            # builtin map wrapped as a callable expecting an iterable
            lambda gen: map(lambda x: x * 2, gen),
            # builtin filter wrapped as callable
            lambda gen: filter(lambda x: x > 5, gen),
        ]
        result = list(compose_steps(data_gen, transformations))
        assert result == [6, 8, 10]

    def test_compose_with_builtin_zip(self):
        data_gen = make_data_generator([1, 2, 3])
        other = make_data_generator([10, 20, 30])
        transformations = [
            apply_map(lambda x: x + 1),
            lambda gen: zip(gen, other),
        ]
        result = list(compose_steps(data_gen, transformations))
        assert result == [(2, 10), (3, 20), (4, 30)]

    def test_compose_with_custom_user_function(self):
        # Custom transformation implemented by user: must be accepted by compose_steps.
        def custom_double(gen):
            for x in gen:
                yield x * 2

        data_gen = make_data_generator([1, 2, 3])
        result = list(compose_steps(data_gen, [custom_double]))
        assert result == [2, 4, 6]
