from unittest import TestCase
from unittest.mock import Mock, patch

from yadil.container import Container
from yadil.declarative.decorators import dependency


class TestDecorators(TestCase):
    @patch("yadil.declarative.decorators.default_container")
    def test_dependency_decorator_without_container(self, default_container_mock):
        @dependency
        class TestClass:
            pass

        default_container_mock.add.assert_called_once_with(TestClass, is_primary=None)

    def test_dependency_decorator_with_container(self):
        container_mock = Mock(spec=Container)

        @dependency(container=container_mock, is_primary=True)
        class TestClass:
            pass

        container_mock.add.assert_called_once_with(TestClass, is_primary=True)
