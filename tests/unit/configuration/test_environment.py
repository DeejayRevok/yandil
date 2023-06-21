from unittest import TestCase
from unittest.mock import patch

from yandil.configuration.environment import Environment


class TestEnvironment(TestCase):
    @patch.dict("yandil.configuration.environment.environ", {"TEST_ENVIRONMENT": "test_value"})
    def test_resolve(self):
        environment = Environment(variable_name="TEST_ENVIRONMENT")

        resolved_environment = environment.resolve()

        self.assertEqual(resolved_environment, "test_value")
        self.assertEqual(environment.value, "test_value")
        self.assertTrue(environment.is_resolved)

    def test_resolve_already_resolved(self):
        environment = Environment(variable_name="TEST_ENVIRONMENT")
        environment.is_resolved = True
        environment.value = "test_resolved_value"

        resolved_environment = environment.resolve()

        self.assertEqual(resolved_environment, "test_resolved_value")
        self.assertEqual(environment.value, "test_resolved_value")
        self.assertTrue(environment.is_resolved)
