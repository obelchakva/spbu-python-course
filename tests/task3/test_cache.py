import pytest
from unittest.mock import patch
from project.task3.cache import cache_results


@cache_results(max_size=3)
def expensive_function(x, y):
    """
    Example function that simulates long computations.
    """
    return x + y


@pytest.mark.parametrize(
    "x, y, expected",
    [
        (1, 2, 3),  # First computation, saved to cache
        (1, 2, 3),  # Get from cache
        (2, 3, 5),  # Saved to cache
        (3, 4, 7),  # Saved to cache: cache full now (3, 5, 7)
        (1, 2, 3),  # Get from cache
        (4, 5, 9),  # Added to cache, removes result 3 from cache
        (1, 2, 3),  # New computation, added to cache
    ],
)
def test_cache_expensive_function(x, y, expected):
    """
    Test to verify caching behavior without flag.
    """
    result = expensive_function(x, y)
    assert result == expected


#  CORRECTIONS:


def test_cache_with_builtin_functions():
    """It tests the operation of caching with built-in functions"""
    call_count = 0

    @cache_results(max_size=2)
    def cached_func(obj):
        nonlocal call_count
        call_count += 1
        return len(obj)

    result1 = cached_func((1, 2, 3))
    assert result1 == 3
    assert call_count == 1

    result2 = cached_func((1, 2, 3))
    assert result2 == 3
    assert call_count == 1


def test_cache_eviction_oldest():
    """Tests that it is the oldest key that is deleted when the limit is exceeded"""
    call_count = 0

    @cache_results(max_size=2)
    def counting_func(x):
        nonlocal call_count
        call_count += 1
        return x * 2

    counting_func(1)
    counting_func(2)

    counting_func(1)

    counting_func(3)

    counting_func(2)
    counting_func(1)
    counting_func(3)


def test_cache_caching_effect():
    """Tests that function calls are indeed cached"""
    call_count = 0

    @cache_results(max_size=2)
    def test_func(x):
        nonlocal call_count
        call_count += 1
        return x * 2

    result1 = test_func(5)
    assert call_count == 1
    assert result1 == 10

    result2 = test_func(5)
    assert call_count == 1
    assert result2 == 10

    result3 = test_func(10)
    assert call_count == 2
    assert result3 == 20
