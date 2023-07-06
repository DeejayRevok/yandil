# pytype: disable=module-attr
import typing
from abc import ABC
from collections import defaultdict
from dataclasses import is_dataclass
from inspect import Parameter, signature
from types import GenericAlias
from typing import (
    Any,
    Dict,
    Final,
    Generic,
    Iterable,
    List,
    Optional,
    Protocol,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from yandil.argument import Argument
from yandil.configuration.configuration_container import ConfigurationContainer, default_configuration_container
from yandil.dependency import Dependency
from yandil.errors.abstract_class_not_allowed_error import AbstractClassNotAllowedError
from yandil.errors.configuration_value_type_mismatch_error import ConfigurationValueTypeMismatchError
from yandil.errors.dependency_not_found_error import DependencyNotFoundError
from yandil.errors.instance_and_class_does_not_match_error import InstanceAndClassDoesNotMatchError
from yandil.errors.missing_configuration_value_error import MissingConfigurationValueError
from yandil.errors.missing_type_hint_item_type_error import MissingTypeHintItemTypeError
from yandil.errors.primary_dependency_already_defined_error import PrimaryDependencyAlreadyDefinedError
from yandil.errors.primary_dependency_not_found_error import PrimaryDependencyNotFoundError
from yandil.typing_tools import is_type_hint_iterable, str_to_builtin_type, type_hint_iterable_builder_factory

DT = TypeVar("DT")


class Container:
    __EXCLUDED_BASES: Final[Set[str]] = {object, Generic}
    __ABSTRACT_BASES: Final[Set[str]] = {Protocol, ABC}
    __BUILTIN_TYPES: Final[Set[str]] = {int, float, str, bool, bytes, bytearray}

    def __init__(self, configuration_container: ConfigurationContainer):
        self.__dependency_map: Dict[Type, Dependency] = {}
        self.__bases_map: Dict[Type | GenericAlias, List[Type]] = defaultdict(list)
        self.__configuration_container = configuration_container

    def add(self, cls: Type, is_primary: Optional[bool] = None) -> None:
        if self.__is_abstract_class(cls):
            raise AbstractClassNotAllowedError(cls)

        if cls in self.__dependency_map:
            return

        dependency = Dependency(cls, is_primary=is_primary)

        self.__dependency_map[cls] = dependency
        self.__update_bases_map(cls, is_primary)

    def __is_abstract_class(self, cls: Type) -> bool:
        for base in cls.__bases__:
            if base in self.__ABSTRACT_BASES:
                return True
        return False

    def __setitem__(self, cls: Type[DT], value: DT) -> None:
        if cls == value.__class__:
            is_primary = None
            dependency = Dependency(cls, value=value, is_resolved=True)
        elif isinstance(value, cls):
            is_primary = self.__get_primary_dependency_from_base_children(self.__bases_map.get(cls, [])) is None
            cls = value.__class__
            dependency = Dependency(cls, value=value, is_resolved=True, is_primary=is_primary)
        else:
            raise InstanceAndClassDoesNotMatchError(value, cls)

        self.__dependency_map[cls] = dependency
        self.__update_bases_map(cls, is_primary)

    def __update_bases_map(
        self,
        cls: Type,
        children_is_primary: Optional[bool],
        reference_class: Optional[Type] = None,
        reference_class_args: Optional[Tuple[Any]] = None,
    ) -> None:
        if reference_class is None:
            reference_class = cls

        orig_classes_args = {}
        if hasattr(reference_class, "__orig_bases__"):
            for base in reference_class.__orig_bases__:
                base_origin_class = get_origin(base)
                if self.__should_skip_base(base_origin_class):
                    continue

                if reference_class_args is not None:
                    base = self.__get_generic_alias_instance_from_alias(base, alias_args=reference_class_args)

                self.__add_children_to_base(cls, base, children_is_primary)
                orig_classes_args[base_origin_class] = get_args(base)

        for base in reference_class.__bases__:
            if self.__should_skip_base(base):
                continue
            if base not in orig_classes_args:
                self.__add_children_to_base(cls, base, children_is_primary)
            self.__update_bases_map(
                cls, children_is_primary, reference_class=base, reference_class_args=orig_classes_args.get(base)
            )

    def __should_skip_base(self, base: Type) -> bool:
        return base in self.__EXCLUDED_BASES or base in self.__ABSTRACT_BASES

    def __get_generic_alias_instance_from_alias(
        self, alias: typing._GenericAlias, alias_args: Optional[Tuple[Any]] = None
    ) -> GenericAlias:
        if alias_args is None:
            alias_args = get_args(alias)
        else:
            number_of_alias_args = len(get_args(alias))
            alias_args = alias_args[:number_of_alias_args]

        return GenericAlias(get_origin(alias), alias_args)

    def __add_children_to_base(self, cls: Type, base: Type, children_is_primary: Optional[bool]) -> None:
        if cls in self.__bases_map[base]:
            return

        if isinstance(base, typing._GenericAlias):
            base = self.__get_generic_alias_instance_from_alias(base)

        if (
            children_is_primary is True
            and base in self.__bases_map
            and self.__is_primary_already_defined_for_base(cls, base)
        ):
            raise PrimaryDependencyAlreadyDefinedError(base)

        self.__bases_map[base].append(cls)

    def __is_primary_already_defined_for_base(self, cls: Type, base: Type | GenericAlias) -> bool:
        primary_dependency = self.__get_primary_dependency_from_base_children(self.__bases_map[base])
        if primary_dependency is None:
            return False
        return primary_dependency != self.__dependency_map[cls]

    def __getitem__(self, cls: Type[DT]) -> Optional[DT]:
        if isinstance(cls, typing._GenericAlias):
            cls = self.__get_generic_alias_instance_from_alias(cls)

        dependency = self.__dependency_map.get(cls, None)
        if dependency is None and cls in self.__bases_map:
            dependency = self.__get_dependency_from_base(cls)

        if dependency is not None:
            self.__set_arguments(dependency)
            return dependency.resolve()

        if dependency is None and self.__is_optional(cls):
            return self.__get_optional_dependency(cls)

        raise DependencyNotFoundError(cls)

    def __get_primary_dependency_from_base_children(self, base_children: List[Type]) -> Optional[Dependency]:
        for base_child in base_children:
            dependency = self.__dependency_map[base_child]
            if dependency is not None and dependency.is_primary:
                return dependency

        return None

    def __get_dependency_from_base(self, cls: Type) -> Dependency:
        base_children = self.__bases_map[cls]
        if len(base_children) == 1:
            return self.__dependency_map[base_children[0]]

        primary_dependency = self.__get_primary_dependency_from_base_children(base_children)
        if primary_dependency is None:
            raise PrimaryDependencyNotFoundError(cls)
        return primary_dependency

    def __is_optional(self, cls: Type) -> bool:
        if get_origin(cls) is not Union:
            return False

        typing_args = get_args(cls)
        if not typing_args:
            raise MissingTypeHintItemTypeError()

        return len(typing_args) == 2 and type(None) in typing_args

    def __get_optional_dependency(self, cls: Type[DT]) -> Optional[DT]:
        optional_inner_type = next(arg for arg in get_args(cls))
        try:
            return self[optional_inner_type]
        except DependencyNotFoundError:
            return None

    def __set_arguments(self, dependency: Dependency) -> None:
        if dependency.is_resolved:
            return

        for argument_name, argument_type in get_type_hints(dependency.cls.__init__).items():
            if self.__should_skip_argument(dependency.cls, argument_name):
                continue

            if self.__is_configuration_argument(argument_type):
                configuration_value = self.__configuration_container[argument_name]
                if configuration_value is None:
                    raise MissingConfigurationValueError(argument_name)

                dependency.arguments.append(
                    Argument(
                        argument_name,
                        self.__adapt_configuration_value_type(argument_type, configuration_value, argument_name),
                    )
                )
                continue

            if is_type_hint_iterable(argument_type):
                argument_value = self.__get_iterable_dependency_value(argument_type)
                dependency.arguments.append(Argument(argument_name, value=argument_value))
                continue

            try:
                argument_value = self[argument_type]
            except DependencyNotFoundError as err:
                dependency_default_value = self.__get_keyword_dependency_default_value(dependency.cls, argument_name)
                if dependency_default_value is None:
                    raise err
                dependency.arguments.append(Argument(argument_name, value=dependency_default_value))
                continue

            dependency.arguments.append(Argument(argument_name, value=argument_value))

    def __is_configuration_argument(self, argument_type: str) -> bool:
        return argument_type in self.__BUILTIN_TYPES

    def __adapt_configuration_value_type(
        self, argument_type: type, configuration_value: Any, configuration_value_name
    ) -> Any:
        actual_type = type(configuration_value)
        if argument_type == actual_type:
            return configuration_value
        if actual_type != str:
            raise ConfigurationValueTypeMismatchError(configuration_value_name, argument_type, actual_type)
        return str_to_builtin_type(configuration_value, argument_type)

    def __should_skip_argument(self, dependency_type: Type, argument_name: str) -> bool:
        if is_dataclass(dependency_type):
            return argument_name == "return"
        return argument_name == "self"

    def __get_iterable_dependency_value(self, iterable_type_hint: Type) -> Iterable:
        type_hint_args = get_args(iterable_type_hint)
        if not type_hint_args:
            raise MissingTypeHintItemTypeError()

        inner_iterable_type = get_args(iterable_type_hint)[0]
        dependency_types = self.__bases_map[inner_iterable_type]
        return type_hint_iterable_builder_factory(iterable_type_hint)(
            self[dependency_type] for dependency_type in dependency_types
        )

    def __get_keyword_dependency_default_value(self, cls: Type, dependency_name: str) -> Optional[Any]:
        init_signature = signature(cls.__init__)
        dependency_param = init_signature.parameters.get(dependency_name)
        if dependency_param is None or dependency_param.default is Parameter.empty:
            return None
        return dependency_param.default


default_container = Container(configuration_container=default_configuration_container)
