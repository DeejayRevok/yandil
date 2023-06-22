from os.path import dirname, join
from unittest import TestCase

from yandil.discovery.class_discovery import (
    class_defines_public_methods,
    class_has_any_decorator,
    discover_classes_from_module,
    exclude_abstract_classes,
    exclude_classes_without_decorators,
    exclude_classes_without_public_methods,
    exclude_dataclasses,
    transform_class_nodes_to_class_data,
)


class TestClassDiscovery(TestCase):
    __DISCOVERY_BASE_PATH = join(dirname(dirname(__file__)), "resources", "dependency_discovery_tests_module")

    def test_discover_classes_from_module(self):
        module_file_path = join(self.__DISCOVERY_BASE_PATH, "first_module", "class_with_public_methods.py")

        discovered_classes = list(discover_classes_from_module(module_file_path))

        self.assertEqual(1, len(discovered_classes))
        discovered_class = discovered_classes[0]
        self.assertEqual("ClassWithPublicMethods", discovered_class.name)

    def test_transform_class_nodes_to_class_data(self):
        module_file_path = join(self.__DISCOVERY_BASE_PATH, "first_module", "class_with_public_methods.py")
        discovered_classes = discover_classes_from_module(module_file_path)

        class_data = list(transform_class_nodes_to_class_data(discovered_classes, module_file_path))

        self.assertEqual(1, len(class_data))
        class_data = class_data[0]
        self.assertEqual("ClassWithPublicMethods", class_data.class_name)
        self.assertEqual(module_file_path, class_data.module_file_path)

    def test_exclude_classes_without_public_methods(self):
        module_file_path = join(self.__DISCOVERY_BASE_PATH, "class_without_public_methods.py")
        discovered_classes = discover_classes_from_module(module_file_path)

        class_excluding_ones_without_public_methods = list(exclude_classes_without_public_methods(discovered_classes))

        self.assertEqual(0, len(class_excluding_ones_without_public_methods))

    def test_class_defines_public_methods(self):
        class_without_public_methods_module_file_path = join(
            self.__DISCOVERY_BASE_PATH, "class_without_public_methods.py"
        )
        class_with_public_methods_module_file_path = join(
            self.__DISCOVERY_BASE_PATH, "first_module", "class_with_public_methods.py"
        )
        class_with_public_methods_discovered_classes = next(
            discover_classes_from_module(class_with_public_methods_module_file_path)
        )
        class_without_public_methods_discovered_classes = next(
            discover_classes_from_module(class_without_public_methods_module_file_path)
        )

        scenarios = [
            {
                "message": "Class defines public methods",
                "class_node": class_with_public_methods_discovered_classes,
                "expected_result": True,
            },
            {
                "message": "Class does not define public methods",
                "class_node": class_without_public_methods_discovered_classes,
                "expected_result": False,
            },
        ]
        for scenario in scenarios:
            with self.subTest(scenario["message"]):
                self.assertEqual(scenario["expected_result"], class_defines_public_methods(scenario["class_node"]))

    def test_exclude_dataclasses(self):
        module_file_path = join(self.__DISCOVERY_BASE_PATH, "class_dataclass.py")
        discovered_classes = discover_classes_from_module(module_file_path)

        class_excluding_dataclasses = list(exclude_dataclasses(discovered_classes))

        self.assertEqual(0, len(class_excluding_dataclasses))

    def test_class_has_any_decorator(self):
        module_file_path = join(self.__DISCOVERY_BASE_PATH, "declarative_dependency_class.py")
        discovered_class = next(discover_classes_from_module(module_file_path))

        scenarios = [
            {"message": "Class has any decorator", "decorator_names": {"dependency", "test"}, "expected_result": True},
            {
                "message": "Class does not have any decorator",
                "decorator_names": {"test1", "test2"},
                "expected_result": False,
            },
        ]
        for scenario in scenarios:
            with self.subTest(scenario["message"]):
                self.assertEqual(
                    scenario["expected_result"], class_has_any_decorator(discovered_class, scenario["decorator_names"])
                )

    def test_exclude_classes_without_decorators(self):
        module_file_path = join(self.__DISCOVERY_BASE_PATH, "declarative_dependency_class.py")
        discovered_classes = discover_classes_from_module(module_file_path)

        class_excluding_ones_without_decorators = list(exclude_classes_without_decorators(discovered_classes, {"test"}))

        self.assertEqual(0, len(class_excluding_ones_without_decorators))

    def test_exclude_abstract_classes(self):
        module_file_path = join(self.__DISCOVERY_BASE_PATH, "abstract_classes.py")
        discovered_classes = discover_classes_from_module(module_file_path)

        classes_excluding_abstract_classes = list(exclude_abstract_classes(discovered_classes))

        self.assertEqual(0, len(classes_excluding_abstract_classes))
