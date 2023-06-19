from integration.resources.dependency_discovery_tests_module.dependency_class import DependencyClass


class ClassWithPublicMethods:
    def __init__(self, dependency: DependencyClass):
        self.dependency = dependency

    def public_method(self):
        pass
