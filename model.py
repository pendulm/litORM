import collections
import sqlite3

class Field:
    def __get__(self, obj, objtype):
        if obj is None:
            return type(self)
        name = self._get_name_from_cls(objtype)
        if name and name in obj._cache:
            return obj._cache[name]
        return None

    def __set__(self, obj, val):
        name = self._get_name_from_cls(type(obj))
        obj._cache[name] = val

    def _get_name_from_cls(self, cls):
        d = cls.__dict__
        for name in d:
            if self is d[name]:
                return name
        # never going here
        assert False


class IntegerField(Field):
    pass

class RealField(Field):
    pass

class TextField(Field):
    pass

class BlobField(Field):
    pass

class DateField(Field):
    pass

class TimeStampField(Field):
    pass

class BolleanField(Field):
    pass


class Meta(type):
    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        "prepare the namespace dict"
        return collections.OrderedDict()
    
    def __new__(cls, name, bases, namespace, **kwds):
        result = type.__new__(cls, name, bases, dict(namespace))
        result._fields = tuple(k for k, v in namespace.items() if
                               isinstance(v, Field))
        return result

class Model(metaclass=Meta):
    def __init__(self):
        self._cache = {}

if __name__ == "__main__":
    class User(Model):
        name = TextField()
        age = IntegerField()

    u = User()
    u.name = "mike"
    u.age = 23
    print(u.__dict__)
    print(u.age)
    print(u.name)
