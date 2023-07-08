from mro.interface import AbstractBaseColumn


class BaseColumn(AbstractBaseColumn):
    def get_schema(self) -> str:
        rep_string = ""
        if self.null:
            rep_string += " NULL"
        if self.primary_key:
            rep_string += " PRIMARY KEY"
        return rep_string

    @classmethod
    def get_class_name(cls) -> str:
        return cls.__name__.lower()


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
