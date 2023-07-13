import datetime
import sqlite3
from abc import ABC, abstractmethod, abstractproperty
from typing import Any, Type


class AbstractBaseColumn(ABC):
    """
    Use this class to create a column for a table.
    Also known as Class Column.
    """

    query_builder: "AbstractQueryBuilder"
    column_name: str

    def __init__(
        self,
        null: bool = False,
        primary_key: bool = False,
        unique: bool = False,
        default: (str | bool | int | float | None | datetime.datetime) = None,
    ) -> None:
        self.null = null
        self.primary_key = primary_key
        self.unique = unique

        self.default = default

    @abstractmethod
    def get_schema(self) -> str:
        """
        Returns the schema of the column.
        """
        ...

    @abstractproperty
    def supported_types(self) -> tuple[Any]:
        """
        Returns the supported types for the class column.
        """
        if self.null:
            return (None,)
        else:
            return tuple()


class AbstractBaseTable(ABC):
    """
    Use this class to create a table.
    Also known as Class Table.
    """

    db: "AbstractQueryBuilder"

    @classmethod
    @abstractmethod
    def get_table_schema(cls) -> str:
        """
        Returns the schema of the table.
        """
        ...

    @classmethod
    @abstractmethod
    def get_columns(cls) -> dict[str, AbstractBaseColumn]:
        """
        Returns the class columns of the class table.
        """
        ...

    @classmethod
    @abstractmethod
    def get_class_name(cls) -> str:
        """
        Returns the `db` name of the class table.
        """
        ...

    @classmethod
    @abstractmethod
    def _inject_query_builder_to_columns(cls):
        """
        Injects the `db` (query builder) to the class columns.
        """
        ...

    @classmethod
    @abstractmethod
    def _inject_cloumn_name_to_columns(cls):
        """
        Injects the `column_name` to the class columns.
        """
        ...


class AbstractQueryBuilder(ABC):
    """
    Query builder class used to build queries.
    is seen as `.db` of a class table.
    """

    class_table: Type[AbstractBaseTable]

    def __init__(self) -> None:
        self.query = ""
        self.class_table_columns: dict[str, AbstractBaseColumn] = {}
        self.class_table_name = ""
        self.query_parameters = []

    @abstractmethod
    def insert(self, **kwargs) -> "AbstractQueryBuilder":
        """
        Insert a row into the table.
        example: `Blog.db.insert(title="Hello").execute(connection)`

        :param kwargs: kwargs must be a class column of the class table.
        """
        ...

    @abstractmethod
    def select(self) -> "AbstractQueryBuilder":
        """
        Select all rows from the table.
        """
        ...

    @abstractmethod
    def execute(self, connection: sqlite3.Connection) -> None | list[AbstractBaseTable]:
        """
        Execute the chained queries.
        example: `Blog.db.select().where(Blog.id == 4).execute(connection)`

        :param connection: sqlite3 connection
        """
        ...

    @abstractmethod
    def where(self, clause) -> "AbstractQueryBuilder":
        """
        Adds a where clause to the query.
        example: `Blog.db.select().where(Blog.id == 4).execute(connection)`

        :param clause: example `Blog.title == "Hello"`
        """
        ...

    @abstractmethod
    def and_(self, __value: object) -> "AbstractQueryBuilder":
        """
        Adds a AND clause to the query.

        :param __value: example `Blog.views > 4`
        """
        ...

    @abstractmethod
    def or_(self, __value: object) -> "AbstractQueryBuilder":
        """
        Adds a OR clause to the query.

        :param __value: example `Blog.likes == 1000`
        """
        ...

    @abstractmethod
    def _set_class_table_values(self) -> None:
        ...

    @abstractmethod
    def _clear(self) -> None:
        """
        Clears the query builder.
        """
        ...

    @abstractmethod
    def update(self, **kwargs) -> "AbstractQueryBuilder":
        """
        Update row(s) in the table.
        example `Blog.db.update(title="Hello").where(Blog.id == 4).execute(connection)`

        :param kwargs: kwargs must be a class column of the class table.
        """
        ...

    @abstractmethod
    def delete(self) -> "AbstractQueryBuilder":
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
    """
    Use this class to get a connection to the database.
    It also bootstraps the tables and columns.
    """

    @abstractmethod
    def register_tables(self, tables: list[Type[AbstractBaseTable]]) -> None:
        """
        Used internally to register the tables.
        """
        ...

    @abstractmethod
    def get_connection(self) -> sqlite3.Connection:
        """
        Returns a connection to the database.
        """
        ...
