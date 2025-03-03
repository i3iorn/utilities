from typing import List, Any, overload, Union


class Where:
    def __init__(
            self,
            column: str,
            operator: str = None,
            param: Union[int, float, str] = None,
            logical_operator: str = "AND"
    ):
        self.column: str = column
        self.operator: str = operator
        self.param: Union[int, float, str] = param
        self.logical_operator: str = logical_operator

    def build(self) -> str:
        """Return the WHERE condition as a string."""
        if self.operator:
            return f"{self.logical_operator} {self.column} {self.operator} ?"

        if self.param is None:
            return f"{self.logical_operator} {self.column} IS NULL"

        return f"{self.logical_operator} {self.column} = ?"

    def as_dict(self) -> dict:
        """Return the WHERE condition as a dictionary."""
        return {
            "column": self.column,
            "operator": self.operator,
            "param": self.param,
            "logical_operator": self.logical_operator,
            "built": self.build(),
        }


class WhereGroup:
    """Helper class for creating complex WHERE conditions."""
    def __init__(self, logical_operator: str = "AND"):
        self.conditions: List[Where] = []
        self.params: List[Any] = []
        self.logical_operator: str = logical_operator

    @overload
    def add(self, column: str) -> "WhereGroup":
        ...

    @overload
    def add(self, column: str, logical_operator: str) -> "WhereGroup":
        ...

    @overload
    def add(self, column: str, param: Union[int, float, str]) -> "WhereGroup":
        ...

    @overload
    def add(self, column: str, param: Union[int, float, str], logical_operator: str) -> "WhereGroup":
        ...

    @overload
    def add(self, column: str, operator: str, param: Union[int, float, str]) -> "WhereGroup":
        ...

    @overload
    def add(self, column: str, operator: str, param: Union[int, float, str], logical_operator: str) -> "WhereGroup":
        ...

    def add(self, *args, **kwargs) -> "WhereGroup":
        """Add a condition to the group."""
        logical_operator = kwargs.get("logical_operator", "AND")
        if logical_operator not in ("AND", "OR"):
            raise ValueError("Logical operator must be 'AND' or 'OR'.")

        if "?" in args[0] and len(args) == 1 and "param" not in kwargs:
            raise ValueError("Parameter value missing for the condition.")

        if " " in args[0] and "param" in kwargs:
            column, operator, q = args[0].split(" ", 2)
            param = kwargs["param"]

        elif len(args) == 1 and " " in args[0]:
            column, operator, param = args[0].split(" ", 2)
            param = param.strip("'").strip('"')

        elif len(args) == 1:
            column = args[0]
            operator = None
            param = None

        elif len(args) == 2:
            column, param = args
            if " " in column:
                column, operator, q = column.split(" ")
            operator = kwargs.get("operator", None)

        elif len(args) == 3:
            column, operator, param = args

        else:
            raise ValueError("Invalid number of arguments.")

        if str(param).isnumeric():
            param = int(param)

        self.conditions.append(Where(column, operator, param, logical_operator))
        if param is not None:
            self.params.append(param)
        return self

    def get_params(self) -> List[Any]:
        """Retrieve the parameters."""
        return self.params

    def build(self) -> str:
        """Return the complete WHERE condition as a string."""
        if not self.conditions:
            return ""

        where_clause = f" ".join([condition.build() for condition in self.conditions])
        return f"({where_clause.strip().split(' ', 1)[1]})"
