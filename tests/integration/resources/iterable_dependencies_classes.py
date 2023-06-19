from typing import Set


class IterableDependencyBaseClass:
    pass


class FirstIterableDependencyClass(IterableDependencyBaseClass):
    pass


class SecondIterableDependencyClass(IterableDependencyBaseClass):
    pass


class ClassWithIterableDependencies:
    def __init__(self, iterable_dependencies: Set[IterableDependencyBaseClass]):
        self.iterable_dependencies = iterable_dependencies
