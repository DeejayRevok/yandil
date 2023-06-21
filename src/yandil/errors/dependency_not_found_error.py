from typing import Type


class DependencyNotFoundError(Exception):
    def __init__(self, dependency_type: Type):
        self.dependency_type = dependency_type
        super().__init__(f"Dependency {dependency_type.__name__} not found")
