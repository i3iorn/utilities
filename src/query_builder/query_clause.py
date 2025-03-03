import logging

from src.utilities.query_builder.where import Where, WhereGroup
from src.utilities.logger import get_logger

logger = get_logger(__name__)
logger.setLevel(logging.DEBUG)


class QueryClauseBuilder:
    def add(self, type_, *args):
        if isinstance(args[0], (Where, WhereGroup)):
            if type_ == "where":
                self.where_conditions.append(args[0])
            elif type_ == "having":
                self.having = args[0]
        elif type_ == "limit":
            self.limit += args[0]
        elif type_ == "order_by":
            self.order_by.append(args)
        elif type_ == "group_by":
            self.group_by.extend(args)
        else:
            raise ValueError(f"Invalid type: {type_}")

    def build_query_clauses(self) -> str:
        clauses = []

        if self.where_conditions:
            logger.debug(f"Building where clause with conditions: {self.where_conditions}")
            where_clause = "WHERE " + " AND ".join(condition.build() for condition in self.where_conditions)
            clauses.append(where_clause)
        if self.group_by:
            group_clause = "GROUP BY " + ", ".join(self.group_by)
            if self.having:
                group_clause += " HAVING " + self.having.build()
            clauses.append(group_clause)
        if self.order_by:
            clauses.append("ORDER BY " + ", ".join(f"{col} {direction}" for col, direction in self.order_by))
        if self.limit is not None:
            clauses.append(f"LIMIT {self.limit}")
        if self.offset is not None:
            clauses.append(f"OFFSET {self.offset}")

        return " ".join(clauses)

    def reset_query_clause(self):
        self.where_conditions = None
        self.order_by = []
        self.limit = None
        self.offset = None
        self.group_by = []
        self.having = None
