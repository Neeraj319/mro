from typing import Any


def map_query_result_with_class(class_columns: dict, result: list[Any]):
    return dict(zip(class_columns.keys(), result))
