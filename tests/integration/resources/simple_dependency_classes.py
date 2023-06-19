from typing import Optional


class SimpleDependencyDependencyClass:
    pass


class SimpleDependencyClass:
    def __init__(self, dependency: SimpleDependencyDependencyClass):
        self.dependency = dependency


class SimpleDependencyClientClass:
    def __init__(self, dependency: Optional[SimpleDependencyDependencyClass] = None):
        self.dependency = dependency
