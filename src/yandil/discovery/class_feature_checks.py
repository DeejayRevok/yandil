from inspect import getmembers, isfunction
from typing import Type


def is_exception(cls: Type) -> bool:
    return issubclass(cls, Exception)


def has_public_methods(cls: Type) -> bool:
    return any(name for name, member in getmembers(cls) if isfunction(member) and not name.startswith("_"))
