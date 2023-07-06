import sqlite3
from typing import Any

from mro import exceptions, validators
from mro.columns import BaseColumn
from mro.result_mapper import map_query_result_with_class


class QueryBuilder:
    def __init__(self) -> None:
        self.query = ""
        self.class_table_columns: dict[str, BaseColumn] = {}
        self.class_table_name = ""

    def _set_class_table_values(self) -> None:
        self.class_table_columns = self.class_table.get_columns()
        self.class_table_name = self.class_table.get_class_name()

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "class_table":
            super().__setattr__(__name, __value)
            self._set_class_table_values()
            return
        return super().__setattr__(__name, __value)

    def __getattribute__(self, __name: str) -> Any:
        if __name == "class_table":
            return super().__getattribute__(__name)
        elif not super().__getattribute__("class_table"):
            raise exceptions.ClassTableNotRegistered()
        return super().__getattribute__(__name)

    def insert(self, **kwargs) -> "QueryBuilder":
        validators.validate_class_table_columns(self.class_table, **kwargs)
        validators.validate_class_table_data(self.class_table, **kwargs)

        self.query = f"INSERT INTO {self.class_table_name} ("
        # fix here
        for index, column_name in enumerate(self.class_table_columns.keys()):
            self.query += f"{column_name}"
            if index != len(self.class_table_columns) - 1:
                self.query += ", "
        self.query += ") VALUES ("
        for index, (_) in enumerate(kwargs.values()):
            self.query += "?"
            if index != len(kwargs.values()) - 1:
                self.query += ","

        self.query += ");"
        return self

    def select(
        self,
    ) -> "QueryBuilder":
        self.query = f"SELECT "
        for index, column in enumerate(self.class_table_columns):
            self.query += f'"{column}" '
            if index != len(self.class_table_columns) - 1:
                self.query += ", "
        self.query += f"from {self.class_table_name}"
        return self

    def execute(self, connection: sqlite3.Connection, values: tuple = ()):
        res = connection.cursor().execute(self.query, values)
        connection.commit()
        result = res.fetchall()
        self.query = ""
        if not result:
            return None
        return map_query_result_with_class(self.class_table, result)
