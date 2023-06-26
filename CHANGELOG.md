## 0.2.2 (2023-06-26)

### Fix

- **DependencyFiller**: allow passing instance args and kwargs to dependency filled classes

## 0.2.1 (2023-06-26)

### Fix

- **Container**: check if cls is already added as dependency before trying to add it in container add
- **Container**: avoid setting arguments for already resolved dependencies checking is_resolved instead of arguments

## 0.2.0 (2023-06-26)

### Feat

- **SelfDiscoverDependencyLoader**: add parameter to allow passing paths of modules to be force loaded without checking any condition

## 0.1.4 (2023-06-24)

### Fix

- **Container**: propagate generic alias arguments to parent classes

## 0.1.3 (2023-06-23)

### Fix

- **Container**: add also the definitions to bases map and update the bases map recursively

## 0.1.2 (2023-06-22)

### Fix

- check class subscriptions for checking abstract classes on discovery

## 0.1.1 (2023-06-22)

### Fix

- exclude abstract classes from self discover

## 0.1.0 (2023-06-21)

### Feat

- add dependency filler
- add declarative dependencies loader
- add self discover dependency loader
- add class discovery functions
- add module discovery functions
- add declarative dependency decorator
- add dependencies container
- add configuration container
- add dependency class

### Refactor

- **pyproject.toml**: rename poetry project to yandil
- rename all ocurrences to yandil
