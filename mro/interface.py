import sqlite3
from abc import ABC, abstractmethod
from typing import Any, Type


class AbstractBaseColumn(ABC):
    def __init__(self, null: bool = False, primary_key: bool = False) -> None:
        self.null = null
        self.primary_key = primary_key

    @abstractmethod
    def get_schema(self) -> str:
        ...

    @classmethod
    @abstractmethod
    def get_class_name(cls) -> str:
        ...

    @property
    @abstractmethod
    def supported_types(self) -> tuple[Any]:
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


class AbstractQueryBuilder(ABC):
    class_table: Type[AbstractBaseTable]

    def __init__(self) -> None:
        self.query = ""
        self.class_table_columns: dict[str, AbstractBaseColumn] = {}
        self.class_table_name = ""
        self.query_paramets = []

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
    def _set_class_table_values(self) -> None:
        ...


class AbstractDatabaseManager(ABC):
    @abstractmethod
    def register_tables(self, table: Type[AbstractBaseTable]) -> None:
        ...

    @abstractmethod
    def __enter__(self) -> sqlite3.Connection:
        ...

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        ...
