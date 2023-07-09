from typing import Type

from mro import exceptions

from .columns import VarChar
from .interface import AbstractBaseTable


def validate_class_table_columns(class_table: Type[AbstractBaseTable], **kwargs):
    class_columns = class_table.get_columns()
    class_name = class_table.get_class_name()
    for key in kwargs.keys():
        if key not in class_columns.keys():
            raise exceptions.InvalidColumnAttribute(
                f"attribute: `{key}` for class `{class_name}`"
            )


def validate_class_table_data(class_table: Type[AbstractBaseTable], **kwargs):
    class_columns = class_table.get_columns()
    class_name = class_table.get_class_name()
    for key, value in kwargs.items():
        if not isinstance(value, getattr(class_table, key).supported_types):
            raise exceptions.InvalidDataTypeGiven(
                f"value: `{value}`, attribute: `{key}` of class `{class_name}` "
                f"expected type(s): {class_columns[key].supported_types}"
            )


def validate_primary_key_null(class_table: Type[AbstractBaseTable], **kwargs):
    class_columns = class_table.get_columns()
    class_name = class_table.get_class_name()
    for column_name, value in class_columns.items():
        if (
            value.primary_key
            and value.supported_types[0] != int
            and kwargs.get(column_name) is None
        ):
            raise exceptions.IntegrityError(
                f"value: `{kwargs.get(column_name)}`, for primary key: `{column_name}` of class `{class_name}`"
            )


def validate_varchar_max_length(class_table: Type[AbstractBaseTable], **kwargs):
    class_columns = class_table.get_columns()
    class_name = class_table.get_class_name()
    for column_name, value in class_columns.items():
        if isinstance(value, VarChar):
            if kwargs.get(column_name) is None:
                continue
            if len(kwargs.get(column_name)) > value._max_length:
                raise exceptions.IntegrityError(
                    f"passed value for attribute: `{column_name}` of class `{class_name}`"
                    f"exceeds max length: {value._max_length}"
                )


def validate(class_table: Type[AbstractBaseTable], **kwargs):
    for name, validtor in globals().items():
        if name.startswith("validate_"):
            validtor(class_table, **kwargs)
