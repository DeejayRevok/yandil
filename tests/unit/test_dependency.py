from unittest import TestCase
from unittest.mock import Mock

from yadil.argument import Argument
from yadil.dependency import Dependency


class TestDependency(TestCase):
    def test_resolve_resolved(self):
        test_class = Mock()
        test_value = Mock()
        dependency = Dependency(test_class, value=test_value, is_resolved=True)
        test_argument = Mock(spec=Argument)
        dependency.arguments.append(test_argument)

        resolved_dependency = dependency.resolve()

        self.assertEqual(test_value, resolved_dependency)
        test_class.assert_not_called()

    def test_resolve_non_resolved(self):
        test_class = Mock()
        test_value = Mock()
        test_class.return_value = test_value
        dependency = Dependency(test_class)
        test_argument_value = Mock()
        test_argument = Mock(spec=Argument)
        test_argument.name = "test_argument"
        test_argument.value = test_argument_value
        dependency.arguments.append(test_argument)

        resolved_dependency = dependency.resolve()

        self.assertEqual(test_value, resolved_dependency)
        self.assertEqual(test_value, dependency.value)
        test_class.assert_called_once_with(test_argument=test_argument_value)
