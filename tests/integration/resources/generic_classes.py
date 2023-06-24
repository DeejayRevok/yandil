from abc import abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class GenericBaseClass(Generic[T]):
    @abstractmethod
    def abstract_method(self, x: T) -> T:
        pass


class GenericSubClass(GenericBaseClass[T]):
    def abstract_method(self, x: T) -> T:
        return x


class GenericSubClassStr(GenericSubClass[str]):
    def abstract_method(self, x: str) -> str:
        return "str"


class GenericSubClassInt(GenericSubClass[int]):
    def abstract_method(self, x: int) -> int:
        return 10


class ClassWithGenericDependency:
    def __init__(self, dependency: GenericBaseClass[str]):
        self.dependency = dependency

    def public_method(self, x: str) -> str:
        return self.dependency.abstract_method(x)
