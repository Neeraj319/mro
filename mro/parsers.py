from typing import Type

from .columns import Float, Int
from .interface import AbstractBaseTable


def parse_float_column(class_table: Type[AbstractBaseTable], **kwargs):
    class_columns = class_table.get_columns()
    for column_name, value in class_columns.items():
        if isinstance(value, Float):
            if kwargs.get(column_name) is None:
                continue
            kwargs[column_name] = float(kwargs[column_name])


def parse_int_column(class_table: Type[AbstractBaseTable], **kwargs):
    class_columns = class_table.get_columns()
    for column_name, value in class_columns.items():
        if isinstance(value, Int):
            if kwargs.get(column_name) is None:
                continue
            kwargs[column_name] = int(kwargs[column_name])


def parse(class_table: Type[AbstractBaseTable], **kwargs):
    for name, parser in globals().items():
        if name.startswith("parse_"):
            parser(class_table, **kwargs)
