from ast import ClassDef
from pathlib import Path
from typing import Iterable, Optional, Set, Type

from yandil.container import Container, default_container
from yandil.discovery.class_discovery import (
    ClassData,
    discover_classes_from_module,
    exclude_abstract_classes,
    exclude_classes_without_public_methods,
    exclude_dataclasses,
    transform_class_nodes_to_class_data,
)
from yandil.discovery.class_feature_checks import has_public_methods, is_enum, is_exception
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
        mandatory_modules: Optional[Set[Path]] = None,
        should_exclude_exceptions: bool = True,
    ):
        if container is None:
            container = default_container
        self.__container = container
        self.__excluded_modules = excluded_modules
        self.__should_exclude_classes_without_public_methods = should_exclude_classes_without_public_methods
        self.__should_exclude_dataclasses = should_exclude_dataclasses
        self.__sources_root_path = sources_root_path
        self.__discovery_base_path = discovery_base_path
        if mandatory_modules is None:
            mandatory_modules = set()
        self.__mandatory_modules = mandatory_modules
        self.__should_exclude_exceptions = should_exclude_exceptions

    def load(self) -> None:
        for module_data in discover_modules(self.__discovery_base_path, self.__excluded_modules):
            module_file_path = module_data.module_path + ".py"

            classes_without_defined_public_methods: Set[ClassDef] = set()
            if self.__is_module_mandatory(module_data.module_path):
                module_classes = self.__get_mandatory_module_classes_discover_iterable(module_file_path)
            else:
                module_classes = self.__get_non_mandatory_module_classes_discover_iterable(
                    module_file_path,
                    self.__should_exclude_classes_without_public_methods,
                    self.__should_exclude_dataclasses,
                    classes_without_defined_public_methods=classes_without_defined_public_methods,
                )

            for class_data in module_classes:
                cls = class_data.to_class(self.__sources_root_path)
                if not self.__class_should_be_added(cls):
                    continue
                self.__container.add(cls)

            self.__add_classes_without_defined_public_methods_with_public_methods(
                classes_without_defined_public_methods,
                module_file_path,
            )

    def __is_module_mandatory(self, module_path: str) -> bool:
        module_path = Path(module_path)
        for mandatory_module_path in self.__mandatory_modules:
            if module_path == mandatory_module_path:
                return True
            if mandatory_module_path in module_path.parents:
                return True
        return False

    def __get_mandatory_module_classes_discover_iterable(self, module_file_path: str) -> Iterable[ClassData]:
        return transform_class_nodes_to_class_data(
            class_nodes=exclude_abstract_classes(discover_classes_from_module(module_file_path)),
            module_file_path=module_file_path,
        )

    def __get_non_mandatory_module_classes_discover_iterable(
        self,
        module_file_path: str,
        should_exclude_classes_without_public_methods: bool,
        should_exclude_dataclasses: bool,
        classes_without_defined_public_methods: Set[ClassDef],
    ) -> Iterable[ClassData]:
        iterable = exclude_abstract_classes(discover_classes_from_module(module_file_path))
        if should_exclude_classes_without_public_methods:
            iterable = exclude_classes_without_public_methods(iterable, classes_without_defined_public_methods)
        if should_exclude_dataclasses:
            iterable = exclude_dataclasses(iterable)
        return transform_class_nodes_to_class_data(iterable, module_file_path)

    def __add_classes_without_defined_public_methods_with_public_methods(
        self,
        classes_without_defined_public_methods: Set[ClassDef],
        module_file_path: str,
    ) -> None:
        for class_without_defined_public_methods in transform_class_nodes_to_class_data(
            classes_without_defined_public_methods,
            module_file_path,
        ):
            class_without_defined_public_methods = class_without_defined_public_methods.to_class(
                self.__sources_root_path
            )
            if has_public_methods(class_without_defined_public_methods) and self.__class_should_be_added(
                class_without_defined_public_methods
            ):
                self.__container.add(class_without_defined_public_methods)

    def __class_should_be_added(self, cls: Type) -> bool:
        if is_enum(cls):
            return False
        if self.__should_exclude_exceptions and is_exception(cls):
            return False
        return True
