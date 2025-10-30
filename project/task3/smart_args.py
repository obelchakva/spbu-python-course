from copy import deepcopy
from inspect import signature
from typing import Any, Callable


class Isolated:
    """
    A class indicating that a parameter should be isolated from mutation.
    """

    pass


class Evaluated:
    """
    A class representing a parameter that evaluates a function only once for its default value.

    Parameters:
        func : Callable[..., Any] (callable that returns the value to be used as the default for the parameter)

    Raises:
        TypeError (If the given function is an instance of Isolated)
    """

    def __init__(self, func: Callable[..., Any]) -> None:
        if isinstance(func, Isolated):
            raise TypeError("Evaluated cannot be used with Isolated.")
        self.func = func

    def get_value(self) -> Any:
        """
        Return the computed value from the function.

        Returns:
            Any (value obtained by calling the stored function)
        """
        return self.func()


def smart_args(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to handle default arguments with special behaviors like Isolated and Evaluated.

    Parameters:
        func : Callable[..., Any] (function to be decorated)

    Returns:
        Callable[..., Any] (wrapper function that applies the behavior modifications)
    """

    func_signature = signature(func)

    def wrapper(**kwargs: Any) -> Any:
        """
        Wrapper function to manage parameter defaults and mutations.

        Parameters:
            **kwargs : Any (keyword arguments passed to the original function)

        Returns:
            Any (result of calling the original function with modified parameters)
        """
        params_to_update = {}

        for param_name, param in func_signature.parameters.items():
            if param_name in kwargs:
                value = kwargs[param_name]
                # Handle Isolated parameters
                if isinstance(param.default, Isolated):
                    params_to_update[param_name] = deepcopy(value)
                else:
                    params_to_update[param_name] = value

            # Handle Evaluated parameters
            elif isinstance(param.default, Evaluated):
                params_to_update[param_name] = param.default.get_value()

        # Call the original function with the updated parameters
        return func(**params_to_update)

    return wrapper
