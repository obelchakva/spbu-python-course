from typing import Callable, Any


def curry_explicit(func: Callable[..., Any], arity: int) -> Callable[..., Any]:
    """
    Curry a function to accept one argument at a time, returning a function that takes
    subsequent arguments until the total number of arguments equals the arity.
    Parameters:
        func : callable (function to be curried)
        arity : int (number of arguments the function expects)
    Returns:
        curried_func : callable (curried function)
    Raises:
        ValueError (if arity is not a non-negative integer)
        TypeError (if too many arguments are provided when calling the curried function)
    """
    if not isinstance(arity, int) or arity < 0:
        raise ValueError("Arity must be a non-negative integer.")

    if arity == 0:
        return lambda: func()

    def curried(arg):
        if arity == 1:
            return func(arg)

        return curry_explicit(lambda *args: func(arg, *args), arity - 1)

    return curried


def uncurry_explicit(curry_func: Callable[..., Any], arity: int) -> Callable[..., Any]:
    """
    Uncurry a curried function so that it can accept all arguments at once.
    Parameters:
        curry_func : callable (curried function to be uncurried)
        arity : int (number of arguments the function expects)
    Returns:
        uncurried_func : callable (uncurried version of the function)
    Raises:
        ValueError (if arity is not a non-negative integer)
        TypeError (if the number of arguments provided does not match the arity)
    """
    if not isinstance(arity, int) or arity < 0:
        raise ValueError("Arity must be a non-negative integer.")

    def uncurried(*args: Any) -> Any:
        if len(args) != arity:
            raise TypeError(f"Expected exactly {arity} arguments, but got {len(args)}.")

        result = curry_func
        for arg in args:
            result = result(arg)
        return result

    return uncurried
