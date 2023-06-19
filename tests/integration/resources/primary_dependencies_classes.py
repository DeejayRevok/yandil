class PrimaryDependencyBaseClass:
    pass


class PrimaryDependencyFirstChildren(PrimaryDependencyBaseClass):
    pass


class PrimaryDependencySecondChildren(PrimaryDependencyBaseClass):
    pass


class ClassWithPrimaryDependencies:
    def __init__(self, primary_dependency: PrimaryDependencyBaseClass):
        self.primary_dependency = primary_dependency
