from mro.table import BaseTable
from mro import columns


class SomeTable(BaseTable):
    age = columns.Int(primary_key=True)
    name = columns.VarChar(max_length=22)
