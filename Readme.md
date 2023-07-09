# MRO (Mero Ramro ORM, eng: My Nice ORM)

### Get started

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
        .and_(Blog.id == None)
        .execute(connection)
    )
    print(blogs)
```

More coming soon.
