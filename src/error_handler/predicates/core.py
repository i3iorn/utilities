import logging
from abc import ABC, abstractmethod
from typing import Callable

from typeguard import typechecked

from ..exceptions import PredicateFunctionException, PredicateNameError
from ..strategies.core import ErrorHandlingStrategy

logger = logging.getLogger(__name__)


@typechecked
class BasePredicate(ABC):
    """
    Abstract base class for error handling strategy predicates that determine if a strategy should be used.
    """
    def __init__(self, name: str):
        self.name: str = name

    @abstractmethod
    def __call__(self, strategy: ErrorHandlingStrategy) -> bool:
        pass

    @abstractmethod
    def predicate(self, strategy: ErrorHandlingStrategy) -> bool:
        pass


@typechecked
class Predicate(BasePredicate):
    """
    A predicate that determines if a strategy should be used.
    """
    def __call__(self, strategy: ErrorHandlingStrategy) -> bool:
        return self.predicate(strategy)

    @abstractmethod
    def predicate(self, strategy: ErrorHandlingStrategy) -> bool:
        pass


@typechecked
class PredicateFactory:
    @staticmethod
    def create_predicate(name: str, func_: Callable) -> Predicate:
        if not isinstance(name, str):
            raise PredicateNameError("Name must be a string.")

        if not callable(func_):
            raise PredicateFunctionException("Function must be callable.")

        class CustomPredicate(Predicate):
            def predicate(self, strategy: ErrorHandlingStrategy) -> bool:
                return func_(strategy)

        return CustomPredicate(name)
