from contextvars import ContextVar
from typing import Callable, Dict, Awaitable, Any


class DynamicLoggingContext:
    def __init__(self):
        self.static_values: Dict[str, Any] = {}
        self.context_values: Dict[str, ContextVar[Any]] = {}
        self.callable_values: Dict[str, Callable[[], Any]] = {}

    def add_static_value(self, key: str, value: Any):
        self.static_values[key] = value

    def add_context_value(self, key: str, value: ContextVar[Any]):
        self.context_values[key] = value

    def add_callable_value(self, key: str, value: Callable[[], Any]):
        self.callable_values[key] = value

    def get_logging_context(self) -> Dict[str, Any]:
        context = {}
        for key, value in self.static_values.items():
            context[key] = value
        for key, value in self.context_values.items():
            context_value = value.get()
            if context_value is not None:
                context[key] = context_value
        for key, value in self.callable_values.items():
            callable_value = value()
            if callable_value is not None:
                context[key] = callable_value
        return context


dynamic_logging_context = DynamicLoggingContext()
