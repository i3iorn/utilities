from src.utilities.logger import get_logger
from src.utilities.query_builder import BuilderBase
from src.utilities.query_builder.base import QueryType
from src.utilities.query_builder.query_clause import QueryClauseBuilder
from src.utilities.error_handler.decorators import error_handler

logger = get_logger(__name__)


class DeleteQueryBuilder(BuilderBase):
    def __init__(self, table: str = None, clause_builder: QueryClauseBuilder = None):
        super().__init__(table, query_type=QueryType.DELETE)
        self.clause_builder = clause_builder

    @error_handler("logging", logger=logger)
    def _build(self) -> str:
        query = f"DELETE FROM {self._table} " + self.clause_builder.build_query_clauses()
        return query

    def _reset(self) -> None:
        pass
