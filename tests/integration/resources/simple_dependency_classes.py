from typing import Optional


class SimpleDependencyDependencyClass:
    pass


class SimpleDependencyClass:
    def __init__(self, dependency: SimpleDependencyDependencyClass):
        self.dependency = dependency


class SimpleDependencyClientClass:
    def __init__(self, dependency: Optional[SimpleDependencyDependencyClass] = None):
        self.dependency = dependency


class MixedDependenciesClientClass:
    def __init__(self, arg: str, kwarg: int = 10, dependency: Optional[SimpleDependencyDependencyClass] = None):
        self.arg = arg
        self.kwarg = kwarg
        self.dependency = dependency
