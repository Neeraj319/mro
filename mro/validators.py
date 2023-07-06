from mro import exceptions


def validate_class_table_columns(class_table, **kwargs):
    class_columns = class_table.get_columns()
    class_name = class_table.get_class_name()
    for key in kwargs.keys():
        if key not in class_columns.keys():
            raise exceptions.InvalidColumnAttribute(
                f"attribute: `{key}` for class `{class_name}`"
            )


def validate_class_table_data(class_table, **kwargs):
    class_columns = class_table.get_columns()
    class_name = class_table.get_class_name()
    for key, value in kwargs.items():
        if not isinstance(value, getattr(class_table, key).supported_types):
            raise exceptions.InvalidDataTypeGiven(
                f"value: `{value}`, attribute: `{key}` of class `{class_name}` "
                f"expected type: {class_columns[key].get_class_name()}"
            )
