import logging
from abc import ABC, abstractmethod
from typing import Callable, Any, Optional, Dict

from src.utilities.logger import get_logger


class ErrorHandlingStrategy(ABC):
    """
    Abstract base class for error handling strategies.
    """
    @abstractmethod
    def handle(self, exception: Exception, func: Callable, args: tuple, **kwargs: dict) -> Any:
        """
        Handle the exception and optionally attempt recovery.
        """
        pass

    def alert(self, exception: Exception, func: Callable, args: tuple, **kwargs: dict) -> Any:
        """
        Alert the user when an exception occurs.
        """
        pass


class LoggingStrategy(ErrorHandlingStrategy):
    """
    Strategy that logs the error details.
    """
    def __init__(self, logger: Optional[logging.Logger] = None, deafult_return: Any = None):
        self.logger = logger or get_logger(__name__)
        self.default_return = deafult_return

    def handle(self, exception: Exception, func: Callable, args: tuple, logger: Optional[logging.Logger] = None, **kwargs: dict) -> Any:
        logger = logger or self.logger
        logger.error(f"Error in {func.__name__}: {exception}", exc_info=True)
        if self.default_return is not None:
            return self.default_return
        raise exception


class RetryStrategy(ErrorHandlingStrategy):
    """
    Strategy that retries function execution a specified number of times.
    """
    def __init__(self, retries: int = 3):
        self.retries = retries

    def handle(self, exception: Exception, func: Callable, args: tuple, **kwargs: dict) -> Any:
        attempt = 1
        while attempt <= self.retries:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                attempt += 1
                if attempt > self.retries:
                    raise e


# Registry to keep track of registered error handling strategies.
STRATEGY_REGISTRY: Dict[str, ErrorHandlingStrategy] = {}


def register_strategy(name: str, strategy: ErrorHandlingStrategy) -> None:
    """
    Register an error handling strategy by a unique name.
    """
    STRATEGY_REGISTRY[name] = strategy


register_strategy("logging", LoggingStrategy())
register_strategy("retry", RetryStrategy(retries=2))
