from os.path import dirname, join
from unittest import TestCase

from yandil.discovery.module_discovery import discover_modules


class TestModuleDiscovery(TestCase):
    __DISCOVERY_BASE_PATH = join(dirname(dirname(__file__)), "resources", "dependency_discovery_tests_module")

    def test_discover_modules_from_path(self):
        discovered_modules = list(discover_modules(self.__DISCOVERY_BASE_PATH))

        self.assertEqual(7, len(discovered_modules))
        discovered_module_names = [module.module_name for module in discovered_modules]
        expected_module_names = [
            "class_with_public_methods",
            "another_class_with_public_methods",
            "class_dataclass",
            "dependency_class",
            "class_without_public_methods",
            "declarative_dependency_class",
            "abstract_class",
        ]
        self.assertCountEqual(expected_module_names, discovered_module_names)

    def test_discover_modules_from_path_with_excluded_modules(self):
        excluded_modules = {"first_module"}

        discovered_modules = list(discover_modules(self.__DISCOVERY_BASE_PATH, excluded_modules))

        self.assertEqual(6, len(discovered_modules))
        discovered_module_names = [module.module_name for module in discovered_modules]
        expected_module_names = [
            "another_class_with_public_methods",
            "class_dataclass",
            "dependency_class",
            "class_without_public_methods",
            "declarative_dependency_class",
            "abstract_class",
        ]
        self.assertCountEqual(expected_module_names, discovered_module_names)
