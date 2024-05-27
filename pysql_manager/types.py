"""
Column Class:
    Used in Table Class to create column class variables
"""


class Column:
    def __init__(self, col_type):
        self.col_type = col_type


class PysMysqlType:
    pass


class StringType(PysMysqlType):
    def __init__(self, length):
        self.length = length


class IntegerType(PysMysqlType):
    def __init__(self):
        pass