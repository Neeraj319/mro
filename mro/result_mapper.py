from typing import Any


def map_query_result_with_class(class_table, result: list[Any]):
    class_columns = class_table.get_columns()
    _object = class_table()
    for index, column in enumerate(class_columns):
        setattr(_object, column, result[index])
    return _object
