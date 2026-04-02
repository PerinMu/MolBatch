from __future__ import annotations

from fnmatch import fnmatch
from pathlib import Path


VALID_SORT_KEYS = {"name", "stem", "path", "mtime"}


def _sort_key(path: Path, sort_by: str):
    if sort_by == "stem":
        return (path.stem.lower(), str(path).lower())
    if sort_by == "path":
        return str(path).lower()
    if sort_by == "mtime":
        return (path.stat().st_mtime, str(path).lower())
    return (path.name.lower(), str(path).lower())


def discover_files(
    directory: str,
    patterns: list[str],
    recursive: bool,
    exclude_patterns: list[str] | None = None,
    sort_by: str = "name",
    limit: int = 0,
) -> list[Path]:
    root = Path(directory)
    if not root.exists():
        return []
    sort_by = sort_by.lower()
    if sort_by not in VALID_SORT_KEYS:
        sort_by = "name"

    excludes = exclude_patterns or []
    files: list[Path] = []
    for pattern in patterns:
        iterator = root.rglob(pattern) if recursive else root.glob(pattern)
        for path in iterator:
            if not path.is_file():
                continue
            relative = path.relative_to(root).as_posix()
            if any(fnmatch(relative, ex) or fnmatch(path.name, ex) for ex in excludes):
                continue
            files.append(path)

    unique = sorted(set(files), key=lambda p: _sort_key(p, sort_by))
    if limit and limit > 0:
        unique = unique[:limit]
    return unique
