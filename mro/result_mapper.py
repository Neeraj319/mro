from typing import Any


def map_query_result_with_class(class_columns: tuple, result: list[Any]):
    return dict(zip(class_columns, result))
