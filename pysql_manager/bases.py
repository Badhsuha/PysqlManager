from csv import DictWriter
from pandas import DataFrame
from .errors import EmptyPysqlCollectionError, ColumnNotFountInClass
from .functions import _ColumnFunc

"""
Dynamic Class Creation from given meta class base
"""


def create_mata(columns, data, meta_class):
    return type(meta_class.__table__, (), {column: d for column, d in zip(columns, data)})


"""
A collection of meta class, for querying data
"""


class PySqlCollection:

    def __init__(self, mysql_data, column, meta_class):
        self.__columns__ = column
        self.__meta_class = meta_class
        self.__data__ = [create_mata(column, data, meta_class) for data in mysql_data]

    def check_data_availability(func):
        def wrap(self, *args, **kwargs):
            if self.count() != 0:
                result = func(self, *args, **kwargs)
                return result
            else:
                raise EmptyPysqlCollectionError()

        return wrap

    @check_data_availability
    def first(self):
        return self.__data__[0]

    @check_data_availability
    def last(self):
        return self.__data__[-1]

    def is_empty(self):
        return not bool(self.__data__)

    def count(self):
        return len(self.__data__)

    @check_data_availability
    def to_df(self):
        return DataFrame.from_dict(self.to_list_dict())

    def to_list_dict(self):
        obj_dicts = map(lambda obj: obj.__dict__, self.__data__)
        return list(map(lambda obj: {key: obj[key] for key in obj if key in self.__columns__}, obj_dicts))

    @check_data_availability
    def save_as_csv(self, path, delimiter=","):

        data = self.to_list_dict()
        with open(path, "w") as file:
            csv_writer = DictWriter(file, data[0].keys(), delimiter=delimiter)
            csv_writer.writeheader()
            csv_writer.writerows(data)

    def show(self):
        str_po = "{:<10}" * len(self.__columns__)
        print(str_po.format(*[col for col in self.__columns__]))
        for data in self.__data__:
            print(str_po.format(*[getattr(data, col) for col in self.__columns__]))

    @check_data_availability
    def select(self, columns=None):
        if not isinstance(columns, list):
            print("Pleas pass column / Column as List")
            return None

        mysql_data = list(map(lambda x: (getattr(x, col) for col in columns), self.__data__))

        if len(columns) == 1:
            return PysqlCollectionSingle(mysql_data, columns, self.__meta_class)

        return PySqlCollection(mysql_data, columns, self.__meta_class)

    @check_data_availability
    def sum(self, col: _ColumnFunc):
        return {col.alias_name("sum"): sum([getattr(row, col.column_name) for row in self.__data__])}

    def unique(self, col: _ColumnFunc):
        return {col.alias_name("unique"): list(set([getattr(row, col.column_name) for row in self.__data__]))}


class PysqlCollectionSingle(PySqlCollection):
    def to_list(self):
        obj_dicts = map(lambda obj: obj.__dict__, self.__data__)
        return {self.__columns__[0]: list(map(lambda obj: obj[self.__columns__[0]], obj_dicts))}


class PySqlFilterObj:
    def __init__(self, filter_query, cursor, meta_class, columns, table, db):
        self.columns = columns
        self._filter_query = filter_query
        self._cursor = cursor
        self._meta_class = meta_class
        self.table = table
        self._db = db

    def update(self, *args, **kwargs):
        if not all([key in self.columns for key in kwargs.keys()]):
            raise (ColumnNotFountInClass(kwargs.keys(), self.table))
        else:
            set_array = [f"{key}='{kwargs[key]}'" for key in kwargs.keys()]
            query = f"UPDATE {self.table} SET " + f"{','.join(set_array)}" + f" WHERE {self._filter_query}"
            self._cursor.execute(query)
            self._db.commit()
            # print(query)
            print("Update Done")

    def delete(self):
        query = f"DELETE FROM {self.table} WHERE " + self._filter_query
        self._cursor.execute(query)
        self._db.commit()
        print("Deletion Done")

    @property
    def fetch_filtered(self):
        self._cursor.execute(f"SELECT {','.join(self.columns)} from {self.table} WHERE {self._filter_query}")
        return PySqlCollection(self._cursor.fetchall(), self.columns, self._meta_class)