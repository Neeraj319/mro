class SqliteFileNotFoundError(Exception):
    pass


class TableNotRegisteredError(Exception):
    pass


class ClassTableIsMissingColumnAttributes(Exception):
    pass


class InvalidColumnAttribute(Exception):
    pass

class InvalidDataTypeGiven(Exception):
    pass
