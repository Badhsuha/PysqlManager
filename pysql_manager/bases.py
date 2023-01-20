from csv import DictWriter
from pandas import DataFrame
from .errors import EmptyPysqlCollectionError

"""
Dynamic Class Creation from given meta class Class base
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
            print("Pleas pass column")
            return None

        mysql_data = list(map(lambda x: (getattr(x, col) for col in columns), self.__data__))

        return PySqlCollection(mysql_data, columns, self.__meta_class)
