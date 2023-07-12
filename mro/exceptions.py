class SqliteFileNotFoundError(Exception):
    pass


class TableNotRegisteredError(Exception):
    pass


class ClassTableIsMissingColumnAttributes(Exception):
    pass


class InvalidClassColumn(Exception):
    pass


class ClassTableNotRegistered(Exception):
    pass


class IntegrityError(Exception):
    pass


class SqliteInterfaceError(Exception):
    pass


class OperationalError(Exception):
    pass


class EmptyUpdateQuery(Exception):
    pass
