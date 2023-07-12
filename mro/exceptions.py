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


class ClassTableNotRegistered(Exception):
    pass


class IntegrityError(Exception):
    pass


class SqliteInterfaceError(Exception):
    pass


class OperationalError(Exception):
    pass
