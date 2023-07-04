from mro import columns


class QueryBuilder:
    @classmethod
    def insert(cls, class_name: str, **kwargs):
        query = f"INSERT INTO {class_name} ("
        for index, column_name in enumerate(kwargs.keys()):
            query += f"{column_name}"
            if index != len(kwargs.keys()) - 1:
                query += ", "
        query += ") VALUES ("
        for index, (value) in enumerate(kwargs.values()):
            if value.__class__ == str:
                query += f"'{value}'"
            else:
                query += f"{value}"
            if index != len(kwargs.values()) - 1:
                query += ","

        query += ");"
        return query
