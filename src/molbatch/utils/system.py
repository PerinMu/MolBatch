from __future__ import annotations

import platform
import shutil
from pathlib import Path


def find_executable(name: str) -> str:
    return shutil.which(name) or ""


def runtime_report() -> dict[str, object]:
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "pymol": find_executable("pymol"),
        "chimerax": find_executable("ChimeraX") or find_executable("chimerax"),
        "cwd": str(Path.cwd()),
    }
