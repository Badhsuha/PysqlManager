from pysql_manager import PySql
from pysql_manager.types import Column, IntegerType, StringType

class User:
    id = Column(col_type=IntegerType())
    name = Column(col_type=StringType(25))
    age = Column(col_type=IntegerType())
    __table__ = "User"

#

class BillingTable:
    id = StringType(255)
    revenue = IntegerType()
    spend = IntegerType()
    paidImpressions = IntegerType()
    entity = StringType(25)
    resourceId = IntegerType()
    timeZone = StringType(6)
    date = StringType(25)

    __table__ = "tbl_daily_monthly_billing"

users = PySql("localhost", "root", "Probadhu@1122", "Test", User)

users.fetch_all.show()
# # data = [{"id": 13, "age": 26}, {"id": 14, "name": "Faisal", "age": 26}]
# #
# # users.insert(data, update_on_duplicate=["name", "age"])
#
# # print(users.filter(named="Faisal").count())
# users.filter(age=30).save_as_csv()
# data = [{'revenue': '234779.855722', 'spend': None, 'paidImpressions': '107863292', 'id': 'publisher1337992022-11-10', 'entity': 'publisher', 'resourceId': '133799', 'timeZone': 'PST', 'date': '2022-11-10'}, {'revenue': '1476.712510', 'spend': None, 'paidImpressions': '14948592', 'id': 'publisher1583902022-11-10', 'entity': 'publisher', 'resourceId': '158390', 'timeZone': 'PST', 'date': '2022-11-10'}]
#
# billing_tbl = PySql("localhost", "root", "Probadhu@1122", "appexplorer", BillingTable)
#
# billing_tbl.insert(data)
