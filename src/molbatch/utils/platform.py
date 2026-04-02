from __future__ import annotations

from pathlib import Path


def as_viewer_path(path: Path) -> str:
    return path.resolve().as_posix()
