# pytype: disable=attribute-error
from typing import Callable, List, Set, Tuple, Type, TypeVar, get_origin

__SUPPORTED_ITERABLE_TYPE_HINTS = {get_origin(List), get_origin(Set), get_origin(Tuple)}


def is_type_hint_iterable(type_hint: Type) -> bool:
    if (origin := get_origin(type_hint)) is not None:
        return origin in __SUPPORTED_ITERABLE_TYPE_HINTS
    return False


def type_hint_iterable_builder_factory(iterator_type_hint: Type) -> Callable:
    match iterator_type_hint.__name__:
        case List.__name__:
            return list
        case Set.__name__:
            return set
        case Tuple.__name__:
            return tuple
        case _:
            raise NotImplementedError(f"Unsupported iterator type hint {iterator_type_hint.__name__}")


TT = TypeVar("TT")


def str_to_builtin_type(value: str, target_type: Type[TT]) -> TT:
    if target_type is bool:
        return str_to_bool(value)
    return target_type(value)


def str_to_bool(value: str) -> bool:
    value = value.lower()
    if value in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif value in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError(f"Invalid truth value {value}")
