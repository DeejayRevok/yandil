from abc import ABC, abstractmethod
from typing import Generic, TypeVar


class AbstractClass(ABC):
    @abstractmethod
    def public_abstract_method(self):
        pass


T = TypeVar("T")


class GenericAbstractClass(Generic[T]):
    @abstractmethod
    def public_abstract_method(self):
        pass
