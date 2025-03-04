from typing import List, Optional, Dict, Any


class CustomError(Exception):
    """
    Base class for custom exceptions.

    Args:
        message (str): The error message to be displayed.

    Attributes:
        message (str): The error message to be displayed.

    Examples:
        >>> raise CustomError("This is a custom error.")
    """
    def __init__(self, message: str):
        """
        Initialize the CustomError with the error message.

        Args:
            message (str): The error message to be displayed.

        Returns:
            None

        Examples:
            >>> raise CustomError("This is a custom error.")
        """
        self.message = message
        super().__init__(self.message)