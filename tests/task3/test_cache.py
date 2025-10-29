import pytest
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
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
    """Тестирует работу кеширования со встроенными функциями"""

    @cache_results(max_size=2)
    def cached_func(obj):
        # CORRECTIONS: Используем встроенную функцию len напрямую
        return len(obj)

    result1 = cached_func((1, 2, 3))
    assert result1 == 3

    result2 = cached_func((1, 2, 3))
    assert result2 == 3

    result3 = cached_func((1, 2, 3, 4))
    assert result3 == 4

    result4 = cached_func((1, 2, 3))
    assert result4 == 3


def test_cache_eviction_oldest():
    """Тестирует, что удаляется именно самый старый ключ при превышении лимита"""
    call_count = 0

    @cache_results(max_size=2)
    def counting_func(x):
        nonlocal call_count
        call_count += 1
        return x * 2

    # CORRECTIONS: Заполняем кеш двумя элементами: 1 и 2
    counting_func(1)
    counting_func(2)

    # CORRECTIONS: Обращаемся к элементу 1, чтобы сделать его "новее"
    counting_func(1)  # теперь порядок: [2, 1]

    # CORRECTIONS: Добавляем третий элемент - должен вытеснить самый старый (2)
    counting_func(3)  # кеш: [1, 3]

    # CORRECTIONS: Проверяем, что 2 был вытеснен и вычисляется заново
    assert counting_func(2) == 4
    # CORRECTIONS: Проверяем, что 1 и 3 остались в кеше
    assert counting_func(1) == 2
    assert counting_func(3) == 6

    # CORRECTIONS: Проверяем итоговое количество вызовов
    assert call_count == 4


def test_cache_caching_effect():
    """Тестирует, что вызовы функций действительно кешируются"""
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
