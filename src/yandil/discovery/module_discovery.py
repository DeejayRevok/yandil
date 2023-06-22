import pkgutil
from dataclasses import dataclass
from importlib.machinery import FileFinder
from os.path import join
from typing import Iterable, Optional, Set


@dataclass(frozen=True)
class ModuleData:
    module_name: str
    module_path: str


def discover_modules(base_path: str, exclude_modules: Optional[Set[str]] = None) -> Iterable[ModuleData]:
    if exclude_modules is None:
        exclude_modules = set()

    for module_finder, module_name, is_pkg in pkgutil.iter_modules([base_path]):
        if module_name in exclude_modules:
            continue

        if not isinstance(module_finder, FileFinder):
            continue

        module_path = join(module_finder.path, module_name)
        if is_pkg:
            yield from discover_modules(module_path, exclude_modules)
        else:
            yield ModuleData(module_name=module_name, module_path=module_path)
