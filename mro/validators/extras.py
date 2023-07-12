from typing import Type

from mro.interface import AbstractBaseTable


def validate_column_default_values(class_table: Type[AbstractBaseTable]) -> None:
    class_columns = class_table.get_columns()

    for column_name, column in class_columns.items():
        if not isinstance(column.default, column.supported_types):
            if column.primary_key and column.supported_types[0] == int:
                continue
            raise TypeError(
                f"Column `{column_name}` default value is not of type "
                f"{column.supported_types}"
            )


def validate(class_table: Type[AbstractBaseTable], **kwargs):
    for name, validator in globals().items():
        if name.startswith("validate_"):
            validator(class_table, **kwargs)
