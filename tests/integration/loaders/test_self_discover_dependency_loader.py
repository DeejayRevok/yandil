from os.path import dirname, join
from pathlib import Path
from unittest import TestCase

from integration.resources.dependency_discovery_tests_module.class_dataclass import ClassDataclass
from integration.resources.dependency_discovery_tests_module.classes_without_defined_public_methods import (
    ClassWithoutDefinedPublicMethods,
    DependencyClassChildrenWithoutDefinedPublicMethods,
)
from integration.resources.dependency_discovery_tests_module.declarative_dependency_class import (
    DeclarativeDependencyClass,
)
from integration.resources.dependency_discovery_tests_module.dependency_class import DependencyClass
from integration.resources.dependency_discovery_tests_module.enum_classes import EnumClass
from integration.resources.dependency_discovery_tests_module.exception_classes import BaseExceptionClass, ExceptionClass
from integration.resources.dependency_discovery_tests_module.first_module.class_with_public_methods import (
    ClassWithPublicMethods,
)
from integration.resources.dependency_discovery_tests_module.second_module.another_class_with_public_methods import (
    AnotherClassWithPublicMethods,
)

from yandil.configuration.configuration_container import ConfigurationContainer
from yandil.container import Container
from yandil.errors.dependency_not_found_error import DependencyNotFoundError
from yandil.loaders.self_discover_dependency_loader import SelfDiscoverDependencyLoader


