class ColumnNotFountInClass(Exception):
    def __init__(self, columns, table, message="Column {0} not found in master class for table "):
        self.salary = columns
        self.table = table
        self.message = message
        super().__init__(self.message.format(list(columns)) + self.table)


class TableNotFoundInClass(Exception):
    def __init__(self,  meta_class_name):
        self.meta_class_name = meta_class_name
        super().__init__(f"Table not defined in Class {self.meta_class_name}")


class EmptyPysqlCollectionError(Exception):
    def __init__(self):
        super().__init__("Empty PysqlCollection Error")