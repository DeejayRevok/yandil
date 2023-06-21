from typing import Type


class PrimaryDependencyNotFoundError(Exception):
    def __init__(self, base_class: Type):
        self.base_class = base_class
        super().__init__(f"Primary dependency for base {base_class.__name__} not found")
