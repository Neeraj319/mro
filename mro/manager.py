import sqlite3
from typing import Type

from mro import query_builder

from .interface import (
    AbstractBaseTable,
    AbstractConnectionManger,
    AbstractDatabaseManager,
)
from .validators import extras


class ConnectionManager(AbstractConnectionManger):
    def __enter__(self) -> sqlite3.Connection:
        self.connection = sqlite3.connect(
            self.sqlite_filename,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


class DatabaseManger(AbstractDatabaseManager):
    def __init__(self, sqlite_filename: str, create_tables: bool = False) -> None:
        self.create_tables = create_tables
        self._tables: list[Type[AbstractBaseTable]] = []
        self._connection_manager = ConnectionManager(sqlite_filename)

    def _create_tables(self):
        with self._connection_manager as connection:
            cursor = connection.cursor()
            for table in self._tables:
                cursor.execute(table.get_table_schema())
            connection.commit()

    def get_connection(self) -> AbstractConnectionManger:
        return self._connection_manager

    def register_tables(self, tables: list[Type[AbstractBaseTable]]) -> None:
        self._tables = tables
        for table in self._tables:
            table.db = query_builder.QueryBuilder()
            table.db.class_table = table
            table._inject_query_builder_to_columns()
            table._inject_cloumn_name_to_columns()
            extras.validate(table)

        if self.create_tables:
            self._create_tables()
