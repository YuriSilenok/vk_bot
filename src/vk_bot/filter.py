from dataclasses import dataclass
from typing import Any


class F:
    class _Field:
        def __init__(self, name: str):
            self.name = name

        def __eq__(self, other):
            return Filter(self.name, 'eq', other)

        def __ne__(self, other):
            return Filter(self.name, 'ne', other)

        def __gt__(self, other):
            return Filter(self.name, 'gt', other)

        def __lt__(self, other):
            return Filter(self.name, 'lt', other)

    def __getattr__(self, name):
        return self._Field(name)


@dataclass
class Filter:
    field: str
    operator: str
    value: Any

    def __call__(self, obj) -> bool:
        obj_value = getattr(obj, self.field, None)

        if self.operator == 'eq':
            return obj_value == self.value
        elif self.operator == 'ne':
            return obj_value != self.value
        elif self.operator == 'gt':
            return obj_value > self.value
        elif self.operator == 'lt':
            return obj_value < self.value
        return False


class CombinedFilter:
    def __init__(self, left, right, operator):
        self.left = left
        self.right = right
        self.operator = operator

    def __call__(self, obj):
        if self.operator == 'and':
            return self.left(obj) and self.right(obj)
        elif self.operator == 'or':
            return self.left(obj) or self.right(obj)
        return False
