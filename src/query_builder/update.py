from typing import Dict, Any

from src.utilities.query_builder import BuilderBase
from src.utilities.query_builder.base import QueryType
from src.utilities.query_builder.query_clause import QueryClauseBuilder

ColumnData = Dict[str, Any]


class UpdateQueryBuilder(BuilderBase):
    def __init__(self, table: str = None, clause_builder: QueryClauseBuilder = None, **data: ColumnData):
        super().__init__(table, query_type=QueryType.UPDATE)
        self.clause_builder = clause_builder
        for column, value in data.items():
            self._columns.append(column)
            self.param_manager.add_param(value)

    def _build(self) -> str:
        set_clause = ", ".join([f"{col} = ?" for col in self._columns])
        query = f"UPDATE {self._table} SET {set_clause} " + self.clause_builder.build_query_clauses()
        return query
