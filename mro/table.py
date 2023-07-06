from mro import columns, exceptions, query_builder


class BaseTable:
    db = query_builder.QueryBuilder()

    @classmethod
    def get_table_schema(cls) -> str:
        table_name = cls.get_class_name()
        schema = f'CREATE TABLE IF NOT EXISTS "{table_name}" ('

        table_columns = cls.get_columns().items()
        if len(table_columns) == 0:
            raise exceptions.ClassTableIsMissingColumnAttributes()

        for index, (column_name, column) in enumerate(table_columns):
            schema += column.get_schema() % {"column_name": column_name}
            if index != len(table_columns) - 1:
                schema += ", "

        return f"{schema});"

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
