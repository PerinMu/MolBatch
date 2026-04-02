from __future__ import annotations

from molbatch.backends.base import Backend
from molbatch.backends.chimerax import ChimeraXBackend
from molbatch.backends.pymol import PyMOLBackend


_BACKENDS = {
    "pymol": PyMOLBackend,
    "chimerax": ChimeraXBackend,
}


def available_backends() -> list[str]:
    return sorted(_BACKENDS)


def get_backend(name: str) -> Backend:
    lowered = name.lower()
    if lowered not in _BACKENDS:
        raise ValueError(f"Unsupported backend: {name}")
    return _BACKENDS[lowered]()
