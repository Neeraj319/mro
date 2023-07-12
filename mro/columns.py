from mro.interface import AbstractBaseColumn


class BaseColumn(AbstractBaseColumn):
    def get_schema(self) -> str:
        rep_string = ""
        if not self.null:
            rep_string += " NOT NULL"
        if self.primary_key:
            rep_string += " PRIMARY KEY"
        if self.unique:
            rep_string += " UNIQUE"
        if self.default is not None:
            rep_string += f" DEFAULT {self.default}"
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
        unique: bool = False,
        default: str | None = None,
    ) -> None:
        super().__init__(
            null=null, primary_key=primary_key, unique=unique, default=default
        )
        self._max_length = max_length

    def get_schema(self: "VarChar"):
        schema = f'"%(column_name)s" VARCHAR({self._max_length}) '
        return schema + super().get_schema()

    @property
    def supported_types(self):
        return (str,) + super().supported_types


class Int(BaseColumn):
    def __init__(
        self,
        null: bool = False,
        primary_key: bool = False,
        unique: bool = False,
        default: int | None = None,
    ) -> None:
        super().__init__(
            null=null, primary_key=primary_key, unique=unique, default=default
        )

    def get_schema(self) -> str:
        schema = '"%(column_name)s" INTEGER ' + super().get_schema()
        if self.primary_key:
            schema += " AUTOINCREMENT"
        return schema

    @property
    def supported_types(self):
        return (int,) + super().supported_types


class Text(BaseColumn):
    def __init__(
        self,
        null: bool = False,
        primary_key: bool = False,
        unique: bool = False,
        default: str | None = None,
    ) -> None:
        super().__init__(
            null=null, primary_key=primary_key, unique=unique, default=default
        )

    def get_schema(self) -> str:
        schema = '"%(column_name)s" TEXT ' + super().get_schema()
        return schema

    @property
    def supported_types(self):
        return (str,) + super().supported_types


class Float(BaseColumn):
    def __init__(
        self,
        null: bool = False,
        primary_key: bool = False,
        unique: bool = False,
        default: float | None = None,
    ) -> None:
        super().__init__(
            null=null, primary_key=primary_key, unique=unique, default=default
        )

    def get_schema(self) -> str:
        schema = '"%(column_name)s" REAL ' + super().get_schema()
        return schema

    @property
    def supported_types(self):
        return (float, int) + super().supported_types


class Boolean(BaseColumn):
    def __init__(
        self, null: bool = False, primary_key: bool = False, default: bool | None = None
    ) -> None:
        super().__init__(null=null, primary_key=primary_key, default=default)

    def get_schema(self) -> str:
        schema = '"%(column_name)s" BOOLEAN ' + super().get_schema()
        return schema

    @property
    def supported_types(self):
        return (bool,) + super().supported_types
