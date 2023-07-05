from typing import Any
from mro import columns, exceptions
import sqlite3
from mro import query_builder


class BaseTable:
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    @classmethod
    def get_table_schema(cls) -> str:
        _class_dict = cls.__dict__
        table_name = cls.__name__.lower()
        schema = f'CREATE TABLE IF NOT EXISTS "{table_name}" ('

        table_columns = list(
            filter(
                lambda x: issubclass(x[1].__class__, columns.BaseColumn),
                _class_dict.items(),
            )
        )
        if len(table_columns) == 0:
            raise exceptions.ClassTableIsMissingColumnAttributes()

        for index, (column_name, column) in enumerate(table_columns):
            schema += column.get_schema() % {"column_name": column_name}
            if index != len(table_columns) - 1:
                schema += ", "

        return f"{schema});"

    @classmethod
    def insert(cls, **kwargs: Any):
        for key in kwargs.keys():
            if key not in cls.__dict__.keys():
                raise exceptions.InvalidColumnAttribute(key, cls.__name__)

        query = query_builder.insert(cls.__name__, **kwargs)
        cls.cursor.execute(query, tuple(kwargs.values()))
        cls.connection.commit()
