
class ErrorHandlerException(Exception):
    """Exception raised for errors in the error handling."""
    pass


class StrategyException(ErrorHandlerException):
    """Base class for exceptions in this module."""
    pass


class StrategyNotImplementedError(StrategyException):
    """Exception raised when a strategy is not implemented."""
    pass


class StrategyTypeError(StrategyException):
    """Exception raised when a strategy is of the wrong type."""
    pass


class StrategyNotFoundError(StrategyException):
    """Exception raised when a strategy is not found."""
    pass


class StrategyAlreadyInUseError(StrategyException):
    """Exception raised when a strategy is already in use."""
    pass


class PredicateException(StrategyException):
    """Exception raised for errors in the predicate function."""
    pass


class PredicateTypeError(PredicateException):
    """Exception raised when the predicate is of the wrong type."""
    pass


class PredicateNotImplementedError(PredicateException):
    """Exception raised when the predicate is not implemented."""
    pass


class PredicateFunctionException(PredicateException):
    """Exception raised when the predicate function is invalid."""
    pass


class PredicateNameError(PredicateException):
    """Exception raised when the predicate name is invalid."""
    pass


class ConfigurationErrorHandlerException(ErrorHandlerException):
    """Exception raised for errors in the configuration."""
    pass
