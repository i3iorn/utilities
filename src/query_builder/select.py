from typing import List, Union, Tuple

from src.utilities.query_builder import BuilderBase
from src.utilities.query_builder.base import QueryType
from src.utilities.query_builder.query_clause import QueryClauseBuilder

OrderByType = Union[Tuple[str, str], str]


class SelectQueryBuilder(BuilderBase):
    def __init__(self, table: str = None, columns: List[str] = None, **kwargs):
        super().__init__(table, query_type=QueryType.SELECT, **kwargs)
        self._joins = None
        self._columns = columns or []

    def limit(self, limit: int) -> "BuilderBase":
        self.clause_builder.limit = limit
        self._state_changed = True
        return self

    def offset(self, offset: int) -> "BuilderBase":
        self.clause_builder.offset = offset
        self._state_changed = True
        return self

    def group_by(self, *columns: str) -> "BuilderBase":
        self.clause_builder.group_by.extend(columns)
        self._state_changed = True
        return self

    def having(self, condition: str) -> "BuilderBase":
        self.clause_builder.having = condition
        self._state_changed = True
        return self

    def order_by(self, *columns: OrderByType) -> "BuilderBase":
        self.clause_builder.order_by.extend(columns)
        self._state_changed = True
        return self

    def join(self, table: str, on_clause: str, join_type: str = "INNER") -> "BuilderBase":
        """
        Add a JOIN clause to the query.

        Args:
            table (str): The table to join.
            on_clause (str): The ON condition for the join.
            join_type (str): Type of join (e.g., INNER, LEFT, RIGHT). Defaults to INNER.
        """
        if not hasattr(self, '_joins'):
            self._joins = []
        self._joins.append(f"{join_type.upper()} JOIN {table} ON {on_clause}")
        self._state_changed = True
        return self

    def _append_joins(self, query: str) -> str:
        if hasattr(self, '_joins') and self._joins:
            query += " " + " ".join(self._joins)
        return query

    def _build(self) -> str:
        query = f"SELECT {', '.join(self._columns)} FROM {self._table} " + self.clause_builder.build_query_clauses()
        query = self._append_joins(query)
        return query

    def _reset(self) -> None:
        self._columns = []
        self._group_by = None
        self._having = None
        self._joins = None
        self.clause_builder = QueryClauseBuilder()
