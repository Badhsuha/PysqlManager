from pandas import DataFrame
from csv import DictWriter
from typing import List, Callable
from pysql_manager.errors import ColumnNotFountInClass
from pysql_manager.functions import _ColumnFunc
from pysql_manager.core.wrapper import check_data_availability
from pysql_manager.types import StringType, IntegerType

"""
A collection of meta class, for querying data
"""


class PySqlCollection:

    def __init__(self, mysql_data, columns, meta_class):
        self.__columns__ = columns
        self.__meta_class = meta_class
        self.__data__ = _generate_data(mysql_data, meta_class, columns)

    @check_data_availability
    def first(self):
        return self.__data__[0]

    @check_data_availability
    def last(self):
        return self.__data__[-1]

    def is_empty(self) -> bool:
        return not bool(self.__data__)

    def count(self) -> int:
        return len(self.__data__)

    @check_data_availability
    def to_df(self) -> DataFrame:
        return DataFrame.from_dict(self.to_list_dict())

    def to_list_dict(self) -> List[dict]:
        return list(map(lambda data: {col: getattr(data, col).get_value() for col in self.__columns__}, self.__data__))

    @check_data_availability
    def save_as_csv(self, path, delimiter=","):

        data = self.to_list_dict()
        with open(path, "w") as file:
            csv_writer = DictWriter(file, data[0].keys(), delimiter=delimiter)
            csv_writer.writeheader()
            csv_writer.writerows(data)

    def show(self):
        str_po = "".join(["{:<" + f"{len(col) + 5}" + "}" for col in self.__columns__])
        print(str_po.format(*[col for col in self.__columns__]))
        for data in self.__data__:
            print(str_po.format(*[getattr(data, col).get_value() for col in self.__columns__]))

    @check_data_availability
    def select(self, columns=None):
        if not isinstance(columns, list):
            print("Pleas pass column / Column as List")
            return None

        mysql_data = list(map(lambda x: [getattr(x, col).get_value() for col in columns], self.__data__))

        if len(columns) == 1:
            return PysqlCollectionSingle(mysql_data, columns, self.__meta_class)

        return PySqlCollection(mysql_data, columns, self.__meta_class)

    @check_data_availability
    def sum(self, col: _ColumnFunc):
        return {col.alias_name("sum"): sum([getattr(row, col.column_name) for row in self.__data__])}

    def unique(self, col: _ColumnFunc):
        return {col.alias_name("unique"): list(set([getattr(row, col.column_name).get_value() for row in self.__data__]))}

    def filter(self, lambda_function: Callable):

        mysql_data = list(map(lambda x: (getattr(x, col).get_value() for col in self.__columns__),
                              list(filter(lambda_function, self.__data__))))

        return PySqlCollection(mysql_data, self.__columns__, self.__meta_class)


class PysqlCollectionSingle(PySqlCollection):
    def to_list(self):
        return {
            self.__columns__[0]: list(map(lambda rec: getattr(rec, self.__columns__[0]).get_value(), self.__data__))}


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

    def delete(self):
        query = f"DELETE FROM {self.table} WHERE " + self._filter_query
        self._cursor.execute(query)
        self._db.commit()

    @property
    def fetch_filtered(self):
        self._cursor.execute(f"SELECT {','.join(self.columns)} from {self.table} WHERE {self._filter_query}")
        return PySqlCollection(self._cursor.fetchall(), self.columns, self._meta_class)


def _get_class_of(meta_class, col):
    return eval(getattr(meta_class, col).__class__.__name__)


def _get_col_feature(meta_class, col, feature):
    return getattr(getattr(meta_class, col), feature)


"""
Dynamic Class Creation from given meta class base
"""


def _generate_data(mysql_data, meta_class, columns) -> List:
    collection_list = []

    for m_data in mysql_data:
        meta_cls = _create_mata(columns, m_data, meta_class)
        collection_list.append(meta_cls)

    return collection_list


def _create_mata(columns, data, meta_class):

    return type(meta_class.__table__, (),

                {column: _get_class_of(meta_class, column)(length=_get_col_feature(meta_class, column, "length")).set_value(d)

                 for column, d in zip(columns, data)})