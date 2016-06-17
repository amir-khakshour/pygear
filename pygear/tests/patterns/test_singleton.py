import unittest

from pygear.patterns import singleton


class SingleFoo(singleton.Singleton):
    pass


class TestSingleton(unittest.TestCase):
    def test_singleton(self):
        foo1 = SingleFoo()
        foo1.bar = 1
        foo2 = SingleFoo()
        self.assertEqual(foo1.bar, foo2.bar)
        self.assertEqual(foo1, foo2)
