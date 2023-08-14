from csv import DictWriter
from typing import List

from pandas import DataFrame
from .errors import ColumnNotFountInClass
from .functions import _ColumnFunc
from .wrapper import check_data_availability
from .types import Column

"""
Dynamic Class Creation from given meta class base
"""


def generate_data(mysql_data, meta_class, columns) -> List:
    collection_list = []

    for m_data in mysql_data:
        meta_cls = create_mata(columns, m_data, meta_class)
        collection_list.append(meta_cls)

    return collection_list


def create_mata(columns, data, meta_class):

    return type(meta_class.__table__, (), {column: getattr(meta_class, column).set_value(d, column) for column, d in zip(columns, data)})


"""
A collection of meta class, for querying data
"""


class PySqlCollection:

    def __init__(self, mysql_data, columns, meta_class):
        self.__columns__ = columns
        self.__meta_class = meta_class
        self.__data__ = generate_data(mysql_data, meta_class, columns)

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
        str_po = "".join(["{:<" + f"{len(col) + 2}" + "}" for col in self.__columns__])
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

    def filter(self, lambda_function):

        mysql_data = list(map(lambda x: (getattr(x, col) for col in self.__columns__),
                              list(filter(lambda_function, self.__data__))))

        return PySqlCollection(mysql_data, self.__columns__, self.__meta_class)

    def join(self, pysql_collection, on: str, how: str):

        if "," in on:
            join_column_self, join_column_other = on.split(",")
        else:
            join_column_self, join_column_other = on, on

        if join_column_self not in self.__columns__:
            raise ColumnNotFountInClass(join_column_self, self.__meta_class.__table__)

        if join_column_other not in pysql_collection.__columns__:
            raise ColumnNotFountInClass(join_column_other, pysql_collection.__meta_class.__table__)

        list_dict_self = self.to_list_dict()
        list_dict_other = pysql_collection.to_list_dict()

        common_join_val: set = set([row.get(join_column_self) for row in list_dict_self]). \
            intersection(set([row.get(join_column_other) for row in list_dict_other]))

        if not common_join_val:
            return self

        list_dict_self_filter = list(filter(lambda x: x[join_column_self] in common_join_val, list_dict_self))
        list_dict_other_filter = list(filter(lambda x: x[join_column_other] in common_join_val, list_dict_other))

        for row in list_dict_self_filter:
            row_to_join = list(filter(lambda x: x[join_column_other] == row[join_column_self],
                                      list_dict_other_filter))[0]

            for key in row_to_join:
                row[key] = row_to_join[key]

        mysql_data = [data.values() for data in list_dict_self_filter]
        join_columns = list_dict_self_filter[0].keys()

        return PySqlCollection(mysql_data, join_columns, self.__meta_class)


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

    def delete(self):
        query = f"DELETE FROM {self.table} WHERE " + self._filter_query
        self._cursor.execute(query)
        self._db.commit()

    @property
    def fetch_filtered(self):
        self._cursor.execute(f"SELECT {','.join(self.columns)} from {self.table} WHERE {self._filter_query}")
        return PySqlCollection(self._cursor.fetchall(), self.columns, self._meta_class)
