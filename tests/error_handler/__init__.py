import unittest
from src.error_handler import catch, ERROR_HANDLER
from src.error_handler.strategies.string_to_int import StringToIntStrategy

from .strategies import *
from .predicates import *


@catch
class DummyClass:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return self.value + other


class TestErrorHandler(unittest.TestCase):
    def setUp(self):
        ERROR_HANDLER.add_strategy(StringToIntStrategy)

    def test_error_handler(self):
        self.assertEqual(DummyClass(1) + "1", 2)


if __name__ == '__main__':
    unittest.main()