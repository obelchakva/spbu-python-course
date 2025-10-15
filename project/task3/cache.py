from collections import OrderedDict
from functools import wraps
from typing import Callable, Tuple, Any

# Version without the flag
def cache_results(max_size: int = 0) -> Callable:
    """
    Decorator for caching the results of a function (without a flag).

    Parameters:
        max_size : int (maximum number of cached results. Defaults to 0 (no caching))
    """

    def decorator(func: Callable) -> Callable:
        cache: OrderedDict[Tuple, Any] = OrderedDict()

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (args, frozenset(kwargs.items()))
            if key in cache:
                return cache[key]  # Return cached result

            result = func(*args, **kwargs)  # Compute the result
            cache[key] = result  # Store result in cache

            # Remove old entries if the cache exceeds max_size
            if max_size > 0 and len(cache) > max_size:
                cache.popitem(last=False)  # Remove the oldest entry (FI-FO)

            return result  # Return the computed result

        return wrapper

    return decorator