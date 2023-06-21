from dataclasses import dataclass, field
from os import environ
from typing import Optional


@dataclass
class Environment:
    variable_name: str
    value: Optional[str] = field(default=None)
    is_resolved: bool = field(default=False)

    def resolve(self) -> str:
        if self.is_resolved is False:
            self.value = self.__get_value_from_env()

        self.is_resolved = True
        return self.value

    def __get_value_from_env(self) -> str:
        return environ[self.variable_name]
