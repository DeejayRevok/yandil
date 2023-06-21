from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True)
class Argument:
    name: str
    value: Optional[Any]