class TestSelfDiscoverDependencyLoader(TestCase):
    __DISCOVERY_BASE_PATH = join(dirname(dirname(__file__)), "resources", "dependency_discovery_tests_module")
    __SOURCES_ROOT_PATH = dirname(dirname(dirname(__file__)))

    def setUp(self) -> None:
        self.configuration_container = ConfigurationContainer()
        self.container = Container(self.configuration_container)

    def test_load_all_dependencies(self):
        loader = SelfDiscoverDependencyLoader(
            discovery_base_path=self.__DISCOVERY_BASE_PATH,
            sources_root_path=self.__SOURCES_ROOT_PATH,
            excluded_modules=None,
            should_exclude_classes_without_public_methods=False,
            should_exclude_dataclasses=False,
            container=self.container,
            should_exclude_exceptions=False,
        )

        loader.load()

        dependency_class_instance = self.container[DependencyClass]
        self.assertIsInstance(dependency_class_instance, DependencyClass)
        declarative_dependency_class_instance = self.container[DeclarativeDependencyClass]
        self.assertIsInstance(declarative_dependency_class_instance, DeclarativeDependencyClass)
        class_without_public_methods_instance = self.container[ClassWithoutDefinedPublicMethods]
        self.assertIsInstance(class_without_public_methods_instance, ClassWithoutDefinedPublicMethods)
        self.assertEqual(dependency_class_instance, class_without_public_methods_instance.dependency)
        class_dataclass_instance = self.container[ClassDataclass]
        self.assertIsInstance(class_dataclass_instance, ClassDataclass)
        class_with_public_methods_instance = self.container[ClassWithPublicMethods]
        self.assertIsInstance(class_with_public_methods_instance, ClassWithPublicMethods)
        self.assertEqual(dependency_class_instance, class_with_public_methods_instance.dependency)
        another_class_with_public_methods_instance = self.container[AnotherClassWithPublicMethods]
        self.assertIsInstance(another_class_with_public_methods_instance, AnotherClassWithPublicMethods)
        base_exception_class_instance = self.container[BaseExceptionClass]
        self.assertIsInstance(base_exception_class_instance, BaseExceptionClass)
        exception_class_instance = self.container[ExceptionClass]
        self.assertIsInstance(exception_class_instance, ExceptionClass)
        with self.assertRaises(DependencyNotFoundError) as context:
            _ = self.container[EnumClass]
        self.assertEqual(EnumClass, context.exception.dependency_type)

    def test_load_dependencies_with_excluded_modules(self):
        loader = SelfDiscoverDependencyLoader(
            discovery_base_path=self.__DISCOVERY_BASE_PATH,
            sources_root_path=self.__SOURCES_ROOT_PATH,
            excluded_modules={"second_module"},
            should_exclude_classes_without_public_methods=False,
            should_exclude_dataclasses=False,
            container=self.container,
        )

        loader.load()

        dependency_class_instance = self.container[DependencyClass]
        self.assertIsInstance(dependency_class_instance, DependencyClass)
        declarative_dependency_class_instance = self.container[DeclarativeDependencyClass]
        self.assertIsInstance(declarative_dependency_class_instance, DeclarativeDependencyClass)
        class_without_public_methods_instance = self.container[ClassWithoutDefinedPublicMethods]
        self.assertIsInstance(class_without_public_methods_instance, ClassWithoutDefinedPublicMethods)
        self.assertEqual(dependency_class_instance, class_without_public_methods_instance.dependency)
        class_dataclass_instance = self.container[ClassDataclass]
        self.assertIsInstance(class_dataclass_instance, ClassDataclass)
        class_with_public_methods_instance = self.container[ClassWithPublicMethods]
        self.assertIsInstance(class_with_public_methods_instance, ClassWithPublicMethods)
        self.assertEqual(dependency_class_instance, class_with_public_methods_instance.dependency)
        with self.assertRaises(DependencyNotFoundError) as context:
            _ = self.container[AnotherClassWithPublicMethods]
        self.assertEqual(AnotherClassWithPublicMethods, context.exception.dependency_type)
        with self.assertRaises(DependencyNotFoundError) as context:
            _ = self.container[EnumClass]
        self.assertEqual(EnumClass, context.exception.dependency_type)

    def test_load_dependencies_with_excluded_classes_without_public_methods(self):
        loader = SelfDiscoverDependencyLoader(
            discovery_base_path=self.__DISCOVERY_BASE_PATH,
            sources_root_path=self.__SOURCES_ROOT_PATH,
            excluded_modules=None,
            should_exclude_classes_without_public_methods=True,
            should_exclude_dataclasses=False,
            container=self.container,
        )

        loader.load()

        dependency_class_instance = self.container[DependencyClass]
        self.assertIsInstance(dependency_class_instance, DependencyClass)
        declarative_dependency_class_instance = self.container[DeclarativeDependencyClass]
        self.assertIsInstance(declarative_dependency_class_instance, DeclarativeDependencyClass)
        class_dataclass_instance = self.container[ClassDataclass]
        self.assertIsInstance(class_dataclass_instance, ClassDataclass)
        class_with_public_methods_instance = self.container[ClassWithPublicMethods]
        self.assertIsInstance(class_with_public_methods_instance, ClassWithPublicMethods)
        self.assertEqual(dependency_class_instance, class_with_public_methods_instance.dependency)
        another_class_with_public_methods_instance = self.container[AnotherClassWithPublicMethods]
        self.assertIsInstance(another_class_with_public_methods_instance, AnotherClassWithPublicMethods)
        dependency_class_children_without_defined_public_methods_instance = self.container[
            DependencyClassChildrenWithoutDefinedPublicMethods
        ]
        self.assertIsInstance(
            dependency_class_children_without_defined_public_methods_instance,
            DependencyClassChildrenWithoutDefinedPublicMethods,
        )
        with self.assertRaises(DependencyNotFoundError) as context:
            _ = self.container[ClassWithoutDefinedPublicMethods]
        self.assertEqual(ClassWithoutDefinedPublicMethods, context.exception.dependency_type)
        with self.assertRaises(DependencyNotFoundError) as context:
            _ = self.container[EnumClass]
        self.assertEqual(EnumClass, context.exception.dependency_type)

    def test_load_dependencies_with_excluded_dataclasses(self):
        loader = SelfDiscoverDependencyLoader(
            discovery_base_path=self.__DISCOVERY_BASE_PATH,
            sources_root_path=self.__SOURCES_ROOT_PATH,
            excluded_modules=None,
            should_exclude_classes_without_public_methods=False,
            should_exclude_dataclasses=True,
            container=self.container,
        )

        loader.load()

        dependency_class_instance = self.container[DependencyClass]
        self.assertIsInstance(dependency_class_instance, DependencyClass)
        declarative_dependency_class_instance = self.container[DeclarativeDependencyClass]
        self.assertIsInstance(declarative_dependency_class_instance, DeclarativeDependencyClass)
        class_without_public_methods_instance = self.container[ClassWithoutDefinedPublicMethods]
        self.assertIsInstance(class_without_public_methods_instance, ClassWithoutDefinedPublicMethods)
        self.assertEqual(dependency_class_instance, class_without_public_methods_instance.dependency)
        class_with_public_methods_instance = self.container[ClassWithPublicMethods]
        self.assertIsInstance(class_with_public_methods_instance, ClassWithPublicMethods)
        self.assertEqual(dependency_class_instance, class_with_public_methods_instance.dependency)
        another_class_with_public_methods_instance = self.container[AnotherClassWithPublicMethods]
        self.assertIsInstance(another_class_with_public_methods_instance, AnotherClassWithPublicMethods)
        with self.assertRaises(DependencyNotFoundError) as context:
            _ = self.container[ClassDataclass]
        self.assertEqual(ClassDataclass, context.exception.dependency_type)
        with self.assertRaises(DependencyNotFoundError) as context:
            _ = self.container[EnumClass]
        self.assertEqual(EnumClass, context.exception.dependency_type)

    def test_load_dependencies_with_mandatory_modules(self):
        class_without_public_methods_module = Path(
            join(self.__DISCOVERY_BASE_PATH, "classes_without_defined_public_methods")
        )
        loader = SelfDiscoverDependencyLoader(
            discovery_base_path=self.__DISCOVERY_BASE_PATH,
            sources_root_path=self.__SOURCES_ROOT_PATH,
            excluded_modules=None,
            should_exclude_classes_without_public_methods=True,
            should_exclude_dataclasses=False,
            container=self.container,
            mandatory_modules={class_without_public_methods_module},
        )

        loader.load()

        dependency_class_instance = self.container[DependencyClass]
        self.assertIsInstance(dependency_class_instance, DependencyClass)
        declarative_dependency_class_instance = self.container[DeclarativeDependencyClass]
        self.assertIsInstance(declarative_dependency_class_instance, DeclarativeDependencyClass)
        class_dataclass_instance = self.container[ClassDataclass]
        self.assertIsInstance(class_dataclass_instance, ClassDataclass)
        class_with_public_methods_instance = self.container[ClassWithPublicMethods]
        self.assertIsInstance(class_with_public_methods_instance, ClassWithPublicMethods)
        self.assertEqual(dependency_class_instance, class_with_public_methods_instance.dependency)
        another_class_with_public_methods_instance = self.container[AnotherClassWithPublicMethods]
        self.assertIsInstance(another_class_with_public_methods_instance, AnotherClassWithPublicMethods)
        class_without_public_methods_instance = self.container[ClassWithoutDefinedPublicMethods]
        self.assertIsInstance(class_without_public_methods_instance, ClassWithoutDefinedPublicMethods)
        self.assertEqual(dependency_class_instance, class_without_public_methods_instance.dependency)
        with self.assertRaises(DependencyNotFoundError) as context:
            _ = self.container[EnumClass]
        self.assertEqual(EnumClass, context.exception.dependency_type)

    def test_load_dependencies_excluding_exceptions(self):
        loader = SelfDiscoverDependencyLoader(
            discovery_base_path=self.__DISCOVERY_BASE_PATH,
            sources_root_path=self.__SOURCES_ROOT_PATH,
            excluded_modules=None,
            should_exclude_classes_without_public_methods=False,
            should_exclude_dataclasses=False,
            container=self.container,
            should_exclude_exceptions=True,
        )

        loader.load()

        dependency_class_instance = self.container[DependencyClass]
        self.assertIsInstance(dependency_class_instance, DependencyClass)
        declarative_dependency_class_instance = self.container[DeclarativeDependencyClass]
        self.assertIsInstance(declarative_dependency_class_instance, DeclarativeDependencyClass)
        class_without_public_methods_instance = self.container[ClassWithoutDefinedPublicMethods]
        self.assertIsInstance(class_without_public_methods_instance, ClassWithoutDefinedPublicMethods)
        self.assertEqual(dependency_class_instance, class_without_public_methods_instance.dependency)
        class_dataclass_instance = self.container[ClassDataclass]
        self.assertIsInstance(class_dataclass_instance, ClassDataclass)
        class_with_public_methods_instance = self.container[ClassWithPublicMethods]
        self.assertIsInstance(class_with_public_methods_instance, ClassWithPublicMethods)
        self.assertEqual(dependency_class_instance, class_with_public_methods_instance.dependency)
        another_class_with_public_methods_instance = self.container[AnotherClassWithPublicMethods]
        self.assertIsInstance(another_class_with_public_methods_instance, AnotherClassWithPublicMethods)
        with self.assertRaises(DependencyNotFoundError) as context:
            _ = self.container[BaseExceptionClass]
        self.assertEqual(BaseExceptionClass, context.exception.dependency_type)
        with self.assertRaises(DependencyNotFoundError) as context:
            _ = self.container[ExceptionClass]
        self.assertEqual(ExceptionClass, context.exception.dependency_type)
        with self.assertRaises(DependencyNotFoundError) as context:
            _ = self.container[EnumClass]
        self.assertEqual(EnumClass, context.exception.dependency_type)
