from enum import Enum, auto

from .base import DataType, BuilderBase
from .select import SelectQueryBuilder
from .delete import DeleteQueryBuilder
from .update import UpdateQueryBuilder
from .insert import InsertQueryBuilder
from .schema import SchemaBuilder
from .trigger import TriggerBuilder


TEXT = DataType.TEXT
INTEGER = DataType.INTEGER
REAL = DataType.REAL
BLOB = DataType.BLOB
NULL = DataType.NULL
TIMESTAMP = DataType.TIMESTAMP

CURRENT_TIMESTAMP = "CURRENT_TIMESTAMP"

BUILDER_CLASSES = [
    SelectQueryBuilder,
    InsertQueryBuilder,
    UpdateQueryBuilder,
    DeleteQueryBuilder,
    SchemaBuilder,
    TriggerBuilder
]


class QueryBuilderMeta(type):
    def __getattr__(cls, item):
        """
        Dynamically resolves attribute access for the class itself.

        Args:
            item: The attribute being accessed.

        Returns:
            The corresponding method or attribute from one of the builder classes.

        Raises:
            AttributeError: If the attribute is not found in any of the builders.
        """
        for class_ in BUILDER_CLASSES:
            if hasattr(class_, item):
                return getattr(class_, item)
        raise AttributeError(f"'{cls.__name__}' object has no attribute '{item}'")


class Builder(metaclass=QueryBuilderMeta):
    def __new__(cls, *args, **kwargs):
        raise NotImplementedError("This class is not meant to be instantiated. Use the factory methods instead.")

    @staticmethod
    def select(*args, **kwargs) -> SelectQueryBuilder:
        """Factory method for SELECT operations."""
        return SelectQueryBuilder(*args, **kwargs)

    @staticmethod
    def insert(*args, **kwargs) -> InsertQueryBuilder:
        """Factory method for INSERT operations."""
        return InsertQueryBuilder(*args, **kwargs)

    @staticmethod
    def update(*args, **kwargs) -> UpdateQueryBuilder:
        """Factory method for UPDATE operations."""
        return UpdateQueryBuilder(*args, **kwargs)

    @staticmethod
    def delete(*args, **kwargs) -> DeleteQueryBuilder:
        """Factory method for DELETE operations."""
        return DeleteQueryBuilder(*args, **kwargs)

    @staticmethod
    def schema() -> SchemaBuilder:
        """Factory method for schema-related operations."""
        return SchemaBuilder()

    @staticmethod
    def trigger() -> TriggerBuilder:
        """Factory method for trigger operations."""
        return TriggerBuilder()
