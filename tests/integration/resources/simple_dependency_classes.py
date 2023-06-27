from typing import Optional


class SimpleDependencyDependencyClass:
    pass


class SimpleDependencyClass:
    def __init__(self, dependency: SimpleDependencyDependencyClass):
        self.dependency = dependency


class SimpleDependencyClientClass:
    def __init__(self, dependency: Optional[SimpleDependencyDependencyClass] = None):
        self.dependency = dependency


class BaseClientDependencyClass:
    pass


class FirstBaseChildrenDependencyClass(BaseClientDependencyClass):
    pass


class SecondBaseChildrenDependencyClass(BaseClientDependencyClass):
    pass


class MixedDependenciesClientClass:
    def __init__(
        self,
        arg: str,
        kwarg: int = 10,
        client_dependency_class: Optional[BaseClientDependencyClass] = None,
        dependency: Optional[SimpleDependencyDependencyClass] = None,
    ):
        self.arg = arg
        self.client_dependency_class = client_dependency_class
        self.kwarg = kwarg
        self.dependency = dependency
