"""
Column Class:
    Used in Table Class to create column class variables
"""
from __future__ import annotations


class Column:
    def __init__(self, col_type):
        self.c_data = None
        self.col_type = col_type

    @property
    def _max_length(self) -> int | None:
        return self.col_type.length

    def set_value(self, data, column):

        if self._max_length is not None:
            if isinstance(data, str):
                if len(data) > self._max_length:
                    raise ValueError(f"Max length for column {column} is {self._max_length}. "
                                     f"Given data ({data}) has length {len(data)}")

        self.c_data = data
        return self

    def get_value(self):
        return self.c_data

    def __str__(self):
        return f"{self.c_data}"


class PysMysqlType:
    def __init__(self, length:  int | None = None):
        self.length = length


class StringType(PysMysqlType):
    def __init__(self, length):
        super().__init__(length)


class IntegerType(PysMysqlType):
    def __init__(self):
        super().__init__()

