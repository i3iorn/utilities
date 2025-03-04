import logging
import os
from typing import List, Optional, Set, Dict, Type, Any
from typeguard import typechecked

from . import ErrorConfig
from .exceptions import StrategyAlreadyInUseError, StrategyTypeError, ErrorHandlerException
from .predicates.core import Predicate, PredicateFactory
from .strategies.core import ErrorHandlingStrategy

StrategiesType = List[ErrorHandlingStrategy]


@typechecked
class BaseErrorHandler:
    """
    Base class for error handling. This class is responsible for handling exceptions using a set of strategies.

    Args:
        config (ErrorConfig): The configuration for the error handler.
        strategies (Optional[StrategiesType]): The list of strategies to be used for error handling.

    Attributes:
        strategies (Optional[StrategiesType]): The list of strategies to be used for error handling.
        config (ErrorConfig): The configuration for the error handler.

    Examples:
        >>> handler = BaseErrorHandler(ErrorConfig())
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BaseErrorHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self, config: ErrorConfig, strategies: Optional[StrategiesType] = None):
        """
        Initialize the BaseErrorHandler with the configuration and strategies.

        Args:
            config (ErrorConfig): The configuration for the error handler.
            strategies (Optional[StrategiesType]): The list of strategies to be used for error handling.

        Returns:
            None

        Examples:
            >>> handler = BaseErrorHandler(ErrorConfig())
        """
        self.strategies: Optional[StrategiesType] = strategies
        self.config: ErrorConfig = config
        self._init_logging()
        if os.getenv("ERROR_HANDLER_INCLUDE_DEFAULT_STRATEGIES", "true").lower() == "true":
            self._include_default_strategies()

    def _include_default_strategies(self):
        """
        Include the default error handling strategies. This method is called during initialization to include the
        default strategies if the environment variable ERROR_HANDLER_INCLUDE_DEFAULT_STRATEGIES is set to true.

        Examples:
            >>> handler._include_default_strategies()
        """
        from .strategies.core import DEFAULT_ERROR_HANDLING_STRATEGIES
        self.logger.debug("Including default error handling strategies")

        if not self.strategies:
            self.strategies = []

        self.strategies.extend(DEFAULT_ERROR_HANDLING_STRATEGIES)

    def _init_logging(self):
        """
        Initialize the logger for the error handler.
        """
        self.logger = logging.getLogger("dev.schrammel.error_handler")
        self.logger.setLevel(self.config.log_level)

    def handle_error(self, error: Exception, *args, **kwargs):
        """
        Handle the given error using the error handling strategies. If the error is not handled, it will be re-raised.

        Args:
            error (Exception): The error to be handled.
            args: The arguments to be passed to the error handling strategies.
            kwargs (Dict): The keyword arguments to be passed to the error handling strategies.

        Returns:
            None

        Examples:
            >>> handler.handle_error(error)
        """
        if not self.strategies:
            self.logger.warning("No strategies available to handle the error")

        errors = [error]

        print(f"args: {args}")
        print(f"kwargs: {kwargs}")

        if self.strategies:
            self.sort_strategies()
            for strategy in self.strategies:
                if strategy.can_handle(error) and strategy.is_enabled():
                    self.logger.info(f"Attempting to handle error {error} with strategy {strategy}")
                    print(f"Attempting to handle error {error} with strategy {strategy}")
                    recovered, response = strategy.handle(error, *args, **kwargs)
                    if recovered:
                        self.logger.info(f"Successfully recovered from error {error} using strategy {strategy}")
                        return response
                    else:
                        self.logger.info(f"Failed to recover from error {error} using strategy {strategy}")
                        errors.append(response)

        self.logger.error(f"Failed to handle error: {error}")

        reraise = kwargs.get("reraise", self.config.re_raise)
        if reraise:
            raise error

    def handle_errors(self, errors: List[Exception]):
        """
        Handle the given list of errors using the error handling strategies. If the error is not handled, it will be
        re-raised.

        Args:
            errors (List[Exception]): The list of errors to be handled.

        Returns:
            None

        Examples:
            >>> handler.handle_errors(errors)
        """
        for error in errors:
            self.handle_error(error)

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""
    " Methods for managing error handling strategies
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def clear_strategies(self):
        """
        Clear the list of strategies
        """
        self.strategies.clear()

    def remove_strategy(self, strategy: ErrorHandlingStrategy):
        """
        Remove the given strategy from the list of strategies.
        """
        self.strategies.remove(strategy)

    def add_strategy(self, strategy: Type[ErrorHandlingStrategy], exists_ok: bool = False):
        """
        Add the given strategy to the list of strategies.

        Args:
            strategy (ErrorHandlingStrategy): The strategy to be added.
            exists_ok (bool): If True, the function will drop the strategy if it already exists.

        Raises:
            StrategyTypeError: If the strategy is not an instance of ErrorHandlingStrategy.
            StrategyAlreadyInUseError: If the strategy is already in the list of strategies.

        Examples:
            >>> handler.add_strategy(strategy)
        """
        self.logger.debug(f"User has requested to add strategy {strategy} to the list of strategies")
        if not issubclass(strategy, ErrorHandlingStrategy):
            raise StrategyTypeError("Strategy must be an instance of ErrorHandlingStrategy")

        if not self.strategies:
            self.strategies = []

        self.logger.debug(f"Currently we have the following strategies: {self.strategies}")
        print(f"Currently we have the following strategies: {self.strategies}")

        if strategy not in self.strategies:
            self.strategies.append(strategy)
        elif not exists_ok:
            raise StrategyAlreadyInUseError("Strategy already exists in list of strategies")

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""
    " Methods for sorting strategies by priority
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def sort_strategies(self):
        """
        Sort the list of strategies by priority.

        Examples:
            >>> handler.sort_strategies()
        """
        self.strategies.sort(key=lambda x: x.priority)

    def reverse_strategies(self):
        """
        Reverse the list of strategies.

        Examples:
            >>> handler.reverse_strategies()
        """
        self.strategies.reverse()

    def sort_strategies_by_name(self):
        """
        Sort the list of strategies by name.

        Examples:
            >>> handler.sort_strategies_by_name()
        """
        self.strategies.sort(key=lambda x: x.name)

    def reverse_strategies_by_name(self):
        """
        Reverse the list of strategies by name.

        Examples:
            >>> handler.reverse_strategies_by_name()
        """
        self.strategies.sort(key=lambda x: x.name, reverse=True)

    def enable_strategy(self, strategy: ErrorHandlingStrategy):
        """
        Enable the given strategy. If the strategy is already enabled, this method has no effect.

        Args:
            strategy (ErrorHandlingStrategy): The strategy to be enabled.

        Examples:
            >>> handler.enable_strategy(strategy)
        """
        strategy.enabled = True

    def disable_strategy(self, strategy: ErrorHandlingStrategy):
        """
        Disable the given strategy. If the strategy is already disabled, this method has no effect.

        Args:
            strategy (ErrorHandlingStrategy): The strategy

        Examples:
            >>> handler.disable_strategy(strategy)
        """
        strategy.enabled = False

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""
    " Methods for filtering strategies
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def filter_strategies(self, predicate: Predicate):
        """
        Filter the list of strategies using the given predicate.

        Args:
            predicate (Predicate): The predicate to be used for filtering.

        Returns:
            List[ErrorHandlingStrategy]: The list of strategies that match the predicate.

        Examples:
            >>> handler.filter_strategies(predicate)
        """
        return list(filter(predicate, self.strategies))

    def filter_strategies_by_name(self, name: str) -> List[ErrorHandlingStrategy]:
        """
        Filter the list of strategies by name.

        Args:
            name (str): The name of the strategy.

        Returns:
            List[ErrorHandlingStrategy]: The list of strategies with the given name.

        Examples:
            >>> handler.filter_strategies_by_name(name)
        """
        return self.filter_strategies(
            PredicateFactory.create_predicate(name, lambda x: x.name == name)
        )

    def filter_strategies_by_priority(self, priority: int):
        """
        Filter the list of strategies by priority.

        Args:
            priority (int): The priority of the strategy.

        Returns:
            List[ErrorHandlingStrategy]: The list of strategies with the given priority.

        Examples:
            >>> handler.filter_strategies_by_priority(priority)
        """
        return self.filter_strategies(
            PredicateFactory.create_predicate('priority', lambda x: x.priority == priority)
        )

    def filter_strategies_by_priority_range(self, min_priority: int, max_priority: int):
        """
        Filter the list of strategies by priority range.

        Args:
            min_priority (int): The minimum priority.
            max_priority (int): The maximum priority.

        Returns:
            List[ErrorHandlingStrategy]: The list of strategies with priority in the given range.

        Examples:
            >>> handler.filter_strategies_by_priority_range(min_priority, max_priority)
        """
        return self.filter_strategies(
            PredicateFactory.create_predicate('priority', lambda x: min_priority <= x.priority <= max_priority)
        )
