from mro import columns


def test_base_column_schema():
    column = columns.BaseColumn()

    assert column.get_schema() == ""

    column = columns.BaseColumn(primary_key=True)
    assert column.get_schema() == " PRIMARY KEY"

    column = columns.BaseColumn(null=True)
    assert column.get_schema() == " NULL"

    column = columns.BaseColumn(primary_key=True, null=True)
    assert column.get_schema() == " NULL PRIMARY KEY"


def test_varchar_class():
    column = columns.VarChar(max_length=255)
    assert column.get_schema() == '"%(column_name)s" VARCHAR(255) '

    column = columns.VarChar(max_length=255, primary_key=True)
    assert column.get_schema() == '"%(column_name)s" VARCHAR(255)  PRIMARY KEY'

    column = columns.VarChar(max_length=255, null=True)
    assert column.get_schema() == '"%(column_name)s" VARCHAR(255)  NULL'

    column = columns.VarChar(max_length=255, primary_key=True, null=True)
    assert column.get_schema() == '"%(column_name)s" VARCHAR(255)  NULL PRIMARY KEY'


def test_integer_class():
    column = columns.Int()
    assert column.get_schema() == '"%(column_name)s" INTEGER '

    column = columns.Int(primary_key=True)
    assert column.get_schema() == '"%(column_name)s" INTEGER  PRIMARY KEY AUTOINCREMENT'

    column = columns.Int(null=True)
    assert column.get_schema() == '"%(column_name)s" INTEGER  NULL'

    column = columns.Int(primary_key=True, null=True)
    assert column.get_schema() == '"%(column_name)s" INTEGER  NULL PRIMARY KEY AUTOINCREMENT'
