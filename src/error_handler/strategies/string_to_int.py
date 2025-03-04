from typing import Callable, Any

from typeguard import typechecked

from .core import ErrorHandlingStrategy, DEFAULT_ERROR_HANDLING_STRATEGIES


@typechecked
class StringToIntStrategy(ErrorHandlingStrategy):
    """
    Strategy that acts if all other strategies do not handle the exception.
    """
    @classmethod
    def can_handle(cls, exception: Exception) -> bool:
        return isinstance(exception, TypeError)

    @staticmethod
    def handle(exception: Exception, *args, **kwargs: Any) -> Any:
        """
        Fallback strategy that attempts to convert all arguments to integers and retry the function. If the function
        still fails, the original exception is raised. This strategy is intended to be used as a last resort,
        implemented just to try something.

        Args:
            exception: The exception that occurred.
            func: The function that raised the exception.
            args: The arguments that were passed to the function.
            kwargs: The keyword arguments that were passed to the function.

        Returns:
            The return value of the function.

        Raises:
            The original exception if the function still fails.
        """
        func = kwargs.pop("func")
        new_args = [int(arg) if str(arg).isnumeric() else arg for arg in args]
        new_kwargs = {key: int(value) if str(value).isnumeric() else value for key, value in kwargs.items()}

        print(f"new_args: {new_args}")
        print(f"new_kwargs: {new_kwargs}")
        try:
            result = func(*new_args, **new_kwargs)
            return True, result
        except Exception as e:
            print(e)
            return False, exception
