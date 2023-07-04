import sqlite3
from mro.table import BaseTable
from typing import Type


class BaseClass:
    def __init__(self, sqlite_filename: str, create_table: bool = False) -> None:
        self.sqlite_filename = sqlite_filename
        self.connection = sqlite3.connect(self.sqlite_filename)
        self.cursor = self.connection.cursor()
        self.create_table = create_table
        self.tables: list[Type[BaseTable]] = []

    def _create_tables(self):
        for table in self.tables:
            self.cursor.execute(table.get_table_schema())
        self.connection.commit()

    def register_tables(self, tables: list[Type[BaseTable]]) -> None:
        self.tables = tables
        for table in self.tables:
            table.connection = self.connection
            table.cursor = self.cursor

        if self.create_table:
            self._create_tables()
