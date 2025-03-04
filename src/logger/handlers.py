import logging
from typing import Optional


class ConsoleLogHandler(logging.StreamHandler):
    """
    A console (stream) handler for logging messages to standard output.
    """
    def __init__(self, level: int = logging.DEBUG, formatter: Optional[logging.Formatter] = None):
        super().__init__()
        self.setLevel(level)
        if formatter:
            self.setFormatter(formatter)


class FileLogHandler(logging.FileHandler):
    """
    A file handler for logging messages to a specified file.
    """
    def __init__(self, file_path: str, level: int = logging.DEBUG, formatter: Optional[logging.Formatter] = None):
        super().__init__(file_path)
        self.setLevel(level)
        if formatter:
            self.setFormatter(formatter)

