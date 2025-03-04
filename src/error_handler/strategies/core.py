import logging
import os
from abc import ABC, abstractmethod
from typing import Callable, Any, Dict, Tuple

from typeguard import typechecked

from src.error_handler.exceptions import ErrorHandlerException

DEFAULT_ERROR_HANDLING_STRATEGIES = []


@typechecked
class ErrorHandlingStrategy(ABC):
    """
    Abstract base class for error handling strategies. Strategies are used to handle exceptions in a specific way.
    """
    _priority: int = int(os.getenv("DEFAULT_ERROR_STRATEGY_PRIORITY", 20))
    _enabled: bool = os.getenv("DEFAULT_ERROR_STRATEGY_ENABLED", "true").lower() == "true"
    _logger: logging.Logger = logging.getLogger(os.getenv("DEFAULT_LOGGER_NAME", "dev.schrammel.error_handler"))

    @classmethod
    def is_enabled(cls) -> bool:
        """
        Check if the strategy is enabled.
        """
        return cls._enabled

    @classmethod
    def enable(cls) -> None:
        """
        Enable the strategy.
        """
        cls._enabled = True

    @classmethod
    def disable(cls) -> None:
        """
        Disable the strategy.
        """
        cls._enabled = False

    @classmethod
    @abstractmethod
    def handle(cls, exception: Exception, func: Callable, args: tuple, **kwargs: dict) -> Tuple[bool, Any]:
        """
        Handle the exception and optionally attempt recovery.
        """
        pass

    @classmethod
    @abstractmethod
    def can_handle(cls, exception: Exception) -> bool:
        """
        Check if the strategy can handle the exception.
        """
        pass

    @classmethod
    def priority(cls) -> int:
        """
        Return the priority of the strategy. Lower values are executed
        first.
        """
        return cls._priority

    @classmethod
    def set_priority(cls, priority: int) -> None:
        """
        Set the priority of the strategy. Lower values are executed first. Value must be an integer between 0 and 100
        inclusive.
        """
        if not isinstance(priority, int):
            raise ValueError("Priority must be an integer.")

        min_priority: int = int(os.getenv("DEFAULT_ERROR_STRATEGY_PRIORITY_MINIMUM", 1))
        max_priority: int = int(os.getenv("DEFAULT_ERROR_STRATEGY_PRIORITY_MAXIMUM", 100))
        if priority < min_priority or priority > max_priority:
            raise ValueError(f"Priority must be between {min_priority} and {max_priority} inclusive.")

        cls._priority = priority



STRATEGY_REGISTRY: Dict[str, ErrorHandlingStrategy] = {}


def register_strategy(name: str, strategy: ErrorHandlingStrategy) -> None:
    """
    Register an error handling strategy by a unique name.
    """
    if not isinstance(strategy, ErrorHandlingStrategy):
        raise ErrorHandlerException("Strategy must be an instance of ErrorHandlingStrategy")

    STRATEGY_REGISTRY[name]: ErrorHandlingStrategy = strategy

def unregister_strategy(name: str) -> bool:
    """
    Unregister an error handling strategy by its name.

    Args:
        name (str): The name of the strategy to unregister

    Returns:
        bool: True if strategy was unregistered, False if not found
    """
    if name in STRATEGY_REGISTRY:
        del STRATEGY_REGISTRY[name]
        return True
    return False


def replace_strategy(name: str, strategy: ErrorHandlingStrategy) -> bool:
    """
    Replace an existing strategy or register a new one if it doesn't exist.

    Args:
        name (str): The name of the strategy to replace
        strategy (ErrorHandlingStrategy): The new strategy

    Returns:
        bool: True if replaced an existing strategy, False if registered new

    Raises:
        TypeError: If strategy is not an ErrorHandlingStrategy instance
    """
    if not isinstance(strategy, ErrorHandlingStrategy):
        raise TypeError("Strategy must be an instance of ErrorHandlingStrategy")

    exists = name in STRATEGY_REGISTRY
    STRATEGY_REGISTRY[name] = strategy
    return exists


def error_handling_strategy(cls):
    """
    Class decorator for ErrorHandlingStrategy. This decorator adds the ability to register the class as an error handling
    strategy.

    Args:
        cls: The class to be decorated.

    Returns:
        The decorated class.

    Examples:
        >>> @error_handling_strategy
        ... class MyStrategy(ErrorHandlingStrategy):
        ...     pass
    """
    register_strategy(cls.__name__, cls)
    return cls