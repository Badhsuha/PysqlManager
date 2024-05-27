

class _ColumnFunc:
    def __init__(self, column_name):
        self.column_name = column_name
        self._alias_name = column_name

    def alias(self, new_column_name):
        self._alias_name = new_column_name
        return self

    def alias_name(self, func):
        return f"{self._alias_name}_{func}"


def col(column_name: str):
    if isinstance(column_name, str):
        return _ColumnFunc(column_name)

    raise TypeError(f"Column Name should be String. Found {type(column_name)}")
