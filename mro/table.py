from mro import exceptions, query_builder

from .interface import AbstractBaseColumn, AbstractBaseTable


class BaseTable(AbstractBaseTable):
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
    def _inject_query_builder_to_columns(cls):
        for column in cls.get_columns().values():
            column.query_builder = cls.db

    @classmethod
    def _inject_cloumn_name_to_columns(cls):
        for column_name, column in cls.get_columns().items():
            column.column_name = column_name

    @classmethod
    def get_columns(cls) -> dict[str, AbstractBaseColumn]:
        table_columns = {}
        for attr, value in cls.__dict__.items():
            if issubclass(value.__class__, (AbstractBaseColumn)):
                table_columns[attr] = value
        return table_columns

    @classmethod
    def get_class_name(cls) -> str:
        return cls.__name__.lower()
