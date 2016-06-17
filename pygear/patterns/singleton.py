# -*- coding: utf-8 -*-
from pygear.core import six


class SingletonMetaClass(type):
    """ Singleton Pattern """
    def __init__(cls, name, bases, attrs):
        super(SingletonMetaClass, cls).__init__(name, bases, attrs)
        original_new = cls.__new__

        def my_new(cls, *args, **kwds):
            if cls.instance is None:
                cls.instance = original_new(cls, *args, **kwds)
            return cls.instance
        cls.instance = None
        cls.__new__ = staticmethod(my_new)


class Singleton(six.with_metaclass(SingletonMetaClass)):
    """
    >>> class SingleFoo(Singleton): pass;
    >>> foo1 = SingleFoo()
    >>> foo1.bar = 1
    >>> foo2 = SingleFoo()
    >>> foo2.bar
    1
    >>> foo1 == foo2
    True
    """
    pass