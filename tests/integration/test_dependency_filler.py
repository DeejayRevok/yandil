from unittest import TestCase

from integration.resources.simple_dependency_classes import SimpleDependencyClientClass, SimpleDependencyDependencyClass

from yadil.configuration.configuration_container import ConfigurationContainer
from yadil.container import Container
from yadil.dependency_filler import DependencyFiller


class TestDependencyFiller(TestCase):
    def setUp(self) -> None:
        self.container = Container(
            configuration_container=ConfigurationContainer(),
        )
        self.container.add(SimpleDependencyDependencyClass)
        self.dependency_filler = DependencyFiller(
            container=self.container,
        )

    def test_fill_dependencies(self):
        self.dependency_filler.fill(SimpleDependencyClientClass)

        container_dependency_class_instance = self.container[SimpleDependencyDependencyClass]
        client_class_instance = SimpleDependencyClientClass()
        self.assertIsInstance(client_class_instance, SimpleDependencyClientClass)
        self.assertEqual(container_dependency_class_instance, client_class_instance.dependency)
