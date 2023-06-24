from types import GenericAlias
from typing import Type


class PrimaryDependencyAlreadyDefinedError(Exception):
    def __init__(self, base_class: Type | GenericAlias):
        self.base_class = base_class
        super().__init__(f"Primary dependency for base {base_class.__name__} already defined")
