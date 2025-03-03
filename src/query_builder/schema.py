from typing import Tuple

from .base import BuilderBase
from .table_creator import TableCreator


class SchemaBuilder(BuilderBase):
    def create_table(self, table_name: str, **kwargs) -> "TableCreator":
        return TableCreator(table_name, **kwargs)

    def create_view(self, name: str, select_query: str) -> str:
        return f"CREATE VIEW {name} AS {select_query}"

    def create_trigger(self, name: str, event: str, table: str, action: str) -> str:
        return f"CREATE TRIGGER {name} {event} ON {table} FOR EACH ROW {action}"

    def create_index(self, name: str, table: str, columns: Tuple[str, ...], unique: bool = False) -> str:
        unique_str = "UNIQUE" if unique else ""
        columns_str = ", ".join(columns)
        return f"CREATE {unique_str} INDEX {name} ON {table} ({columns_str})"

    def drop_table(self, table_name: str) -> str:
        return f"DROP TABLE {table_name}"

    def drop_view(self, view_name: str) -> str:
        return f"DROP VIEW {view_name}"

    def drop_trigger(self, trigger_name: str) -> str:
        return f"DROP TRIGGER {trigger_name}"

    def drop_index(self, index_name: str) -> str:
        return f"DROP INDEX {index_name}"
