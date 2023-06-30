from integration.resources.dependency_discovery_tests_module.dependency_class import DependencyClass


class ClassWithoutDefinedPublicMethods:
    def __init__(self, dependency: DependencyClass):
        self.dependency = dependency

    def __private_method(self):
        pass

    def _protected_method(self):
        pass

    @classmethod
    def public_class_method(cls):
        pass


class DependencyClassChildrenWithoutDefinedPublicMethods(DependencyClass):
    def __private_method(self):
        pass

    def _protected_method(self):
        pass
