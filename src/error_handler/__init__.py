from dotenv import dotenv_values

dotenv_values()

from .config import ErrorConfig
from .handlers import BaseErrorHandler


ERROR_HANDLER = BaseErrorHandler(ErrorConfig())


def configure_error_handler(config: ErrorConfig) -> None:
    """
    Configure the error handler with the given configuration. This function should be called before using the error
    handler to ensure that the handler is properly configured. If this function is not called, the error handler will
    use the default configuration.

    Make sure that your logger is configured before calling this function as the error handler will use the logger
    set by logging.setLogger().

    Args:
        config (ErrorConfig): The configuration to be used for the error handler.

    Returns:
        None

    Examples:
        >>> configure_error_handler(config)
    """
    global ERROR_HANDLER
    ERROR_HANDLER = BaseErrorHandler(config)


# Decorator to wrap all methods in an error handler
def catch(cls):
    """
    Decorator to wrap all methods in an error handler.

    Args:
        cls: The class to be wrapped.

    Returns:
        The wrapped class.

    Examples:
        >>> @catch
        >>> class MyClass:
        >>>     pass
    """
    def error_handler_method(method):
        def wrapper(*args, **kwargs):
            try:
                return method(*args, **kwargs)
            except Exception as e:
                return ERROR_HANDLER.handle_error(e, func=method,*args, **kwargs)
        return wrapper

    for name, method in cls.__dict__.items():
        if callable(method):
            setattr(cls, name, error_handler_method(method))
    return cls