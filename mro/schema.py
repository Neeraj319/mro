class BaseSchemaClass:
    sql_create = "CREATE TABLE IF NOT EXISTS %(table_name)s (%(fields)s);"


