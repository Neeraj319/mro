from mro.interface import AbstractBaseColumn


class BaseColumn(AbstractBaseColumn):
    def get_schema(self) -> str:
        rep_string = ""
        if self.null:
            rep_string += " NULL"
        if self.primary_key:
            rep_string += " PRIMARY KEY"
        return rep_string

    def __eq__(self: AbstractBaseColumn, other: object) -> str:
        self.query_builder.query_parameters.append(other)
        return self.column_name + " = ?"

    def __lt__(self, __value: object) -> str:
        self.query_builder.query_parameters.append(__value)
        return self.column_name + " < ?"

    def __gt__(self, __value: object) -> str:
        self.query_builder.query_parameters.append(__value)
        return self.column_name + " > ?"

    def __le__(self, __value: object) -> str:
        self.query_builder.query_parameters.append(__value)
        return self.column_name + " <= ?"

    def __ge__(self, __value: object) -> str:
        self.query_builder.query_parameters.append(__value)
        return self.column_name + " >= ?"

    def __ne__(self, __value: object) -> str:
        self.query_builder.query_parameters.append(__value)
        return self.column_name + " != ?"


class VarChar(BaseColumn):
    def __init__(
        self,
        max_length: int,
        null: bool = False,
        primary_key: bool = False,
    ) -> None:
        super().__init__(null=null, primary_key=primary_key)
        self._max_length = max_length

    def get_schema(self: "VarChar"):
        schema = f'"%(column_name)s" VARCHAR({self._max_length}) '
        return schema + super().get_schema()

    @property
    def supported_types(self):
        return (str,)


class Int(BaseColumn):
    def __init__(self, null: bool = False, primary_key: bool = False) -> None:
        super().__init__(null=null, primary_key=primary_key)

    def get_schema(self) -> str:
        schema = '"%(column_name)s" INTEGER ' + super().get_schema()
        if self.primary_key:
            schema += " AUTOINCREMENT"
        return schema

    @property
    def supported_types(self):
        return (int,)
