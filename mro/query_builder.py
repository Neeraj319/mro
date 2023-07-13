import sqlite3
from typing import Any

from mro import exceptions, parsers
from mro.result_mapper import map_query_result_with_class
from mro.validators import query_validators

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
        query_validators.validate(self.class_table, **kwargs)
        parsers.parse(self.class_table, kwargs)

        self.query = f'INSERT INTO "{self.class_table_name}" ('
        for index, (column_name, _column) in enumerate(
            self.class_table_columns.items()
        ):
            if _column.primary_key and _column.supported_types[0] == int:
                continue
            if _column.default and kwargs.get(column_name) is None:
                continue

            self.query += f'"{column_name}"'
            if index != len(self.class_table_columns) - 1:
                self.query += ", "
        self.query += ") VALUES ("

        for index, (_column, value) in enumerate(self.class_table_columns.items()):
            if value.default and kwargs.get(_column) is None:
                continue
            if value.primary_key and value.supported_types[0] == int:
                continue
            if value.null and kwargs.get(_column) is None:
                value = None
            self.query += "?"
            self.query_parameters.append(kwargs.get(_column))
            if index != len(self.class_table_columns) - 1:
                self.query += ", "

        self.query += ");"

        l_right_paren = self.query.rfind(")")
        l_left_paren = self.query.rfind("(")
        f_right_paren = self.query.find(")")
        f_left_paren = self.query.find("(")
        if l_right_paren - l_left_paren == 1 and f_right_paren - f_left_paren == 1:
            self.query = f'INSERT INTO "{self.class_table_name}" DEFAULT VALUES;'

        return self

    def and_(self, __value: object) -> "QueryBuilder":
        self.query += f" AND {__value}"
        return self

    def or_(self, __value: object) -> "QueryBuilder":
        self.query += f" OR {__value}"
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

    def where(self, clause) -> AbstractQueryBuilder:
        self.query += " WHERE "
        self.query += clause
        return self

    def update(self, **kwargs) -> AbstractQueryBuilder:
        query_validators.validate(self.class_table, **kwargs)
        query_validators.update_query_validate(**kwargs)

        self.query = f'UPDATE "{self.class_table_name}" SET '
        for index, (column_name, value) in enumerate(kwargs.items()):
            if (
                self.class_table_columns[column_name].primary_key
                and self.class_table_columns[column_name].supported_types[0] == int
            ):
                continue

            self.query += f'"{column_name}" = ?'
            self.query_parameters.append(value)
            if index != len(kwargs) - 1:
                self.query += ", "

        return self

    def delete(self) -> AbstractQueryBuilder:
        self.query = f'DELETE FROM "{self.class_table_name}"'
        return self

    def _clear(self):
        self.query = ""
        self.query_parameters = []

    def execute(self, connection: sqlite3.Connection) -> None | list[AbstractBaseTable]:
        try:
            res = connection.cursor().execute(self.query, tuple(self.query_parameters))
        except sqlite3.IntegrityError as e:
            raise exceptions.IntegrityError(e)
        except sqlite3.InterfaceError:
            raise exceptions.SqliteInterfaceError(
                "Interface error due to bug in sqlite3 api"
            )
        except sqlite3.OperationalError as e:
            raise exceptions.OperationalError(
                f"class table: `{self.class_table_name}`, {e}"
            )

        connection.commit()
        result = res.fetchall()
        self._clear()
        if not result:
            return None
        return map_query_result_with_class(self.class_table, result)
