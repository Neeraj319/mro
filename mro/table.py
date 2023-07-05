import sqlite3
from typing import Any

from mro import columns, exceptions, query_builder
from mro.result_mapper import map_query_result_with_class


class BaseTable:
    @classmethod
    def get_table_schema(cls) -> str:
        _class_dict = cls.__dict__
        table_name = cls.get_class_name()
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
        class_columns = cls.get_columns()
        class_name = cls.get_class_name()
        for key, value in kwargs.items():
            if key not in class_columns.keys():
                raise exceptions.InvalidColumnAttribute(
                    f"attribute: `{key}` for class `{class_name}`"
                )
            if not isinstance(value, cls.__dict__[key].supported_types):
                raise exceptions.InvalidDataTypeGiven(
                    f"value: `{value}`, attribute: `{key}` of class `{class_name}` "
                    f"expected type: {class_columns[key].get_class_name()}"
                )

        query = query_builder.insert(cls.__name__, **kwargs)
        connection.cursor().execute(query, tuple(kwargs.values()))
        connection.commit()

    @classmethod
    def get_columns(cls) -> dict[str, columns.BaseColumn]:
        table_columns = {}
        for attr, value in cls.__dict__.items():
            if issubclass(value.__class__, (columns.BaseColumn)):
                table_columns[attr] = value
        return table_columns

    @classmethod
    def get_class_name(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def select(
        cls, connection: sqlite3.Connection, select_columns: tuple = (), **where: Any
    ):
        class_columns = cls.get_columns()
        class_name = cls.get_class_name()
        if len(select_columns) == 0:
            select_columns = tuple(class_columns.keys())
        else:
            for _column in select_columns:
                if _column not in class_columns:
                    raise exceptions.InvalidColumnAttribute(
                        f"attribute: `{_column}` for class `{class_name}`"
                    )
        query = query_builder.select(class_name, select_columns, **where)
        res = connection.cursor().execute(query, tuple(where.values()))
        values = res.fetchall()
        query_result = list()
        for r in values:
            result = map_query_result_with_class(class_columns, r)
            _object = cls()
            for key, value in result.items():
                setattr(_object, key, value)
            query_result.append(_object)
        return query_result
