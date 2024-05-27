# PysqlManager
A python package to manage sql

# GETTING STARTED !

Creating a PySql object is the first step. All function are defined in PySql Class (Which is base class for PysqlManager Module)

For creating PySql object we need a meta_class / reference class (meta_class is nothing but a class structure for SQL table)

User(id varchar(25), name varchar(20), Age INT)

For above table , the reference class will be

```Python
from pysql_manager.types import IntegerType, StringType


class User:
    id = IntegerType()
    name = StringType(length=25)
    age = IntegerType()
    __table__ = "User"


# Now we can use this meta_class to create actual PySql objcet 

from pysql_manager import PySql

users = PySql("localhost", "root", "passowrd", "DB", User)
users.fetch_all.show()  # sample method for fetching and showing all the data from table User
```  


## FETCH ALL DATA FROM SQL TABLE

```Python
from pysql_manager.types import IntegerType, StringType


class User:
    id = IntegerType()
    name = StringType(25)
    age = IntegerType()
    __table__ = "User"


from pysql_manager import PySql

users = PySql("localhost", "root", "passowrd", "DB", User)
users.fetch_all  # Return PySqlConnection
```

fetch_all method will return a PySqlCollection object , which contain rich functionalities.

<br />

### .show() - To show data in table form
```Python
users.fetch_all.show()  # Return None
```
<br />

### .first() - Return first row
A single Row is nothing but an object of base class. For above example , each row will be an object of class User
means, we can access `row.column` (In this case row.age, row.id, row.name etc)

```Python
users.fetch_all.first() # Return single meta_class object
```

### .last() - To get last row
```Python
users.fetch_all.last() # Return single meta_class object
```
<br />

### .is_empty() - To get last row
```Python
users.fetch_all.is_empty() # Return Boolean
```
<br />

### .count() - To get total count of rows
```Python
users.fetch_all.count() # Return Integer
```
<br />

### .to_df() - Create pandas DataFrame
Column name defined in meta_class will be taken for Pandas DataFrame creation
```Python
users.fetch_all.to_df() # Return pandas DataFrame
```

<br />

### .to_list_dict() - Creates List of python dictionaries
List of python dictionaries. Where each dictionary will be a SQL record
```Python
users.fetch_all.to_list_dict() # Return List[dict]
```

<br />

### .save_as_csv() - To save PySqlCollection object as CSV file.
```Python
users.fetch_all.save_as_csv("path", delimiter="|") # Return None
```

<br />

### .select() - To select specific columns from PySqlCollection
```Python
users.fetch_all.select(["age", "id"]) # Return PySqlCollection 
```
    
Since this is also returning a PySqlCollection, this can be again chained with all above methods.

Eg
```Python
users.fetch_all.select(["age", "id"]).count()
users.fetch_all.select(["age", "id"]).first()
users.fetch_all.select(["age", "id"]).last()
users.fetch_all.select(["age", "id"]).show()
```

## FILTER DATA FROM SQL

For filtering data from SQL using PySql-Manager just use the inbuilt filter() method
    

```Python
users.filter("age > 10") # Return PySqlFilterObj
```

<br />

filter is a special method which will return a PySqlFilterObj which can be then used to fetch filtered data
(which will return same PySqlCollection when using fetch_all() - fetch_all will return all data from SQL, but filter().fetch_filtered will return filtered data)
or can be used to update, or delete filtered data

<br />

### .fetch_filtered - To get PySqlCollection of filtered SQL data
```Python
users.filter("age > 10").fetch_filtered # Return PySqlCollection
```
<br />

### .update() - To update filtered data
```Python
users.filter("age > 10").update(nam="newName", age="12") # Return None
```

<br />

### .delete() - To delete filtered data
```Python
users.filter("age > 10").delete() # Return None
```

## INSERT DATA TO SQL TABLE
Insert is done using .insert() method, The data should be List of python dictionaries.

```Python
from pysql_manager.types import IntegerType, StringType


class User:
    id = IntegerType()
    name = StringType(25)
    age = IntegerType()
    __table__ = "User"


from pysql_manager import PySql

users = PySql("localhost", "root", "passowrd", "DB", User)
sql_data = [{"id": 1, "name": "user1", "age": 22}, {"id": 2, "name": "user2", "age": 12}]
users.insert(sql_data)  # Return PySql self
```

If there is duplicate entry for primary key (In this case `id` column, it will raise `PRIMARY KEY ERROR`). To avoid this and update on duplicate key you can use `update_on_duplicate` argument and pass list columns you need to update when there is a duplicate entry.

```Python
from pysql_manager.types import IntegerType, StringType


class User:
    id = IntegerType()
    name = StringType(25)
    age = IntegerType()
    __table__ = "User"


from pysql_manager import PySql

users = PySql("localhost", "root", "passowrd", "DB", User)
sql_data = [{"id": 1, "name": "user1", "age": 22}, {"id": 2, "name": "user2", "age": 12}]
users.insert(sql_data, update_on_duplicate=["age"])  # Return PySql self
```


