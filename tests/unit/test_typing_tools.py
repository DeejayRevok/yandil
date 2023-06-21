from typing import List, Set, Tuple
from unittest import TestCase

from yandil.typing_tools import is_type_hint_iterable, str_to_builtin_type, type_hint_iterable_builder_factory


class TestTypingTools(TestCase):
    def test_is_type_hint_iterable(self):
        scenarios = [
            {"message": "List type hint", "type_hint": List, "expected": True},
            {"message": "Set type hint", "type_hint": Set, "expected": True},
            {"message": "Tuple type hint", "type_hint": Tuple, "expected": True},
        ]
        for scenario in scenarios:
            with self.subTest(scenario["message"]):
                self.assertEqual(scenario["expected"], is_type_hint_iterable(scenario["type_hint"]))

    def test_is_type_hint_iterable_not_iterable(self):
        result = is_type_hint_iterable(int)

        self.assertFalse(result)

    def test_type_hint_iterable_builder_factory(self):
        scenarios = [
            {"message": "List type hint", "type_hint": List, "expected": list},
            {"message": "Set type hint", "type_hint": Set, "expected": set},
            {"message": "Tuple type hint", "type_hint": Tuple, "expected": tuple},
        ]
        for scenario in scenarios:
            with self.subTest(scenario["message"]):
                self.assertEqual(scenario["expected"], type_hint_iterable_builder_factory(scenario["type_hint"]))

    def test_type_hint_iterable_builder_factory_not_iterable(self):
        with self.assertRaises(NotImplementedError):
            type_hint_iterable_builder_factory(int)

    def test_str_to_builtin_type(self):
        scenarios = [
            {"message": "int", "value": "1", "target_type": int, "expected": 1},
            {"message": "bool", "value": "True", "target_type": bool, "expected": True},
            {"message": "bool", "value": "False", "target_type": bool, "expected": False},
            {"message": "float", "value": "1.0", "target_type": float, "expected": 1.0},
        ]
        for scenario in scenarios:
            with self.subTest(scenario["message"]):
                self.assertEqual(scenario["expected"], str_to_builtin_type(scenario["value"], scenario["target_type"]))

    def test_str_to_bool_invalid_value(self):
        with self.assertRaises(ValueError):
            str_to_builtin_type("invalid", bool)

    def test_str_to_bool(self):
        scenarios = [
            {"message": "True", "value": "True", "expected": True},
            {"message": "False", "value": "False", "expected": False},
            {"message": "true", "value": "true", "expected": True},
            {"message": "false", "value": "false", "expected": False},
            {"message": "1", "value": "1", "expected": True},
            {"message": "0", "value": "0", "expected": False},
            {"message": "y", "value": "y", "expected": True},
            {"message": "n", "value": "n", "expected": False},
            {"message": "yes", "value": "yes", "expected": True},
            {"message": "no", "value": "no", "expected": False},
            {"message": "t", "value": "t", "expected": True},
            {"message": "f", "value": "f", "expected": False},
            {"message": "on", "value": "on", "expected": True},
            {"message": "off", "value": "off", "expected": False},
        ]
        for scenario in scenarios:
            with self.subTest(scenario["message"]):
                self.assertEqual(scenario["expected"], str_to_builtin_type(scenario["value"], bool))
