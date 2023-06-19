from typing import Type


class AbstractClassNotAllowedError(Exception):
    def __init__(self, abstract_class: Type):
        self.abstract_class = abstract_class
        super().__init__(f"Abstract class {abstract_class.__name__} not allowed")
