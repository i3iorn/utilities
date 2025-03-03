import logging
from typing import List, Any, Optional, Iterable, Tuple

from src.utilities.logger import get_logger
from src.utilities.error_handler.decorators import error_handler

logger = get_logger(__name__)
logger.debug(logging.INFO)


class ParameterManager:
    def __init__(self):
        self._params: List[Any] = []
        self._cached_query: Optional[str] = None
        self._cached_params: Optional[List[Any]] = None

    @property
    def params(self) -> List[Any]:
        return self._params

    @error_handler("logging", logger=logger)
    def add_param(self, value: Any) -> None:
        self._params.append(value)

    @error_handler("logging", logger=logger)
    def extend(self, values: Iterable[Any]) -> None:
        self._params.extend(values)

    @error_handler("logging", logger=logger)
    def cache(self, query: str) -> None:
        self._cached_query = query
        self._cached_params = self._params.copy()

    @error_handler("logging", logger=logger)
    def get_cached(self) -> Optional[Tuple[str, List[Any]]]:
        if self._cached_query is not None:
            return self._cached_query, self._cached_params
        return None

    @error_handler("logging", logger=logger)
    def generate_placeholders(self) -> str:
        return ", ".join("?" for _ in self._params)

    @staticmethod
    def generate_named_placeholders(column_names: List[str]) -> str:
        return ", ".join(f":{col}" for col in column_names)

    @error_handler("logging", logger=logger)
    def reset_cache(self) -> None:
        self._cached_query = None
        self._cached_params = None
