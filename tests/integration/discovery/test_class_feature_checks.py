from unittest import TestCase

from integration.resources.dependency_discovery_tests_module.classes_without_defined_public_methods import (
    ClassWithoutDefinedPublicMethods,
    DependencyClassChildrenWithoutDefinedPublicMethods,
)
from integration.resources.dependency_discovery_tests_module.enum_classes import EnumClass
from integration.resources.dependency_discovery_tests_module.exception_classes import ExceptionClass

from yandil.discovery.class_feature_checks import has_public_methods, is_enum, is_exception


class TestClassFeatureChecks(TestCase):
    def test_has_public_methods(self):
        scenarios = [
            {
                "message": "Class has public methods",
                "class": DependencyClassChildrenWithoutDefinedPublicMethods,
                "expected_result": True,
            },
            {
                "message": "Class has not public methods",
                "class": ClassWithoutDefinedPublicMethods,
                "expected_result": False,
            },
        ]
        for scenario in scenarios:
            with self.subTest(scenario["message"]):
                class_has_public_methods = has_public_methods(scenario["class"])

                self.assertEqual(class_has_public_methods, scenario["expected_result"])

    def test_is_exception(self):
        scenarios = [
            {
                "message": "Class is exception",
                "class": ExceptionClass,
                "expected_result": True,
            },
            {
                "message": "Class is not exception",
                "class": ClassWithoutDefinedPublicMethods,
                "expected_result": False,
            },
        ]
        for scenario in scenarios:
            with self.subTest(scenario["message"]):
                class_is_exception = is_exception(scenario["class"])

                self.assertEqual(class_is_exception, scenario["expected_result"])

    def test_is_enum(self):
        scenarios = [
            {
                "message": "Class is enum",
                "class": EnumClass,
                "expected_result": True,
            },
            {
                "message": "Class is not enum",
                "class": ClassWithoutDefinedPublicMethods,
                "expected_result": False,
            },
        ]
        for scenario in scenarios:
            with self.subTest(scenario["message"]):
                class_is_enum = is_enum(scenario["class"])

                self.assertEqual(class_is_enum, scenario["expected_result"])
