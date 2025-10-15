import pytest
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
