from unittest import TestCase

from integration.resources.simple_dependency_classes import (
    FirstBaseChildrenDependencyClass,
    MixedDependenciesClientClass,
    SecondBaseChildrenDependencyClass,
    SimpleDependencyClientClass,
    SimpleDependencyDependencyClass,
)

from yandil.configuration.configuration_container import ConfigurationContainer
from yandil.container import Container
from yandil.dependency_filler import DependencyFiller


class TestDependencyFiller(TestCase):
    def setUp(self) -> None:
        self.container = Container(
            configuration_container=ConfigurationContainer(),
        )
        self.container.add(SimpleDependencyDependencyClass)
        self.container.add(FirstBaseChildrenDependencyClass)
        self.container.add(SecondBaseChildrenDependencyClass)
        self.dependency_filler = DependencyFiller(
            container=self.container,
        )

    def test_fill_dependencies(self):
        self.dependency_filler.fill(SimpleDependencyClientClass)

        container_dependency_class_instance = self.container[SimpleDependencyDependencyClass]
        client_class_instance = SimpleDependencyClientClass()
        self.assertIsInstance(client_class_instance, SimpleDependencyClientClass)
        self.assertEqual(container_dependency_class_instance, client_class_instance.dependency)

    def test_fill_dependencies_with_fixed_args(self):
        self.dependency_filler.fill(MixedDependenciesClientClass)

        container_dependency_class_instance = self.container[SimpleDependencyDependencyClass]
        client_class_instance = MixedDependenciesClientClass("arg", kwarg=20)
        self.assertIsInstance(client_class_instance, MixedDependenciesClientClass)
        self.assertEqual(container_dependency_class_instance, client_class_instance.dependency)
        self.assertEqual("arg", client_class_instance.arg)
        self.assertEqual(20, client_class_instance.kwarg)
        self.assertIsNone(client_class_instance.client_dependency_class)
