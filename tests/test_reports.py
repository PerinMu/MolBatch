from pathlib import Path

from molbatch.core.reports import write_reports
from molbatch.types import AppConfig, Plan, StructureItem


def test_write_reports(tmp_path: Path):
    cfg = AppConfig()
    cfg.output.directory = str(tmp_path)
    cfg.output.basename = "demo"
    plan = Plan(
        config=cfg,
        structures=[StructureItem(Path("ref.cif"), "ref", "ref", 0)],
        reference=StructureItem(Path("ref.cif"), "ref", "ref", 0),
        display_chains=["X"],
        reference_keep_chains=["A", "X"],
        object_color_map={},
        backend="pymol",
    )
    write_reports(plan, tmp_path)
    assert (tmp_path / "demo_summary.json").exists()
    assert (tmp_path / "demo_summary.csv").exists()
