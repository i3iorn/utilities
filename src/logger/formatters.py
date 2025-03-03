import logging


class CustomFormatter(logging.Formatter):
    """
    A custom formatter that enriches log messages with additional metadata.
    It formats extra contextual data (passed via the 'custom' keyword) into a
    human-readable string.
    """
    def format(self, record: logging.LogRecord) -> str:
        # If extra contextual data is provided, attach it as a formatted string.
        if hasattr(record, "custom_context") and record.custom_context:
            record.custom = " ".join(f"{k}={v}" for k, v in record.custom_context.items())
        else:
            record.custom = ""
        return super().format(record)
