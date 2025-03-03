import logging
from typing import Optional, Dict, Any

from src.utilities.logger.formatters import CustomFormatter
from src.utilities.logger.handlers import ConsoleLogHandler, FileLogHandler


class CustomLogger(logging.Logger):
    """
    A custom logger that extends the built-in logging.Logger to support passing
    extra contextual data via a dedicated keyword argument 'custom'. This ensures
    that each log record can carry additional metadata (e.g., user info, module tags).
    """
    def debug(self, msg, *args, custom: Optional[Dict[str, Any]] = None, **kwargs):
        if custom:
            kwargs.setdefault("extra", {})["custom_context"] = custom
        super().debug(msg, *args, **kwargs)

    def info(self, msg, *args, custom: Optional[Dict[str, Any]] = None, **kwargs):
        if custom:
            kwargs.setdefault("extra", {})["custom_context"] = custom
        super().info(msg, *args, **kwargs)

    def warning(self, msg, *args, custom: Optional[Dict[str, Any]] = None, **kwargs):
        if custom:
            kwargs.setdefault("extra", {})["custom_context"] = custom
        super().warning(msg, *args, **kwargs)

    def error(self, msg, *args, custom: Optional[Dict[str, Any]] = None, **kwargs):
        if custom:
            kwargs.setdefault("extra", {})["custom_context"] = custom
        super().error(msg, *args, **kwargs)

    def critical(self, msg, *args, custom: Optional[Dict[str, Any]] = None, **kwargs):
        if custom:
            kwargs.setdefault("extra", {})["custom_context"] = custom
        super().critical(msg, *args, **kwargs)

# Configure the logging module to use our CustomLogger.
logging.setLoggerClass(CustomLogger)


def get_logger(name: str) -> logging.Logger:
    """
    Retrieve a custom logger instance by name.
    """
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    # Create a custom formatter that includes timestamp, log level, module, function,
    # line number, message, and any extra custom context.
    console_formatter = CustomFormatter(
        fmt="%(name)32s:%(lineno)d | %(levelname)8s | %(message)s %(custom)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_formatter = CustomFormatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(module)s:%(lineno)3d | %(message)s %(custom)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Create and register output handlers.
    console_handler = ConsoleLogHandler(level=logging.DEBUG, formatter=console_formatter)
    file_handler = FileLogHandler(file_path="application.log", level=logging.INFO, formatter=file_formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


if __name__ == "__main__":
    # Instantiate our custom logger.
    logger = logging.getLogger("MyCustomLogger")
    logger.setLevel(logging.DEBUG)

    # Create a custom formatter that includes timestamp, log level, module, function,
    # line number, message, and any extra custom context.
    formatter = CustomFormatter(
        fmt="%(asctime)s | %(levelname)8s | %(name)16s | %(module)s:%(lineno)d | %(message)s %(custom)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Create and register output handlers.
    console_handler = ConsoleLogHandler(level=logging.DEBUG, formatter=formatter)
    file_handler = FileLogHandler(file_path="application.log", level=logging.INFO, formatter=formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Log messages at various levels with extra contextual data.
    logger.debug("Debug message", custom={"user": "alice", "operation": "init"})
    logger.info("Application started", custom={"module": "main", "status": "started"})
    logger.warning("Potential configuration issue", custom={"warning_code": 101})
    logger.error("An error occurred", custom={"error_code": 500})
    logger.critical("Critical failure encountered", custom={"shutdown": True})
