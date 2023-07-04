class SqliteFileNotFoundError(Exception):
    pass


class TableNotRegisteredError(Exception):
    pass


class ClassTableIsMissingColumnAttributes(Exception):
    pass


class InvalidColumnAttribute(Exception):
    def __init__(self, column_name: str, table_name: str):
        self.column_name = column_name
        self.table_name = table_name

