from abc import ABC, abstractmethod


class AbstractClass(ABC):
    @abstractmethod
    def public_abstract_method(self):
        pass
