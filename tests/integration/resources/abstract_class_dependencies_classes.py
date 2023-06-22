from abc import ABC, abstractmethod


class AbstractBaseClass(ABC):
    @abstractmethod
    def method(self):
        pass


class AbstractBaseClassFirstChildren(AbstractBaseClass):
    def method(self):
        pass


class AbstractBaseClassSecondChildren(AbstractBaseClass):
    def method(self):
        pass


class ClassWithAbstractClassDependencies:
    def __init__(self, abstract_class_dependencies: AbstractBaseClass):
        self.abstract_class_dependencies = abstract_class_dependencies
