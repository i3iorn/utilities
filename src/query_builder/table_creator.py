import re
from typing import List, Dict, Optional, Set, Any, Union, Iterable, Tuple

from src.utilities.query_builder.base import BuilderBase, DataType, SQLKeywords


class TableCreator(BuilderBase):
    def __init__(
            self,
            table_name: str,
            primary: bool = True,
            created_at: bool = True,
            updated_at: bool = True,
            deleted_at: bool = True,
            meta_columns: bool = True,
            **kwargs
    ):
        super().__init__()
        if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", table_name) is None:
            raise ValueError("Invalid table name.")

        self.table_name = table_name
        self.columns: Dict[str, str] = {}
        self.primary_key: Optional[str] = None
        self.unique_constraints: Set[str] = set()
        self.foreign_keys: List[Dict[str, str]] = []  # [{'column': str, 'ref_table': str, 'ref_column': str}]

        # Add default columns
        if primary and meta_columns:
            self.add_primary_column()

        if created_at and meta_columns:
            self.add_column("created_at", DataType.TIMESTAMP, allow_nulls=True, default="CURRENT_TIMESTAMP")

        if updated_at and meta_columns:
            self.add_column("updated_at", DataType.TIMESTAMP, allow_nulls=True, default="CURRENT_TIMESTAMP")

        if deleted_at and meta_columns:
            self.add_column("deleted_at", DataType.TIMESTAMP, default="NULL")

        self._metadata = {
            "temporary": False,
            "if_not_exists": False,
            "on_conflict": "FAIL"
        }
        self._metadata.update(kwargs)

    def get_metadata(self, key: str) -> str:
        return self._metadata[key]

    def add_metadata(self, key: str, value: Union[str, bool]) -> "TableCreator":
        if key not in self._metadata:
            raise KeyError(f"Metadata key '{key}' not found.")
        self._metadata[key] = value
        return self

    def add_column(
            self,
            name: str,
            data_type: DataType,
            allow_nulls: bool = True,
            default: Optional[Any] = None,
            override: bool = False
    ) -> "TableCreator":
        """Adds a column to the table schema."""

        if name in self.columns and not override:
            raise ValueError(f"Column '{name}' already exists in the table. Use 'override=True' to replace it.")

        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", name):
            raise ValueError(f"Invalid column name '{name}'.")

        if name.upper() in SQLKeywords.all_keywords():
            raise ValueError(f"Column name '{name}' is a reserved keyword.")

        if not isinstance(data_type, DataType):
            raise ValueError(f"Invalid data type '{data_type}'.")

        default_data_types = {
            DataType.INTEGER: int,
            DataType.TEXT: str,
            DataType.REAL: float,
            DataType.BLOB: (bytes, str),
            DataType.NULL: type(None),
            DataType.TIMESTAMP: str
        }

        if default is not None:
            types = default_data_types[data_type]
            if not isinstance(default, (types, type(DataType.NULL))):
                raise ValueError(f"Default value '{default}' does not match data type '{data_type}'.")

        column_definition = f"{name} {data_type}"

        if not allow_nulls:
            column_definition += " NOT NULL"

        if default is not None:
            column_definition += f" DEFAULT {default}"

        self.columns[name] = column_definition
        return self

    def add_primary_column(self, name: str = "id", data_type: DataType = DataType.INTEGER) -> "TableCreator":
        """Adds a primary column to the table schema."""
        self.add_column(name, data_type, False)
        self.set_primary_key(name)
        return self

    def set_primary_key(self, column: str) -> "TableCreator":
        """Sets a column as the primary key."""
        if column not in self.columns:
            raise ValueError(f"Primary key column '{column}' not found in table columns.")
        self.primary_key = column
        return self

    def add_unique_constraint(self, column: str) -> "TableCreator":
        """Adds a unique constraint to a column."""
        self.unique_constraints.add(column)
        return self

    def add_foreign_key(self, column: str, ref_table: str, ref_column: str = "id") -> "TableCreator":
        """Adds a foreign key constraint to a column."""
        if column not in self.columns:
            raise ValueError(f"Foreign key column '{column}' not found in table columns.")

        self.foreign_keys.append({
            "column": column,
            "ref_table": ref_table,
            "ref_column": ref_column
        })
        return self

    def build_query_clauses(self) -> Tuple[str, Iterable]:
        """Generates the SQL query for table creation."""
        if not self.columns or len(self.columns) == 0:
            raise ValueError("No columns defined for the table.")

        # Column definitions
        column_definitions = ", ".join(self.columns.values())

        # Primary key
        if self.primary_key:
            column_definitions += f", PRIMARY KEY ({self.primary_key})"

        # Unique constraints
        for unique in self.unique_constraints:
            column_definitions += f", UNIQUE ({unique})"

        # Foreign keys
        for fk in self.foreign_keys:
            column_definitions += (
                f", FOREIGN KEY ({fk['column']}) REFERENCES {fk['ref_table']} ({fk['ref_column']})"
            )

        parts = [
            "CREATE",
            "TEMPORARY" if self._metadata.get("temporary", False) else "",
            "TABLE",
            "IF NOT EXISTS" if self._metadata.get("if_not_exists", False) else "",
            self.table_name,
            f"({column_definitions})"
        ]
        return " ".join([p for p in parts if len(p) > 0]) + ";",
