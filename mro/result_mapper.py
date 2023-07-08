from typing import Any, Type

from .interface import AbstractBaseTable


def map_query_result_with_class(
    class_table: Type[AbstractBaseTable], results: list[Any]
) -> list[AbstractBaseTable]:
    class_columns = class_table.get_columns().keys()
    _objects = list()
    for row in results:
        _object = class_table()
        for _column_index, column in enumerate(class_columns):
            setattr(_object, column, row[_column_index])
        _objects.append(_object)
    return _objects
