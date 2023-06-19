from typing import Optional


class OptionalDependencyClass:
    pass


class ClassWithOptionalDependencies:
    def __init__(self, optional_dependency: Optional[OptionalDependencyClass]):
        self.optional_dependency = optional_dependency
