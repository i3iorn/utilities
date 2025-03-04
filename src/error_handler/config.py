import logging
import os
from typing import Optional

from typeguard import typechecked


@typechecked
class ErrorConfig:
    def __init__(
            self,
            log_level: Optional[int] = None,
            re_raise: Optional[bool] = None,
    ):
        self.log_level: int = log_level or int(getattr(logging, os.getenv('DEFAULT_LOG_LEVEL', "INFO")))
        self.re_raise: bool = re_raise or os.getenv('DEFAULT_TO_RERAISE_EXCEPTIONS', "false").lower() == "true"
