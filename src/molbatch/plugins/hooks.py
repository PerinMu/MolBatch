from __future__ import annotations

import importlib
from typing import Iterable

from molbatch.types import Plan


class HookManager:
    def __init__(self, module_names: Iterable[str] | None = None):
        self._modules = []
        for name in module_names or []:
            self._modules.append(importlib.import_module(name))

    def before_render(self, plan: Plan) -> Plan:
        current = plan
        for module in self._modules:
            func = getattr(module, "before_render", None)
            if callable(func):
                current = func(current) or current
        return current

    def after_render(self, plan: Plan, text: str) -> str:
        current = text
        for module in self._modules:
            func = getattr(module, "after_render", None)
            if callable(func):
                current = func(plan, current) or current
        return current
