import unittest
from unittest.mock import Mock

from typeguard import TypeCheckError

from src.error_handler.exceptions import PredicateNameError
from src.error_handler.predicates.core import PredicateFactory, BasePredicate, Predicate
from src.error_handler.strategies.core import ErrorHandlingStrategy

class TestPredicateFactory(unittest.TestCase):
    def test_creates_predicate_with_valid_function(self):
        mock_strategy = Mock(spec=ErrorHandlingStrategy)
        func = Mock(return_value=True)
        predicate = PredicateFactory.create_predicate("test_predicate", func)
        self.assertTrue(predicate(mock_strategy))

    def test_creates_predicate_with_invalid_function(self):
        mock_strategy = Mock(spec=ErrorHandlingStrategy)
        func = Mock(return_value=False)
        predicate = PredicateFactory.create_predicate("test_predicate", func)
        self.assertFalse(predicate(mock_strategy))

    def test_raises_error_with_invalid_name(self):
        with self.assertRaises(TypeCheckError):
            PredicateFactory.create_predicate(None, lambda x: True)

    def test_raises_error_with_invalid_function(self):
        with self.assertRaises(TypeCheckError):
            PredicateFactory.create_predicate("test_predicate", None)


class TestBasePredicate(unittest.TestCase):
    def test_cannot_instantiate_base_predicate(self):
        with self.assertRaises(TypeError):
            BasePredicate("test")


class TestPredicate(unittest.TestCase):
    def test_cannot_instantiate_predicate(self):
        with self.assertRaises(TypeError):
            Predicate("test")


if __name__ == '__main__':
    unittest.main()