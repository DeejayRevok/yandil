from functools import wraps
from typing import Optional, TypeVar

from yandil.container import Container, default_container

DT = TypeVar("DT")


def dependency(
    cls: Optional[DT] = None, /, *, container: Optional[Container] = None, is_primary: Optional[bool] = None
):
    if container is None:
        container = default_container

    @wraps(cls)
    def wrap(cls: DT) -> DT:
        container.add(cls, is_primary=is_primary)
        return cls

    if cls is None:
        return wrap

    return wrap(cls)
