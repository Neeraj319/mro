def insert(class_name: str, **kwargs):
    query = f"INSERT INTO {class_name} ("
    for index, column_name in enumerate(kwargs.keys()):
        query += f"{column_name}"
        if index != len(kwargs.keys()) - 1:
            query += ", "
    query += ") VALUES ("
    for index, (_) in enumerate(kwargs.values()):
        query += "?"
        if index != len(kwargs.values()) - 1:
            query += ","

    query += ");"
    return query
