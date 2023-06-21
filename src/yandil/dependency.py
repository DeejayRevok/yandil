# pytype: disable=invalid-annotation
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Type, TypeVar

from yandil.argument import Argument

DT = TypeVar("DT")


@dataclass
class Dependency:
    cls: Type[DT]
    arguments: List[Argument] = field(default_factory=list, init=False)
    value: Optional[DT] = field(default=None)
    is_resolved: bool = field(default=False)
    is_primary: Optional[bool] = field(default=None)

    def resolve(self) -> Type:
        if not self.is_resolved:
            args = self.__resolve_args()
            self.value = self.cls(**args)
            self.is_resolved = True

        return self.value

    def __resolve_args(self) -> Dict[str, Any]:
        return {argument.name: argument.value for argument in self.arguments}
