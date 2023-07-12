# MRO (Mero Ramro ORM, eng: My Nice ORM)

A sqlite3 ORM in python.

## Table of Contents

- [ Quick Example ](#quick-example)

1. [ Creating a Table ](#creating-a-table)
2. [ Adding Class Columns to a class table ](#adding-class-columns-to-the-class-table)
3. [ DatabaseManager ](#database-manager)
4. [ Query Methods ](#query-methods)

## Creating a Table

To create a table we need to import from the `BaseTable` class.

Tables are known as `class table` in mro.

```python
from mro.table import BaseTable

class Foo(BaseTable):
    ...

```

---

## Adding Class Columns to the Class Table.

Class columns can be found in `mro.columns`

All columns are the subclasses of `mro.interface.AbstractBaseColumn`

- The `AbstractBaseColumn` and `BaseColumns` don't do anything by themselves.

Default parameters in all the class columns are:

```
:param null: default value is false, sets the column to be nullable.
:param primary_key: default value is false, sets the column to be a primary key.
:param unique: default value is False, sets the column to have unique values only.
:param default: default value is None, set a default value for the supported data type of the column, in this case int.
```

- By default if you don't pass any of these parameters while creating the class column object, it will create a `not null`, `not unique` and `non primary key` column in the database.

- Passing Invalid datatype to the default parameter raises `TypeError`.

There are 5 types of class columns that are available.

- [ Int ](#int)
- [ Float ](#float)
- [ VarChar ](#varchar)
- [ Text ](#text)
- [ Boolean ](#boolean)
- [ Example ](#boolean)

## Int

Import from: `mro.columns`

As the name suggests it will create an Integer column.

```python
from mro.columns import Int
from mro.table import BaseTable

class Foo(BaseTable):

    id = Int()
```

Here's an example of how to create a `int` primary key.

```python

from mro.columns import Int
from mro.table import BaseTable

class Foo(BaseTable):
    id = Int(primary_key = True)
```

- ID value will auto-increment and altering the value is possible cause of the nature of `sqlite3`.

## Float

Import from: `mro.columns`

As the name suggests it will create an Integer column.

```python
from mro.columns import Float
from mro.table import BaseTable

class Foo(BaseTable):

    price = Float()
```

## VarChar

Import from: `mro.columns`

Create a column with character limit.

- VarChar and Text have the same effect in `sqlite3`.

```python
from mro.column import VarChar

class Foo(BaseTable):

    name = VarChar(max_length = 10)
```

```
:param max_length: Specify max length for the VarChar class column.
```

- If the passed value to the column exceeds the `max_length` it raises `mro.IntegrityError` error.

## Text

Import from: `mro.columns`

Create a column with no character limit.

```python
from mro.column import VarChar

class Foo(BaseTable):

    description = Text()
```

## Boolean

Import from: `mro.columns`

```python
from mro.column import Boolean

class Her(BaseTable):
    loves_me = Boolean(default = False)
```

## Example of a Class table

```python
from mro.table import BaseTable
from mro.column import Int, Float, VarChar, Boolean, Text

class Her(BaseTable):
    first_name = VarChar(max_length = 20)
    last_name = VarChar(max_length = 20)
    age = Int()
    loves_me = Boolean(default = False)
    description = Text(default = "Beautiful Girl", null = True)
```

---

After Creating Tables we need to register them. But before that We need to know about
`DatabaseManager`

## Database Manager

- [ DatabaseManager Object ](#database-manager-object)
- [ Registering Tables ](#registering-tables)
- [ Connection Object ](#getting-connection-object)

Import from: `mro.manager`

### Database Manager Object

The `DatabaseManager` is the heart of whole `mro` orm. It is responsible for registering tables, creating tables, adding query builder to the classes and creating a database connection.

```python
from mro.manager import DatabaseManager

db_manager = DatabaseManger("test.db", create_tables = True)
```

```
:param sqlite_filename: name of the sqlite3 db file, if the file doesn't exist it will create a new one
:param create_tables: creates table in the database (doesn't update them)
```

### Registering Tables

`THIS IS A MANDATORY STEP TO EXECUTE QUIRES`.

- This method creates tables if specified.
- This method also injects the `query builder` (db) object into the passed table classes.

```python
from mro.manager import DatabaseManager

db_manager = DatabaseManger("test.db", create_tables = True)
db_manager.register_tables([Her]) # mandatory step
```

```
register_tables
:param tables: must be a list with class tables
```

After this step you should be able to access the `db` object in each registered class tables.

### Getting Connection Object

To get the `sqlite3` connection object use the `get_connection` method of the `DatabaseManager` object.

```python
from mro.manager import DatabaseManager

db_manager = DatabaseManger("test.db", create_tables = True)
db_manager.register_tables([Her]) # mandatory step

with db_manager.get_connection() as connection:
    ...
```

- Note that the object returned by `get_connection` is a `sqlite3.Connection` object.

---

### Execute

Executes the whole chained query methods.

```python

from mro.manager import DatabaseManager

db_manager = DatabaseManger("test.db", create_tables = True)
db_manager.register_tables([Her]) # mandatory step

with db_manager.get_connection() as connection:
    her = Her.db.select().where(loves_me = True).execute(connection)

```

```
:param connection: sqltie3.connection returned by .get_connection
```

- Execute either returns query results in a `List` or `None`

---

## Query Methods

Now that we have everything we can access the `.db` attribute of registered class columns to execute query.

TO GET THE RESULT OF QUERY METHODS CALLING [ execute ](#execute) IS MANDATORY.

- [ Insert ](#insert)
- [ Select ](#select)
- [ Where ](#where)
- [ Update ](#update)
- [ Delete ](#delete)
- [ And ](#and)
- [ Or ](#or)

### Insert

```python
from mro.manager import DatabaseManager

db_manager = DatabaseManger("test.db", create_tables = True)
db_manager.register_tables([Her]) # mandatory step

with db_manager.get_connection() as connection:
    Her.db.insert(first_name="Foo", last_name="bar", age = 18).execute(connection)
```

```
:param kwargs: class column(s)
```

**The return value of execute with execute is None**

- Passing invalid datatype to the insert method raises `TypeError`
- Passing None to primary key column raises `TypeError`
- Passing invalid class columns raises `mro.exceptions.InvalidClassColumn`

### Select

Get rows from database.

```python
from mro.manager import DatabaseManager

db_manager = DatabaseManger("test.db", create_tables = True)
db_manager.register_tables([Her]) # mandatory step

with db_manager.get_connection() as connection:
    Her.db.insert(first_name="Foo", last_name="bar", age = 18).execute(connection)
    so_many_her = Her.db.select().execute(connection)
    print(so_many_her)
```

**This returns a `List` of `Her` objects or `None` if nothing was found**

### Where

Chain this method with `select`, `update` and `delete`

```python
from mro.manager import DatabaseManager

db_manager = DatabaseManger("test.db", create_tables = True)
db_manager.register_tables([Her]) # mandatory step

with db_manager.get_connection() as connection:
    Her.db.insert(first_name="Foo", last_name="bar", age = 18).execute(connection)
    only_her = Her.db.select().where(Her.loves_me == True).execute(connection)
    print(only_her)
```

```
:param clause: Must be ClassTable.ClassColumn "operator" and "value"
```

- Supported operators:

  - "==": Blog.title == "Foo"
  - ">" : Blog.likes > 50
  - ">=": Blog.views >= 10
  - "<" : Blog.views < 30
  - "<=": Blog.views <= 90
  - "!" : Blog.title != "Bar"

- You can have only one where chained.
- Passing invalid class column names to where raises `IntegrityError`

### Update

Update row(s) in the database

```python
from mro.manager import DatabaseManager

db_manager = DatabaseManger("test.db", create_tables = True)
db_manager.register_tables([Her]) # mandatory step

with db_manager.get_connection() as connection:
    Her.db.insert(first_name="Foo", last_name="bar", age = 18).execute(connection)
    only_her = Her.db.select().where(Her.loves_me == True).execute(connection)
    print(only_her)
    Her.db.update(first_name = "bar", last_name = "Foo").where(Her.loves_me == False).execute(connection)
```

- Passing invalid datatype to the insert method raises `TypeError`
- Passing None to primary key column raises `TypeError`
- Passing invalid class columns raises `mro.exceptions.InvalidClassColumn`

### Delete

Delete row(s) from the database.

```python
from mro.manager import DatabaseManager

db_manager = DatabaseManger("test.db", create_tables = True)
db_manager.register_tables([Her]) # mandatory step

with db_manager.get_connection() as connection:
    Her.db.insert(first_name="Foo", last_name="bar", age = 18).execute(connection)
    only_her = Her.db.select().where(Her.loves_me == True).execute(connection)
    Her.db.delete().execute(connection) # Deletes all Her rows
    Her.db.delete().where(id = 1).execute(connection) # method chain with `where`
```

### And

Only to be chained with [ where ](#where).

**Don't confuse with `and` it's `and_`**

```python
from mro.manager import DatabaseManager

db_manager = DatabaseManger("test.db", create_tables = True)
db_manager.register_tables([Her]) # mandatory step

with db_manager.get_connection() as connection:
    Her.db.insert(first_name="Foo", last_name="bar", age = 18).execute(connection)
    only_her = Her.db.select().where(Her.loves_me == True).and_(Her.first_name = "Foo").execute(connection)
    print(only_her)
```

For parameters check [ where ](#where).

## Or

Only to be chained with [ where ](#where) or [ and\_ ](#and).

**Don't confuse with `or` it's `or_`**

```python
from mro.manager import DatabaseManager

db_manager = DatabaseManger("test.db", create_tables = True)
db_manager.register_tables([Her]) # mandatory step

with db_manager.get_connection() as connection:
    Her.db.insert(first_name="Foo", last_name="bar", age = 18).execute(connection)
    only_her = Her.db.select().where(Her.loves_me == True).or_(Her.first_name = "Foo").execute(connection)
    print(only_her)
```

### Quick Example

```python
from mro import columns, manager, table

class Blog(table.BaseTable):
    id = columns.Int(primary_key=True)
    title = columns.VarChar(max_length=255)

    def __str__(self) -> str:
        return f"Blog | {self.title}"

    def __repr__(self) -> str:
        return f"Blog | {self.title}"

base_manager = manager.DatabaseManger("test.db", create_tables=True)
base_manager.register_tables([Blog])

with base_settings.get_connection() as connection:
    Blog.db.insert(title="something").execute(connection)
    Blog.db.insert(title="something else").execute(connection)
    Blog.db.insert(title="Loo rem").execute(connection)
    blogs = (
        Blog.db.select()
        .where(Blog.title == "something")
        .and_(Blog.id == 1)
        .execute(connection)
    )
    print(blogs)
```
