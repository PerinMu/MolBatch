from __future__ import annotations

import re


def sanitize_object_name(name: str) -> str:
    base = re.sub(r"\s+", "_", name.strip())
    base = re.sub(r"[^A-Za-z0-9_.-]+", "_", base)
    return base or "unnamed_object"


def make_unique_object_name(name: str, used_names: set[str]) -> str:
    candidate = sanitize_object_name(name)
    if candidate not in used_names:
        used_names.add(candidate)
        return candidate
    idx = 2
    while True:
        alt = f"{candidate}__{idx}"
        if alt not in used_names:
            used_names.add(alt)
            return alt
        idx += 1
