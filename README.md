# PysqlManager
A python package to manage sql

## How to Use ? 

Creating a PySql object is the first step. All function are defined in PySql Class (Which is base class for PysqlManager Module)

For creating PySql object we need a meta_class / reference class (meta_class is nothing but a class structure for SQL table)

User(id varchar(25), name varchar(20), Age INT)

For above table , the reference class will be 

    from pysql_manager.types import Column, IntegerType, StringType
    
    class User:
        id = Column(col_type=IntegerType())
        name = Column(col_type=StringType(25))
        age = Column(col_type=IntegerType())
        __table__ = "User"

Now we can use this meta_class to create actual PySql objcet 

    from pysql_manager import PySql

    users = PySql("localhost", "root", "passowrd", "DB", User)
    users.fetch_all.show() #sample method for fetching and shoing all the data from table User
    
