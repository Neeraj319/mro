from mro import columns


class BaseTable:
    def get_table_schema(self) -> str:
        _class = self.__class__
        _class_dict = _class.__dict__
        table_name = _class.__name__.lower()
        schema = f'CREATE TABLE IF NOT EXISTS "{table_name}" ('

        for index, filed in enumerate(_class_dict):
            if issubclass(_class_dict[filed].__class__, columns.BaseColumn):
                schema += _class_dict[filed].get_db_representation() % {
                    "column_name": filed
                }
                if index != len(_class_dict) - 2:
                    schema += ", "
        return f"{schema});"
