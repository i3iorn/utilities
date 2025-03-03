from typing import List, Optional, Dict, Any


class RGSException(Exception):
    """Base exception class for the RGS package."""
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        self.message = message
        self.context = context or {}
        super().__init__(message)

    def __str__(self):
        context_str = f" | Context: {self.context}" if self.context else ""
        return f"{self.message}{context_str}"


class HTTPRequestError(RGSException):
    """Exception raised when an HTTP request fails."""
    def __init__(
            self,
            message: str,
            status_code: int,
            method: str,
            status_text: str,
            context: Optional[Dict[str, Any]] = None
    ):
        self.status_code = status_code
        self.method = method
        self.status_text = status_text
        super().__init__(message, context)


class DataValidationError(ValueError):
    """
    Exception raised when data validation fails.

    Attributes:
        errors (List[str]): A list of error messages.
    """

    def __init__(self, errors: List[str]) -> None:
        message = "Data validation errors: " + "; ".join(errors)
        super().__init__(message)
        self.errors = errors
