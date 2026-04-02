from pathlib import Path

from molbatch.backends.pymol import PyMOLBackend
from molbatch.types import AppConfig, Plan, StructureItem


def test_pymol_backend_contains_load_and_align():
    cfg = AppConfig()
    plan = Plan(
        config=cfg,
        structures=[
            StructureItem(Path("ref.cif"), "ref", "ref", 0),
            StructureItem(Path("mob.cif"), "mob", "mob", 1),
        ],
        reference=StructureItem(Path("ref.cif"), "ref", "ref", 0),
        display_chains=["X", "Y", "Z"],
        reference_keep_chains=["A", "C", "E", "X", "Y", "Z"],
        object_color_map={"mob": "cyan"},
        backend="pymol",
    )
    text = PyMOLBackend().render(plan)
    assert 'load "' in text
    assert "super" in text
