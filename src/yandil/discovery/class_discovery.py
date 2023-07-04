from ast import Call, ClassDef, FunctionDef, Name, Subscript, parse
from dataclasses import dataclass
from importlib import import_module
from os import path
from os.path import relpath, splitext
from typing import Iterable, Optional, Set, Type


@dataclass(frozen=True)
class ClassData:
    module_file_path: str
    class_name: str

    def to_class(self, sources_root_path: str) -> Type:
        module_path_without_ext = splitext(self.module_file_path)[0]
        module_rel_path = relpath(module_path_without_ext, sources_root_path)
        module = import_module(module_rel_path.replace(path.sep, "."))
        return getattr(module, self.class_name)


def discover_classes_from_module(module_file_path: str) -> Iterable[ClassDef]:
    with open(module_file_path, "r", encoding="utf-8") as file:
        module_ast = parse(file.read())

    for node in module_ast.body:
        if isinstance(node, ClassDef):
            yield node


def exclude_abstract_classes(class_nodes: Iterable[ClassDef]) -> Iterable[ClassDef]:
    abstract_bases = {"Protocol", "ABC"}

    def __is_abstract_class_node(node: ClassDef) -> bool:
        for base in node.bases:
            if isinstance(base, Name) and base.id in abstract_bases:
                return True

            if isinstance(base, Subscript) and isinstance(base.value, Name) and base.value.id in abstract_bases:
                return True
        return False

    for class_node in class_nodes:
        if not __is_abstract_class_node(class_node):
            yield class_node


def transform_class_nodes_to_class_data(class_nodes: Iterable[ClassDef], module_file_path: str) -> Iterable[ClassData]:
    for class_node in class_nodes:
        yield ClassData(
            module_file_path=module_file_path,
            class_name=class_node.name,
        )


def exclude_classes_without_public_methods(
    class_nodes: Iterable[ClassDef],
    classes_without_defined_public_methods: Optional[Set[ClassDef]] = None,
) -> Iterable[ClassDef]:
    for class_node in class_nodes:
        if class_defines_public_methods(class_node):
            yield class_node
        elif classes_without_defined_public_methods is not None:
            classes_without_defined_public_methods.add(class_node)


def class_defines_public_methods(class_node: ClassDef) -> bool:
    for node in class_node.body:
        if not isinstance(node, FunctionDef) or node.name.startswith("_") or is_class_method(node):
            continue
        return True
    return False


def is_class_method(node: FunctionDef) -> bool:
    for decorator_node in node.decorator_list:
        if isinstance(decorator_node, Name) and decorator_node.id == "classmethod":
            return True
    return False


def exclude_dataclasses(class_nodes: Iterable[ClassDef]) -> Iterable[ClassDef]:
    for class_node in class_nodes:
        if class_has_any_decorator(class_node, {"dataclass"}):
            continue
        yield class_node


def class_has_any_decorator(class_node: ClassDef, decorator_names: Set[str]) -> bool:
    for decorator_node in class_node.decorator_list:
        decorator_id = None
        if isinstance(decorator_node, Name):
            decorator_id = decorator_node.id
        elif isinstance(decorator_node, Call):
            decorator_id = decorator_node.func.id

        if decorator_id in decorator_names:
            return True
    return False


def exclude_classes_without_decorators(
    class_nodes: Iterable[ClassDef], decorator_names: Set[str]
) -> Iterable[ClassDef]:
    for class_node in class_nodes:
        if class_has_any_decorator(class_node, decorator_names):
            yield class_node
