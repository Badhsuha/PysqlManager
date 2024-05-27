from pysql_manager.errors import EmptyPysqlCollectionError


def check_data_availability(func):
    def wrap(self, *args, **kwargs):
        if self.count() != 0:
            result = func(self, *args, **kwargs)
            return result
        else:
            raise EmptyPysqlCollectionError()

    return wrap
