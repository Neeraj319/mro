import datetime
from typing import Type

from .columns import Date, DateTime, Float, Int
from .interface import AbstractBaseTable


def parse_float_column(class_table: Type[AbstractBaseTable], _query_dict: dict):
    class_columns = class_table.get_columns()
    for column_name, value in class_columns.items():
        if isinstance(value, Float):
            if _query_dict.get(column_name) is None:
                continue
            _query_dict[column_name] = float(_query_dict[column_name])


def parse_int_column(class_table: Type[AbstractBaseTable], _query_dict):
    class_columns = class_table.get_columns()
    for column_name, value in class_columns.items():
        if isinstance(value, Int):
            if _query_dict.get(column_name) is None:
                continue
            _query_dict[column_name] = int(_query_dict[column_name])


def parse_datetime_column(class_table: Type[AbstractBaseTable], _query_dict):
    class_columns = class_table.get_columns()
    for column_name, value in class_columns.items():
        if isinstance(value, DateTime):
            if _query_dict.get(column_name) is None and not value.auto_now_add:
                continue
            _query_dict[column_name] = datetime.datetime.now()
        if isinstance(value, Date):
            if _query_dict.get(column_name) is None and not value.auto_now_add:
                continue
            _query_dict[column_name] = datetime.date.today()


def parse(class_table: Type[AbstractBaseTable], _query_dict):
    for name, parser in globals().items():
        if name.startswith("parse_"):
            parser(class_table, _query_dict)
