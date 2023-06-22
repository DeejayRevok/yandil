from typing import Iterable, Optional, Set

from yandil.container import Container, default_container
from yandil.discovery.class_discovery import (
    ClassData,
    discover_classes_from_module,
    exclude_abstract_classes,
    exclude_classes_without_public_methods,
    exclude_dataclasses,
    transform_class_nodes_to_class_data,
)
from yandil.discovery.module_discovery import discover_modules


class SelfDiscoverDependencyLoader:
    def __init__(
        self,
        discovery_base_path: str,
        sources_root_path: str,
        container: Optional[Container] = None,
        excluded_modules: Optional[Set[str]] = None,
        should_exclude_classes_without_public_methods: bool = True,
        should_exclude_dataclasses: bool = True,
    ):
        if container is None:
            container = default_container
        self.__container = container
        self.__excluded_modules = excluded_modules
        self.__should_exclude_classes_without_public_methods = should_exclude_classes_without_public_methods
        self.__should_exclude_dataclasses = should_exclude_dataclasses
        self.__sources_root_path = sources_root_path
        self.__discovery_base_path = discovery_base_path

    def load(self) -> None:
        for module_data in discover_modules(self.__discovery_base_path, self.__excluded_modules):
            module_file_path = module_data.module_path + ".py"
            for class_data in self.__get_classes_discover_iterable(
                module_file_path,
                self.__should_exclude_classes_without_public_methods,
                self.__should_exclude_dataclasses,
            ):
                cls = class_data.to_class(self.__sources_root_path)
                self.__container.add(cls)

    def __get_classes_discover_iterable(
        self,
        module_file_path: str,
        should_exclude_classes_without_public_methods: bool,
        should_exclude_dataclasses: bool,
    ) -> Iterable[ClassData]:
        iterable = exclude_abstract_classes(discover_classes_from_module(module_file_path))
        if should_exclude_classes_without_public_methods:
            iterable = exclude_classes_without_public_methods(iterable)
        if should_exclude_dataclasses:
            iterable = exclude_dataclasses(iterable)
        return transform_class_nodes_to_class_data(iterable, module_file_path)
