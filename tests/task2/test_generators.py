import pytest
from typing import List, Tuple
from itertools import count, islice
from functools import reduce
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
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


# CORRECTIONS:


class TestLaziness:
    """Tests demonstrating the lazy nature of the pipeline"""

    def test_laziness_with_side_effects(self):
        """Test that elements are processed only when consumed"""
        processed_elements = []

        def track_processing(gen):
            for x in gen:
                processed_elements.append(f"processed_{x}")
                yield x

        data_gen = make_data_generator([1, 2, 3, 4, 5])
        transformations = [
            track_processing,
            apply_map(lambda x: x * 2),
            apply_filter(lambda x: x > 5),
        ]

        # Pipeline created but not consumed yet
        pipeline = compose_steps(data_gen, transformations)
        assert (
            processed_elements == []
        ), "No elements should be processed before consumption"

        first_element = next(pipeline)
        assert first_element == 6
        assert processed_elements == [
            "processed_1",
            "processed_2",
            "processed_3",
        ], "Should process elements until first match is found"

        # Consume next element
        second_element = next(pipeline)
        assert second_element == 8
        assert processed_elements == [
            "processed_1",
            "processed_2",
            "processed_3",
            "processed_4",
        ]

        # Consume remaining elements
        remaining = list(pipeline)
        assert remaining == [10]
        assert processed_elements == [
            "processed_1",
            "processed_2",
            "processed_3",
            "processed_4",
            "processed_5",
        ]

    def test_laziness_with_infinite_generator(self):
        """Test that pipeline can work with infinite generators"""

        def infinite_counter():
            n = 0
            while True:
                yield n
                n += 1

        # Create pipeline with infinite generator
        transformations = [
            apply_filter(lambda x: x % 2 == 0),  # only even numbers
            apply_map(lambda x: x * 10),  # multiply by 10
        ]

        pipeline = compose_steps(infinite_counter(), transformations)

        # Take only first 5 elements from infinite stream
        result = []
        for i, value in enumerate(pipeline):
            if i >= 5:
                break
            result.append(value)

        assert result == [
            0,
            20,
            40,
            60,
            80,
        ], "Should be able to work with infinite generators"

    def test_laziness_early_termination(self):
        """Test that pipeline stops when result is found early"""
        processed_count = [0]  # use list to allow modification in nested function

        def counting_generator(data):
            for item in data:
                processed_count[0] += 1
                yield item

        data_gen = counting_generator([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        transformations = [apply_map(lambda x: x * 2), apply_filter(lambda x: x > 10)]

        pipeline = compose_steps(data_gen, transformations)

        # Take only first 2 elements that satisfy condition
        result = []
        for i, value in enumerate(pipeline):
            if i >= 2:
                break
            result.append(value)

        assert result == [12, 14]
        assert (
            processed_count[0] == 8
        ), f"Should process exactly 8 elements, but processed {processed_count[0]}"

    def test_laziness_no_processing_before_consumption(self):
        """Test that nothing is processed before we start consuming"""
        processed = []

        def track_processing(gen):
            for x in gen:
                processed.append(x)
                yield x

        data_gen = make_data_generator([1, 2, 3, 4, 5])
        transformations = [
            track_processing,
            apply_map(lambda x: x + 1),
            apply_filter(lambda x: x % 2 == 0),
            apply_map(lambda x: x * 3),
        ]

        pipeline = compose_steps(data_gen, transformations)

        assert processed == [], "No elements should be processed before consumption"

        first = next(pipeline)
        assert first == 6
        assert processed == [1], "Should process only the first element"

    def test_laziness_with_islice(self):
        """Test lazy processing with islice"""
        processed = []

        def infinite_sequence():
            n = 0
            while True:
                processed.append(n)
                yield n
                n += 1

        transformations = [
            apply_filter(lambda x: x % 3 == 0),
            apply_map(lambda x: x**2),
        ]

        pipeline = compose_steps(infinite_sequence(), transformations)

        result = list(islice(pipeline, 4))

        assert result == [0, 9, 36, 81]
        assert (
            len(processed) == 10
        ), f"Should process only 10 elements, but processed {len(processed)}"
        assert processed == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
