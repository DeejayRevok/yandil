from abc import ABC, abstractmethod


class BaseAbstractClass(ABC):
    @abstractmethod
    def abstract_method(self) -> str:
        pass


class BaseClass(BaseAbstractClass):
    def abstract_method(self) -> str:
        return "str"


class DependencyClass(BaseClass):
    def public_method(self) -> str:
        return self.abstract_method()


class ClassWithBaseClassDependency:
    def __init__(self, dependency: BaseClass):
        self.dependency = dependency

    def public_method(self) -> str:
        return self.dependency.abstract_method()


class ClassWithBaseAbstractClassDependency:
    def __init__(self, dependency: BaseAbstractClass):
        self.dependency = dependency

    def public_method(self) -> str:
        return self.dependency.abstract_method()
