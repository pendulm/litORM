import collections
import sqlite3
from datetime import datetime

class DataBase:
    _cursor = None
    @classmethod
    def connect(cls, dbname=":memory:"):
        if cls._cursor:
            return cls._cursor
        conn = sqlite3.connect(dbname)
        cls._conn = conn
        cursor = conn.cursor()
        cls._cursor = cursor
        return cursor


class Field:
    _type = None

    def __get__(self, obj, objtype):
        if obj is None:
            return self
        name = self._get_name_from_cls(objtype)
        if name and name in obj._cache:
            return obj._cache[name]
        return None

    def __set__(self, obj, val):
        if not isinstance(val, self._type):
            # TODO: trackback in true assign context
            raise TypeError("expect {} but got {}".format(self._type, type(val)))
        obj._cache[self._columnname] = val



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
    _type = bool


class Meta(type):
    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        "prepare the namespace dict"
        return collections.OrderedDict()
    
    def __new__(cls, name, bases, namespace, **kwds):
        result = type.__new__(cls, name, bases, dict(namespace))
        result._fields = tuple(k for k, v in namespace.items() if
                               isinstance(v, Field))
        for column in result._fields:
            namespace[column]._columnname = column

        return result

class Model(metaclass=Meta):
    def __init__(self):
        self._cache = {}

    def save(self):
        if self.isnew():
            cursor.execute("")
        else:
            cursor.execute("")


if __name__ == "__main__":
    class User(Model):
        name = TextField()
        age = IntegerField()

    u = User()
    u.name = "mike"
    u.age = 24
    print(u.__dict__)
    u.age = 25
    print(u.__dict__)
