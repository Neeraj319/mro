from mro import base, columns, table


class Blog(table.BaseTable):
    id = columns.Int(primary_key=True)
    title = columns.VarChar(max_length=255)

    def __str__(self) -> str:
        return f"Blog | {self.title}"

    def __repr__(self) -> str:
        return f"Blog | {self.title}"


base_settings = base.BaseClass("test.db")
base_settings.register_tables([Blog])

with base_settings as connection:
    blogs = Blog.db.select().execute(connection)
    Blog.db.insert().execute(connection)
    print(blogs)
