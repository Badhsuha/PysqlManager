# PysqlManager
A python package to manage sql

# GETTING STARTED !

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
    


## FETCH ALL DATA FROM SQL TABLE

    from pysql_manager.types import Column, IntegerType, StringType
    
    class User:
        id = Column(col_type=IntegerType())
        name = Column(col_type=StringType(25))
        age = Column(col_type=IntegerType())
        __table__ = "User"
    
        from pysql_manager import PySql

    users = PySql("localhost", "root", "passowrd", "DB", User)
    users.fetch_all.show()

fetch_all method will return a PySqlCollection object , which contain rich functionalities().

<br />

### .show() - To show data in table form
    users.fetch_all.show() -> None
<br />

### .first() - Return first row
A single Row is nothing but an object of base class. For above example , each row will be an object of class User
means, we can access row.column (In this case row.age, row.id, row.name etc)

    users.fetch_all.fisrt() -> single meta_class object

### .last() - To get last row
    users.fetch_all.last() -> single meta_class object
<br />

### .is_empty() - To get last row
    users.fetch_all.is_empty() -> Boolean
<br />

### .count() - To get total count of rows
    users.fetch_all.count() -> Integer
<br />

### .count() - To get total count of rows
    users.fetch_all.count() -> Integer
<br />

### .to_df() - Create pandas DataFrame
Column name defined in meta_class will be taken for Pandas DataFrame creation

    users.fetch_all.to_df() -> Pandas DataFrame
<br />

### .to_list_dict() - Creates List of python dictionaries
List of python dictionaries. Where each dictionary will be a SQL record

    users.fetch_all.count() -> List[dict]
<br />

### .save_as_csv() - To save PySqlCollection object as CSV file.

    users.fetch_all.save_as_csv(path, delimiter="|") -> None
<br />

### .select() - To select specific columns from PySqlCollection
    users.fetch_all.select(["age", "id]) -> PySqlCollection
Since this is also returning a PySqlCollection, this can be again chained with all above methods.

Eg

    users.fetch_all.select(["age", "id]).count()
    users.fetch_all.select(["age", "id]).fisrt()
    users.fetch_all.select(["age", "id]).last()
    users.fetch_all.select(["age", "id]).show()


## FILTER DATA FROM SQL

For filtering data from SQL using PySql-Manager just use the inbuilt filter() method

    users.filter("age > 10") -> PySqlFilterObj

<br />

filter is a special method which will return a PySqlFilterObj which can be then used to fetch filtered data
(which will return same PySqlCollection when using fetch_all() - fetch_all will return all data from SQL, but filter().fetch_filtered will return filtered data)
or can be used to update, or delete filtered data

<br />

### .fetch_filtered - To get PySqlCollection of filtered SQL data
        users.filter("age > 10").fecth_filtered -> PySqlCollection
<br />

### .update() - To update filtered data
        users.filter("age > 10").update(nam="newName", age="12") -> None
<br />

### .delete() - To delete filtered data
        users.filter("age > 10").delete() -> None
