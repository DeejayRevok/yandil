from abc import ABC, abstractmethod
from typing import Protocol


class AbstractClass(ABC):
    @abstractmethod
    def public_abstract_method(self):
        pass


class ProtocolAbstractClass(Protocol):
    def public_abstract_method(self):
        ...
