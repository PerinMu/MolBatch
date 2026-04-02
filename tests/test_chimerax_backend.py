from pathlib import Path

from molbatch.backends.chimerax import ChimeraXBackend
from molbatch.types import AppConfig, Plan, StructureItem


def test_chimerax_backend_contains_open_and_mmaker():
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
        backend="chimerax",
    )
    text = ChimeraXBackend().render(plan)
    assert 'open "' in text
    assert "mmaker" in text
