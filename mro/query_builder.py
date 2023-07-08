import sqlite3
from typing import Any

from mro import exceptions, validators
from mro.result_mapper import map_query_result_with_class

from .interface import AbstractBaseTable, AbstractQueryBuilder


class QueryBuilder(AbstractQueryBuilder):
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

    def insert(self, **kwargs) -> AbstractQueryBuilder:
        validators.validate_class_table_columns(self.class_table, **kwargs)
        validators.validate_class_table_data(self.class_table, **kwargs)

        self.query = f'INSERT INTO "{self.class_table_name}" ('
        for index, (column_name, _column) in enumerate(
            self.class_table_columns.items()
        ):
            if _column.primary_key and _column.supported_types[0] == int:
                continue

            self.query += f'"{column_name}"'
            if index != len(self.class_table_columns) - 1:
                self.query += ", "
        self.query += ") VALUES ("

        for index, (_column, value) in enumerate(self.class_table_columns.items()):
            if value.primary_key and value.supported_types[0] == int:
                continue
            if value.null and kwargs.get(_column) is None:
                value = None
            self.query += "?"
            self.query_paramets.append(kwargs.get(_column))
            if index != len(self.class_table_columns) - 1:
                self.query += ", "

        self.query += ");"
        return self

    def select(
        self,
    ) -> AbstractQueryBuilder:
        self.query = f"SELECT "
        for index, column in enumerate(self.class_table_columns):
            self.query += f'"{column}" '
            if index != len(self.class_table_columns) - 1:
                self.query += ", "
        self.query += f"from {self.class_table_name}"
        return self

    def execute(self, connection: sqlite3.Connection) -> None | list[AbstractBaseTable]:
        try:
            res = connection.cursor().execute(self.query, tuple(self.query_paramets))
        except sqlite3.IntegrityError as e:
            raise exceptions.IntegrityError(e)
        except sqlite3.InterfaceError:
            raise exceptions.SqliteInterfaceErro(
                "Interface error due to bug in sqlite3 api"
            )

        connection.commit()
        result = res.fetchall()
        self.query = ""
        self.query_paramets = []
        if not result:
            return None
        return map_query_result_with_class(self.class_table, result)
