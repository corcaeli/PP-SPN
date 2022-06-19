import pytest


class ClassPropertyDescriptor(object):
    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self


def classproperty(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return ClassPropertyDescriptor(func)


class Bar(object):

    _bar = 1

    @classproperty
    def bar(cls):
        return cls._bar

    @bar.setter
    def bar(cls, value):
        cls._bar = value


# test instance instantiation
foo = Bar()
assert foo.bar == 1

baz = Bar()
assert baz.bar == 1

# test static variable
baz.bar = 5
print(baz.bar)
assert foo.bar == 5
print(foo.bar)

# test setting variable on the class
Bar.bar = 50
assert baz.bar == 50
assert foo.bar == 50
print(Bar.bar)
