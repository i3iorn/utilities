from enum import Enum, auto
from typing import Optional, Dict, Any

from src.utilities.logger import get_logger
from src.utilities.query_builder import BuilderBase
from src.utilities.query_builder.base import QueryType
from src.utilities.error_handler.decorators import error_handler

ColumnData = Dict[str, Any]

logger = get_logger(__name__)


class ConflictStrategy(Enum):
    """Enum for ON CONFLICT strategies."""
    IGNORE = auto()
    REPLACE = auto()
    ROLLBACK = auto()
    ABORT = auto()
    FAIL = auto()

    def __str__(self) -> str:
        return self.name.upper()


class InsertQueryBuilder(BuilderBase):
    def __init__(self, table: str = None, on_conflict: Optional[str] = None, **data: ColumnData):
        super().__init__(table, query_type=QueryType.INSERT)
        self._on_conflict = on_conflict
        for column, value in data.items():
            self._columns.append(column)
            self.add_param(value)

    @error_handler("logging", logger=logger)
    def on_conflict(self, action: ConflictStrategy) -> "BuilderBase":
        """Set the ON CONFLICT clause (https://www.sqlite.org/lang_conflict.html)"""
        if action not in ConflictStrategy:
            raise ValueError(f"Invalid ON CONFLICT strategy '{action}'.")
        self._on_conflict = action
        self._state_changed = True
        return self

    @error_handler("logging", logger=logger)
    def on_conflict_ignore(self) -> "BuilderBase":
        """Set the ON CONFLICT clause to IGNORE (https://www.sqlite.org/lang_conflict.html)"""
        return self.on_conflict(ConflictStrategy.IGNORE)

    @error_handler("logging", logger=logger)
    def _build(self) -> str:
        columns = ", ".join(self._columns)
        placeholders = self.generate_placeholders()
        conflict_clause = f" OR {self._on_conflict}" if self._on_conflict else ""
        query = f"INSERT{conflict_clause} INTO {self._table} ({columns}) VALUES ({placeholders})"
        return query

    @error_handler("logging", logger=logger)
    def _reset(self) -> None:
        self._table = None
        self._data = {}
        self._on_conflict = None
        self._state_changed = False
