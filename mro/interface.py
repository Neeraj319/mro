import sqlite3
from abc import ABC, abstractmethod, abstractproperty
from typing import Any, NewType, Type


class WhereClause(str):
    """
    Used to represent a where clause in a query
    """


where_clause = NewType("where_clause", WhereClause)


class AbstractBaseColumn(ABC):
    query_builder: "AbstractQueryBuilder"
    column_name: str

    def __init__(
        self,
        null: bool = False,
        primary_key: bool = False,
        unique: bool = False,
        default: (str | bool | int | float | None) = None,
    ) -> None:
        self.null = null
        self.primary_key = primary_key
        self.unique = unique

        self.default = default

    @abstractmethod
    def get_schema(self) -> str:
        ...

    @abstractproperty
    def supported_types(self) -> tuple[Any]:
        if self.null:
            return (None,)
        else:
            return tuple()


class AbstractBaseTable(ABC):
    db: "AbstractQueryBuilder"

    @classmethod
    @abstractmethod
    def get_table_schema(cls) -> str:
        ...

    @classmethod
    @abstractmethod
    def get_columns(cls) -> dict[str, AbstractBaseColumn]:
        ...

    @classmethod
    @abstractmethod
    def get_class_name(cls) -> str:
        ...

    @classmethod
    @abstractmethod
    def _inject_query_builder_to_columns(cls):
        ...

    @classmethod
    @abstractmethod
    def _inject_cloumn_name_to_columns(cls):
        ...


class AbstractQueryBuilder(ABC):
    class_table: Type[AbstractBaseTable]

    def __init__(self) -> None:
        self.query = ""
        self.class_table_columns: dict[str, AbstractBaseColumn] = {}
        self.class_table_name = ""
        self.query_parameters = []

    @abstractmethod
    def insert(self, **kwargs) -> "AbstractQueryBuilder":
        ...

    @abstractmethod
    def select(self) -> "AbstractQueryBuilder":
        ...

    @abstractmethod
    def execute(self, connection: sqlite3.Connection):
        ...

    @abstractmethod
    def where(self, clause) -> "AbstractQueryBuilder":
        ...

    @abstractmethod
    def and_(self, __value: object) -> "AbstractQueryBuilder":
        ...

    @abstractmethod
    def or_(self, __value: object) -> "AbstractQueryBuilder":
        ...

    @abstractmethod
    def _set_class_table_values(self) -> None:
        ...

    @abstractmethod
    def _clear(self) -> None:
        ...


class AbstractConnectionManger(ABC):
    sqlite_filename: str

    def __init__(self, sqlite_filename: str) -> None:
        self.sqlite_filename: str = sqlite_filename

    @abstractmethod
    def __enter__(self) -> sqlite3.Connection:
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...


class AbstractDatabaseManager(ABC):
    @abstractmethod
    def register_tables(self, table: Type[AbstractBaseTable]) -> None:
        ...

    @abstractmethod
    def get_connection(self) -> sqlite3.Connection:
        ...
