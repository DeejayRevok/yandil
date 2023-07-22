# YANDIL
[![YANDIL CI](https://github.com/DeejayRevok/yandil/actions/workflows/pythonapp.yml/badge.svg?branch=main)](https://github.com/DeejayRevok/yandil/actions/workflows/pythonapp.yml)
[![PyPI version](https://badge.fury.io/py/yandil.svg)](https://pypi.org/project/yandil/)

## What is YANDIL?
YANDIL(**Yet ANother Dependency Injection Library**) is a python dependency injection library with two main aims:
- **Decouple the application source code totally from the dependency injection schema**.
- **Avoid the need of dependency injection definitions**.

## How does it work?
In order to achieve the decoupling between the source code and the dependency injection,
YANDIL uses two main strategies:
- **Use the source code type hints to infer the dependency injection definitions**.
- **Allow dependencies "client classes" to get the dependencies without using the dependency injection container itself**.

On the other hand, for achieving the aim of avoiding the need of dependency injection definitions
YANDIL provides a **configurable way of scanning the source code searching for candidate components of the application**.

Alternatively, in order to allow more control over the dependency injection it provides simple ways
to define explicitly the dependency injection definitions.

## Code requirements
**At least all the __init__ methods of the classes which will be used as dependencies should be properly type hinted
using the python typing module**.

## How to load dependencies?

### Non-declarative way
In this way, it is assumed that all the classes which meets some conditions should be loaded as dependencies.

Giving the following python project structure:
```
├── app
│   │   ├── dependency_injection_configuration.py
├── src
│   ├── first_package
│   │   ├── first_package_first_module.py
│   │   ├── first_package_second_module.py
│   ├── second_package
│   │   ├── second_package_first_module.py
```
Having the src folder as the sources root folder (with PYTHONPATH properly configured).
The following code placed inside the dependency_injection_configuration.py file
will load all the classes defined inside the first_package folder as dependencies
into the dependency injection container:

```python
from yandil.configuration.configuration_container import ConfigurationContainer
from yandil.container import Container
from yandil.loaders.self_discover_dependency_loader import SelfDiscoverDependencyLoader

configuration_container = ConfigurationContainer()
dependency_container = Container(
    configuration_container=configuration_container,
)

SelfDiscoverDependencyLoader(
    discovery_base_path="src",
    sources_root_path="src",
    should_exclude_classes_without_public_methods=False,
    should_exclude_dataclasses=False,
    container=dependency_container,
).load()
```
Typically, you would want to load all the classes defined inside the src folder as dependencies,
which can be achieved just setting the discovery_base_path same as the sources_root_path.

If you do not want to manage the dependency_container you can just leave it empty and the dependencies will be loaded
into the library default_container which can be accessed through the following import:

```python
from yandil.container import default_container
```

In order to tune the dependency injection discovery process the loader has the following options:
- **excluded_modules**: Set of module or package names to be excluded from the dependency injection discovery process. For example for excluding the folder which contains the models in a web application.
- **should_exclude_classes_without_public_methods**: If set to True, classes which not define any public method will be excluded from the dependency injection discovery process. For example for excluding DTO classes.
- **should_exclude_dataclasses**: If set to True, dataclasses will be excluded from the dependency injection discovery process.
- **mandatory_modules**: Set of module paths which classes contained should be loaded as dependencies without checking if they meet any condition.
- **should_exclude_exceptions**: If set to True, exceptions will be excluded from the dependency injection discovery process.

### Declarative way
In this way you will need to decorate the classes which you want to be loaded as dependencies.

Giving the following python project structure:
```
├── app
│   │   ├── dependency_injection_configuration.py
├── src
│   ├── first_package
│   │   ├── first_package_first_module.py
```
Having the src folder as the sources root folder (with PYTHONPATH properly configured).
If the first_package_first_module.py file contains the following code:

```python
from yandil.declarative.decorators import dependency


@dependency
class SimpleDependencyClass:
    pass
```
The following code placed inside the dependency_injection_configuration.py file
will load all the classes defined inside the first_package folder as dependencies
into the dependency injection container:

```python
from yandil.loaders.declarative_dependency_loader import DeclarativeDependencyLoader

DeclarativeDependencyLoader(
    discovery_base_path="../src/first_package",
    sources_root_path="../src",
).load()
```
Take into account that this way of work will load the decorated class as dependencies in the default dependency container.

## How to load the configuration values?
In some scenarios, components of the application will need to depend on some specific literal values
coming for example from environment variables.

Giving the following class:
```python
class ClassWithConfigurationValues:
    def __init__(self, first_config_var: str, second_config_var: int):
        self.first_config_var = first_config_var
        self.second_config_var = second_config_var
```

The following code will load the configuration values to be injected into the class:

```python
from yandil.configuration.configuration_container import ConfigurationContainer
from yandil.configuration.environment import Environment
from yandil.container import Container

configuration_container = ConfigurationContainer()
dependency_container = Container(
    configuration_container=configuration_container,
)

dependency_container.add(ClassWithConfigurationValues)

configuration_container["first_config_var"] = "first_config_var_value"
configuration_container["second_config_var"] = Environment(
    "YANDIL_EXAMPLE_SECOND_CONFIG_ENV_VAR",
)
```

With the previous setup, when the ClassWithConfigurationValues dependency is retrieved,
the first_config_var will be filled with first_config_var_value and the second_config_var
will be filled with the value of the environment variable YANDIL_EXAMPLE_SECOND_CONFIG_ENV_VAR.

Again, if you do not want to manage the configuration container you can also use the default one with the following import:

```python
from yandil.configuration.configuration_container import default_configuration_container
```

## How to load fixed instances for specific classes?
By default, if a class is added to the dependency container using the add method, if will be instantiated lazily when used
as well as its dependencies. But there could some scenarios where you need a class to have an specific instance,
like for example when creating connection objects for communicating with external systems.

For this scenario the following code will always use the same instance
when the dependency for the class ClassWithConfigurationValues is requested:

```python
from yandil.configuration.configuration_container import ConfigurationContainer
from yandil.container import Container

configuration_container = ConfigurationContainer()
dependency_container = Container(
    configuration_container=configuration_container,
)

dependency_container[ClassWithConfigurationValues] = ClassWithConfigurationValues(
    first_config_var="first_config_var_value",
    second_config_var=23,
)
```

## How to retrieve the dependencies?
The following code will return the instance of the ClassWithConfigurationValues dependency:
```python
dependency_container[ClassWithConfigurationValues]
```
If it is the first time the dependency is resolved its initialization arguments and recursively
their initialization arguments will be resolved also in order to resolve the requested dependency.

## How to retrieve dependencies without using the container itself?
In order to achieve the aim of fully decoupling the source code from the dependency injection library,
we are still missing the possibility of retrieving the dependencies without using the container itself.

Giving the following class:
```python
class ClassWithDependencies:
    def __init__(
            self,
            first_dependency: Optional[FirstDependency] = None,
            second_dependency: Optional[SecondDependency] = None
    ):
        self.first_dependency = first_dependency
        self.second_dependency = second_dependency
```

The following code allows the class to have the dependencies injected when it is instantiated:

```python
from yandil.configuration.configuration_container import ConfigurationContainer
from yandil.container import Container
from yandil.dependency_filler import DependencyFiller

configuration_container = ConfigurationContainer()
dependency_container = Container(
    configuration_container=configuration_container,
)

dependency_container.add(FirstDependency)
dependency_container.add(SecondDependency)

dependency_filler = DependencyFiller(dependency_container)
dependency_filler.fill(ClassWithDependencies)

# At this point the class_with_dependencies instance will have the dependencies injected
class_with_dependencies = ClassWithDependencies()
```

## What about abstractions?
YANDIL supports the usage of abstractions in the code and it will automatically inject the
abstraction implementation class if the abstraction only has one implementation defined.

If the abstraction has multiple implementations defined there could be two scenarios:

### Class depends on all the implementations of the abstraction
Giving the following class:
```python
from abc import ABC
from typing import List


class AbstractClass(ABC):
    pass

class FirstImplementation(AbstractClass):
    pass

class SecondImplementation(AbstractClass):
    pass

class ClassWithAllAbstractionDependencies:
    def __init__(self, abstract_class_implementations: List[AbstractClass]):
        self.abstract_class_implementations = abstract_class_implementations
```
When retrieving the ClassWithAllAbstractionDependencies dependency, the dependency container will inject
all the implementations of AbstractClass into the abstract_class_implementations argument.

### Class depends on one implementation of the abstraction
In this scenario you need to define which is the primary implementation. Which could be achieved in the following ways:
```python
dependency_container.add(FirstImplementation, primary=True)
```
or
```python
@dependency(primary=True)
class FirstImplementation(AbstractClass):
    pass
```
In this way, when retrieving the ClassWithOneAbstractionDependency dependency, the dependency container will inject
that implementation of AbstractClass into the abstract_class_implementation argument.

## Extra features
- **Possibility to define optional dependencies**: In this scenario, if the dependency retrieved depends on an optional dependency not defined, then it will have the None value injected.
- **Allow usage of keyword arguments**: In this scenario, if the dependency retrieved depends on a keyword argument, and the argument type dependency is not defined, then it will have the default value of the keyword argument injected.
