import functools
import logging
from typing import Optional, Callable, Any

from src.utilities.error_handler.strategy import STRATEGY_REGISTRY


def error_handler(strategy_name: Optional[str] = None, **strategy_kwargs) -> Callable:
    """
    Decorator to wrap functions for error handling.
    It intercepts exceptions and delegates handling to a registered strategy.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                try:
                    return func(*args, **kwargs)
                except TypeError as e:
                    if str(e).endswith("takes 1 positional argument but 2 were given"):
                        return func(args[0])
                    else:
                        raise e
            except Exception as e:
                if strategy_name and strategy_name in STRATEGY_REGISTRY:
                    strategy = STRATEGY_REGISTRY[strategy_name]
                    return strategy.handle(e, func, args, **strategy_kwargs, **kwargs)
                else:
                    logging.error(f"Unhandled exception in {func.__name__}: {e}", exc_info=True)
                    raise e
        return wrapper
    return decorator
