from typing import Iterable

from yandil.discovery.class_discovery import (
    ClassData,
    discover_classes_from_module,
    exclude_classes_without_decorators,
    transform_class_nodes_to_class_data,
)
from yandil.discovery.module_discovery import discover_modules


class DeclarativeDependencyLoader:
    def __init__(
        self,
        discovery_base_path: str,
        sources_root_path: str,
    ):
        self.__sources_root_path = sources_root_path
        self.__discovery_base_path = discovery_base_path

    def load(self) -> None:
        for module_data in discover_modules(self.__discovery_base_path, set()):
            module_file_path = module_data.module_path + ".py"
            for class_data in self.__get_classes_discover_iterable(
                module_file_path,
            ):
                class_data.to_class(self.__sources_root_path)

    def __get_classes_discover_iterable(
        self,
        module_file_path: str,
    ) -> Iterable[ClassData]:
        iterable = exclude_classes_without_decorators(discover_classes_from_module(module_file_path), {"dependency"})
        return transform_class_nodes_to_class_data(iterable, module_file_path)
