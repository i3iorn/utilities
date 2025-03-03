import logging

from src.logger import get_logger
import re
from abc import abstractmethod
from enum import Enum, auto
from typing import Optional, List, Any, Union, Tuple

from .parameter_manager import ParameterManager
from .query_clause import QueryClauseBuilder
from src.error_handler.decorators import error_handler

logger = get_logger(__name__)
logger.setLevel(logging.INFO)


class QueryType(Enum):
    """Enum for query types."""
    SELECT = auto()
    INSERT = auto()
    UPDATE = auto()
    DELETE = auto()

    def __str__(self) -> str:
        return self.name.upper()

    @classmethod
    @error_handler("logging", logger=logger)
    def from_string(cls, query_type: str) -> "QueryType":
        logger.debug(f"Getting query type from string: {query_type}")
        try:
            return cls[query_type.upper()]
        except KeyError:
            raise ValueError(f"Unknown query type: {query_type}")


class SQLKeywords:
    SELECT = ["SELECT", "FROM", "WHERE", "ORDER BY", "LIMIT", "OFFSET"]
    INSERT = ["INSERT INTO", "VALUES"]
    UPDATE = ["UPDATE", "SET", "WHERE"]
    DELETE = ["DELETE FROM", "WHERE"]

    @classmethod
    def all_keywords(cls) -> List[str]:
        return cls.SELECT + cls.INSERT + cls.UPDATE + cls.DELETE

    @classmethod
    def query_types(cls) -> List[QueryType]:
        return [QueryType.SELECT, QueryType.INSERT, QueryType.UPDATE, QueryType.DELETE]

    @classmethod
    def operators(cls) -> List[str]:
        return ["=", "!=", ">", "<", ">=", "<=", "IS", "IS NOT", "LIKE", "IN", "BETWEEN", "NOT IN", "NOT LIKE",
                "NOT BETWEEN"]


TABLE_NAME_REGEX = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")

QueryParam = Union[str, int, float, bool]


class QueryBuilderError(Exception):
    """Exception raised for errors in the query builder."""
    pass


class DataType(Enum):
    """Enum for column types."""
    TEXT = auto()
    INTEGER = auto()
    REAL = auto()
    BLOB = auto()
    NULL = auto()
    TIMESTAMP = auto()

    def __str__(self) -> str:
        return self.name.upper()

    @classmethod
    @error_handler("logging", logger=logger)
    def from_string(cls, type_str: str) -> "DataType":
        try:
            return cls[type_str.upper()]
        except KeyError:
            raise ValueError(f"Unknown data type: {type_str}")

    def is_null(self):
        return self != DataType.NULL


class BuilderBase(QueryClauseBuilder, ParameterManager):
    """Base class for all query builders."""

    def __init__(
            self,
            table: str = None,
            columns: List[str] = None,
            query_type: Optional[QueryType] = None,
            where_group: "WhereGroup" = None,
            order_by: List[Tuple[str, str]] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            group_by: List[str] = None,
            having: str = None,
    ):
        super().__init__()

        self._columns = columns or []
        self._table: Optional[str] = table
        self._state_changed = True
        self._query_type: Optional[QueryType] = query_type
        self._where_conditions = [where_group] if where_group else []
        self._order_by = order_by or []
        self._limit = limit
        self._offset = offset
        self._group_by = group_by or []
        self._having = having or []

    @error_handler("logging", logger=logger)
    def build_query_clauses(self) -> Tuple[str, list]:
        cached = self.get_cached()
        if not self._state_changed and cached:
            return cached

        if not self._table:
            raise QueryBuilderError("No table specified")

        try:
            query = self._build()
        except Exception as e:
            raise QueryBuilderError(f"Query building failed with error: {e}") from e

        self.cache(query)
        logger.debug(f"Built query: {query} with params: {self.params}")
        return query, self.params

    @error_handler("logging", logger=logger)
    def where(self, where_group: "WhereGroup") -> "BuilderBase":
        self.add("where", where_group)
        self.extend(where_group.get_params())
        self._state_changed = True
        return self

    @error_handler("logging", logger=logger)
    def _append_group_by(self, query: str) -> str:
        if hasattr(self, '_group_by') and self._group_by:
            query += " GROUP BY " + ", ".join(self._group_by)
            if hasattr(self, '_having'):
                query += " HAVING " + self._having
        self._state_changed = True
        return query

    @abstractmethod
    def _build(self) -> str:
        """Build the query."""
        pass

    @error_handler("logging", logger=logger)
    def execute(self, db: "Database") -> Any:
        """Execute the query."""
        return db.execute(*self.build_query_clauses())

    @staticmethod
    def _validate_table_name(table: str) -> None:
        if not TABLE_NAME_REGEX.match(table):
            raise QueryBuilderError(f"Invalid table name: {table}")

    @error_handler("logging", logger=logger)
    def table(self, table: str) -> "BuilderBase":
        """Set the table name for the query."""
        self._validate_table_name(table)
        self._table = table
        return self

    @error_handler("logging", logger=logger)
    def reset(self) -> "BuilderBase":
        """
        Reset the builder's internal state to prepare for a new query. The table is not reset to allow for
        chaining of queries on the same table.

        Returns:
            BuilderBase: The builder instance.
        """
        self._query_type = None
        self._state_changed = False
        self.reset_cache()
        self.reset_query_clause()
        self._reset()
        return self

    @abstractmethod
    def _reset(self) -> None:
        """Reset the builder's internal state."""
        pass


