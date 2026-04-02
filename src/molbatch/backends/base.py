from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from molbatch.types import Plan


class Backend(ABC):
    name: str
    script_suffix: str

    @abstractmethod
    def render(self, plan: Plan) -> str:
        raise NotImplementedError

    def default_output_path(self, plan: Plan) -> Path:
        return Path(plan.config.output.directory) / f"{plan.config.output.basename}{self.script_suffix}"
