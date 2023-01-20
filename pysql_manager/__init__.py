from typing import List

import mysql.connector
from mysql.connector.errors import ProgrammingError
from .bases import PySqlCollection
from .types import Column
from .errors import ColumnNotFountInClass, TableNotFoundInClass

__version__ = "0.1.0"
__author__ = 'Badhusha K Muhammed'


"""
Main Class for bkm-pysql_manager, Used to connect to mysql, Getting data and create PySqpDataCollection
"""

class PySql:
    def __init__(self, host, username, password, dbname, meta_class):
        self.db = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=dbname
        )
        self._meta_class = meta_class
        self.columns = list(filter(lambda x: isinstance(getattr(self._meta_class, x), Column), dir(meta_class)))
        print(self.columns)
        try:
            self.table = getattr(self._meta_class, "__table__")
        except AttributeError:
            raise TableNotFoundInClass(self._meta_class.__name__)

        self._cursor = self.db.cursor()

    @property
    def fetch_all(self):
        try:
            self._cursor.execute(f"SELECT {','.join(self.columns)} from {self.table}")
            return PySqlCollection(self._cursor.fetchall(), self.columns, self._meta_class)
        except ProgrammingError as e:
            print(e)

    def filter(self, *args, **kwargs):
        if not all([key in self.columns for key in kwargs.keys()]):
            raise (ColumnNotFountInClass(kwargs.keys(), self.table))
        else:
            where_clause = " and ".join([f"{key}='{kwargs[key]}'" for key in kwargs])
            self._cursor.execute(f"SELECT {','.join(self.columns)} from {self.table} WHERE {where_clause}")
            return PySqlCollection(self._cursor.fetchall(), self.columns, self._meta_class)

    def insert(self, ins_data: List[dict], update_on_duplicate=None):
        query = f"INSERT INTO {self.table}({','.join(self.columns)}) VALUES "
        gen = ["(" + ','.join([f"'{data.get(col)}'" for col in self.columns]) + ")" for data in ins_data]
        print(self.columns)
        ex_query = query + ",".join(gen)
        if update_on_duplicate is not None:
            ex_query += "ON DUPLICATE KEY UPDATE " + ",".join([f"{col}=VALUES({col})" for col in update_on_duplicate])

        print(ex_query)
        self._cursor.execute(ex_query)

        self.db.commit()
        return self
