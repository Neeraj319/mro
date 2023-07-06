import sqlite3
from typing import Type

from mro.table import BaseTable


class BaseClass:
    def __init__(self, sqlite_filename: str, create_table: bool = False) -> None:
        self.sqlite_filename = sqlite_filename
        self.create_table = create_table
        self._tables: list[Type[BaseTable]] = []

    def _create_tables(self):
        connection = sqlite3.connect(self.sqlite_filename)
        cursor = connection.cursor()
        for table in self._tables:
            cursor.execute(table.get_table_schema())
        connection.commit()
        connection.close()

    def register_tables(self, tables: list[Type[BaseTable]]) -> None:
        self._tables = tables
        for table in self._tables:
            table.db.class_table = table

        if self.create_table:
            self._create_tables()

    def __enter__(self) -> sqlite3.Connection:
        self.connection = sqlite3.connect(self.sqlite_filename)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
