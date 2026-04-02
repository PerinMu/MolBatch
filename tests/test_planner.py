from pathlib import Path

from molbatch.core.planner import build_plan
from molbatch.types import AppConfig


def test_build_plan(tmp_path: Path):
    (tmp_path / "ref.cif").write_text("data", encoding="utf-8")
    (tmp_path / "other.cif").write_text("data", encoding="utf-8")

    cfg = AppConfig()
    cfg.input.directory = str(tmp_path)
    cfg.reference.selector = "stem"
    cfg.reference.stem = "ref"

    plan = build_plan(cfg, backend="pymol")
    assert len(plan.structures) == 2
    assert plan.reference.stem == "ref"
