import sqlite3
from typing import Any

from mro import columns, exceptions, query_builder


class BaseTable:
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
    def insert(cls, connection: sqlite3.Connection, **kwargs: Any):
        for key, value in kwargs.items():
            if key not in cls.__dict__.keys():
                raise exceptions.InvalidColumnAttribute(
                    f"attribute: `{key}` of class `{cls.__name__}`"
                )
            if not isinstance(value, cls.__dict__[key].supported_types):
                raise exceptions.InvalidDataTypeGiven(
                    f"value: `{value}`, attribute: `{key}` of class `{cls.__name__}` "
                    f"expected type: {cls.__dict__[key].__class__.__name__}"
                )

        query = query_builder.insert(cls.__name__, **kwargs)
        connection.cursor.execute(query, tuple(kwargs.values()))
        connection.commit()
