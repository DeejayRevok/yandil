from yadil.declarative.decorators import dependency


@dependency(is_primary=True)
class DeclarativeDependencyClass:
    def public_method(self):
        pass
