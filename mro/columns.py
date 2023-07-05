class BaseColumn:
    def __init__(self, null: bool = False, primary_key: bool = False) -> None:
        self.null = null
        self.primary_key = primary_key

    def get_schema(self) -> str:
        rep_string = ""
        if self.null:
            rep_string += " NULL"
        if self.primary_key:
            rep_string += " PRIMARY KEY"
        return rep_string


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
        rep_string = f'"%(column_name)s" VARCHAR({self.max_length}) '
        return rep_string + super().get_schema()

    @property
    def max_length(self) -> int:
        return self._max_length


class Int(BaseColumn):
    def __init__(self, null: bool = False, primary_key: bool = False) -> None:
        super().__init__(null=null, primary_key=primary_key)

    def get_schema(self) -> str:
        schema = '"%(column_name)s" INTEGER ' + super().get_schema()
        if self.primary_key:
            schema += " AUTOINCREMENT"
        return schema
