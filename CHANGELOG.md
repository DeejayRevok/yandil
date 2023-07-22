## 0.4.0 (2023-07-22)

### Feat

- exclude enums from class discovery
- add option to exclude exceptions from class discovery

## 0.3.3 (2023-07-06)

### Fix

- **Container**: avoid adding to the base map of a base which has already been added to its correspondant generic alias base

## 0.3.2 (2023-07-05)

### Fix

- **Container**: when adding class to base map check if the already existing primary is the same as the one to add

### Refactor

- **Container**: refactor new check in order to make it more readable

## 0.3.1 (2023-07-05)

### Fix

- **Container**: check if class has already been added to the base map before trying to add it
- **Container**: reorder the execution of dependency map update and update bases map

## 0.3.0 (2023-07-04)

### Fix

- remove generic from the list of abstract bases

### Refactor

- **Container**: refactor the way container set instance adds classes to parents

## 0.2.4 (2023-06-30)

### Fix

- when filtering classes without public methods take into account also public methods inherited from parent class

## 0.2.3 (2023-06-27)

### Fix

- **DependencyFiller**: catch PrimaryDependencyNotFoundError and MissingConfigurationValueError on dependency filling

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
