from typing import Any, Callable, List, Optional

from .filter import Filter


class Router:
    def __init__(self):
        self.handlers: List[tuple[Filter, Callable]] = []

    def message(self, filter_obj: Filter):
        """
        Декоратор для регистрации обработчика с фильтром
        """
        def decorator(func: Callable) -> Callable:
            self.handlers.append((filter_obj, func))
            return func
        return decorator

    def process(self, event_obj) -> Optional[Any]:
        """
        Обрабатывает событие через все зарегистрированные фильтры
        Возвращает результат первого подходящего обработчика
        """
        for filter_obj, handler in self.handlers:
            if filter_obj(event_obj):
                return handler(event_obj)
        return None
