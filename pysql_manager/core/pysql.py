import sys
from typing import List
import mysql.connector
from mysql.connector.errors import ProgrammingError
from pysql_manager.core.bases import PySqlFilterObj, PySqlCollection
from pysql_manager.types import _Column
from pysql_manager.errors import TableNotFoundInClass

__version__ = "0.0.1"
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
        self.columns = list(filter(lambda x: isinstance(getattr(self._meta_class, x), _Column), dir(meta_class)))

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

    def filter(self, filter_opt):
        return PySqlFilterObj(filter_query=filter_opt,
                              cursor=self._cursor,
                              meta_class=self._meta_class,
                              columns=self.columns,
                              table=self.table,
                              db=self.db
                              )

    def insert(self, ins_data: List[dict], update_on_duplicate=None):
        query = f"INSERT INTO {self.table}({','.join(self.columns)}) VALUES "
        gen = ["(" + ','.join([f"'{data.get(col) if data.get(col) else  getattr(self._meta_class, col).default}'" for col in self.columns]) + ")" for data in ins_data]

        ex_query = query + ",".join(gen)
        print(ex_query)
        # sys.exit(-1)
        if update_on_duplicate is not None:
            ex_query += "ON DUPLICATE KEY UPDATE " + ",".join([f"{col}=VALUES({col})" for col in update_on_duplicate])

        self._cursor.execute(ex_query)

        self.db.commit()
        return self
