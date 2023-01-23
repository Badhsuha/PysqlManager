from pysql_manager import PySql
from pysql_manager.types import Column, IntegerType, StringType

class User:
    id = Column(col_type=IntegerType())
    name = Column(col_type=StringType(25))
    age = Column(col_type=IntegerType())
    __table__ = "User"

#
users = PySql("localhost", "root", "Probadhu@1122", "Test", User)

data = [{"name": "user1", "id": 1, "age": "22"}, {"name": "user2", "id": 2, "age": "17"}, {"name": "user2", "id": 3, "age": "22"},
        {"name": "user4", "id": 4, "age": "26"}
        ]

# users.insert(data)

# users.fetch_all.show()


# # data = [{"id": 13, "age": 26}, {"id": 14, "name": "Faisal", "age": 26}]
# #
# # users.insert(data, update_on_duplicate=["name", "age"])
#
# # print(users.filter(named="Faisal").count())
# users.filter(age=30).save_as_csv()
# data = [{'revenue': '234779.855722', 'spend': None, 'paidImpressions': '107863292', 'id': 'publisher1337992022-11-10', 'entity': 'publisher', 'resourceId': '133799', 'timeZone': 'PST', 'date': '2022-11-10'}, {'revenue': '1476.712510', 'spend': None, 'paidImpressions': '14948592', 'id': 'publisher1583902022-11-10', 'entity': 'publisher', 'resourceId': '158390', 'timeZone': 'PST', 'date': '2022-11-10'}]
#
# billing_tbl = PySql("localhost", "root", "password", "appexplorer", BillingTable)
#
# billing_tbl.insert(data)