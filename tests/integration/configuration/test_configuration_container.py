from os import environ
from unittest import TestCase

from yandil.configuration.configuration_container import ConfigurationContainer
from yandil.configuration.environment import Environment


class TestConfigurationContainer(TestCase):
    def setUp(self) -> None:
        self.configuration_container = ConfigurationContainer()

    def test_get_configuration_value(self):
        self.configuration_container["test"] = "test"

        configuration_value = self.configuration_container["test"]

        self.assertEqual("test", configuration_value)

    def test_get_configuration_value_with_environment(self):
        environ["YANDIL_TEST"] = "test"
        self.configuration_container["test"] = Environment("YANDIL_TEST")

        configuration_value = self.configuration_container["test"]

        self.assertEqual("test", configuration_value)

        del environ["YANDIL_TEST"]
