from pysql_manager.types import Column, StringType, IntegerType

from pysql_manager import PySql

class Users:
    id = Column(col_type=StringType(25))
    name = Column(col_type=StringType(20))
    age = Column(col_type=IntegerType())
    __table__ = "Users"


users = PySql("localhost", "root", "password", "Test", Users)

data = [{"id": "1", "name": "user1", "age": 45},
        {"id": "2", "name": "user2", "age": 17},
        {"id": "3", "name": "user3", "age": 23},
        {"id": "4", "name": "user4", "age": 22}]



# users.insert(data, update_on_duplicate=["dataSize"])

print(users.fetch_all.to_list_dict())
print(users.fetch_all.count())
print(users.fetch_all.save_as_csv("users.csv", delimiter="|"))
print(users.fetch_all.to_df().head())
# users.fetch_all.show()