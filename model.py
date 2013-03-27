import collections
import sqlite3
from datetime import datetime

cursor = None

class DataBase:
    _cursor = None
    _conn = None

    class WrapperCursor(sqlite3.Cursor):
        def execute(self, sql, param=None):
            if True:
                print(sql, param)
            if param:
                super().execute(sql, param)
            else:
                super().execute(sql)

    @classmethod
    def connect(cls, dbname):
        if cls._cursor:
            return cls._cursor
        conn = sqlite3.connect(dbname)
        cls._conn = conn
        cursor = cls.WrapperCursor(conn)
        cls._cursor = cursor
        cursor.row_factory = sqlite3.Row
        return cursor


def usedb(dbname=":memory:"):
    global cursor
    cursor = DataBase.connect(dbname)


class Field:
    _type = None

    def __get__(self, obj, objtype):
        if obj is None:
            return self
        name = self._columnname
        if name and name in obj._cache:
            return obj._cache[name]
        return None

    def __set__(self, obj, val):
        if not isinstance(val, self._type):
            print(self._columnname, val)
            raise TypeError("expect {} but got {}".format(self._type, type(val)))
        obj._cache[self._columnname] = val

    @classmethod
    def sqltype(cls):
        return cls.__name__[:-5].upper()


class IntegerField(Field):
    _type = int

class RealField(Field):
    _type = float

class TextField(Field):
    _type = str

class BlobField(Field):
    _type = bytes

class DateField(Field):
    _type = datetime

class TimeStampField(Field):
    # TODO: what its exactly type
    _type = int

class BolleanField(Field):
    _type = int


class Meta(type):
    # first class will be the model class
    define_model = False

    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        # prepare the namespace dict
        return collections.OrderedDict()
    
    def __new__(cls, name, bases, namespace, **kwds):
        result = type.__new__(cls, name, bases, dict(namespace))
        return result

    def __init__(self, name, bases, namespace):
        # namespace is same as which in __new__
        # but namespace is not self.__dict__ so don't insert in namespace
        # first __new__ then __init__
        if not Meta.define_model:
            Meta.define_model = True
            return

        self._fields = tuple((k, v.sqltype()) for k, v in namespace.items() if
                               isinstance(v, Field))
        for column, _ in self._fields:
            namespace[column]._columnname = column

        self._rows = 0
        self._iscreated = False
        self._tablename = self.__name__.lower()
        self.create_table()
    
    def __len__(self):
        if not self._iscreated:
            raise RuntimeError("table '{}' has not create yet".format(
                self._tablename))

        cursor.execute("select count(*) from " + self._tablename + ";")
        self._rows = cursor.fetchone()[0]
        return self._rows


class Model(metaclass=Meta):

    def __init__(self):
        self._cache = {}
    
    @classmethod
    def create_table(cls):
        if cls._iscreated:
            return
        column_def = ", ".join([a + " " + b for (a, b) in cls._fields]) 
        # must define extra fields
        sql_stmt = "create table if not exists {} (_id INTEGER PRIMARY KEY, {});"
        sql_stmt = sql_stmt.format(cls.__name__.lower(), column_def)
        cursor.execute(sql_stmt)
        cls._iscreated = True

    @classmethod
    def find(cls, _id):
        sql_stmt = "select * from {} where _id = ?;".format(cls._tablename)
        cursor.execute(sql_stmt, (_id,))
        row = cursor.fetchone()
        if row is None:
            return None

        obj = cls()

        for k in row.keys():
            if row[k] is not None:
                if k == '_id':
                    obj._cache['_id'] = row[k]
                else:
                    setattr(obj, k, row[k])
        return obj


    def save(self):
        name_seq = [n for (n, t) in self._fields if n in self._cache] 
        value_seq = tuple(self._cache[n] for n in name_seq)
        tablename = self._tablename
        if '_id' in self._cache:
            sql_stmt = "update {} set {} where _id = {};".format(tablename,
                    ', '.join(n + ' = ?' for n in name_seq), self._cache['_id'])
            cursor.execute(sql_stmt, value_seq)
        else:
            sql_stmt = "insert into {} ({}) values ({});".format(tablename,
                    ", ".join(name_seq), ("?,"*len(name_seq))[:-1])
            cursor.execute(sql_stmt, value_seq)

