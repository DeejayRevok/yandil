from abc import abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class GenericBaseClass(Generic[T]):
    @abstractmethod
    def abstract_method(self) -> T:
        pass


class GenericSubClassStr(GenericBaseClass[str]):
    def abstract_method(self) -> str:
        return "str"


class GenericSubClassInt(GenericBaseClass[int]):
    def abstract_method(self) -> int:
        return 10


class ClassWithGenericDependency:
    def __init__(self, dependency: GenericBaseClass[str]):
        self.dependency = dependency

    def public_method(self) -> str:
        return self.dependency.abstract_method()
