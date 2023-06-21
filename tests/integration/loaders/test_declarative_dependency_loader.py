from os.path import dirname, join
from unittest import TestCase

from yandil.container import default_container
from yandil.errors.dependency_not_found_error import DependencyNotFoundError
from yandil.loaders.declarative_dependency_loader import DeclarativeDependencyLoader


class TestDeclarativeDependencyLoader(TestCase):
    __DISCOVERY_BASE_PATH = join(dirname(dirname(__file__)), "resources", "dependency_discovery_tests_module")
    __SOURCES_ROOT_PATH = dirname(dirname(dirname(__file__)))

    def setUp(self) -> None:
        self.loader = DeclarativeDependencyLoader(
            discovery_base_path=self.__DISCOVERY_BASE_PATH,
            sources_root_path=self.__SOURCES_ROOT_PATH,
        )

    def test_load(self):
        self.loader.load()

        from integration.resources.dependency_discovery_tests_module.declarative_dependency_class import (
            DeclarativeDependencyClass,
        )

        declarative_dependency_class_instance = default_container[DeclarativeDependencyClass]
        self.assertIsNotNone(declarative_dependency_class_instance)
        self.assertIsInstance(declarative_dependency_class_instance, DeclarativeDependencyClass)
        from integration.resources.dependency_discovery_tests_module.dependency_class import DependencyClass

        with self.assertRaises(DependencyNotFoundError) as context:
            _ = default_container[DependencyClass]
        self.assertEqual(DependencyClass, context.exception.dependency_type)
