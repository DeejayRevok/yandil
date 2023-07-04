from typing import Any, Type


class InstanceAndClassDoesNotMatchError(Exception):
    def __init__(self, instance: Any, cls: Type):
        self.instance = instance
        self.cls = cls
        super().__init__(f"Instance of {instance.__class__} is not an instance of {cls}")
