"""
Column Class:
    Used in Table Class to create column class variables
"""
from __future__ import annotations


class _Column:
    def __init__(self):
        self.c_data = None

    def set_value(self, data):
        self.c_data = data
        return self

    def get_value(self):
        return self.c_data

    def __str__(self):
        return f"{self.c_data}"

    def __eq__(self, other):
        return self.get_value() == other


class StringType(_Column):
    def __init__(self, length):
        self.length = length
        super().__init__()


class IntegerType(_Column):
    def __init__(self, **kwargs):
        self.length = None
        super().__init__()
