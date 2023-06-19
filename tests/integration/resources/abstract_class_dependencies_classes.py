from abc import ABC


class AbstractBaseClass(ABC):
    pass


class AbstractBaseClassFirstChildren(AbstractBaseClass):
    pass


class AbstractBaseClassSecondChildren(AbstractBaseClass):
    pass


class ClassWithAbstractClassDependencies:
    def __init__(self, abstract_class_dependencies: AbstractBaseClass):
        self.abstract_class_dependencies = abstract_class_dependencies
